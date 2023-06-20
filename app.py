from flask import Flask, render_template, request
import json

app = Flask(__name__)


@app.route("/", methods=["GET", "POST"])
def handle_form():
    if request.method == "POST":
        form_data = dict(
            fname=request.form.get("fname"),
            lname=request.form.get("lname"),
            email=request.form.get("email"),
            phone=request.form.get("phone"),
            address1=request.form.get("address1"),
            address2=request.form.get("address2"),
            city=request.form.get("city"),
            state=request.form.get("state"),
            zip=request.form.get("zip"),
            birthdate=request.form.get("birthdate"),
            age=request.form.get("age"),
            gender=request.form.get("gender"),
            weight=request.form.get("weight"),
            profilePic=request.form.get("profilePic"),
            school=request.form.get("school"),
            coach=request.form.get("coach"),
            beltRank=request.form.get("beltRank"),
            events=request.form.get("eventList"),
        )

        # Return a response or redirect to another page
        with open(f"/data/{form_data['fname']}_{form_data['lname']}.json", "w") as f:
            json.dump(form_data, f)

        return render_template("success.html", form_data=form_data, indent=4)
    else:
        # Display the form
        return render_template("form.html")


if __name__ == "__main__":
    app.run(host="0.0.0.0")
