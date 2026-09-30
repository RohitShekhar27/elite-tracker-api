from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
import datetime

app = FastAPI(title="Elite Tracker API", version="1.0")

# CORS setup for Next.js frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_methods=["*"],
    allow_headers=["*"],
)

class Task(BaseModel):
    title: str
    category: str
    status: str = "pending"

class DailyLog(BaseModel):
    date: str
    hours_mtech: float
    hours_dsa: float
    hours_ai: float
    notes: str

# In-memory storage for demonstration (Replace with Supabase Client)
tasks_db = []
logs_db = []

@app.post("/api/tasks")
async def create_task(task: Task):
    tasks_db.append(task.dict())
    return {"message": "Task added to ecosystem", "task": task}

@app.get("/api/tasks")
async def get_tasks():
    return {"tasks": tasks_db}

@app.post("/api/ai-insights")
async def generate_insights(log: DailyLog):
    """
    Future integration point for LangChain + Ollama.
    Will analyze study logs to suggest dynamic timetable adjustments.
    """
    logs_db.append(log.dict())
    
    # Placeholder AI Logic
    insight = "Optimal progress."
    if log.hours_dsa < 2.0:
        insight = "Warning: DSA hours below threshold for upcoming tech interviews. Prioritize Leetcode today."
    elif log.hours_mtech > 5.0:
        insight = "Heavy academic load detected. Shift focus to AI implementation or rest to prevent burnout."
        
    return {
        "status": "success",
        "date_analyzed": log.date,
        "ai_recommendation": insight
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
