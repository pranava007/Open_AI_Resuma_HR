import os
from dotenv import load_dotenv
from openai import OpenAI
from pypdf import PdfReader
import json
import re

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def extract_resume_data(pdf_path):

    reader = PdfReader(pdf_path)
    full_text = " ".join(page.extract_text() or "" for page in reader.pages)

    prompt = f"""
    You are a resume parser.

    Extract details and return ONLY valid JSON.
    Do NOT add explanations.
    Do NOT add markdown.
    Do NOT wrap with ```.

    JSON format:
    {{
      "Name": "",
      "Email": "",
      "Phone": "",
      "Skills": "",
      "Education": "",
      "Location": ""
    }}

    Resume Text:
    {full_text}
    """

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        temperature=0
    )

    raw = response.choices[0].message.content.strip()

    # 🔧 CLEAN JSON (very important)
    cleaned = re.search(r"\{.*\}", raw, re.S)
    if cleaned:
        raw = cleaned.group()

    try:
        data = json.loads(raw)
    except Exception as e:
        print("JSON parse error:", e)
        print("RAW RESPONSE:", raw)

        data = {
            "Name": "",
            "Email": "",
            "Phone": "",
            "Skills": "",
            "Education": "",
            "Location": ""
        }

    # ✅ Ensure all keys exist
    for key in ["Name", "Email", "Phone", "Skills", "Education", "Location"]:
        data.setdefault(key, "")

    return {
        "parsed": data,
        "text": full_text
    }
