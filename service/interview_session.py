import uuid
from service.question_generator import generate_question
from service.resume_parser import parse_resume12,extract_text
from service.ai_model import evaluate_answer
import json
import time
import redis


r = redis.Redis(host='localhost', port=6379, db=0)

def question_genrator(resume_text):
    #resume_text=extract_text(file_path)
    data=parse_resume12(resume_text)
    resume_output=json.dumps(data,indent=2)
    gererated_questions=generate_question(resume_output)
    return gererated_questions


# def start_interview_session(resume_text):
#     value=question_genrator(resume_text)
#     questions=[]
#     for i in value:
#         time.sleep(3)
#         for j in range(len(value[i])):
#             questions.append(value[i][j]['question'])

#     session_id=str(uuid.uuid4())
#     interview_session[session_id]={
#         "questions":questions,
#         "current_question":0,
#         #'resume_text':value,
#         "answers":[]
#     } 

#     return session_id,questions[0]


def start_interview_session(user_id,resume_text):
    value = generate_question(resume_text)
    questions = []
    for key in value:
        time.sleep(0.5) 
        for q in value[key]:
            questions.append(q['question'])

    session_id = str(uuid.uuid4())
    session_data = {
        "user_id": user_id,
        "questions": questions,
        "current_question": 0,
        "answers": []
        # 'resume_text': value  
    }

    r.set(session_id, json.dumps(session_data))
    r.expire(session_id, 86400)  

    return session_id, questions[0]

# def handle_interview_session(session_id,answer):
#     session=interview_session[session_id]
#     max_questions=len(session['questions'])
#     q_index=session['current_question']
#     session['answers'].append({
#         "question":session['questions'][q_index],
#         "answer":answer
#     })
#     evaluation = evaluate_answer(
#     #resume_text=session['resume_text'],
#     question=session['questions'][q_index],
#     answer=answer,
#     max_questions=max_questions,
#     current_index=q_index
#     )
    
#     session['answers'][-1]['evaluation'] = evaluation
#     session['current_question'] += 1

#     if session['current_question'] >= max_questions:
#         return {
#             "next_question": None,
#             "stop": True
#         }
#     return {
#         "next_question": session['questions'][session['current_question']],
#         "stop": False,
#     }


def handle_interview_session(session_id, answer):
    data = r.get(session_id)
    if not data:
        return {"error": "Session not found."}
    session = json.loads(data)

    q_index = session['current_question']
    max_questions = len(session['questions'])

    evaluation = evaluate_answer(
        question=session['questions'][q_index],
        answer=answer,
        max_questions=max_questions,
        current_index=q_index
    )

    session['answers'].append({
        "question": session['questions'][q_index],
        "answer": answer,
        "evaluation": evaluation
    })

    session['current_question'] += 1

    r.set(session_id, json.dumps(session))
    r.expire(session_id, 86400)
    if session['current_question'] >= max_questions:
        return {
            "next_question": None,
            "stop": True
        }

    return {
        "next_question": session['questions'][session['current_question']],
        "stop": False
    }


def get_session_report(session_id):
    data = r.get(session_id)
    if not data:
        return {"error": "Session not found."}
    session = json.loads(data)
    return session