from flask import Flask, render_template, request, make_response
import random

app = Flask(__name__)


@app.route("/", methods=["GET"])
def index():
    secret_number = request.cookies.get("secret_number")
    response = make_response(render_template("index.html"))
    if not secret_number:
        new_secret = random.randint(1, 30)
        response.set_cookie("secret_number", str(new_secret))

    return response


@app.route("/result", methods=["POST"])
def result():
    try:
        guess = int(request.form.get("my_guess"))
    except ValueError as err:
        print("No Value.", err)
        return render_template("index.html")

    secret_number = int(request.cookies.get("secret_number"))

    if guess == secret_number:
        correct_hl = "Congratulations!!!"
        correct_message = "Correct! The secret number is {0}.".format(str(secret_number))
        response = make_response(render_template("result.html", correct=correct_message, correct_hl=correct_hl))
        response.set_cookie("secret_number", str(random.randint(1, 30)))
        return response

    elif guess > secret_number:
        message = "Sorry, {0} is not correct. Try something smaller...".format(str(guess))
        return render_template("result.html", message=message)
    elif guess < secret_number:
        message = "Sorry, {0} is incorrect. Try something bigger...".format(str(guess))
        return render_template("result.html", message=message)
    elif not guess:
        return render_template("index.html")


if __name__ == '__main__':
    app.run()
