from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from .ingestion import query_vector_db
import json
import re
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize LLM (Gemini)
# Ensure GOOGLE_API_KEY is set in environment variables
api_key = os.environ.get("GOOGLE_API_KEY")
if not api_key:
    print("WARNING: GOOGLE_API_KEY not found in environment variables.")

llm = ChatGoogleGenerativeAI(model="gemini-2.0-flash", google_api_key=api_key)

def generate_test_cases(feature_description):
    # 1. Retrieve Context
    context_docs = query_vector_db(feature_description, k=5)
    context_text = "\n\n".join([doc.page_content for doc in context_docs])

    # 2. Prompt Engineering
    prompt_template = """
    You are an expert QA Engineer. Your task is to generate comprehensive test cases based strictly on the provided documentation.
    
    Context from documentation:
    {context}
    
    User Request: {feature}
    
    Generate a list of test cases in JSON format. Each test case should have:
    - test_id (e.g., TC-001)
    - feature (The feature being tested)
    - test_scenario (Description of the test)
    - expected_result (What should happen)
    - grounded_in (The specific document or rule this is based on)
    
    Do not hallucinate features. Only use the provided context.
    Output ONLY valid JSON.
    """
    
    prompt = PromptTemplate(template=prompt_template, input_variables=["context", "feature"])
    chain = prompt | llm | StrOutputParser()
    
    # 3. Generate
    response = chain.invoke({"context": context_text, "feature": feature_description})
    
    # 4. Parse JSON (Basic cleanup if LLM adds text around JSON)
    try:
        # Find JSON substring
        match = re.search(r'\[.*\]', response, re.DOTALL)
        if match:
            json_str = match.group(0)
            return json.loads(json_str)
        else:
            # Try parsing the whole thing
            return json.loads(response)
    except Exception as e:
        print(f"Error parsing LLM response: {e}")
        return [{"test_id": "ERROR", "feature": "Error", "test_scenario": "Failed to parse LLM output", "expected_result": str(e), "grounded_in": "System"}]

def generate_selenium_script(test_case_json):
    # 1. Retrieve Context (HTML and Rules)
    # We specifically want the HTML content for selectors
    context_docs = query_vector_db("checkout.html HTML structure IDs classes", k=3)
    # Also get rules related to the test case
    rule_docs = query_vector_db(test_case_json.get('test_scenario', ''), k=3)
    
    context_text = "\n\n".join([doc.page_content for doc in context_docs + rule_docs])

    # 2. Prompt
    prompt_template = """
    You are an expert Selenium Python automation engineer.
    
    Task: Generate a runnable Selenium Python script for the following test case.
    
    Test Case:
    {test_case}
    
    Context (HTML and Rules):
    {context}
    
    Requirements:
    - Use `webdriver.Chrome()`
    - Use explicit waits (`WebDriverWait`) where appropriate.
    - Use correct selectors based on the HTML context provided.
    - Include assertions to verify the Expected Result.
    - The script should be complete and runnable.
    - Assume the HTML file is at `file:///C:/Users/kaush/OneDrive/Desktop/oceanai/qa_agent/assets/checkout.html` (Adjust path if needed but keep it local).
    
    Output ONLY the Python code. No markdown formatting like ```python.
    """
    
    prompt = PromptTemplate(template=prompt_template, input_variables=["context", "test_case"])
    chain = prompt | llm | StrOutputParser()
    
    response = chain.invoke({"context": context_text, "test_case": json.dumps(test_case_json)})
    
    # Cleanup markdown code blocks if present
    response = response.replace("```python", "").replace("```", "").strip()
    
    return response
