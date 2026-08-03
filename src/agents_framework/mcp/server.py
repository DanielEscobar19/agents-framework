from mcp.server.mcpserver import MCPServer

from agents_framework.mcp.tools.index_tool import make_index_tool
from agents_framework.mcp.tools.search_tool import make_search_tools
from agents_framework.retrieval.retrieval_service import RetrievalService
from config.config import load_config


def create_mcp_server() -> MCPServer:
    config = load_config()
    service = RetrievalService(config)

    search_code, get_context = make_search_tools(service)
    index_codebase = make_index_tool(config)

    mcp = MCPServer("agents-framework")
    mcp.tool()(search_code)
    mcp.tool()(get_context)
    mcp.tool()(index_codebase)

    return mcp


def run():
    create_mcp_server().run(transport="stdio")
