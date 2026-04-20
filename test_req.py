import httpx
r = httpx.post("http://127.0.0.1:8000/chat", json={"user_id":"u01","session_id":"s01","feature":"qa","message":"What is your refund policy? My email is student@vinuni.edu.vn"})
print(r.status_code, r.text)
