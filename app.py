from flask import Flask, render_template, request
import os
import PyPDF2

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/analyze', methods=['POST'])
def analyze():

    file = request.files['resume']
    job_desc = request.form.get('job_desc')

    filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
    file.save(filepath)

    # Extract text from PDF
    text = ""
    if file.filename.endswith('.pdf'):
        pdf = PyPDF2.PdfReader(filepath)
        for page in pdf.pages:
            if page.extract_text():
                text += page.extract_text()

    # Simple AI scoring logic
    score = 0
    if job_desc:
        words = job_desc.lower().split()
        for w in words:
            if w in text.lower():
                score += 5

    score = min(score, 100)

    return render_template(
        "result.html",
        filename=file.filename,
        score=score,
        preview=text[:300]
    )


if __name__ == '__main__':
    app.run(debug=True)