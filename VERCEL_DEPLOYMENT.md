# Vercel Deployment Guide

This document provides instructions for deploying the TranscriptHub application to Vercel.

## Prerequisites

1. A Vercel account (free tier works fine)
2. Git repository with your code

## Configuration Overview

The application is already configured for Vercel deployment with:

- **In-memory database**: Due to Vercel's serverless model and read-only filesystem, the app uses an in-memory SQLite database with pre-populated demo data when running on Vercel.
- **Custom handler**: A special `vercel_handler.py` file is used to initialize the Flask app properly in the Vercel environment.
- **Static files**: Static assets are properly routed in the configuration.

## Steps to Deploy

### 1. Install Vercel CLI (Optional)

```bash
npm i -g vercel
```

### 2. Login to Vercel (Optional if using Vercel dashboard)

```bash
vercel login
```

### 3. Deploy from Vercel Dashboard

1. Go to [Vercel Dashboard](https://vercel.com/dashboard)
2. Click "New Project"
3. Import your Git repository
4. Configure the following settings:
   - Framework Preset: Other
   - Build Command: Leave blank (uses `./build.sh` from vercel.json)
   - Output Directory: Leave blank
   - Install Command: Leave blank (handled by build.sh)
   
### 4. Environment Variables

The following environment variables are already configured in `vercel.json` but you should update them in the Vercel dashboard for security:

- `MISTRAL_API_KEY`: Your Mistral API key (update this with your actual key)
- `FLASK_SECRET_KEY`: Secret key for Flask sessions

### 5. Deploy

Click "Deploy" button in Vercel dashboard, or if using CLI:

```bash
vercel
```

### 6. Check Your Deployment

After deployment completes, Vercel will provide a URL to access your application.

## Deployment Details

### Database Management

The application will:
1. Detect the Vercel environment automatically
2. Use an in-memory SQLite database when running on Vercel
3. Pre-populate the database with a demo user and sample data for demonstration purposes
4. The demo account credentials are: username=`demo`, password=`demo123`

### Troubleshooting

If you encounter any issues during deployment:

1. Check the Vercel build logs for specific error messages
2. Ensure all required environment variables are set
3. Verify the Python version is compatible (we're using Python 3.9)
4. Look for any logs from our custom error handler

## Updating Your Deployment

For subsequent deployments, simply push changes to your Git repository, and Vercel will automatically rebuild and deploy your application.

## Production Considerations

- The in-memory database is reset on each serverless function invocation, which means data will not persist between requests in the Vercel environment. This setup is for demonstration purposes only.
- For a production deployment with persistent data, consider using a managed database service.
- Vercel's serverless functions have execution time limits, which may affect some API calls.