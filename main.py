import os
from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from youtube_transcript_api._api import YouTubeTranscriptApi
from youtube_transcript_api._errors import NoTranscriptFound, TranscriptsDisabled
from urllib.parse import urlparse, parse_qs
from models import db, User, Transcript

app = Flask(__name__)
app.config['SECRET_KEY'] = 'c1a4f89c0e3e44b88ac44f3458f0d391'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize extensions
db.init_app(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

def extract_video_id(url):
    parsed = urlparse(url)
    if parsed.hostname in ['youtu.be']:
        return parsed.path[1:]
    if parsed.path == '/watch':
        return parse_qs(parsed.query).get('v', [None])[0]
    return None

# Setup database tables
with app.app_context():
    db.create_all()

@app.route('/')
@login_required
def index():
    return render_template('index.html')

@app.route('/extract', methods=['POST'])
@login_required
def extract():
    video_url = request.form.get('video_url', '').strip()
    video_id = extract_video_id(video_url)

    if not video_id:
        flash('Invalid YouTube URL provided.', 'danger')
        return redirect(url_for('index'))

    try:
        transcript_list = YouTubeTranscriptApi.get_transcript(video_id, languages=['en'])
        transcript_text = "\n".join([entry['text'] for entry in transcript_list])

        # Save to database
        transcript = Transcript(video_url=video_url, content=transcript_text, user_id=current_user.id)
        db.session.add(transcript)
        db.session.commit()

        return render_template('result.html', transcript=transcript_text, video_url=video_url)

    except NoTranscriptFound:
        flash('No transcript found for this video.', 'warning')
    except TranscriptsDisabled:
        flash('Transcripts are disabled for this video.', 'warning')
    except Exception as e:
        flash('An unexpected error occurred.', 'danger')

    return redirect(url_for('index'))

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        password = generate_password_hash(request.form['password'])

        if User.query.filter_by(username=username).first():
            flash('Username already exists.', 'warning')
            return redirect(url_for('signup'))

        user = User(username=username, password=password)
        db.session.add(user)
        db.session.commit()
        flash('Account created! Please log in.', 'success')
        return redirect(url_for('login'))

    return render_template('signup.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user = User.query.filter_by(username=request.form['username']).first()
        if user and check_password_hash(user.password, request.form['password']):
            login_user(user)
            return redirect(url_for('index'))
        flash('Invalid username or password.', 'danger')

    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/dashboard')
@login_required
def dashboard():
    transcripts = Transcript.query.filter_by(user_id=current_user.id).order_by(Transcript.created_at.desc()).all()
    return render_template('dashboard.html', transcripts=transcripts)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)