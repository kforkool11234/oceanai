from pydantic import BaseModel
from typing import List, Optional

class TestCase(BaseModel):
    test_id: str
    feature: str
    test_scenario: str
    expected_result: str
    grounded_in: str

class TestPlan(BaseModel):
    test_cases: List[TestCase]

class ScriptRequest(BaseModel):
    test_case: TestCase

class ScriptResponse(BaseModel):
    script_code: str
    explanation: Optional[str] = None
