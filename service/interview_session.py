import uuid
from service.llm_model import dynamic_questions_gen_model
from service.resume_parser import parse_resume12,extract_text
from service.ai_model import evaluate_answer
import json
import time
import redis


r = redis.Redis(host='localhost', port=6379, db=0)

"""
def question_genrator(resume_text):
    #resume_text=extract_text(file_path)
    data=parse_resume12(resume_text)
    resume_output=json.dumps(data,indent=2)
    gererated_questions=generate_question(resume_output)
    return gererated_questions

"""

"""
# def start_interview_session(user_id,resume_text):
#     value = generate_question(resume_text)
#     questions = []
#     session_id = str(uuid.uuid4())
#     session_data = {
#         "user_id": user_id,
#         "questions": questions,
#         "current_question": 0,
#         "answers": []
#         # 'resume_text': value  
#     }

#     r.set(session_id, json.dumps(session_data))
#     r.expire(session_id, 86400)  

#     return session_id, questions[0]
"""

def start_interview_session(user_id):
    questions = "Tell me about yourself"
    session_id = str(uuid.uuid4())
    session_data = {
        "user_id": user_id,
        "question_no":1,
        "data":[]  
    }
    session_data['data'].append({
        'question':questions,
        'answer':None
    })

    r.set(session_id, json.dumps(session_data))
    r.expire(session_id, 86400)  
    return session_id,questions


"""
# def handle_interview_session(session_id, answer):
#     data = r.get(session_id)
#     if not data:
#         return {"error": "Session not found."}
#     session = json.loads(data)

#     q_index = session['current_question']
#     max_questions = len(session['questions'])

#     evaluation = evaluate_answer(
#         question=session['questions'][q_index],
#         answer=answer,
#         max_questions=max_questions,
#         current_index=q_index
#     )

#     session['answers'].append({
#         "question": session['questions'][q_index],
#         "answer": answer,
#         "evaluation": evaluation
#     })

#     session['current_question'] += 1

#     r.set(session_id, json.dumps(session))
#     r.expire(session_id, 86400)
#     if session['current_question'] >= max_questions:
#         return {
#             "next_question": None,
#             "stop": True
#         }

#     return {
#         "next_question": session['questions'][session['current_question']],
#         "stop": False
#     }
"""

def handle_interview_session(session_id, answer,resume_data):
    data = r.get(session_id)
    if not data:
        return {"error": "Session not found."}
    session = json.loads(data)
    current_question=session['question_no']
    session['data'][current_question-1]['answer']=answer
    next_question=dynamic_questions_gen_model(resume_data,session,answer)
    print(f"Next question generated: {next_question}")
    session['data'].append({
        'question':next_question,
        'answer':None
    })
    session['question_no']=current_question+1
    print(f'This is the session:{session}')
    r.set(session_id, json.dumps(session))
    r.expire(session_id, 86400)
    if session['question_no'] >= 3:
        return {
            "next_question": None,
            "stop": True
        }

    return {
        "next_question": next_question,
        "stop": False
    }


def get_session_report(session_id):
    data = r.get(session_id)
    if not data:
        return {"error": "Session not found."}
    session = json.loads(data)
    return session