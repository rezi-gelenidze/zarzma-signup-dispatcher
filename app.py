from flask import Flask, request, render_template, redirect, url_for, session
from dotenv import load_dotenv
from itsdangerous import URLSafeSerializer
import os
import json

from utils import send_html_email, render_email_template, get_worksheet, hash_email

# Load .env variables
load_dotenv()
app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY")

# Token serializer
serializer = URLSafeSerializer(app.secret_key)

# Step 1: Email entry
@app.route("/", methods=["GET", "POST"])
def request_email():
    if request.method == "POST":
        email = request.form["email"]
        session["email"] = email

        token = serializer.dumps(email)
        verify_url = url_for("verify_email", token=token, _external=True)

        html_body = render_email_template("emails/verification_email.html", verify_url=verify_url)
        send_html_email(email, "ელფოსტის დადასტურება", html_body)

        return render_template("register.html", step="check_email")  # New "Check your email" step
    return render_template("register.html", step="email")

# Step 2: Link-based verification
@app.route("/verify/<token>")
def verify_email(token):
    try:
        email = serializer.loads(token)
        session["verified"] = True
        session["email"] = email
        return redirect(url_for("student_info"))
    except Exception:
        return render_template("register.html", step="verify", error="ბმული არასწორია ან ვადა გაუვიდა")

# Step 3: Registration form
@app.route("/submit", methods=["GET", "POST"])
def student_info():
    if not session.get("verified"):
        return redirect(url_for("request_email"))

    if request.method == "POST":
        fname = request.form["fname"]
        lname = request.form["lname"]
        region = request.form["region"]
        district = request.form["district"]
        school = request.form["school"]
        personal_id = request.form["personalId"]

        reg_id = hash_email(session["email"])

        worksheet = get_worksheet()
        worksheet.append_row([
            session["email"], reg_id, fname, lname,
            personal_id, region, district, school
        ])

        html_body = render_email_template("emails/registration_success_email.html", reg_id=reg_id)
        send_html_email(session["email"], "რეგისტრაცია დასრულდა", html_body)

        return render_template("register.html", step="done", reg_id=reg_id)

    with open("schools.json", "r", encoding="utf-8") as f:
        schools = json.load(f)

    return render_template("register.html", step="info", schools=schools)
