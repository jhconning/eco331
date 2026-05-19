import re

block = """## Shayoni Nandi 
<!-- user_id: 35471007 | submitted_at: 2026-03-17T03:20:29Z | days_late: 0 -->

Chatgpt suggests"""

uid_match = re.search(r'user_id:\s*(\d+)', block)
print("UID MATCH:", uid_match.group(1) if uid_match else None)
