from flask import Flask, render_template, request
import PyPDF2
import spacy
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import os

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'

nlp = spacy.load("en_core_web_sm")

def extract_text(file_path):
    text = ""
    try:
        with open(file_path, 'rb') as file:
            reader = PyPDF2.PdfReader(file)
            for page in reader.pages:
                content = page.extract_text()
                if content:
                    text += content
    except:
        text = "Error reading PDF"
    return text

def extract_skills(text):
    skills_list = ['python', 'java', 'c', 'c++', 'html', 'css', 'javascript', 'machine learning']
    found_skills = []
    text = text.lower()

    for skill in skills_list:
        if skill in text:
            found_skills.append(skill)

    return found_skills

def calculate_similarity(resume, job_desc):
    cv = CountVectorizer()
    vectors = cv.fit_transform([resume, job_desc])
    similarity = cosine_similarity(vectors)[0][1]
    return round(similarity * 100, 2)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/analyze', methods=['POST'])
def analyze():
    file = request.files['resume']
    job_desc = request.form['job_desc']

    if not file.filename.endswith('.pdf'):
        return "Upload PDF only"

    if not os.path.exists('uploads'):
        os.makedirs('uploads')

    file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
    file.save(file_path)

    resume_text = extract_text(file_path)
    skills = extract_skills(resume_text)
    score = calculate_similarity(resume_text, job_desc)

    return render_template('result.html', skills=skills, score=score)

if __name__ == '__main__':
    app.run(debug=True)