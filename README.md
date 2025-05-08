# TranscriptHub

A web application that extracts transcripts from YouTube videos and provides an AI-powered chatbot interface to interact with the content.

## Features

- Extract transcripts from YouTube videos
- Automatically generate summaries of video content
- Chat with an AI assistant about the video content
- User authentication system
- Mobile-responsive design

## Local Development

1. Clone the repository
2. Install dependencies: `pip install -r requirements.txt`
3. Run the application: `python main.py`

## Deployment on Vercel

This application is configured to deploy on Vercel. Follow these steps to deploy:

1. Fork or clone this repository to your GitHub account
2. Connect your Vercel account to your GitHub repository
3. Set up the following environment variables in Vercel:
   - `MISTRAL_API_KEY`: Your Mistral AI API key

4. Deploy the application

## Environment Variables

- `MISTRAL_API_KEY`: API key for Mistral AI (required for production)
- `DATABASE_URL`: PostgreSQL database URL (auto-configured in Replit)

## Tech Stack

- Flask: Web framework
- SQLAlchemy: Database ORM
- Mistral AI: Large language model for chat and summarization
- YouTube Transcript API: For extracting video transcripts
- PostgreSQL (local) / SQLite (Vercel): Database

## License

MIT