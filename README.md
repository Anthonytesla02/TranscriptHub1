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
   - `MISTRAL_API_KEY`: Your Mistral API key (from [Mistral AI platform](https://console.mistral.ai/))
   - `SECRET_KEY`: A secure random string for Flask sessions
   - `FLASK_ENV`: Set to `production`
4. Deploy!

### Setting Up Mistral API Key

1. Sign up at [console.mistral.ai](https://console.mistral.ai/)
2. Go to your API Keys section
3. Create a new API key
4. Copy the key value
5. In Vercel, go to your project settings
6. Add the environment variable `MISTRAL_API_KEY` with the value you copied
7. Redeploy your project

If you don't set up the API key correctly, transcript summarization and chat features won't work.

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

## Troubleshooting Vercel Deployment

If you encounter errors during Vercel deployment, check the following:

1. **Missing API Key**: Make sure the `MISTRAL_API_KEY` environment variable is set in Vercel.
   - Error message: "No Mistral API key found in environment" 
   - Solution: Add the API key in your Vercel project settings

2. **Database Errors**: SQLite database needs to be properly initialized.
   - Error message: "Error setting up SQLite database"
   - Solution: This should be handled automatically by the improved setup script

3. **YouTube Transcript API Errors**: Make sure your video URLs are valid.
   - Error message: "No transcript found for this video"
   - Solution: Try a different video or format

4. **Runtime Errors**: Check the Vercel function logs for specific error details.
   - Solution: Logs can be viewed in your Vercel dashboard under the "Functions" tab