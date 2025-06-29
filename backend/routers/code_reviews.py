import subprocess, os, uuid
from fastapi import APIRouter, UploadFile, File
from ai_engine.refactor import ask_ai_for_review
from fastapi.responses import JSONResponse

router = APIRouter()


@router.post("/code-review")
async def review_code(file: UploadFile = File(...)):
    file_id = str(uuid.uuid4())
    path = f"uploaded_code/{file_id}_{file.filename}"

    os.makedirs("uploaded_code", exist_ok=True)  # ✅ Add this line

    with open(path, "wb") as f:
        f.write(await file.read())

    # Run Semgrep
    semgrep_cmd = f"semgrep --config=auto {path} --json"
    result = subprocess.run(semgrep_cmd.split(), capture_output=True, text=True)

    # Run Trivy (optional - if it's a repo)
    # trivy_cmd = f"trivy fs {path}"
    # ...

    # AI Feedback
    ai_feedback = ask_ai_for_review(path)

    # Risk Score (basic heuristic)
    issue_count = result.stdout.count('"check_id"')
    risk_score = min(100, issue_count * 10)

    return JSONResponse({
        "semgrep_output": result.stdout,
        "ai_feedback": ai_feedback,
        "risk_score": risk_score
    })
