#!/usr/bin/env python3
import smtplib
import os
import sys
import mimetypes
from email.message import EmailMessage

# ---------------- CONFIG ----------------
SMTP_HOST    = "smtp.gmail.com"
SMTP_PORT    = 465
SMTP_USE_SSL = True
SMTP_USER    = "niranprempanakal@gmail.com"
SMTP_PASS    = "kqlp ibua ckrf dipj"

FROM_NAME  = "Niran Prem"
FROM_EMAIL = SMTP_USER
SUBJECT    = "Application for DevOps / Cloud Engineer Role - Niran Prem | 4.6 Yrs | AWS, Azure, GCP, Kubernetes | Immediate Joiner"

BODY = """Dear Hiring Manager,

I hope this message finds you well. I am writing to express my strong interest in a DevOps or Cloud Engineer opportunity within your organization. With 4.6 years of hands-on experience architecting, automating, and managing cloud-native infrastructure across AWS, Azure, and GCP, I bring both depth and breadth to modern DevOps practices.

Currently working as a Senior Technical Analyst at PIT Solutions Pvt. Ltd. (Kochi), and previously as a System Engineer at Infosys Limited (Bangalore), I have delivered enterprise-scale solutions in CI/CD automation, Kubernetes orchestration, and multi-cloud observability.


KEY HIGHLIGHTS
--------------

CI/CD Pipelines
Built and maintained enterprise pipelines using Azure DevOps, AWS CodePipeline, Jenkins, and GitHub Actions, reducing release cycle time by 45%.

Infrastructure as Code
Automated cloud provisioning with Terraform and Ansible across 15+ production environments, ensuring consistency and eliminating configuration drift.

Kubernetes at Scale
Managed EKS, AKS, GKE, and on-premises Hetzner Kubernetes clusters for microservices with zero-downtime rollouts and blue-green deployments.

Observability Platform
Architected a centralized monitoring stack using Grafana, Prometheus, Loki, Mimir, Tempo, and Pyroscope on Kubernetes, fully replacing legacy Zabbix infrastructure.

Network Monitoring
Deployed LibreNMS on Kubernetes for org-wide visibility into network devices, traffic, and infrastructure health.

Security and Virtualization
Hardened endpoints with Symantec SEP, managed VMware vSphere workloads, and configured enterprise networking including TCP/IP, DNS, VPN, and firewalls.

Certifications
AWS Certified Cloud Practitioner | Microsoft PL-300 | Microsoft MS-900 | AWS Solutions Architect Associate (In Progress)


TECH SNAPSHOT
-------------
Cloud       : AWS | Azure | GCP
DevOps      : Terraform | Ansible | Docker | Kubernetes | CI/CD | GitOps
Monitoring  : Grafana | Prometheus | Loki | CloudWatch | Zabbix | LibreNMS
Languages   : Bash | Python | C++
OS          : Linux (Ubuntu/RHEL) | Windows Server


I am an immediate joiner and ready to contribute from day one. Please find my resume attached for your review. I would welcome the opportunity to discuss how my experience aligns with your team's goals.

Thank you for your time and consideration.

Best regards,
Niran Prem
Phone    : +91 9895165491
Email    : niranprempanakal@gmail.com
LinkedIn : https://linkedin.com/in/niran-prem-b8b420232
Location : Trivandrum, Kerala (Open to relocation / remote)
"""

# ---------------- FUNCTIONS ----------------
def attach_file(msg: EmailMessage, filepath: str):
    if not os.path.isfile(filepath):
        print(f"[ERROR] Attachment not found: {filepath}")
        sys.exit(2)
    ctype, encoding = mimetypes.guess_type(filepath)
    if ctype is None or encoding is not None:
        ctype = "application/octet-stream"
    maintype, subtype = ctype.split("/", 1)
    with open(filepath, "rb") as f:
        data = f.read()
    msg.add_attachment(data, maintype=maintype, subtype=subtype,
                       filename=os.path.basename(filepath))

def send_mail(to_email: str, resume_path: str, smtp: smtplib.SMTP):
    msg = EmailMessage()
    msg["Subject"] = SUBJECT
    msg["From"]    = f"{FROM_NAME} <{FROM_EMAIL}>"
    msg["To"]      = to_email
    msg.set_content(BODY)
    attach_file(msg, resume_path)
    smtp.send_message(msg)

# ---------------- MAIN ----------------
def main():
    if len(sys.argv) < 3:
        print("Usage: python bulk_mailer.py recipients.txt resume.pdf")
        print()
        print("  recipients.txt  -- one email address per line")
        print("  resume.pdf      -- path to your resume file")
        sys.exit(1)

    recipients_file = sys.argv[1]
    resume_path     = sys.argv[2]

    if not os.path.isfile(recipients_file):
        print(f"[ERROR] Recipients file not found: {recipients_file}")
        sys.exit(1)

    with open(recipients_file, "r") as f:
        recipients = [line.strip() for line in f if line.strip() and "@" in line]

    if not recipients:
        print("[ERROR] No valid email addresses found in file.")
        sys.exit(1)

    print(f"Loaded     : {len(recipients)} recipient(s) from '{recipients_file}'")
    print(f"Resume     : {resume_path}")
    print(f"From       : {FROM_NAME} <{FROM_EMAIL}>")
    print(f"Subject    : {SUBJECT[:70]}...")
    print("-" * 60)

    success = []
    failed  = []

    try:
        if SMTP_USE_SSL:
            smtp = smtplib.SMTP_SSL(SMTP_HOST, SMTP_PORT)
        else:
            smtp = smtplib.SMTP(SMTP_HOST, SMTP_PORT)
            smtp.starttls()
        smtp.login(SMTP_USER, SMTP_PASS)
        print(f"SMTP connected to {SMTP_HOST}:{SMTP_PORT}\n")
    except Exception as e:
        print(f"[ERROR] SMTP connection failed: {e}")
        sys.exit(1)

    for i, email in enumerate(recipients, start=1):
        try:
            send_mail(email, resume_path, smtp)
            print(f"[{i:>3}/{len(recipients)}] Sent    -> {email}")
            success.append(email)
        except Exception as e:
            print(f"[{i:>3}/{len(recipients)}] FAILED  -> {email}  ({e})")
            failed.append(email)

    smtp.quit()

    print()
    print("=" * 60)
    print("                    SEND SUMMARY")
    print("=" * 60)
    print(f"  Successfully sent : {len(success)}")
    print(f"  Failed            : {len(failed)}")
    if failed:
        print("\n  Failed recipients:")
        for addr in failed:
            print(f"    - {addr}")
    print("=" * 60)

if __name__ == "__main__":
    main()
