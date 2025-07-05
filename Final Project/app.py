from flask import Flask, render_template, request, redirect
from omr_checker import process_omr
import os
from answer_key import ANSWER_KEY

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Ensure upload folder exists
os.makedirs(UPLOAD_FOLDER, exist_ok=True)


@app.route("/", methods=["GET", "POST"])
def upload_form():
    if request.method == "POST":
        # Retrieve form details
        name = request.form["name"]
        class_name = request.form["class"]
        section = request.form["section"]
        roll_number = request.form["roll"]

        # Handle file upload
        if 'omr' not in request.files:
            return "No file part"
        file = request.files["omr"]
        if file.filename == "":
            return "No selected file"

        filepath = os.path.join(app.config["UPLOAD_FOLDER"], file.filename)
        file.save(filepath)

        # Process the OMR sheet
        result = process_omr(filepath)
        grade = f"{result['score']} / {result['total']}"

        # Save student data with grade
        with open("uploads/student_results.txt", "a") as f:
            f.write(f"{name}, {class_name}, {section}, {roll_number}, Score: {grade}\n")

        return f"OMR Processed! {name}'s Score: {grade}"
    return render_template("form.html")


if __name__ == "__main__":
    app.run(debug=True)
