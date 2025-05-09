import os

# Environment detection
IS_VERCEL = 'VERCEL' in os.environ
IS_PRODUCTION = IS_VERCEL or os.environ.get('FLASK_ENV') == 'production'

# Database configuration
if IS_VERCEL:
    # SQLite for Vercel (serverless) environment
    SQLALCHEMY_DATABASE_URI = 'sqlite:///transcripthub.db'
    DATABASE_TYPE = 'sqlite'
else:
    # PostgreSQL for local development
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')
    DATABASE_TYPE = 'postgresql'

SQLALCHEMY_TRACK_MODIFICATIONS = False

# App secret key - preferably from environment, with fallback
SECRET_KEY = os.environ.get('SECRET_KEY', 'c1a4f89c0e3e44b88ac44f3458f0d391')

# API configuration
MISTRAL_API_KEY = os.environ.get('MISTRAL_API_KEY')
MISTRAL_API_URL = "https://api.mistral.ai/v1/chat/completions"

# Get API key, first from environment, then fallback if needed
def get_mistral_api_key():
    if MISTRAL_API_KEY:
        print("Using Mistral API key from environment variables")
        return MISTRAL_API_KEY
    
    # This fallback should only be used for development/testing
    if not IS_PRODUCTION:
        print("WARNING: Using fallback Mistral API key (for development only)")
        return "nCmZyPuNmY8PfYzg8NyjAE8BpQQKAftB"
    
    print("ERROR: No Mistral API key found in environment")
    return None