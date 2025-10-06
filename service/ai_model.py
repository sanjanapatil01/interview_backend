from openai import OpenAI
import json
import re

client = OpenAI(
    api_key="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"
)

def evaluate_answer( question, answer, max_questions, current_index):
    prompt = f"""
You are an experienced technical interviewer.
Evaluate the candidate's answer based on their resume and the asked question.




Question:
{question}

Answer:
{answer}

Instructions:
1. Give a score from 0 to 10 based on correctness, clarity, and relevance.
2. Provide short constructive feedback (1-2 sentences).
3. Suggest the next question (related to the resume or previous question).
4. If {current_index+1} >= {max_questions}, then stop the interview.

Return JSON only in this exact format:
{{
  "evaluation": {{
    "score": 0-10,
    "feedback": "short feedback"
  }},
  "next_question": {{
    "question": "text of the next question",
    "type": "Technical|HR|General"
  }},
  "stop": true|false
}}
"""

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "system", "content": "You are a helpful interviewer AI."},
                  {"role": "user", "content": prompt}],
        temperature=0.3 
    )

    
    try:
        result = json.loads(response.choices[0].message.content)
    except Exception as e:
        result = {
            "evaluation": {"score": 0, "feedback": "Error parsing AI response."},
            "next_question": {"question": "Please continue.", "type": "General"},
            "stop": False
        }
    return result

def clean_report(raw_data):
    sections = re.split(r'\n## ', raw_data)  # Split by section headers at level 2

    report_dict = {}

    for sec in sections:
        if sec.strip():
            lines = sec.strip().split('\n', 1)
            header = lines[0].strip()
            content = lines[1].strip() if len(lines) > 1 else ''
            report_dict[header] = content
    result=json.loads(report_dict) 
    return result
      

# def generate_final_report(session_data):
#     prompt=f"""You are an AI interview evaluator. You are given a candidate’s interview session data, which includes:
#     - Resume context
#     - Questions asked
#     - Candidate’s answers
#     - Scores (1–10) for each answer
#     - Feedback for each answer
#     {session_data}
#     Your task is to generate a structured final report that looks professional and concise.  
     
#     The report must include the following sections:

#     1. Candidate Overview
#       - Summarize the candidate’s background based on their resume.

#     2. Overall Performance
#       - Average score across all questions (round to 1 decimal).
#       - Performance level (e.g., Beginner, Intermediate, Advanced).
#       - 2–3 line summary of overall performance.

#     3. Strengths
#       - Bullet points highlighting strong aspects from higher-scoring answers.

#     4. Weaknesses
#       - Bullet points highlighting areas that need improvement from lower-scoring answers.

#     5. Section-wise Evaluation
#       - If questions are categorized (e.g., Technical, HR, General), give average score and short feedback for each section.

#     6. Question-wise Breakdown
#       - For each question: show Question, Answer (candidate’s), Score, and Feedback.

#     7. Final Recommendation
#       - Choose one: “Hire”, “Consider with Training”, or “Not Recommended”.
#       - Give 1–2 sentences justification.

#     Format the output in clean, readable text with headings and bullet points (not raw JSON) """

#     response = client.chat.completions.create(
#     model="gpt-4o-mini",
#     messages=[{"role": "user", "content": prompt}]
#     )
#     content = response.choices[0].message.content.strip()

#     if content.startswith('{') or content.startswith('['):
#         raw_data = json.loads(content)
#         #result=clean_report(raw_data)
#         resul=raw_data
#     else:
#         result=content  
#     return  result


import json

def generate_final_report(session_data):
    prompt = f"""
You are an AI interview evaluator. You are given a candidate’s interview session data:
{session_data}

Your task is to generate a structured final report in **JSON format only**. 
The JSON must have the following structure:

{{
  "candidate_overview": {{
    "name": "<candidate name>",
    "email": "<candidate email>",
    "summary": "<brief summary based on resume>"
  }},
  "overall_performance": {{
    "average_score": <average score>,
    "performance_level": "<Beginner|Intermediate|Advanced>",
    "summary": "<2-3 line summary of overall performance>"
  }},
  "strengths": ["<bullet points of strengths>"],
  "weaknesses": ["<bullet points of weaknesses>"],
  "section_wise_evaluation": {{
    "Technical": {{
      "average_score": <score>,
      "feedback": "<short feedback>"
    }},
    "HR": {{
      "average_score": <score>,
      "feedback": "<short feedback>"
    }},
    "General": {{
      "average_score": <score>,
      "feedback": "<short feedback>"
    }}
  }},
  "question_wise_breakdown": [
    {{
      "question": "<question text>",
      "answer": "<candidate answer>",
      "score": <score>,
      "feedback": "<feedback>",
      "type": "<Technical|HR|General>"
    }}
  ],
  "final_recommendation": {{
    "decision": "<Hire|Consider with Training|Not Recommended>",
    "justification": "<1-2 sentence justification>"
  }}
}}

Return the JSON **only**, do not add any text or explanation outside the JSON.
"""

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}]
    )

    content = response.choices[0].message.content.strip()

    try:
        result = json.loads(content)
    except json.JSONDecodeError:
        # fallback if AI fails to generate valid JSON
        result = {"error": "AI did not return valid JSON", "raw_output": content}

    return result

