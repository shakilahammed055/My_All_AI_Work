from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import os
import httpx
from typing import List, Dict, Any
from app.service.sytem_prompt import sytempromptchatbot


router = APIRouter()


@router.post("/systemprompt")
async def chat_endpoint(prompt: str):
    try:
        msg = sytempromptchatbot(prompt)
        return {"response": msg}
    except Exception as e:
        detail = str(e)
        # If it's a rate-limit upstream, forward 429 to the client
        if "429" in detail or "rate-limited" in detail or "rate limit" in detail:
            raise HTTPException(status_code=429, detail=detail)
        raise HTTPException(status_code=500, detail=detail)
