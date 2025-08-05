from fastapi import FastAPI, UploadFile, File, HTTPException, BackgroundTasks, Form, Request, Header, Body
from typing import Optional, Any, Annotated
from pathlib import Path
import httpx
import shutil, asyncio
from dotenv import load_dotenv
from pydantic import BaseModel
from pydantic_ai import Agent, BinaryContent
from pydantic_ai.mcp import MCPServerStdio
import os
import re


app = FastAPI()

# Where all uploaded purchase-order files will live
UPLOAD_DIR = Path("POs")
UPLOAD_DIR.mkdir(exist_ok=True)               # creates POs/ if it isn’t there already

# ---------- one-time Agent / MCP server setup ----------
load_dotenv()                                              # pull API keys etc. from .env

server = MCPServerStdio(
    "uv",
    args=["run", "--python", "3.12",
          os.getenv("MCP_SERVER_FILE_PATH")],
)
agent = Agent("anthropic:claude-3-5-haiku-latest", mcp_servers=[server])


async def agent_flow(pdf_path: Path, subject: str, html: str) -> None:
    """
    Async coroutine that talks to the MCP server + Pydantic-AI agent
    for a freshly-uploaded PO PDF.
    """
    async with agent.run_mcp_servers():
        prompt = (
            "Can you create a sales order for this PO? "
            "But before you create the order you should search if there is a salesorder with the same online order number, using the custom field id {cf_online_order}" 
            "The online Order number should be listed within the subject of the email if it isn't don't search for the online order number"
            f"The is the subject of the email: ({subject})"
            "After creating a salesorder then attach the pdf to the salesorder. "
            "Please also include the SO id within your final response."
            "It should be in the format: salserder_id:{{id}} Make sure the id is surounded by {{}}"
            "It would also be good if you give a summary of what you did and the SO Number of the order you created"
            "If you can't find a customer that seeems right don't create the sales order"
            "When searching for an item you should prefer K blades vs Z Names those will show up better in searches"
            f"The file path to the pdf is {pdf_path}"
        )

        pdf_bytes = pdf_path.read_bytes()                 # one read, reused twice
        result = await agent.run(
            [prompt,
             BinaryContent(data=pdf_bytes, media_type="application/pdf"),
             BinaryContent(data=pdf_bytes, media_type="application/pdf")]
        )
    # post this to a webhook ?  
    print(f"Agent output for {pdf_path.name}:\n{result.output}")
    
    m = re.search(r'\{{(.*?)\}}', result.output)
    if m:
        id = m.group(0).replace('{{', '').replace('}}', '')
        print('SO id:', id)
    else:
        print("No SO id found in agent output. Alert User to check po Manually")
        id = None 
    # post to a webhook after the agent has run 
    webhook_url = os.getenv("WEBHOOK_URL")

    if webhook_url:
        httpx.post(webhook_url, json={'message': result.output, 'salesorder_id': id})


def kick_off_agent(pdf_path: Path, subject: str, html: str) -> None:
    """Sync wrapper so FastAPI BackgroundTasks can fire our async workflow."""
    asyncio.run(agent_flow(pdf_path, subject, html))

# ---------- the upload endpoint ----------
@app.post("/po")
async def upload_po(
    background_tasks: BackgroundTasks,
    content: Optional[UploadFile] = File(None, alias="content"),  # <-- renamed
    subject: Annotated[str, Body()] = None,
    html: Annotated[str, Body()] = None,
):
    if content is None:                          # “setup-only” request
        return {"mode": "setup", "detail": "No file supplied; setup tasks started."}

    dest_path = UPLOAD_DIR / content.filename
    try:
        with dest_path.open("wb") as buf:
            shutil.copyfileobj(content.file, buf)
            print("file copied to server")
            print(f"subject is {subject}")
            print(f"html is {html}")
    except Exception as exc:
        raise HTTPException(500, f"Failed to save file: {exc}")
    finally:
        await content.close()

    background_tasks.add_task(kick_off_agent, dest_path, subject, html)
    return {
        "mode": "upload",
        "filename": content.filename,
        "saved_to": str(dest_path),
        "agent_task": "started",
    }


@app.get("/test")
async def test_endpoint():
    """
    A simple test endpoint to verify that the server is running.
    """
    return {"message": "Server is running!"}

