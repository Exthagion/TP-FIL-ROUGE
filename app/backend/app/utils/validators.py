import re
from fastapi import HTTPException

def validate_email(email: str):
    email_regex = r"[^@]+@[^@]+\.[^@]+"
    if not re.match(email_regex, email):
        raise HTTPException(status_code=400, detail="Invalid email address.")
