import os


from fastapi import FastAPI, Request
from langchain_openai import ChatOpenAI
from mcp.server.fastmcp import FastMCP
from mcp.server.sse import SseServerTransport
from starlette.routing import Mount, Route
import uvicorn

llm = ChatOpenAI(model="gpt-4o")

mcp = FastMCP("chatbot")

@mcp.tool()
async def chat(input: str) -> str:
    """LLM과 일반적인 대화를 수행합니다."""
    result = await llm.ainvoke(input)

    if hasattr(result, "content"):
        return str(result.content)
    return str(result)

sse = SseServerTransport("/messages/")

async def handle_sse(request: Request) -> None:
    async with sse.connect_sse(
        request.scope,
        request.receive,
        request._send,
    ) as (read_stream, write_stream):
        await mcp._mcp_server.run(
            read_stream,
            write_stream,
            mcp._mcp_server.create_initialization_options(),
        )

app = FastAPI(
    debug=True,
    routes=[
        Route("/sse", endpoint=handle_sse),
        Mount("/messages/", app=sse.handle_post_message),
    ],
)

if __name__ == "__main__":
    uvicorn.run("sse_server:app", host="127.0.0.1", port=3000, reload=True)
