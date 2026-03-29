# Copyright 2026 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

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
