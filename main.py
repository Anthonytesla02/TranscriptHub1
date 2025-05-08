import os
import json
from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from youtube_transcript_api._api import YouTubeTranscriptApi
from youtube_transcript_api._errors import NoTranscriptFound, TranscriptsDisabled
from urllib.parse import urlparse, parse_qs
from models import db, User, Transcript, Chat, Message
from utils import get_chat_response, summarize_transcript
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('FLASK_SECRET_KEY', 'c1a4f89c0e3e44b88ac44f3458f0d391')
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize extensions
db.init_app(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

def extract_video_id(url):
    """
    Extract the YouTube video ID from various YouTube URL formats.
    
    Supports:
    - Standard YouTube URLs: https://www.youtube.com/watch?v=VIDEO_ID
    - Short YouTube URLs: https://youtu.be/VIDEO_ID
    - Embed URLs: https://www.youtube.com/embed/VIDEO_ID
    - Video URLs: https://www.youtube.com/v/VIDEO_ID
    - Mobile URLs: https://m.youtube.com/watch?v=VIDEO_ID
    - Playlist URLs: Also extracts video ID from playlist URLs
    """
    if not url:
        return None
        
    # Clean the URL
    url = url.strip()
    
    # Extract using urlparse
    parsed_url = urlparse(url)
    
    # Check for youtu.be domain (short URLs)
    if parsed_url.netloc in ['youtu.be']:
        return parsed_url.path.strip('/')
    
    # For standard or mobile YouTube domains
    if any(domain in parsed_url.netloc for domain in ['youtube.com', 'm.youtube.com', 'www.youtube.com']):
        # Handle /watch path with v parameter
        if parsed_url.path == '/watch':
            query = parse_qs(parsed_url.query)
            return query.get('v', [None])[0]
            
        # Handle /embed/ or /v/ paths
        if '/embed/' in parsed_url.path or '/v/' in parsed_url.path:
            path_parts = parsed_url.path.split('/')
            # The ID should be after /embed/ or /v/
            for i, part in enumerate(path_parts):
                if part in ['embed', 'v'] and i < len(path_parts) - 1:
                    return path_parts[i + 1]
    
    # If all checks fail, return None
    return None

# Setup database tables
with app.app_context():
    db.create_all()
    
    # Create a test user if it doesn't exist
    if not User.query.filter_by(username='testuser').first():
        test_user = User(username='testuser', password=generate_password_hash('password123'))
        db.session.add(test_user)
        db.session.commit()

@app.route('/')
def landing():
    """Landing page with pricing and features"""
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    return render_template('landing.html')

@app.route('/home')
@login_required
def index():
    """Home page for authenticated users"""
    return render_template('index.html')

@app.route('/extract', methods=['POST'])
@login_required
def extract():
    video_url = request.form.get('video_url', '').strip()
    video_id = extract_video_id(video_url)

    if not video_id:
        flash('Invalid YouTube URL provided.', 'danger')
        return redirect(url_for('dashboard'))

    try:
        # Try with English first
        try:
            transcript_list = YouTubeTranscriptApi.get_transcript(video_id, languages=['en'])
        except NoTranscriptFound:
            # Fallback: try to get any available transcript if English isn't available
            transcript_list = YouTubeTranscriptApi.list_transcripts(video_id)
            
            # Get the first available transcript
            if transcript_list:
                transcript = transcript_list[0]
                transcript_list = transcript.fetch()
            else:
                raise NoTranscriptFound(f"No transcripts found for video ID: {video_id}")
                
        # Format the transcript with timestamps
        formatted_entries = []
        for entry in transcript_list:
            # Convert timestamp to minutes:seconds format
            timestamp_seconds = int(entry['start'])
            minutes = timestamp_seconds // 60
            seconds = timestamp_seconds % 60
            timestamp = f"[{minutes:02d}:{seconds:02d}] "
            
            # Add formatted entry
            formatted_entries.append(f"{timestamp}{entry['text']}")
            
        transcript_text = "\n".join(formatted_entries)

        # Save to database
        transcript = Transcript(video_url=video_url, content=transcript_text, user_id=current_user.id)
        db.session.add(transcript)
        db.session.commit()

        # Create an automatic summary
        try:
            summary = summarize_transcript(transcript_text)
        except Exception as e:
            print(f"Error generating summary: {str(e)}")
            summary = "Summary could not be generated automatically."

        return render_template('result.html', 
                              transcript=transcript_text, 
                              video_url=video_url, 
                              transcript_id=transcript.id,
                              summary=summary)

    except NoTranscriptFound:
        flash('No transcript found for this video.', 'warning')
    except TranscriptsDisabled:
        flash('Transcripts are disabled for this video.', 'warning')
    except Exception as e:
        import traceback
        error_details = traceback.format_exc()
        print(f"Error extracting transcript: {str(e)}")
        print(f"Traceback: {error_details}")
        flash(f'An error occurred: {str(e)}', 'danger')

    return redirect(url_for('dashboard'))

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
            return redirect(url_for('dashboard'))
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

@app.route('/create_chat/<int:transcript_id>', methods=['POST'])
@login_required
def create_chat(transcript_id):
    """Create a new chat for a transcript and redirect to the chat page"""
    transcript = Transcript.query.get_or_404(transcript_id)
    
    # Verify user has access to this transcript
    if transcript.user_id != current_user.id:
        flash('You do not have permission to access this transcript.', 'danger')
        return redirect(url_for('dashboard'))
    
    # Create a new chat
    title = f"Chat about YouTube video ({transcript.video_url})"
    chat = Chat(
        title=title,
        user_id=current_user.id,
        transcript_id=transcript_id
    )
    db.session.add(chat)
    db.session.commit()
    
    return redirect(url_for('chat', chat_id=chat.id))

@app.route('/chat/<int:chat_id>')
@login_required
def chat(chat_id):
    """Show the chat interface for a specific chat"""
    chat = Chat.query.get_or_404(chat_id)
    
    # Verify user has access to this chat
    if chat.user_id != current_user.id:
        flash('You do not have permission to access this chat.', 'danger')
        return redirect(url_for('dashboard'))
    
    # Get the transcript content
    transcript = Transcript.query.get(chat.transcript_id)
    messages = Message.query.filter_by(chat_id=chat_id).order_by(Message.timestamp).all()
    
    return render_template(
        'chat.html',
        chat=chat,
        transcript=transcript,
        messages=messages
    )

@app.route('/api/send_message', methods=['POST'])
@login_required
def send_message():
    """API endpoint to send a message and get an AI response"""
    data = request.json
    chat_id = data.get('chat_id')
    content = data.get('content')
    
    if not chat_id or not content:
        return jsonify({'error': 'Missing chat_id or content'}), 400
    
    # Verify the chat exists and belongs to the user
    chat = Chat.query.get_or_404(chat_id)
    if chat.user_id != current_user.id:
        return jsonify({'error': 'You do not have permission to access this chat'}), 403
    
    # Get the transcript
    transcript = Transcript.query.get(chat.transcript_id)
    
    # Save the user message
    user_message = Message(
        content=content,
        role='user',
        chat_id=chat_id
    )
    db.session.add(user_message)
    db.session.commit()
    
    # Get all messages for context
    messages = Message.query.filter_by(chat_id=chat_id).order_by(Message.timestamp).all()
    formatted_messages = [{'role': msg.role, 'content': msg.content} for msg in messages]
    
    # Get AI response
    try:
        ai_response = get_chat_response(formatted_messages, transcript.content)
        
        # Save the AI response
        assistant_message = Message(
            content=ai_response,
            role='assistant',
            chat_id=chat_id
        )
        db.session.add(assistant_message)
        db.session.commit()
        
        return jsonify({
            'response': ai_response,
            'message_id': assistant_message.id
        })
    except Exception as e:
        print(f"Error getting AI response: {str(e)}")
        return jsonify({'error': f'Error getting AI response: {str(e)}'}), 500

@app.route('/chats')
@login_required
def chats():
    """Show all chats for the current user"""
    user_chats = Chat.query.filter_by(user_id=current_user.id).order_by(Chat.created_at.desc()).all()
    return render_template('chats.html', chats=user_chats)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)