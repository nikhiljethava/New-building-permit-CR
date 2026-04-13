import urllib.request
import urllib.parse
import json
import time
import random
import uuid
import mimetypes
import os

BASE_URL = os.getenv("API_URL", "http://localhost:8080")

def encode_multipart(fields, files):
    boundary = b'----WebKitFormBoundary' + uuid.uuid4().hex.encode('utf-8')
    body = []
    for key, value in fields.items():
        body.extend([
            b'--' + boundary,
            b'Content-Disposition: form-data; name="' + key.encode('utf-8') + b'"',
            b'',
            str(value).encode('utf-8')
        ])
    for key, filename, file_content in files:
        body.extend([
            b'--' + boundary,
            b'Content-Disposition: form-data; name="' + key.encode('utf-8') + b'"; filename="' + filename.encode('utf-8') + b'"',
            b'Content-Type: ' + (mimetypes.guess_type(filename)[0] or 'application/octet-stream').encode('utf-8'),
            b'',
            file_content
        ])
    body.extend([b'--' + boundary + b'--', b''])
    return b'\r\n'.join(body), b'multipart/form-data; boundary=' + boundary

def post_json(url, data):
    req = urllib.request.Request(url, data=json.dumps(data).encode('utf-8'), headers={'Content-Type': 'application/json'})
    try:
        with urllib.request.urlopen(req) as response:
            return json.loads(response.read().decode('utf-8'))
    except Exception as e:
        print(f"Error posting to {url}: {e}")
        return None

def get_json(url):
    try:
        with urllib.request.urlopen(url) as response:
            return json.loads(response.read().decode('utf-8'))
    except Exception as e:
        print(f"Error getting from {url}: {e}")
        return None

def simulate_traffic():
    email = f"user_{uuid.uuid4().hex[:8]}@example.com"
    print(f"Simulating traffic for {email}")

    # 1. Login
    user = post_json(f"{BASE_URL}/api/login", {"email": email})
    if not user:
        print("Failed to login")
        return
    user_id = user.get("id")
    print(f"Logged in user ID: {user_id}")

    # 2. Create Property
    property_data = {
        "address": f"{random.randint(100, 999)} Main St, San Paloma, CA",
        "lot_size_sqft": random.randint(5000, 10000),
        "owner": email,
        "assessed_value": random.randint(100000, 500000)
    }
    prop = post_json(f"{BASE_URL}/api/users/{user_id}/properties", property_data)
    if not prop:
        print("Failed to create property")
        return
    property_id = prop.get("id")
    print(f"Created property ID: {property_id}")

    # 3. Create Permit
    permit_data = {
        "description": "Remodel Kitchen",
        "type": "Building"
    }
    permit = post_json(f"{BASE_URL}/api/properties/{property_id}/permits", permit_data)
    if not permit:
        print("Failed to create permit")
        return
    permit_id = permit.get("id")
    print(f"Created permit ID: {permit_id}")

    # 4. Upload Plan
    pdf_path = "tests/sample_building_plan.pdf"
    if not os.path.exists(pdf_path):
        print(f"File not found: {pdf_path}. Skipping upload.")
        return

    with open(pdf_path, "rb") as f:
        pdf_content = f.read()

    fields = {"permit_id": str(permit_id)}
    files = [("file", "sample_building_plan.pdf", pdf_content)]
    body, content_type = encode_multipart(fields, files)

    req = urllib.request.Request(f"{BASE_URL}/api/analyze-plan", data=body, headers={'Content-Type': content_type.decode('utf-8')})
    try:
        with urllib.request.urlopen(req) as response:
            print(f"Uploaded plan, status: {response.status}")
    except Exception as e:
        print(f"Error uploading plan: {e}")

    # 5. Chat
    chat_data = {
        "messages": [
            {"role": "user", "content": "What are the violations?"}
        ],
        "permit_id": str(permit_id)
    }
    post_json(f"{BASE_URL}/api/chat", chat_data)
    print("Sent chat message")

if __name__ == "__main__":
    # Run a few iterations for testing, or loop forever
    # The user asked to create a service, so a loop is appropriate.
    # We will run 5 iterations and then stop for this demo, or loop forever.
    # Let's loop forever but with a way to stop if needed (e.g. KeyboardInterrupt).
    try:
        while True:
            simulate_traffic()
            sleep_time = random.randint(2, 5)
            print(f"Sleeping for {sleep_time} seconds...")
            time.sleep(sleep_time)
    except KeyboardInterrupt:
        print("Stopped traffic simulation")
