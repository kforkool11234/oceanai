# Autonomous QA Agent

An intelligent, autonomous QA agent capable of constructing a "testing brain" from project documentation to generate test cases and Selenium scripts.

## Features
- **Knowledge Base Ingestion**: Uploads and processes project documents (Markdown, TXT, HTML) into a vector database.
- **Test Case Generation**: Uses LLM (Gemini API) to generate grounded test cases based on the knowledge base.
- **Selenium Script Generation**: Converts test cases into executable Python Selenium scripts using the target HTML structure.

## Prerequisites
- Python 3.8+
- [Google Gemini API Key](https://aistudio.google.com/app/apikey)

## Setup

1. **Clone/Download the repository**.
2. **Create a virtual environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: .\venv\Scripts\activate
   ```
3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```
4. **Set Environment Variables**:
   - Create a `.env` file or set it in your terminal:
     ```bash
     export GOOGLE_API_KEY="your_api_key_here"
     # On Windows PowerShell:
     $env:GOOGLE_API_KEY="your_api_key_here"
     ```

## Usage

### 1. Start the Backend (Flask)
Open a terminal and run:
```bash
python backend/main.py
```
The API will be available at `http://localhost:8000`.

### 2. Start the Frontend (Streamlit)
Open a new terminal and run:
```bash
streamlit run frontend/app.py
```
The UI will open in your browser at `http://localhost:8501`.

### 3. Workflow
1. **Build Knowledge Base**:
   - Go to the "Knowledge Base" tab.
   - Upload `checkout.html`, `product_specs.md`, and `ui_ux_guide.txt` (located in `assets/`).
   - Click "Upload & Build KB".
2. **Generate Test Cases**:
   - Go to the "Test Case Generation" tab.
   - Enter a feature to test (e.g., "Discount Code").
   - Click "Generate Test Cases".
3. **Generate Script**:
   - Go to the "Script Generation" tab.
   - Select a generated test case.
   - Click "Generate Script".
   - Copy the generated Python code and run it (ensure you have the correct webdriver installed).

## Project Structure
- `backend/`: Flask application and RAG logic.
- `frontend/`: Streamlit user interface.
- `data/`: Storage for uploaded docs and vector DB.
- `assets/`: Sample project files (`checkout.html`, etc.).
