from flask import Flask
from service.question_generator import generate_question
from service.resume_parser import parse_resume12,extract_text
from service.interview_session import start_interview_session,handle_interview_session,get_session_report
import json
import time
import os
  
session_id, question = start_interview_session('resume.pdf')

while True:
    print("AI asks:", question)
    answer = input("Your Answer: ")
    response = handle_interview_session(session_id, answer)
    os.system('cls')
    if response["stop"]:
        print("Interview Finished!")
        print(f'Final Report:{get_session_report(session_id)}')
        break
    question = response["next_question"]
