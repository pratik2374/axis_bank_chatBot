"""Simple chatbot UI for Axis Bank Document Verification."""

import streamlit as st
from pathlib import Path
import tempfile
import os
from dotenv import load_dotenv

# Page configuration
st.set_page_config(
    page_title="Axis Bank Document Verification Chatbot",
    page_icon="🏦",
    layout="wide"
)

    # Title
st.title("🏦 Axis Bank Document Verification Chatbot")
st.markdown("Chat with our AI assistant to verify your documents")


OPENAI_API_KEY = st.secrets["OPENAI_API_KEY"]

if OPENAI_API_KEY :
    os.environ["OPENAI_API_KEY"] = OPENAI_API_KEY
    from verification_agent import create_agent

    # Initialize session state
    if "agent" not in st.session_state:
        st.session_state.agent = create_agent()
    if "messages" not in st.session_state:
        st.session_state.messages = []
    if "uploaded_files" not in st.session_state:
        st.session_state.uploaded_files = {}
    if "temp_dir" not in st.session_state:
        st.session_state.temp_dir = tempfile.mkdtemp()


    def save_uploaded_file(uploaded_file, temp_dir: str) -> str:
        """Save uploaded file to temporary directory and return path."""
        file_path = os.path.join(temp_dir, uploaded_file.name)
        with open(file_path, "wb") as f:
            f.write(uploaded_file.getbuffer())
        return file_path


    # Sidebar
    with st.sidebar:
        st.header("📋 Quick Info")
        
        st.markdown("""
        ### Supported Documents
        - Aadhaar Card
        - PAN Card
        - Passport
        - Utility Bills
        - Bank Statements
        - Salary Slips
        - Form 16
        - ITR Documents
        
        ### Common Purposes
        - Account Opening
        - Address Update
        - Loan Application
        - Credit Card KYC
        - Business Account
        """)
        
        st.markdown("---")
        st.markdown("### Document Upload")
        uploaded_files = st.file_uploader(
            "Upload Documents",
            type=["jpg", "jpeg", "png", "pdf"],
            accept_multiple_files=True,
            help="Upload your documents here, then ask the chatbot to verify them"
        )
        
        if uploaded_files:
            # Save all uploaded files
            new_files = []
            for uploaded_file in uploaded_files:
                file_path = save_uploaded_file(uploaded_file, st.session_state.temp_dir)
                if uploaded_file.name not in st.session_state.uploaded_files:
                    new_files.append(uploaded_file.name)
                st.session_state.uploaded_files[uploaded_file.name] = file_path
            
            if new_files:
                st.success(f"✅ {len(new_files)} new file(s) uploaded: {', '.join(new_files)}")
                file_list = "\n".join([f"- **{name}**" for name in new_files])
                st.session_state.messages.append({
                    "role": "assistant",
                    "content": f"✅ I've received your document(s):\n\n{file_list}\n\nYou can ask me to verify them by saying:\n- 'Verify {new_files[0]}'\n- 'Check my uploaded documents'\n- 'Analyze my PAN card' (or other document type)\n- 'Is my Aadhaar card valid?'"
                })
                st.rerun()
            else:
                st.info(f"📁 {len(uploaded_files)} file(s) already uploaded")

    # Display chat messages
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Chat input
    if prompt := st.chat_input("Ask me about document verification..."):
        # Add user message
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)
        
        # Get agent response
        with st.chat_message("assistant"):
            with st.spinner("Analyzing..."):
                try:
                    # Build context about uploaded files
                    user_message = prompt
                    
                    # Always include file information if files are uploaded
                    if st.session_state.uploaded_files:
                        file_info = "\n\n[UPLOADED FILES AVAILABLE FOR ANALYSIS]\n"
                        for filename, file_path in st.session_state.uploaded_files.items():
                            # Verify file exists
                            if os.path.exists(file_path):
                                file_info += f"File: {filename}\nPath: {file_path}\n\n"
                            else:
                                file_info += f"File: {filename} (path not found: {file_path})\n\n"
                        
                        file_info += "You can use the analyze_document_image tool with these file paths to verify documents."
                        user_message = prompt + file_info
                    
                    # Get response from agent
                    response = st.session_state.agent.run(user_message)
                    
                    # Display response
                    assistant_response = response.content if hasattr(response, 'content') else str(response)
                    st.markdown(assistant_response)
                    
                    # Add to messages
                    st.session_state.messages.append({
                        "role": "assistant",
                        "content": assistant_response
                    })
                    
                except Exception as e:
                    error_msg = f"Sorry, I encountered an error: {str(e)}"
                    st.error(error_msg)
                    st.exception(e)
                    st.session_state.messages.append({
                        "role": "assistant",
                        "content": error_msg
                    })

    # Clear chat button
    if st.button("🗑️ Clear Chat"):
        st.session_state.messages = []
        st.session_state.uploaded_files = {}
        st.rerun()

    # Instructions
    with st.expander("ℹ️ How to use"):
        st.markdown("""
        ### How to Use This Chatbot
        
        1. **Upload Documents**: Use the sidebar to upload your documents (PAN, Aadhaar, etc.)
        
        2. **Ask Questions**: Type questions like:
        - "What documents do I need to open a savings account?"
        - "Verify my uploaded PAN card"
        - "Check if my documents are valid"
        - "Analyze my Aadhaar card"
        - "Is my passport valid?"
        
        3. **Get Verification**: The chatbot will:
        - Use AI vision to analyze your documents
        - Identify document types
        - Extract relevant information (with proper masking)
        - Check validity and detect tampering
        - Provide verification decisions
        - Guide you on next steps
        
        ### Example Prompts
        
        - "I want to open a savings account. What documents do I need?"
        - "Please verify the PAN card I uploaded"
        - "Check all my uploaded documents"
        - "Is my Aadhaar card valid?"
        - "Analyze my passport and tell me if it's authentic"
        
        ### Security Note
        
        All sensitive information (Aadhaar numbers, PAN numbers, etc.) will be automatically masked in responses for your security.
        """)
else:
    st.info("❗ OpenAI API Key Not Found, Please setup in (secrets.toml) file.")