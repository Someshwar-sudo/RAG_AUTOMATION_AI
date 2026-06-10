import streamlit as st
import requests
import uuid

# 1. Setup Browser Page Canvas Setup
st.set_page_config(page_title="RAG AI Automation", page_icon="🏢", layout="centered")
st.title("RAG Automation Engine")
st.write("Ask your local AI assistant any questions regarding your company policy manual.")

# 2. Generate and track a persistent user session tracking token
if "session_id" not in st.session_state:
    st.session_state.session_id = f"user_{str(uuid.uuid4())[:8]}"

# Initialize screen history array layout
if "messages" not in st.session_state:
    st.session_state.messages = []

# 3. Sidebar System Monitor Module panel
with st.sidebar:
    st.subheader("System Control Deck")
    st.info(f"**Active Session ID:** {st.session_state.session_id}")
    st.write("Wiping cache here resets the chat canvas but retains the master database layers.")
    if st.button("Flush Cache / New Session"):
        st.session_state.session_id = f"user_{str(uuid.uuid4())[:8]}"
        st.session_state.messages = []
        st.rerun()

# 4. Render existing conversation states to browser
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

# 5. Capture User Entry Actions from the input box
if user_input := st.chat_input("Ask a policy rule question..."):
    # Render user prompt locally
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.write(user_input)

    # 6. Setup Network Communication target maps
    FASTAPI_URL = "http://localhost:8000/api/chat"
    payload = {
        "session_id": st.session_state.session_id,
        "user_message": user_input
    }

    # Render loading spinner animation while executing the background network transaction
    with st.chat_message("assistant"):
        with st.spinner("Searching knowledge base via FastAPI..."):
            try:
                # Dispatch the data packet using HTTP POST
                response = requests.post(FASTAPI_URL, json=payload)
                
                if response.status_code == 200:
                    api_data = response.json()
                    ai_response = api_data.get("response", "Error parsing response payload.")
                else:
                    ai_response = f"Connection Failure: Backend returned server code {response.status_code}"
            
            except requests.exceptions.ConnectionError:
                ai_response = "Network Error: Could not establish connection with FastAPI on port 8000."

            # Render final text response on screen and append to state storage memory
            st.write(ai_response)
            st.session_state.messages.append({"role": "assistant", "content": ai_response})
