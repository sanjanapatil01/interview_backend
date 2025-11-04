from flask import Flask,jsonify,request
from flask_cors import CORS
import re
from service.resume_parser import parse_resume12,extract_text
from service.interview_session import start_interview_session,handle_interview_session,get_session_report
import json
import time
import os
from service.ai_model import generate_final_report
from models import db
from config import DevelopmentConfig
from models import Candidate, FinalReport
import redis
from flask_migrate import Migrate

r = redis.Redis(host='localhost', port=6379, db=0)

def create_app():
    app = Flask(__name__)
    CORS(app,resources={r"/api/flask/*":{"origins":"*"}})
    app.config.from_object(DevelopmentConfig)
    #app.config.from_object(ProductionConfig)


    db.init_app(app)

    # with app.app_context():
    #     db.create_all()
    migrate = Migrate(app, db)

    return app


app = create_app()

# # session_id, question = start_interview_session('data\Suhen M G_Resume (2).pdf')

# # while True:
# #     print("AI asks:", question)
# #     answer = input("Your Answer: ")
# #     response = handle_interview_session(session_id, answer)
# #     os.system('cls')
# #     if response["stop"]:
# #         print("Interview Finished!")
# #         result=get_session_report(session_id)
# #         final_report=generate_final_report(result)
# #         print(final_report)
# #         break
# #     question = response["next_question"]




def save_resume_file(file):
    upload_dir = "uploads/"
    os.makedirs(upload_dir, exist_ok=True)
    file_path = os.path.join(upload_dir, file.filename)
    file.save(file_path)
    return file_path


@app.route('/api/flask/upload_resume', methods=['POST'])
def upload_resume():
    file = request.files['resume']
    name = request.form['name']
    email = request.form['email']

    file_path = save_resume_file(file)
    resume_text = extract_text(file_path)

    user = Candidate(name=name, email=email, resume_text=resume_text, resume_path=file_path)
    db.session.add(user)
    db.session.commit()

    return jsonify({
        "user_id": user.id,
        "message": "Resume uploaded successfully"
    })


@app.route('/api/flask/start_interview', methods=['POST'])
def start_interview():
    user_id = request.json.get('user_id')
    user = Candidate.query.get(user_id)

    if not user:
        return jsonify({"error": "User not found"}), 404

    session_id, first_question = start_interview_session(user_id)

    return jsonify({
        "session_id": session_id,
        "first_question": first_question
    })


@app.route('/api/flask/submit_answer/<int:user_id>', methods=['POST'])
def submit_answer(user_id):
    data = request.json
    session_id = data.get('session_id')
    answer = data.get('answer')

    session_data = r.get(session_id)
    user_id = request.json.get('user_id')

    user = Candidate.query.get(user_id)
    resume_data = user.resume_text if user else None
    if not session_id or not answer:
        return jsonify({"error": "session_id and answer are required"}), 400

    result = handle_interview_session(session_id, answer,resume_data)

    if result.get("stop"):
        session_data = r.get(session_id)
        if session_data:
            session = json.loads(session_data)
            user_id = session['user_id']
            final_report_data = generate_final_report(session)

            if isinstance(final_report_data, dict):
                final_report_text = json.dumps(final_report_data)
            else:
                final_report_text = final_report_data  
            report = FinalReport(user_id=user_id, report_text=final_report_text)
            db.session.add(report)
            db.session.commit()
        r.delete(session_id)

        return jsonify({
            "message": "Interview Finished!",
            "final_report": final_report_data 
        })

    return jsonify(result)



# # @app.route('/api/flask/save_report', methods=['POST'])
# # def save_report():
# #     data = request.json
# #     user_id = data.get("user_id")
# #     report_text = data.get("report_text")
# #     user = Candidate.query.get(user_id)
# #     if not user:
# #         return jsonify({"error": "User not found"}), 404
# #     final_report = FinalReport(user_id=user_id, report_text=report_text)
# #     db.session.add(final_report)
# #     db.session.commit()
# #     return jsonify({"message": "Final report saved successfully"})


@app.route('/api/flask/get_report/<int:user_id>', methods=['GET'])
def get_report(user_id):
    user = Candidate.query.get(user_id)
    if not user:
        return jsonify({"error": "User not found"}), 404
    report = FinalReport.query.filter_by(user_id=user_id).order_by(FinalReport.id.desc()).first()
    if not report:
        return jsonify({"error": "Report not found"}), 404

    return jsonify({
        "user_id": user.id,
        "name": user.name,
        "email": user.email,
        "report_text": json.loads(report.report_text)
    })


if __name__=='__main__':
    app.run()

