# Vercel Deployment Guide

This document provides instructions for deploying the application to Vercel.

## Prerequisites

1. A Vercel account (free tier works fine)
2. Git repository with your code

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
   - Build Command: Leave default (or use `./build.sh` if needed)
   - Output Directory: Leave default
   - Development Command: Leave default
   
### 4. Environment Variables

The following environment variables are already configured in `vercel.json` but you may want to update them in the Vercel dashboard for security:

- `SQLALCHEMY_DATABASE_URI`: Database connection string (currently configured for SQLite)
- `MISTRAL_API_KEY`: Your Mistral API key
- `FLASK_SECRET_KEY`: Secret key for Flask sessions

### 5. Deploy

Click "Deploy" button in Vercel dashboard, or if using CLI:

```bash
vercel
```

### 6. Check Your Deployment

After deployment completes, Vercel will provide a URL to access your application.

## Troubleshooting

If you encounter any issues during deployment:

1. Check the Vercel build logs for specific error messages
2. Ensure all required environment variables are set
3. Verify the Python version is compatible (we're using Python 3.9)
4. Check if the database connection is working properly

## Updating Your Deployment

For subsequent deployments, simply push changes to your Git repository, and Vercel will automatically rebuild and deploy your application.

## Notes

- The application uses SQLite for simplicity, but for production use, consider migrating to a more robust database like PostgreSQL.
- Vercel deployments are serverless and have certain limitations, including a maximum execution time.