from fastapi import FastAPI
from pydantic import BaseModel
import chat
import main

app = FastAPI()

class request(BaseModel):
    query: str
    user: str

@app.post("/message")
def message_message(request: request):
    return chat.chat(query=request.query, user=request.user)

@app.post("/setapptrue")
def set_appointment_true(numerical: str):
    main.set_visited(numerical=numerical)

