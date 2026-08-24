
from flask import Flask, render_template, request
import joblib
import sqlite3
import os

from s3_upload import upload_resume
from sqs_service import send_prediction
from lambda_service import invoke_lambda

app = Flask(__name__)

UPLOAD_FOLDER = "uploads"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

os.makedirs(UPLOAD_FOLDER, exist_ok=True)

model = joblib.load("model.pkl")


def create_database():
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS students(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            email TEXT,
            cgpa REAL,
            dsa INTEGER,
            projects INTEGER,
            internship INTEGER,
            communication INTEGER,
            resume_url TEXT,
            prediction TEXT,
            confidence REAL
        )
    """)

    conn.commit()
    conn.close()


create_database()


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/predict", methods=["POST"])
def predict():

    name = request.form["name"]
    email = request.form["email"]
    cgpa = float(request.form["cgpa"])
    dsa = int(request.form["dsa"])
    projects = int(request.form["projects"])
    internship = int(request.form["internship"])
    communication = int(request.form["communication"])

    resume = request.files["resume"]

    resume_url = ""

    if resume and resume.filename:

        filename = resume.filename

        local_path = os.path.join(
            app.config["UPLOAD_FOLDER"],
            filename
        )

        resume.save(local_path)

        resume_url = upload_resume(
            local_path,
            filename
        )

    features = [[
        cgpa,
        dsa,
        projects,
        internship,
        communication
    ]]

    prediction = model.predict(features)

    confidence = round(
        max(model.predict_proba(features)[0]) * 100,
        2
    )

    if prediction[0] == 1:
        result = "High Chance of Placement"
    else:
        result = "Low Chance of Placement"

    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT INTO students(
            name,
            email,
            cgpa,
            dsa,
            projects,
            internship,
            communication,
            resume_url,
            prediction,
            confidence
        )
        VALUES(?,?,?,?,?,?,?,?,?,?)
        """,
        (
            name,
            email,
            cgpa,
            dsa,
            projects,
            internship,
            communication,
            resume_url,
            result,
            confidence
        )
    )

    conn.commit()
    conn.close()

    send_prediction(
        name,
        email,
        result
    )

    try:
        invoke_lambda(
            name=name,
            email=email,
            cgpa=cgpa,
            dsa=dsa,
            projects=projects,
            communication=communication,
            prediction=result,
            confidence=confidence
        )
        print("Lambda invoked successfully")
    except Exception as e:
        print(f"Lambda Error: {e}")

    return render_template(
        "result.html",
        name=name,
        email=email,
        cgpa=cgpa,
        dsa=dsa,
        projects=projects,
        communication=communication,
        result=result,
        probability=confidence,
        confidence=confidence,
        resume_url=resume_url
    )


if __name__ == "__main__":
    app.run(debug=True)
