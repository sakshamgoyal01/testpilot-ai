from fastapi import APIRouter
from pydantic import BaseModel
from ai_engine.generator import generate_tests_with_type

router = APIRouter()

class TestGenRequest(BaseModel):
    input_text: str
    type: str  # "Unit Tests", "API Tests", etc.

@router.post("/gen-tests")
def generate_tests(req: TestGenRequest):
    output, filename = generate_tests_with_type(req.input_text, req.type)
    return {"output": output, "filename": filename}
