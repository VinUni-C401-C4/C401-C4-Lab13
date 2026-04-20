from __future__ import annotations

import argparse

import httpx

BASE_URL = "http://127.0.0.1:8000"


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--scenario", required=True, choices=["rag_slow", "tool_fail", "cost_spike"])
    parser.add_argument("--disable", action="store_true")
    args = parser.parse_args()

    path = f"/incidents/{args.scenario}/disable" if args.disable else f"/incidents/{args.scenario}/enable"
    action_text = "DISABLED" if args.disable else "ENABLED"
    
    try:
        r = httpx.post(f"{BASE_URL}{path}", timeout=10.0)
        
        status_color = "\033[92m" if r.status_code == 200 else "\033[91m"
        print(f"[{status_color}{r.status_code}\033[0m] Incident '{args.scenario}' {action_text}")
        
        # In trạng thái của tất cả các incidents
        if r.status_code == 200:
            active_incidents = [k for k, v in r.json().get('incidents', {}).items() if v]
            if active_incidents:
                print(f"    Current ACTIVE incidents: \033[91m{', '.join(active_incidents)}\033[0m")
            else:
                print("    System is clear (No active incidents).")
                
    except httpx.ConnectError:
        print("[\033[91mFAIL\033[0m] Cannot connect to server. Is it running on port 8000?")


if __name__ == "__main__":
    main()
