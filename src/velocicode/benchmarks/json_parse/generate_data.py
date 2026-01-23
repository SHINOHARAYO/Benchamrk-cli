import json
import random
import string
import os

def generate_random_string(length=10):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

def generate_data(num_records=10000):
    data = []
    for i in range(num_records):
        record = {
            "id": i,
            "name": generate_random_string(20),
            "email": generate_random_string(10) + "@example.com",
            "is_active": random.choice([True, False]),
            "tags": [generate_random_string(5) for _ in range(random.randint(1, 5))],
            "meta": {
                "created_at": "2023-01-01T12:00:00Z",
                "score": random.uniform(0, 100)
            }
        }
        data.append(record)
    return data

def main():
    # Target size: ~2-5 MB
    data = generate_data(50000) 
    
    output_path = os.path.join(os.path.dirname(__file__), "data.json")
    with open(output_path, "w") as f:
        json.dump(data, f)
    
    size_mb = os.path.getsize(output_path) / (1024 * 1024)
    print(f"Generated {output_path} ({size_mb:.2f} MB)")

if __name__ == "__main__":
    main()
