# 🔐 BrokenAuthDetect
**An Automated Broken Authentication Vulnerability Detector using Python, Hydra, Burp Suite, and bWAPP**

BrokenAuthDetect is a Python-based automation tool designed to simulate and detect common broken authentication vulnerabilities such as brute-force login, missing rate limiting, and session fixation issues in web applications. The tool integrates Hydra for brute-forcing, Burp Suite for request capturing, and bWAPP as the vulnerable web target. Findings are documented in a professional PDF report using ReportLab.

---
## 🚀 Features
-  Brute-Force Testing with Hydra – Simulates login attacks using common credentials.

-  Rate Limiting Evaluation – Sends multiple login attempts to check for lack of account lockout.

-  Session Fixation Detection – Compares PHP session tokens before and after login.

-  PDF Report Generation – Summarizes all test results in a timestamped, downloadable report.

-  Burp Suite Integration – Captures live requests and structures payloads dynamically.

---
## 📁 File Structure

```
BrokenAuthDetect/
├── auth_tester.py       # Main script for executing all tests
├── auth_report.pdf      # Auto-generated PDF report
├── passwords.txt        # Dictionary file used by Hydra
├── venv/                # Python virtual environment
├── __pycache__/         # Compiled Python bytecode (auto-generated)
```
---
## ⚙ Requirements
- Python 3.6+
- Kali Linux or Linux with Hydra installed
- Burp Suite 
- ReportLab (for PDF generation)
- Local vulnerable app (bWAPP) running
---

## 💥 Attack Techniques Simulated
- Brute-Force Login via Hydra
- No Rate Limiting Detection (10 rapid failed logins)
- Session Fixation Test (PHPSESSID analysis)
---

## 🛠 Installation & Usage
```
# 1. Create project directory and virtual environment
mkdir BrokenAuthDetect && cd BrokenAuthDetect
python3 -m venv venv
source venv/bin/activate

# 2. Install required Python packages
pip install requests
pip install requests reportlab

# 3. Ensure Hydra is installed and test it with:
hydra -l bee -P passwords.txt 192.168.100.5 http-post-form "/bWAPP/login.php:login=^USER^&password=^PASS^&security_level=0&form=submit:Invalid"

# 4. Run the script
python3 auth_tester.py
```
---
## 🗂 Report Includes
- Brute-force attempt logs with timestamps
- Rate limiting behavior summary
- Session IDs before and after login
- Final vulnerability evaluation with pass/fail status
---
## 🛠 Tech Stack
- Python
- Hydra
- Burp Suite
- ReportLab
- bWAPP (as target application)




