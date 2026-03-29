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
    c.execute("SELECT * FROM parcels WHERE apn = '123-45-678'")
    row = c.fetchone()
    conn.close()
    
    print(f"Database row for 123-45-678: {row}")
    if not row:
        print("Data not found in database! Seeding database might be needed or data is missing.")
        # Try to seed it if needed, or assume it's there.
        # Let's check if we can call the tool function directly.
    
    # Call the tool function from main.py
    # In main.py, lookup_parcel is registered as a tool.
    
    result = main.lookup_parcel("123-45-678")
    
    # Assertions for standard unit test
    assert "apn" in result, f"Expected 'apn' in result, got {result}"
    assert result["apn"] == "123-45-678", f"Expected apn '123-45-678', got {result.get('apn')}"
    assert "address" in result, f"Expected 'address' in result, got {result}"
    assert result["address"] == "123 Main St, Santa Clara, CA 95050", f"Expected address '123 Main St, Santa Clara, CA 95050', got {result.get('address')}"

if __name__ == "__main__":
    test_lookup_parcel()
