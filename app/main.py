from fastapi import FastAPI, HTTPException
from app.github import get_pull_request_files
from app.analyzer import analyze_code_with_ai
from app.notifier import send_slack_message
from app.schemas import ReviewRequest

app = FastAPI()

@app.post("/review-pr")
async def review_pull_request(data: ReviewRequest):
    try:
        files = get_pull_request_files(data.owner, data.repo, data.pr_number)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Failed to fetch PR files: {e}")

    results = []

    for file in files:
        if file.get("filename", "").endswith(".py"):
            patch = file.get("patch")
            if patch:
                feedback = analyze_code_with_ai(patch)
                results.append(f"File: {file['filename']}\nFeedback:\n{feedback}\n")

    summary = "\n\n".join(results) if results else "No Python code changes detected."

    try:
        send_slack_message(f"Code review results for PR #{data.pr_number} in {data.owner}/{data.repo}:\n\n{summary}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to send Slack message: {e}")

    return {"message": "Review completed and notification sent.", "review": summary}
