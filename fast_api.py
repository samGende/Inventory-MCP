from fastapi import FastAPI, UploadFile, File, HTTPException, BackgroundTasks
from typing import Optional
from pathlib import Path
import shutil, asyncio
from dotenv import load_dotenv
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


async def agent_flow(pdf_path: Path) -> None:
    """
    Async coroutine that talks to the MCP server + Pydantic-AI agent
    for a freshly-uploaded PO PDF.
    """
    async with agent.run_mcp_servers():
        prompt = (
            "Can you create a sales order for this PO? "
            "And then attach the pdf to the salesorder. "
            "Please also include the SO id within your final response."
            "It should be in the format: salserder_id:{{id}} Make sure the id is surounded by {{}}"
            f"The file path to the pdf is {pdf_path}"
        )

        pdf_bytes = pdf_path.read_bytes()                 # one read, reused twice
        result = await agent.run(
            [prompt,
             BinaryContent(data=pdf_bytes, media_type="application/pdf"),
             BinaryContent(data=pdf_bytes, media_type="application/pdf")]
        )
    # Whatever you want to do with the agent’s answer:
    print(f"Agent output for {pdf_path.name}:\n{result.output}")

    #print(f"Agent messages for {pdf_path.name}: \n")
    #for message in result.all_messages():
    #    print(f"{message}")

    m = re.search(r'\{{(.*?)\}}', result.output)
    if m:
        print('SO id:', m.group(0).replace('{{', '').replace('}}', ''))
    else:
        print("No SO id found in agent output. Alert User to check po Manually")


def kick_off_agent(pdf_path: Path) -> None:
    """Sync wrapper so FastAPI BackgroundTasks can fire our async workflow."""
    asyncio.run(agent_flow(pdf_path))


# ---------- the upload endpoint ----------
@app.post("/po")
async def upload_po(
    background_tasks: BackgroundTasks,
    content: Optional[UploadFile] = File(None, alias="content"),  # <-- renamed
):
    if content is None:                          # “setup-only” request
        return {"mode": "setup", "detail": "No file supplied; setup tasks started."}

    dest_path = UPLOAD_DIR / content.filename
    try:
        with dest_path.open("wb") as buf:
            shutil.copyfileobj(content.file, buf)
    except Exception as exc:
        raise HTTPException(500, f"Failed to save file: {exc}")
    finally:
        await content.close()

    background_tasks.add_task(kick_off_agent, dest_path)
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

