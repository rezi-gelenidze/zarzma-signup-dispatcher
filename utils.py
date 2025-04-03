import os
import smtplib
import random
import string
import hashlib
import gspread

from flask import render_template

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from oauth2client.service_account import ServiceAccountCredentials

SHEET_ID = os.getenv("SHEET_ID")


def get_worksheet():
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    creds = ServiceAccountCredentials.from_json_keyfile_name("service_account.json", scope)
    client = gspread.authorize(creds)
    return client.open_by_key(SHEET_ID).sheet1


def send_html_email(to_email, subject, html_body):
    msg = MIMEMultipart("alternative")
    msg["Subject"] = subject
    msg["From"] = os.getenv("EMAIL_ADDRESS")
    msg["To"] = to_email

    mime_html = MIMEText(html_body, "html")
    msg.attach(mime_html)

    with smtplib.SMTP(os.getenv("EMAIL_HOST"), int(os.getenv("EMAIL_PORT"))) as server:
        server.starttls()
        server.login(os.getenv("EMAIL_ADDRESS"), os.getenv("EMAIL_PASSWORD"))
        server.send_message(msg)


def render_email_template(template_name, **kwargs):
    return render_template(template_name, **kwargs)


def generate_code():
    return ''.join(random.choices(string.digits, k=6))


def hash_email(email: str) -> str:
    email = email.strip().lower()
    local, domain = email.split('@')
    local = local.replace('.', '')  # remove dots only from local part
    cleaned_email = f"{local}@{domain}"
    hashed = hashlib.sha256(cleaned_email.encode()).hexdigest()
    return hashed[:6].lower()  # return first 6 hex chars in lower
