import os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

app = FastAPI(
    title="AI Proposal Writer API",
    description="API for generating professional client proposals using Groq AI.",
    version="1.0.0"
)

# Configure CORS for frontend access
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # For production, replace "*" with the Vercel frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize Groq client
api_key = os.getenv("GROQ_API_KEY")
client = Groq(api_key=api_key) if api_key else None

class ProposalRequest(BaseModel):
    client_name: str
    project_name: str
    project_description: str
    budget: str
    timeline: str
    additional_notes: str = ""

@app.post("/generate-proposal")
async def generate_proposal(request: ProposalRequest):
    if not client:
        raise HTTPException(
            status_code=500, 
            detail="Groq API key is not configured on the server."
        )

    prompt = f"""
You are an expert freelance/agency proposal writer. Write a professional, compelling, and tailored client proposal based on the following details:

Client Name: {request.client_name}
Project Name: {request.project_name}
Project Description: {request.project_description}
Budget: {request.budget}
Timeline: {request.timeline}
Additional Notes: {request.additional_notes}

The proposal MUST include the following sections formatted exactly as headers:
1. Executive Summary
2. Scope of Work
3. Deliverables
4. Timeline
5. Pricing Section
6. Terms & Conditions
7. Next Steps

Use clear, professional language. Format the output in Markdown so it is easy to read. 
Do not include any introductory conversation; output only the final proposal starting directly with the title or first header.
"""

    try:
        chat_completion = client.chat.completions.create(
            messages=[
                {
                    "role": "system",
                    "content": "You are a senior SaaS engineer and professional proposal writer."
                },
                {
                    "role": "user",
                    "content": prompt,
                }
            ],
            model="llama-3.3-70b-versatile",  # Using Groq's high-performance Llama 3.3 model
            temperature=0.7,
            max_tokens=2048,
        )
        
        proposal = chat_completion.choices[0].message.content
        return {"proposal": proposal}
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to generate proposal: {str(e)}")
