import streamlit as st

class StreamlitUI:
    def __init__(self, db_handler, llm_handler):
        self.db_handler = db_handler
        self.llm_handler = llm_handler
        if "messages" not in st.session_state:
            st.session_state.messages = []

    def display_instructions(self):
        st.markdown(
            """
            ###### [Click to check Sample Database ERD](https://omnidevx.netlify.app/logo/postgresqlerd.png)
            ###### [Click to setup your own database](https://ai-pro.gitbook.io/ai-sql-linguist/installation/database-uri)

            ##### Sample queries
            - List all the films by ordered by their length
            - List how many films there are in each film category
            - Show the actors and actresses ordered by how many movies they are featured in
            - Get a list of all active customers, ordered by their first name

            ##### Challenge
            - What is the total revenue of each rental store?
            - Can you list the top 5 film genres by their gross revenue?
            - The film.description has the text type, allowing for full text search queries, what will you search for?        
            """)
        st.error("DON'T TRY: `DELETE, TRUNCATE, DROP TABLE, DROP DATABASE` ")

    def start_chat(self, uri):
        st.session_state.db_uri = uri
        st.session_state.unique_id = self.db_handler.save_db_details()
        return {"message": "Connection established to Database!"}

    def send_message(self, message):
        solution = self.llm_handler.get_the_output_from_llm(
            message, st.session_state.unique_id, st.session_state.db_uri)
        result = self.llm_handler.execute_the_solution(
            solution, st.session_state.db_uri)
        return {"message": solution + "\n\nResult:\n" + result}

    def display_chat(self):

        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.write(message["content"])

        if prompt := st.chat_input("Start with: show tables"):
            st.chat_message("user").markdown(prompt)
            st.session_state.messages.append(
                {"role": "user", "content": prompt})
            response = self.send_message(prompt)["message"]
            with st.chat_message("assistant"):
                st.markdown(response)
            st.session_state.messages.append(
                {"role": "assistant", "content": response})

    def run(self):
        self.display_instructions()
        if not st.session_state.get("db_uri"):
            st.warning("Please enter a valid database URI.")
        else:
            chat_response = self.start_chat(st.session_state.db_uri)
            if "error" in chat_response:
                st.error("Error: Failed to start the chat. Please check the URI and try again.")
            else:
                st.success("Chat started successfully!")
        
        self.display_chat()