from fastapi import APIRouter
from datetime import datetime, timedelta
import random

router = APIRouter()

def generate_test_logs(n=200):
    projects = [
        "Login API", "Signup UI", "Dashboard View", "Payment Gateway",
        "User Profile", "Notification Service", "Search Engine", "Analytics UI"
    ]
    statuses = ["passed", "failed"]
    logs = []
    today = datetime.today()

    for i in range(1, n + 1):
        status = random.choice(statuses)
        log = {
            "id": i,
            "project": random.choice(projects),
            "status": status,
            "risk_score": random.randint(10, 95) if status == "failed" else random.randint(10, 50),
            "date": (today - timedelta(days=random.randint(0, 7))).strftime("%Y-%m-%d")
        }
        logs.append(log)

    return logs


@router.get("/metrics")
def get_dashboard_metrics():
    """
    Return test run metrics for dashboard consumption
    """
    return generate_test_logs(n=200)  # You can change `n` as needed
