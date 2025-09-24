from openai import OpenAI
import json

client = OpenAI(
    api_key="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"
)

def evaluate_answer(resume_text, question, answer, max_questions, current_index):
    prompt = f"""
You are an experienced technical interviewer.
Evaluate the candidate's answer based on their resume and the asked question.

Resume:
{resume_text}

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
