import argparse
import concurrent.futures
import json
import time
from pathlib import Path

import httpx

BASE_URL = "http://127.0.0.1:8000"
QUERIES = Path("data/sample_queries.jsonl")


def send_request(client: httpx.Client, payload: dict) -> None:
    try:
        start = time.perf_counter()
        r = client.post(f"{BASE_URL}/chat", json=payload)
        latency = (time.perf_counter() - start) * 1000
        
        # Format output based on status code for better visibility during demo
        status_color = "\033[92m" if r.status_code == 200 else "\033[91m"
        reset_color = "\033[0m"
        
        try:
            resp_json = r.json()
            corr_id = resp_json.get('correlation_id', 'MISSING_ID')
            error_detail = resp_json.get('detail', '')
        except:
            corr_id = "PARSE_ERROR"
            error_detail = r.text[:20]
            
        print(f"[{status_color}{r.status_code}{reset_color}] {corr_id:<12} | {payload['feature']:<8} | {latency:>7.1f}ms | {error_detail}")
        
        return {
            "status": r.status_code,
            "latency": latency,
            "error": r.status_code != 200
        }
    except Exception as e:
        print(f"[\033[91mFAIL\033[0m] Request failed: {e}")
        return {"status": 0, "latency": 0, "error": True}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--concurrency", type=int, default=1, help="Number of concurrent requests")
    args = parser.parse_args()

    lines = [line for line in QUERIES.read_text(encoding="utf-8").splitlines() if line.strip()]
    print(f"Starting load test (Concurrency={args.concurrency})...")
    print("-" * 60)
    
    results = []
    with httpx.Client(timeout=30.0) as client:
        if args.concurrency > 1:
            with concurrent.futures.ThreadPoolExecutor(max_workers=args.concurrency) as executor:
                futures = [executor.submit(send_request, client, json.loads(line)) for line in lines]
                for future in concurrent.futures.as_completed(futures):
                    res = future.result()
                    if res: results.append(res)
        else:
            for line in lines:
                res = send_request(client, json.loads(line))
                if res: results.append(res)
                
    # Print summary
    print("-" * 60)
    total = len(results)
    if total > 0:
        errors = sum(1 for r in results if r["error"])
        avg_latency = sum(r["latency"] for r in results) / total
        print(f"Total Requests: {total}")
        print(f"Success Rate:   {((total - errors) / total) * 100:.1f}%")
        print(f"Avg Latency:    {avg_latency:.1f}ms")


if __name__ == "__main__":
    main()
