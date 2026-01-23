import random
import string
import os

def generate_phone():
    # XXX-XXX-XXXX
    return f"{random.randint(100, 999)}-{random.randint(100, 999)}-{random.randint(1000, 9999)}"

def generate_email():
    return ''.join(random.choices(string.ascii_lowercase, k=8)) + "@example.com"

def generate_text_block():
    sentences = [
        "This is a sample sentence.",
        "Please contact me at EMAIL.",
        "My phone number is PHONE.",
        "Ignore this line.",
        "Another EMAIL is here.",
        "Call PHONE for support."
    ]
    block = []
    for _ in range(100):
        s = random.choice(sentences)
        if "EMAIL" in s:
            s = s.replace("EMAIL", generate_email())
        if "PHONE" in s:
            s = s.replace("PHONE", generate_phone())
        block.append(s)
    return " ".join(block)

def main():
    # Generate ~5MB of text
    output_path = os.path.join(os.path.dirname(__file__), "data.txt")
    
    with open(output_path, "w") as f:
        # 1000 blocks * ~5KB each?
        for _ in range(5000):
            f.write(generate_text_block() + "\n")
            
    size_mb = os.path.getsize(output_path) / (1024 * 1024)
    print(f"Generated {output_path} ({size_mb:.2f} MB)")

if __name__ == "__main__":
    main()
