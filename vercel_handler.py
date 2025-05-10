"""
Vercel serverless handler for Flask application
This file helps with handling Flask application in Vercel serverless environment
"""

import sys
import traceback
import os
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger("vercel_handler")

# Set environment variables for Vercel
os.environ["VERCEL"] = "1"

try:
    logger.info("Initializing app in Vercel environment")
    from wsgi import app
    logger.info("App initialized successfully")
    
    # Log database configuration (without sensitive info)
    db_uri = os.environ.get('SQLALCHEMY_DATABASE_URI', 'Not set')
    if 'sqlite' in db_uri:
        logger.info(f"Using SQLite database: {db_uri}")
    else:
        # Don't log full URI to avoid exposing credentials
        db_type = db_uri.split('://')[0] if '://' in db_uri else 'unknown'
        logger.info(f"Using database type: {db_type}")
    
except Exception as e:
    logger.error(f"Error initializing app: {str(e)}")
    logger.error(traceback.format_exc())
    raise e

def handler(event, context):
    """
    Vercel serverless function handler
    """
    try:
        return app(event, context)
    except Exception as e:
        logger.error(f"Error handling request: {str(e)}")
        logger.error(traceback.format_exc())
        return {
            'statusCode': 500,
            'body': f'Internal Server Error: {str(e)}'
        }