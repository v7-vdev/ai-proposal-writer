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
You are a world-class freelance and agency proposal writer. Your goal is to write a highly professional, compelling, and tailored proposal for {request.client_name} regarding the "{request.project_name}" project.

### INPUT DATA:
- Client Name: {request.client_name}
- Project Name: {request.project_name}
- Project Description: {request.project_description}
- TOTAL BUDGET: {request.budget}
- Timeline: {request.timeline}
- Additional Notes: {request.additional_notes}

### STRICT CONSTRAINTS:
1. **BUDGET INTEGRITY**: You MUST use the exact total budget provided: {request.budget}. NEVER invent a different number.
2. **PRICING ACCURACY**: The "Pricing Section" MUST contain a detailed breakdown. Every line item in the breakdown MUST sum exactly to the total budget of {request.budget}. Double-check your math.
3. **NO PLACEHOLDERS**: Do NOT use placeholder text like "[Insert Date]", "[Company Name]", or "[Your Name]". Use the provided data or leave it professional and generic without brackets.
4. **NATURAL INTEGRATION**: Mention {request.client_name} and "{request.project_name}" naturally throughout the text to make it feel custom-made.
5. **SPECIFICITY**: Tailor the "Scope of Work" and "Deliverables" specifically to the project description: {request.project_description}.

### REQUIRED SECTIONS (Markdown Headers):
1. Executive Summary
2. Scope of Work
3. Deliverables
4. Timeline
5. Pricing Section
6. Terms & Conditions
7. Next Steps

Format the entire output in clean Markdown. Do not include any pre-text, post-text, or conversational filler. Start immediately with the first header or a professional title.
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
