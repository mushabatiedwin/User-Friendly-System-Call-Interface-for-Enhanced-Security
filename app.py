from fastapi import FastAPI, Depends, HTTPException
from auth import get_current_user
from auth import create_jwt_token, fake_users_db
from fastapi.security import OAuth2PasswordRequestForm
from logger import log_system_call
import subprocess
from pydantic import BaseModel

app = FastAPI()

class CommandRequest(BaseModel):
    command: str

@app.get("/")
def read_root():
    return {"message": "Welcome to the Secure System Call API!"}

@app.post("/login")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = fake_users_db.get(form_data.username)
    if not user or user["password"] != form_data.password:
        raise HTTPException(status_code=401, detail="Invalid username or password")

    token = create_jwt_token(user["username"])
    return {"access_token": token, "token_type": "bearer"}

# Secure System Call Execution
@app.post("/execute")
async def execute_command(data: CommandRequest, user: dict = Depends(get_current_user)):
    allowed_commands = ["ls", "whoami", "uptime"]

    if data.command not in allowed_commands:
        raise HTTPException(status_code=403, detail="Unauthorized command")

    try:
        output = subprocess.check_output(data.command, shell=True, text=True)
        log_system_call(user["username"], data.command, output)  # Log command
        return {"user": user["username"], "command": data.command, "output": output}
    except subprocess.CalledProcessError as e:
        raise HTTPException(status_code=500, detail=str(e))

# uvicorn app:app --reload
