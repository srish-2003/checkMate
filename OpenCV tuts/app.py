from flask import Flask, request, render_template, jsonify
import subprocess

app = Flask(__name__)

# Route to serve the HTML form
@app.route('/')
def index():
    return render_template('index.html')

# Route to handle form submission
@app.route('/submit', methods=['POST'])
def submit_form():
    # Get data from the form
    name = request.form.get('name')
    student_class = request.form.get('class')
    section = request.form.get('section')
    roll = request.form.get('roll')

    try:
        # Run your Python script with the form data
        result = subprocess.run(
            ['python', 'your_script.py', name, student_class, section, roll],
            capture_output=True,
            text=True,
            check=True
        )
        return jsonify({'message': 'Python script executed successfully!', 'output': result.stdout})
    except subprocess.CalledProcessError as e:
        return jsonify({'message': 'Error executing Python script', 'error': e.stderr}), 500

if __name__ == '__main__':
    app.run(debug=True)
