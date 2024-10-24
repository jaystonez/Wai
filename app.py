from dotenv import load_dotenv
load_dotenv()
from flask import Flask, render_template, request, jsonify
from flask_jwt_extended import JWTManager, create_access_token, jwt_required
from flask_socketio import SocketIO, send
from dotenv import load_dotenv
import os
import threading
import time
from openai import OpenAI

client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

# Load environment variables from .env
load_dotenv()

app = Flask(__name__)
app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY', 'super-secret-key')

# Initialize JWT Manager and SocketIO
jwt = JWTManager(app)
socketio = SocketIO(app)

# ChatGPT Assistant route
@app.route('/chat', methods=['POST'])
def chat_with_gpt():
    user_message = request.json.get('message')
    if not user_message:
        return jsonify({"error": "No message provided"}), 400

    # Call OpenAI GPT-3.5-turbo
    try:
        response = client.chat.completions.create(model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": user_message}],
        max_tokens=150)
        return jsonify({"response": response.choices[0].message.content})
    except Exception as e:
        return jsonify({"error": f"OpenAI API error: {str(e)}"}), 500

# VIP repair logic
def standard_repair():
    print("Performing standard repair...")

def intermediate_repair():
    print("Performing intermediate repair...")

def advanced_repair():
    print("Performing advanced repair...")

def vip_repair():
    print("Performing VIP repair...")

@app.route('/repair/<level>', methods=['POST'])
def repair(level):
    if level == 'standard':
        standard_repair()
    elif level == 'intermediate':
        intermediate_repair()
    elif level == 'advanced':
        advanced_repair()
    elif level == 'vip':
        vip_repair()
    else:
        return jsonify({"error": "Invalid repair level"}), 400

    return jsonify({"message": f"{level.capitalize()} repair initiated."}), 200

# Dashboard
@app.route('/dashboard')
def dashboard():
    last_repair = "2024-10-13 14:22:05"
    last_commit = "Added security fixes"
    active_users = 4
    return render_template('dashboard.html', last_repair=last_repair, last_commit=last_commit, active_users=active_users)

# Git Clone API
@app.route('/git_clone', methods=['POST'])
def git_clone():
    repo_url = request.json.get('repo_url')
    try:
        git.Repo.clone_from(repo_url, "cloned_repo")
        socketio.emit('task_complete', {'message': f"Repository cloned successfully from {repo_url}"} )
        return jsonify({"message": "Repository cloned successfully."}), 200
    except Exception as e:
        return jsonify({"message": f"Error cloning repository: {str(e)}"}), 400

# Git Push API
@app.route('/git_push', methods=['POST'])
def git_push():
    try:
        repo = git.Repo("my_flask_app")
        repo.git.add(all=True)
        repo.index.commit("Auto commit from Flask Assistant")
        origin = repo.remote(name="origin")
        origin.push()
        socketio.emit('task_complete', {'message': "Changes pushed to the remote repository."})
        return jsonify({"message": "Changes pushed to the remote repository."}), 200
    except Exception as e:
        return jsonify({"message": f"Error pushing changes: {str(e)}"}), 400

# Git Diff API
@app.route('/git_diff', methods=['GET'])
def git_diff():
    try:
        repo = git.Repo("my_flask_app")
        diff = repo.git.diff('HEAD~1..HEAD')  # Compare the last two commits
        return jsonify({"diff": diff}), 200
    except Exception as e:
        return jsonify({"message": f"Error fetching Git diff: {str(e)}"}), 400

# Real-Time Collaboration via WebSocket
@socketio.on('code_edit')
def handle_code_edit(data):
    send(f"Code updated by user: {data['changes']}", broadcast=True)

# Schedule VIP Repairs
def run_scheduler():
    while True:
        schedule.run_pending()
        time.sleep(1)

@app.route('/schedule_vip_repair', methods=['POST'])
def schedule_vip_repair():
    schedule.every().day.at("02:00").do(lambda: print("Running VIP repair..."))
    return jsonify({"message": "VIP repair scheduled for 2 AM daily."}), 200

threading.Thread(target=run_scheduler).start()

# JWT Authentication route
@app.route('/api/login', methods=['POST'])
def login():
    if not request.json or 'username' not in request.json or 'password' not in request.json:
        return jsonify({"msg": "Missing username or password"}), 400

    username = request.json.get('username')
    password = request.json.get('password')

    if username == 'admin' and password == 'password':
        access_token = create_access_token(identity=username)
        return jsonify(access_token=access_token), 200
    else:
        return jsonify({"msg": "Invalid credentials"}), 401

# Code Saving API (for the real-time code editor)
@app.route('/save_code', methods=['POST'])
def save_code():
    new_code = request.json.get('code')
    try:
        with open("my_flask_app/app.py", "w") as f:
            f.write(new_code)
        return jsonify({"message": "Code saved successfully."}), 200
    except Exception as e:
        return jsonify({"message": f"Error saving code: {str(e)}"}), 400

# Run Flask and SocketIO
if __name__ == '__main__':
    socketio.run(app, debug=True)
