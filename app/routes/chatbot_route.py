from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import os
import httpx
from typing import List, Dict, Any
from app.service.chatbot import chatboat

router = APIRouter()

@router.post("/chat")
async def chat_endpoint(prompt:str):
    try:
        msg =chatboat(prompt)
        return {"response": msg}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
