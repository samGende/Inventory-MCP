from pydantic_ai import Agent, BinaryContent
from pydantic_ai.mcp import MCPServerStdio
import asyncio
from dotenv import load_dotenv
from pathlib import Path
import sys
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
load_dotenv()  # Load environment variables from .env file

print("Starting MCP server...")
server = MCPServerStdio("uv", args= ["run", "--python", "3.12","/Users/samg/Documents/dev/Inventory-MCP/src/server.py"])
print("MCP server started. Starting the Pydantic Agent")

agent = Agent('anthropic:claude-3-5-haiku-latest', mcp_servers=[server])
print("Agent initialized with MCP server.")

pdf_path = Path("./POs/PO-00003.pdf")

async def main():

    async with agent.run_mcp_servers():
        res = await agent.run([f"Can you create a sales order for this PO? And then attach the pdf to the salesorder. The file path to the pdf is {pdf_path}", BinaryContent(data=pdf_path.read_bytes(), media_type="application/pdf"), BinaryContent(data=pdf_path.read_bytes(), media_type="application/pdf")]) 
    print(res.output)


if __name__ == "__main__":
    asyncio.run(main())