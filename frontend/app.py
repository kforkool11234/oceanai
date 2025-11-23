import streamlit as st
import requests
import json
import os

# Backend API URL
API_URL = "http://localhost:8001"

st.set_page_config(page_title="Autonomous QA Agent", layout="wide")

st.title("🤖 Autonomous QA Agent")

# Sidebar
st.sidebar.header("Configuration")
st.sidebar.info("Ensure the Backend is running on port 8000 and Ollama is serving.")

# Tabs
tab1, tab2, tab3 = st.tabs(["📚 Knowledge Base", "🧪 Test Case Generation", "📜 Script Generation"])

# --- Tab 1: Knowledge Base ---
with tab1:
    st.header("Build Knowledge Base")
    
    uploaded_files = st.file_uploader("Upload Support Documents & HTML", accept_multiple_files=True)
    
    if st.button("Upload & Build KB"):
        if uploaded_files:
            files = [('files', (file.name, file, file.type)) for file in uploaded_files]
            try:
                with st.spinner("Uploading files..."):
                    response = requests.post(f"{API_URL}/upload", files=files)
                
                if response.status_code == 200:
                    st.success("Files uploaded successfully!")
                    
                    with st.spinner("Ingesting documents into Vector DB..."):
                        build_response = requests.post(f"{API_URL}/build-kb")
                    
                    if build_response.status_code == 200:
                        st.success(f"Knowledge Base Built! {build_response.json()['message']}")
                    else:
                        st.error(f"Error building KB: {build_response.text}")
                else:
                    st.error(f"Error uploading files: {response.text}")
            except Exception as e:
                st.error(f"Connection Error: {e}")
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
                    response = requests.post(f"{API_URL}/generate-tests", params={"query": feature_query})
                
                if response.status_code == 200:
                    test_cases = response.json()
                    st.session_state['test_cases'] = test_cases
                    st.success(f"Generated {len(test_cases)} test cases.")
                else:
                    st.error(f"Error generating tests: {response.text}")
            except Exception as e:
                st.error(f"Connection Error: {e}")
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
                    payload = {"test_case": selected_test_case}
                    response = requests.post(f"{API_URL}/generate-script", json=payload)
                
                if response.status_code == 200:
                    script_code = response.json()['script_code']
                    st.subheader("Generated Python Script")
                    st.code(script_code, language='python')
                else:
                    st.error(f"Error generating script: {response.text}")
            except Exception as e:
                st.error(f"Connection Error: {e}")
    else:
        st.info("Please generate test cases in the previous tab first.")
