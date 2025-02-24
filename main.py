from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
import os
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from resume_parser import extract_text_from_pdf, extract_text_from_docx, extract_skills_and_experience

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///candidates.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)
class Candidate(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    skills = db.Column(db.Text, nullable=False)
    experience = db.Column(db.Text, nullable=False)
    match_score = db.Column(db.Float, nullable=False)

    def __init__(self, name, skills, experience, match_score):
        self.name = name
        self.skills = ", ".join(skills)
        self.experience = experience
        self.match_score = match_score

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)


@app.route('/')
def index():
    return render_template("index.html", skills=None, experience=None)
UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

job_description_text = ""  # Store the job description text

@app.route("/upload_job", methods=["POST"])
def upload_job():
    global job_description_text
    job_file = request.files["job_file"]

    if job_file:
        file_path = os.path.join(UPLOAD_FOLDER, job_file.filename)
        job_file.save(file_path)

        # Extract text based on file type
        if job_file.filename.endswith(".pdf"):
            job_description_text = extract_text_from_pdf(file_path)
        elif job_file.filename.endswith(".docx"):
            job_description_text = extract_text_from_docx(file_path)
        elif job_file.filename.endswith(".txt"):
            with open(file_path, "r", encoding="utf-8") as file:
                job_description_text = file.read()

        return "Job description uploaded successfully!"

    return "Failed to upload job description."


@app.route('/upload', methods=['POST'])

@app.route('/download_report')
def download_report():
    file_path = "static/candidate_report.pdf"  # Save file in static folder
    c = canvas.Canvas(file_path, pagesize=letter)
    width, height = letter

    c.setFont("Helvetica-Bold", 16)
    c.drawString(200, height - 50, "Candidate Report")

    candidates = Candidate.query.order_by(Candidate.match_score.desc()).all()

    y_position = height - 100
    c.setFont("Helvetica", 12)

    for candidate in candidates:
        c.drawString(50, y_position, f"Name: {candidate.name}")
        c.drawString(50, y_position - 20, f"Skills: {candidate.skills}")
        c.drawString(50, y_position - 40, f"Experience: {candidate.experience}")
        c.drawString(50, y_position - 60, f"Match Score: {candidate.match_score:.2f}")
        c.drawString(50, y_position - 80, "-" * 80)
        y_position -= 100

        if y_position < 100:  # Create a new page if space is running out
            c.showPage()
            y_position = height - 100

    c.save()
    return send_file(file_path, as_attachment=True)
def upload_file():
    if 'resume' not in request.files:
        return "No file part"

    file = request.files['resume']
    if file.filename == '':
        return "No selected file"

    file_path = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(file_path)

    # Extract text based on file type
    if file.filename.endswith(".pdf"):
        text = extract_text_from_pdf(file_path)
    elif file.filename.endswith(".docx"):
        text = extract_text_from_docx(file_path)
    else:
        return "Invalid file type"

    # Extract skills and experience
    skills, experience = extract_skills_and_experience(text)
    candidate = Candidate(uploaded_file.filename, skills, experience, match_score)
    db.session.add(candidate)
    db.session.commit()

    return render_template("index.html", skills=skills, experience=experience)


if __name__ == '__main__':
    if __name__ == '__main__':
        port = int(os.environ.get("PORT", 10000))  # Default to 10000 if PORT is not set
        app.run(host='0.0.0.0', port=port)
    app.run(debug=True)
