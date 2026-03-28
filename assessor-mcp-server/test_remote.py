import asyncio
import time
from mcp.client.streamable_http import streamablehttp_client
from mcp import ClientSession

async def test_network_lookup():
    url = "https://building-permit-assessor-mcp-123456789000.us-central1.run.app/mcp"

    print(f"Connecting to {url}...")

    try:
        async with streamablehttp_client(url=url) as (read_stream, write_stream, get_session_id):
            async with ClientSession(read_stream, write_stream) as session:
                await session.initialize()

                # Invoke the tool
                result = await session.call_tool("lookup_parcel", arguments={"apn": "123-45-678"})
                print(f"Result: {result}")

                # Assertions
                assert result is not None
                # The result is expected to be a CallToolResult, which has 'content' attribute.
                # Let's verify what it returns exactly or if it prints it.
    finally:
        print("Stopping server...")

if __name__ == "__main__":
    asyncio.run(test_network_lookup())
