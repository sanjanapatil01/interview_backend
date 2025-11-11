from openai import OpenAI
import json

# API_KEY='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'


# client = OpenAI(
#   api_key="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"
# )

# def generate_question(input):
#     prompt = f"""
#     You are an experienced interviewer. Based on this candidate resume:
#     {input}
#     Generate interview questions with the following rules:
#     - The very first question must always be: "Tell me about yourself."
#     - For technical: Generate 1 questions, mostly hard-level and a few moderate-level, based strictly on the candidate's skills and projects. 
#       Include scenario-based, problem-solving, and real-world application questions.
#     - For HR: Generate 1 questions (moderate-to-hard) focusing on behavior, decision-making, and conflict resolution.
#     - For general: Generate 0 questions (career goals, achievements, personality, current trends, industry knowledge).
#     - Make sure the majority of the questions are hard-level, but 0-1 can be moderate.
#     - Output strictly in JSON format with keys: technical, hr, general.

#     """
#     response = client.responses.create(
#     model="gpt-4o-mini",
#     input=prompt,
#     store=True,
#     )
#     raw_data=response.output_text
#     try:
#       json_index=raw_data.index('{')
#       data = json.loads(raw_data[json_index:-3])
#       return data
#     except json.JSONDecodeError as e:
#       return f"JSON Decode Error: {e}"
        
from llama_cpp import Llama
from flask import jsonify
llm=Llama(model_path='models/mistral-7b-instruct-v0.1.Q4_K_M.gguf',n_ctx=4096)


def dynamic_questions_gen_model(resume_data, history, last_answer):

  prompt= f"""
        You are continuing a professional job interview. You are an expert HR and Technical interviewer.
        Your primary goal is to generate the next question for the candidate, strictly adhering to the specified format.

        # Resume Data:
        {resume_data}

        # Candidate's Last Answer Analysis:
        The candidate just finished answering the previous question: "{last_answer}" 

        # GOAL AND INSTRUCTION FOR NEXT QUESTION:
        1.  **Analyze the Last Answer:** Evaluate the candidate's last response for depth, clarity, and specific claims.
        2.  **Determine Next Focus (Priority Order):**
            * **Priority 1 (Technical Drill-Down/Hard):** If the candidate mentioned a specific technology, metric, or project detail in their last answer, generate a **Hard-level follow-up question** to drill down into that specific point (e.g., "How would you handle a race condition in the specific microservice architecture you just described?").
            * **Priority 2 (Topic Coverage/Moderate to Hard):** If a drill-down isn't warranted, switch to a topic that has NOT been covered yet, rotating between the following categories:
                * **Technical Core Skill:** Ask a hard question about a core skill from the resume.
                * **Behavioral/HR:** Ask a moderate-to-hard question focusing on conflict, ethics, or decision-making.
                * **General/Career:** Ask a moderate question about career goals, weaknesses, or industry trends.
        3.  **Interview Termination Rule (CRITICAL):** If you believe the candidate is fully assessed and the interview is complete, output the following termination JSON object: 
            {{ "action": "terminate", "reason": "All core areas assessed, ready for final report." }}

        # FINAL OUTPUT CONSTRAINT:
        - If the interview is NOT complete, you must generate **ONLY** a single JSON object.
        - The JSON object must contain the generated question text under the key "question".
        - **DO NOT include any analysis, labels (e.g., # Analysis:), prefixes, or explanation outside of the JSON structure.**

        # JSON Output Format:
        {{
          "action": "ask", 
          "question": "<The single generated question text>"
        }}
        """
  
  formatted = f"<s>[INST] {prompt.strip()} [/INST]"
  output = llm(
      formatted, 
      max_tokens=512,
      stream=False,
      )
  question_text = output["choices"][0]["text"].strip()
  print(f'the generated question is :{question_text}')
  # return question_text
  try:
    parsed = json.loads(question_text)
  except json.JSONDecodeError as e:
    print("Failed to parse JSON:", e)
    raise ValueError("LLM returned invalid JSON format")
  if not isinstance(parsed, dict) or "question" not in parsed:
     raise ValueError("Parsed output missing 'question' key")
  return parsed['question']











#
