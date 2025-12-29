from flask import Flask, render_template, request
from services.ai_engine import generate_plan

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/onboarding", methods=["GET", "POST"])
def onboarding():
    if request.method == "POST":
        user_data = {
            "age": request.form.get("age"),
            "sex": request.form.get("sex"),
            "activity": request.form.get("activity"),
            "time": request.form.get("time"),
            "injuries": request.form.get("injuries"),
            "equipment": request.form.get("equipment")
        }

        plan = generate_plan(user_data)
        plan = plan.replace(" - ", "\n\n")
        plan = plan.replace("WEEK_1_PLAN", "\nWEEK 1 PLAN\n")
        plan = plan.replace("WHY_THESE_EXERCISES", "\nWHY THESE EXERCISES\n")
        plan = plan.replace("PROGRESSION_PREVIEW", "\nPROGRESSION PREVIEW\n")

        return render_template(
            "plan.html",
            user=user_data,
            plan=plan
        )

    return render_template("onboarding.html")

if __name__ == "__main__":
    app.run(debug=True)
