#!/usr/bin/env python
# coding: utf-8

# In[4]:


import re

def clean_spacing(text):
    return re.sub(r"([a-z])([A-Z])", r"\1 \2", text)

def normalize_bullets(text):
    return text.replace("\uf0b7", "•").replace("•", "\n•")

def extract_sections(text):
    headers = [
        "Objective", "Education", "PCMC", "SSLC", "Projects",
        "Skills", "Technical Skills", "Achievements", "Extra-Curricular Activities", "NLP"
    ]
    pattern = r"(?i)(" + "|".join(headers) + r")\s*(.*?)(?=\n(" + "|".join(headers) + r")\s|\Z)"
    matches = re.finditer(pattern, text, flags=re.DOTALL|re.IGNORECASE)
    return {
        m.group(1).strip().lower().replace(" ", "_"): clean_spacing(m.group(2).strip())
        for m in matches
    }

def extract_embedded_sections(text):
    headers = ["Skills", "Technical Skills", "Achievements", "Extra-Curricular Activities"]
    pattern = r"(?i)(" + "|".join(headers) + r")\s*(.*?)(?=\n(" + "|".join(headers) + r")\s|\Z)"
    matches = re.finditer(pattern, text, flags=re.DOTALL)
    return {
        m.group(1).strip().lower().replace(" ", "_"): clean_spacing(m.group(2).strip())
        for m in matches
    }

def parse_education_block(text):
    parts = text.split("|")
    return {
        "stream": parts[0].strip() if len(parts) > 0 else None,
        "percentage": parts[1].strip() if len(parts) > 1 else None,
        "duration": parts[2].strip() if len(parts) > 2 else None,
        "institution": clean_spacing(parts[-1].strip()) if parts else None
    }

def detect_graduation(text):
    lines = text.split("\n")
    for line in lines:
        if "Bachelor" in line or "Engineering" in line:
            return {
                "degree": line.strip(),
                "institution": next((l.strip() for l in lines if "College" in l), None),
                "duration": next((l.strip() for l in lines if re.search(r"\d{4}", l)), None)
            }
    return None

def parse_projects(text):
    lines = text.strip().split("\n")
    projects = []
    buffer = []
    title = None
    for line in lines:
        line_clean = clean_spacing(line.strip())
        if re.match(r"^[A-Z].*\(.*\)$", line_clean) or re.match(r"^\d+\.", line_clean):
            if buffer:
                projects.append({
                    "title": title or "Untitled Project",
                    "description": " ".join(buffer).strip()
                })
                buffer = []
            title = re.sub(r"^\d+\.\s*", "", line_clean)
        else:
            buffer.append(line_clean)
    if buffer:
        projects.append({
            "title": title or "Untitled Project",
            "description": " ".join(buffer).strip()
        })
    return projects

def parse_skills(text):
    skills = {}
    lines = text.split("\n")
    for line in lines:
        line_clean = clean_spacing(line.strip())
        if ":" in line_clean:
            key, val = line_clean.split(":", 1)
            skills[key.strip().lower().replace(" ", "_")] = [v.strip() for v in val.split(",")]
        elif line_clean:
            skills.setdefault("misc", []).append(line_clean)
    return skills

def parse_bullets(text):
    return [clean_spacing(line.strip("•").strip()) for line in text.split("\n") if line.strip("•").strip()]

def parse_resume12(raw_text):
    raw_text = normalize_bullets(raw_text)
    sections = extract_sections(raw_text)
    structured = {}

    
    if "objective" in sections:
        structured["objective"] = sections["objective"]

    
    structured["education"] = {}
    if "pcmc" in sections:
        structured["education"]["pcmc"] = parse_education_block(sections["pcmc"])
        embedded = extract_embedded_sections(sections["pcmc"])
        if "skills" in embedded or "technical_skills" in embedded:
            structured["skills"] = parse_skills(
                embedded.get("skills", "") + embedded.get("technical_skills", "")
            )
        if "extra_curricular_activities" in embedded:
            structured["extra_curricular"] = parse_bullets(embedded["extra_curricular_activities"])
        if "achievements" in embedded:
            structured["achievements"] = parse_bullets(embedded["achievements"])

    if "sslc" in sections:
        structured["education"]["sslc"] = parse_education_block(sections["sslc"])

    
    if "education" not in structured or "bachelor" not in structured["education"]:
        grad = detect_graduation(raw_text)
        if grad:
            structured["education"]["bachelor"] = grad

    
    if "projects" in sections:
        structured["projects"] = parse_projects(sections["projects"])

    
    if "skills" in sections:
        structured.setdefault("skills", {}).update(parse_skills(sections["skills"]))
    if "technical_skills" in sections:
        structured.setdefault("skills", {}).update(parse_skills(sections["technical_skills"]))
    if "nlp" in sections:
        tools_match = re.search(r"Tools&Platforms:(.*?)\n", sections["nlp"])
        if tools_match:
            structured.setdefault("skills", {})["tools_and_platforms"] = [
                t.strip() for t in tools_match.group(1).split(",")
            ]

    
    if "achievements" in sections:
        structured["achievements"] = parse_bullets(sections["achievements"])

    
    if "extra_curricular_activities" in sections:
        structured["extra_curricular"] = parse_bullets(sections["extra_curricular_activities"])

    return structured


# In[5]:


#import docx
import pdfplumber
from pathlib import Path

def extract_text_from_pdf(pdf_path):
    text = ""
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            text += page.extract_text() or ""   
            text += "\n" 
    return text

def extract_text_from_docx(docx_path):
    doc = docx.Document(docx_path)
    full_text = []
    for para in doc.paragraphs:
        full_text.append(para.text)
    return "\n".join(full_text)

def extract_text(file_path):
    path = Path(file_path)
    if path.suffix.lower() == ".pdf":
        extracted_text=extract_text_from_pdf(file_path)
        return extracted_text
    elif path.suffix.lower() in [".docx", ".doc"]:
        return extract_text_from_docx(file_path)
    else:
        raise ValueError("Unsupported file type: only PDF/DOCX allowed")


