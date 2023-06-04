from flask import Flask, render_template, request

app = Flask(__name__)


@app.route("/", methods=["GET", "POST"])
def handle_form():
    if request.method == "POST":
        # Form was submitted, process the data
        name = request.form.get("name")
        email = request.form.get("email")
        # ... process the form data as needed

        # Return a response or redirect to another page
        return "Registration submitted successfully!"
    else:
        # Display the form
        return render_template("form.html")


if __name__ == "__main__":
    app.run(host="0.0.0.0")
