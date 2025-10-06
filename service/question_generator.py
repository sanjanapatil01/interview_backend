from openai import OpenAI
import json

API_KEY='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'


client = OpenAI(
  api_key="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"
)

def generate_question(input):
    prompt = f"""
    You are an experienced interviewer. Based on this candidate resume:
    {input}
    Generate interview questions with the following rules:
    - The very first question must always be: "Tell me about yourself."
    - For technical: Generate 1 questions, mostly hard-level and a few moderate-level, based strictly on the candidate's skills and projects. 
      Include scenario-based, problem-solving, and real-world application questions.
    - For HR: Generate 1 questions (moderate-to-hard) focusing on behavior, decision-making, and conflict resolution.
    - For general: Generate 0 questions (career goals, achievements, personality, current trends, industry knowledge).
    - Make sure the majority of the questions are hard-level, but 0-1 can be moderate.
    - Output strictly in JSON format with keys: technical, hr, general.

    """
    response = client.responses.create(
    model="gpt-4o-mini",
    input=prompt,
    store=True,
    )
    raw_data=response.output_text
    try:
      json_index=raw_data.index('{')
      data = json.loads(raw_data[json_index:-3])
      return data
    except json.JSONDecodeError as e:
      return f"JSON Decode Error: {e}"
        
     












#
