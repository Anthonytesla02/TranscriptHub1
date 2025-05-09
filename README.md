# TranscriptHub

A web application that extracts YouTube video transcripts and allows users to chat with AI about the content.

## Features

- Extract transcripts from YouTube videos
- Chat with AI about the video content
- Summarize video transcripts
- User authentication system
- Persistent chat history

## Local Development

1. Clone the repository
2. Install dependencies:
   ```
   pip install -r requirements.txt
   ```
3. Set up environment variables:
   - Copy `.env.example` to `.env`
   - Fill in required values (especially the Mistral API key)
4. Run the application:
   ```
   python main.py
   ```

## Deploying to Vercel

1. Push your code to GitHub
2. Connect your GitHub repository to Vercel
3. Set up the following environment variables in Vercel:
   - `MISTRAL_API_KEY`: Your Mistral API key
   - `SECRET_KEY`: A secure random string for Flask sessions
   - `FLASK_ENV`: Set to `production`
4. Deploy!

## Important Notes for Vercel Deployment

- The application uses SQLite in Vercel's serverless environment for simplicity
- For production use with higher traffic, consider using a proper database service
- Make sure to set your Mistral API key in Vercel's environment variables

## Libraries Used

- Flask: Web framework
- Flask-SQLAlchemy: ORM for database operations
- Flask-Login: User authentication
- youtube-transcript-api: Extract YouTube transcripts
- Mistral AI: AI model for chat functionality