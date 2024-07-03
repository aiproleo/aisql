import streamlit as st
from utils import sidebar_definition

sidebar_definition.st_logo('🦣PostgreSQL')
#------------------------------------------------------------------------------------------------
import os

from app.db  import db_handler
from app.llm import llm_handler
from app.ui  import streamlit_ui

with st.spinner('loading'):
    if __name__ == "__main__":
        # Initialize the database handler with the PostgreSQL URI
        db_handler = db_handler.DatabaseHandler(os.environ.get('POSTGRESQL_AI_URI'))
        
        # Initialize the language model handler with the OpenAI API key
        openai_api_key = os.getenv("OPENAI_API_KEY")
        llm_handler = llm_handler.LLMHandler(openai_api_key)
        
        # Create an instance of the Streamlit UI and pass the handlers to it
        app = streamlit_ui.StreamlitUI(db_handler, llm_handler)
        
        # Run the Streamlit application
        app.run()