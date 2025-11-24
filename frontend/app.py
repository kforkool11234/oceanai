import streamlit as st
import os
import sys

# Add the parent directory to sys.path to allow imports from backend
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from backend.ingestion import ingest_docs
from backend.rag_agent import generate_test_cases, generate_selenium_script
from werkzeug.utils import secure_filename

# Paths
DOCS_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), "../data/docs"))
os.makedirs(DOCS_PATH, exist_ok=True)

st.set_page_config(page_title="Autonomous QA Agent", layout="wide")

st.title("🤖 Autonomous QA Agent")

# Sidebar
st.sidebar.header("Configuration")
st.sidebar.info("This app runs entirely in Streamlit. Ensure Ollama is serving.")

# Tabs
tab1, tab2, tab3 = st.tabs(["📚 Knowledge Base", "🧪 Test Case Generation", "📜 Script Generation"])

# --- Tab 1: Knowledge Base ---
with tab1:
    st.header("Build Knowledge Base")
    
    uploaded_files = st.file_uploader("Upload Support Documents & HTML", accept_multiple_files=True)
    
    if st.button("Upload & Build KB"):
        if uploaded_files:
            try:
                saved_files = []
                with st.spinner("Uploading and saving files..."):
                    for file in uploaded_files:
                        if file.name == '':
                            continue
                        filename = secure_filename(file.name)
                        file_path = os.path.join(DOCS_PATH, filename)
                        with open(file_path, "wb") as f:
                            f.write(file.getbuffer())
                        saved_files.append(filename)
                
                st.success(f"Successfully saved {len(saved_files)} files.")
                    
                with st.spinner("Ingesting documents into Vector DB..."):
                    result = ingest_docs()
                    st.success(f"Knowledge Base Built! {result}")
                    
            except Exception as e:
                st.error(f"Error: {e}")
        else:
            st.warning("Please upload at least one file.")

# --- Tab 2: Test Case Generation ---
with tab2:
    st.header("Generate Test Cases")
    
    feature_query = st.text_input("Enter Feature to Test", placeholder="e.g., Discount code validation")
    
    if st.button("Generate Test Cases"):
        if feature_query:
            try:
                with st.spinner("Generating test cases... (This may take a while)"):
                    test_cases = generate_test_cases(feature_query)
                
                st.session_state['test_cases'] = test_cases
                st.success(f"Generated {len(test_cases)} test cases.")
            except Exception as e:
                st.error(f"Error generating tests: {e}")
        else:
            st.warning("Please enter a feature description.")
            
    if 'test_cases' in st.session_state:
        st.subheader("Generated Test Cases")
        for i, tc in enumerate(st.session_state['test_cases']):
            with st.expander(f"{tc.get('test_id', 'ID')} - {tc.get('test_scenario', 'Scenario')}"):
                st.json(tc)

# --- Tab 3: Script Generation ---
with tab3:
    st.header("Generate Selenium Script")
    
    if 'test_cases' in st.session_state and st.session_state['test_cases']:
        # Create a list of options for the selectbox
        options = [f"{tc.get('test_id')} - {tc.get('test_scenario')}" for tc in st.session_state['test_cases']]
        selected_option = st.selectbox("Select a Test Case", options)
        
        if st.button("Generate Script"):
            # Find the selected test case object
            selected_index = options.index(selected_option)
            selected_test_case = st.session_state['test_cases'][selected_index]
            
            try:
                with st.spinner("Generating Selenium script..."):
                    script_code = generate_selenium_script(selected_test_case)
                
                st.subheader("Generated Python Script")
                st.code(script_code, language='python')
            except Exception as e:
                st.error(f"Error generating script: {e}")
    else:
        st.info("Please generate test cases in the previous tab first.")
