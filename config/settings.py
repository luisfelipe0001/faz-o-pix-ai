import os

ENVIRONMENT = os.getenv("ENVIRONMENT", "development")
DEBUG = os.getenv("DEBUG", "False").lower() == "true"

# Streamlit Config
STREAMLIT_PAGE_TITLE = "Faz o Pix AI"
STREAMLIT_PAGE_ICON = "💰"
STREAMLIT_LAYOUT = "wide"
STREAMLIT_INITIAL_SIDEBAR_STATE = "expanded"

# App Config
APP_NAME = "Faz o Pix AI"
APP_VERSION = "1.0.0"

# Database Config
DATABASE_TIMEZONE = "America/Sao_Paulo"
