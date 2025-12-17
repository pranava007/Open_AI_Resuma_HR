from flask import Flask, render_template, request
import os

from services.resume_parser import extract_resume_data
from services.jd_matcher import match_resume_with_jd

app = Flask(__name__)
UPLOAD_FOLDER = "resumes"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":

        jd = request.form["job_description"]
        files = request.files.getlist("resumes")

        results = []

        for file in files:
            path = os.path.join(UPLOAD_FOLDER, file.filename)
            file.save(path)

            resume = extract_resume_data(path)
            match, reason = match_resume_with_jd(resume["text"], jd)

            parsed = resume["parsed"]

            results.append({
                "name": parsed.get("Name", ""),
                "email": parsed.get("Email", ""),
                "skills": parsed.get("Skills", ""),
                "education": parsed.get("Education", ""),
                "location": parsed.get("Location", ""),
                "match": match,
                "reason": reason
            })

        results.sort(key=lambda x: x["match"], reverse=True)
        return render_template("result.html", results=results)

    return render_template("index.html")

if __name__ == "__main__":
    app.run("0.0.0.0", port=5000, debug=True)
