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

import time
import main
import db

def run_benchmark(iterations=1000):
    # Get a valid APN to benchmark with
    conn = db.get_connection()
    c = conn.cursor()
    c.execute("SELECT apn FROM parcels LIMIT 1")
    apn = c.fetchone()[0]

    start_time = time.time()
    for _ in range(iterations):
        result = main.lookup_parcel(apn)
    end_time = time.time()

    total_time = end_time - start_time
    avg_time = total_time / iterations

    print(f"Benchmark Results for {iterations} iterations:")
    print(f"Total time: {total_time:.4f} seconds")
    print(f"Average time per call: {avg_time * 1000:.4f} ms")

if __name__ == "__main__":
    # Ensure database is initialized
    db.init_db()
    run_benchmark(5000)
