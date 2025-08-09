from pydantic import BaseModel

class ReviewRequest(BaseModel):
    owner: str
    repo: str
    pr_number: int
