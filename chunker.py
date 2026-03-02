"""
Converts structured resume dict into flat text chunks for embedding.
Each chunk has a 'key' (category) and 'text' (embeddable string).
"""


def build_chunks(resume: dict) -> list:
    chunks = []

    # --- Personal ---
    p = resume.get("personal", {})
    chunks.append({
        "key": "personal",
        "text": (
            f"Name: {p.get('name')}. "
            f"Email: {p.get('email')}. "
            f"Phone: {p.get('phone')}. "
            f"Location: {p.get('location')}."
        )
    })

    # --- Summary ---
    if resume.get("summary"):
        chunks.append({
            "key": "summary",
            "text": f"Professional Summary: {resume['summary']}"
        })

    # --- Skills (one chunk per category) ---
    for category, items in resume.get("skills", {}).items():
        label = category.replace("_", " ").title()
        chunks.append({
            "key": "skills",
            "text": f"Vamsi's {label} skills: {', '.join(items)}."
        })

    # --- Education ---
    for edu in resume.get("education", []):
        chunks.append({
            "key": "education",
            "text": (
                f"Education: {edu['degree']} from {edu['college']}, "
                f"{edu['location']}. Year: {edu['year']}. CGPA: {edu['cgpa']}."
            )
        })

    # --- Experience ---
    for exp in resume.get("experience", []):
        chunks.append({
            "key": "experience",
            "text": (
                f"Work Experience: {exp.get('role')} at {exp.get('company')}. "
                f"Duration: {exp.get('duration')}. "
                f"Details: {exp.get('description')}"
            )
        })

    # --- Projects ---
    for proj in resume.get("projects", []):
        chunks.append({
            "key": "projects",
            "text": (
                f"Project: {proj['title']}. "
                f"Technologies used: {', '.join(proj['tech'])}. "
                f"Description: {proj['description']}"
            )
        })

    # --- Certifications ---
    if resume.get("certifications"):
        chunks.append({
            "key": "certifications",
            "text": f"Certifications: {'; '.join(resume['certifications'])}."
        })

    # --- Achievements ---
    if resume.get("achievements"):
        chunks.append({
            "key": "achievements",
            "text": f"Achievements: {' '.join(resume['achievements'])}"
        })

    # --- Soft Skills ---
    if resume.get("soft_skills"):
        chunks.append({
            "key": "soft_skills",
            "text": f"Soft skills: {', '.join(resume['soft_skills'])}."
        })

    # --- Languages ---
    if resume.get("languages_known"):
        chunks.append({
            "key": "languages",
            "text": f"Languages known: {', '.join(resume['languages_known'])}."
        })

    return chunks
