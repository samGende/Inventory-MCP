from fastapi import FastAPI, UploadFile, File, HTTPException, BackgroundTasks
from pathlib import Path
import shutil, asyncio
from dotenv import load_dotenv
from pydantic_ai import Agent, BinaryContent
from pydantic_ai.mcp import MCPServerStdio

app = FastAPI()

# Where all uploaded purchase-order files will live
UPLOAD_DIR = Path("POs")
UPLOAD_DIR.mkdir(exist_ok=True)               # creates POs/ if it isn’t there already

# ---------- one-time Agent / MCP server setup ----------
load_dotenv()                                              # pull API keys etc. from .env

server = MCPServerStdio(
    "uv",
    args=["run", "--python", "3.12",
          "/Users/samg/Documents/dev/Inventory-MCP/src/server.py"],
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


def kick_off_agent(pdf_path: Path) -> None:
    """Sync wrapper so FastAPI BackgroundTasks can fire our async workflow."""
    asyncio.run(agent_flow(pdf_path))


# ---------- the upload endpoint ----------
@app.post("/po")
async def upload_po(
    file: UploadFile = File(...),
    background_tasks: BackgroundTasks = BackgroundTasks(),
):
    dest_path = UPLOAD_DIR / file.filename

    try:
        with dest_path.open("wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"Failed to save file: {exc}")
    finally:
        await file.close()

    # hand work off to the background so the caller isn’t kept waiting
    background_tasks.add_task(kick_off_agent, dest_path)

    return {
        "filename": file.filename,
        "saved_to": str(dest_path),
        "agent_task": "started",
    }

@app.get("/test")
async def test_endpoint():
    """
    A simple test endpoint to verify that the server is running.
    """
    return {"message": "Server is running!"}

