from flask import Flask, request, redirect, render_template
from itsdangerous import URLSafeSerializer
import os

from data import get_data

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY")
serializer = URLSafeSerializer(app.secret_key)


@app.route("/", methods=["GET", "POST"])
def form_redirect():
    if request.method == "POST":
        o_id = request.form.get("o_id")
        p_id = request.form.get("p_id")
        grade = request.form.get("class")


        if not o_id or not p_id:
            return render_template("enter.html", error="გთხოვ შეავსო სამივე ველი.")

        data = get_data()

        if (o_id, p_id) not in data:
            return render_template("enter.html", error="მოსწავლე ვერ მოიძებნა. გთხოვ გადაამოწმე მონაცემები.")

        if int(grade) == 5:
            target_url = f"https://docs.google.com/forms/d/e/1FAIpQLSeOw4wRb4ZDfhLdB7N-JlN5Yl1ZlP2bxCaI6n5zU0xXLbwcDg/viewform?usp=pp_url&entry.69264929={o_id}&entry.760426637={p_id}"
        elif int(grade) == 6:
            target_url = f"https://docs.google.com/forms/d/e/1FAIpQLScDF-zI6WYV6hf5YDNmC-7AVh6Gp4I6mB9GSEVtP9DvUi7cvg/viewform?usp=pp_url&entry.1548843900={o_id}&entry.1331201179={p_id}"
        else:
            return "არასწორი მონაცემები", 400

        return redirect(target_url)

    return render_template("enter.html")
