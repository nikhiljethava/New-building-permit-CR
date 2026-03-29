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

import main
import db

# Test the tool logic directly
def test_lookup_parcel():
    print("Testing lookup_parcel tool logic directly...")
    
    # Verify the database has the data first
    conn = main.get_connection()
    c = conn.cursor()

    # Get any valid APN and address instead of hardcoding one
    c.execute("SELECT apn, address FROM parcels LIMIT 1")
    row = c.fetchone()
    # No longer closing connection since it's global
    
    if not row:
        print("Data not found in database! Seeding database might be needed or data is missing.")
        return

    test_apn = row["apn"]
    test_address = row["address"]
    print(f"Testing with database row: APN={test_apn}, Address={test_address}")
    
    # Call the tool function from main.py
    # In main.py, lookup_parcel is registered as a tool.
    
    result = main.lookup_parcel(test_apn)
    
    # Assertions for standard unit test
    assert "apn" in result, f"Expected 'apn' in result, got {result}"
    assert result["apn"] == test_apn, f"Expected apn '{test_apn}', got {result.get('apn')}"
    assert "address" in result, f"Expected 'address' in result, got {result}"
    assert result["address"] == test_address, f"Expected address '{test_address}', got {result.get('address')}"

if __name__ == "__main__":
    test_lookup_parcel()
