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
