import uuid
from service.question_generator import generate_question
from service.resume_parser import parse_resume12,extract_text
from service.answer_evaluation import evaluate_answer
import json
import time

interview_session={}

def question_genrator(file_path):
    resume_text=extract_text(file_path)
    data=parse_resume12(resume_text)
    resume_output=json.dumps(data,indent=2)
    gererated_questions=generate_question(resume_output)
    return gererated_questions


def start_interview_session(file_path):
    value=question_genrator(file_path)
    questions=[]
    for i in value:
        time.sleep(3)
        for j in range(len(value[i])):
            questions.append(value[i][j]['question'])

    session_id=str(uuid.uuid4())
    interview_session[session_id]={
        "questions":questions,
        "current_question":0,
        'resume_text':value,
        "answers":[]
    } 

    return session_id,questions[0]

def handle_interview_session(session_id,answer):
    session=interview_session[session_id]
    max_questions=len(session['questions'])
    q_index=session['current_question']
    session['answers'].append({
        "question":session['questions'][q_index],
        "answer":answer
    })
    evaluation = evaluate_answer(
    resume_text=session['resume_text'],
    question=session['questions'][q_index],
    answer=answer,
    max_questions=max_questions,
    current_index=q_index
    )
    
    session['answers'][-1]['evaluation'] = evaluation
    session['current_question'] += 1

    if session['current_question'] >= max_questions:
        return {
            "next_question": None,
            "stop": True
        }
    return {
        "next_question": session['questions'][session['current_question']],
        "stop": False,
    }

def get_session_report(session_id):
    session=interview_session[session_id]
    if not session:
        return f"Session with id {session_id} not found."
    else:
        data=json.dumps(session,indent=2)
        return data