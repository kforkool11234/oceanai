import sys
import os

# Add current directory to sys.path
sys.path.append(os.path.abspath(os.getcwd()))

try:
    from backend.ingestion import ingest_docs
    from backend.rag_agent import generate_test_cases, generate_selenium_script
    print("Imports successful!")
except ImportError as e:
    print(f"Import failed: {e}")
    sys.exit(1)
except Exception as e:
    print(f"An error occurred: {e}")
    sys.exit(1)
