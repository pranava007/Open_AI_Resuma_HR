import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def match_resume_with_jd(resume_text, job_description):

    prompt = f"""
    You are an ATS system.

    Compare resume vs job description.

    Respond strictly as:
    Match: <number>
    Reason: <one sentence>

    Resume:
    {resume_text}

    Job Description:
    {job_description}
    """

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        temperature=0
    )

    text = response.choices[0].message.content

    match = 0
    reason = ""

    for line in text.splitlines():
        if line.lower().startswith("match"):
            match = int("".join(filter(str.isdigit, line)) or 0)
        elif line.lower().startswith("reason"):
            reason = line.split(":", 1)[-1].strip()

    return match, reason
