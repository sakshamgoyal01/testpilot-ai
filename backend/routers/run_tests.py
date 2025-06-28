from fastapi import APIRouter, UploadFile, File, Form
from fastapi.responses import JSONResponse
import subprocess, os
from backend.ai_engine.error_analyzer import analyze_error

router = APIRouter()

@router.post("/run-tests")
async def run_tests(
    file: UploadFile = File(...),
    type: str = Form(...),
    debug_with_ai: bool = Form(False)
):
    # Save file to disk
    os.makedirs("temp_tests", exist_ok=True)
    file_path = f"temp_tests/{file.filename}"
    with open(file_path, "wb") as f:
        f.write(await file.read())

    # Run the test using subprocess (pytest or custom command)
    result = subprocess.run(["pytest", file_path], capture_output=True, text=True)

    ai_analysis = None
    if debug_with_ai and result.returncode != 0:
        ai_analysis = analyze_error(result.stderr)

    return JSONResponse({
        "output": result.stdout + result.stderr,
        "error_ai": ai_analysis
    })
