import json
import httpx
import time

BASE_URL = "http://127.0.0.1:8000"
SAMPLES = [
    {"user_id":"u01","session_id":"s01","feature":"qa","message":"What is your refund policy? My email is student@vinuni.edu.vn"},
    {"user_id":"u02","session_id":"s02","feature":"qa","message":"Explain why metrics traces and logs work together"},
    {"user_id":"u03","session_id":"s03","feature":"summary","message":"Summarize the monitoring policy for production logging"},
    {"user_id":"u04","session_id":"s04","feature":"qa","message":"Can I get help with policy and monitoring?"},
    {"user_id":"u05","session_id":"s05","feature":"qa","message":"Here is my phone 0987654321, what should be logged?"},
    {"user_id":"u06","session_id":"s06","feature":"summary","message":"Give me a short summary of the observability workflow"},
    {"user_id":"u07","session_id":"s07","feature":"qa","message":"What should not appear in app logs?"},
    {"user_id":"u08","session_id":"s08","feature":"qa","message":"How do I debug tail latency?"},
    {"user_id":"u09","session_id":"s09","feature":"qa","message":"What is the policy for PII and credit card 4111 1111 1111 1111?"},
    {"user_id":"u10","session_id":"s10","feature":"qa","message":"How should alerts be designed?"},
    {"user_id":"u11","session_id":"s11","feature":"qa","message":"I lost my passport C9876543 while traveling for company business, can HR help?"},
    {"user_id":"u12","session_id":"s12","feature":"summary","message":"My home address is 123 Vinhomes Ocean Park, Hanoi. Is it safe to save this?"},
    {"user_id":"u13","session_id":"s13","feature":"qa","message":"My student ID is vni123456. Can I get a refund for my tuition fee?"}
]

def main():
    print(f"{'Status':<8} | {'ID':<12} | {'Latency':<8} | {'Message Preview'}")
    print("-" * 70)
    with httpx.Client(timeout=30.0) as client:
        for sample in SAMPLES:
            try:
                start = time.perf_counter()
                r = client.post(f"{BASE_URL}/chat", json=sample)
                latency = (time.perf_counter() - start) * 1000
                data = r.json()
                cid = data.get('correlation_id', '???')
                msg_preview = sample['message'][:40] + "..."
                
                status_color = "\033[92m" if r.status_code == 200 else "\033[91m"
                print(f"[{status_color}{r.status_code}\033[0m]    | {cid:<12} | {latency:>6.1f}ms | {msg_preview}")
            except Exception as e:
                print(f"[FAIL]    | Error: {e}")

if __name__ == "__main__":
    main()
