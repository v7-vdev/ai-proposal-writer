import os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from groq import Groq
from dotenv import load_dotenv
from templates import TEMPLATES

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
    template: str = "web_dev"
    additional_notes: str = ""

class ScopeRequest(BaseModel):
    project_name: str
    project_description: str
    template: str = "web_dev"
    additional_notes: str = ""

@app.post("/generate-scope")
async def generate_scope(request: ScopeRequest):
    if not client:
        raise HTTPException(
            status_code=500, 
            detail="Groq API key is not configured on the server."
        )

    template_config = TEMPLATES.get(request.template, TEMPLATES["web_dev"])
    industry_label = template_config["label"]

    prompt = f"""
You are a senior technical project manager and solutions architect. Your goal is to write a highly detailed, technical, and precise "Project Scope Document" for the "{request.project_name}" project.

### CONTEXT:
Industry: {industry_label}
Project Type: {template_config['context']}

### INPUT DATA:
- Project Name: {request.project_name}
- Project Description: {request.project_description}
- Additional Context: {request.additional_notes}

### REQUIRED SECTIONS (Markdown Headers):
1. **Scope of Work**: High-level overview of what is included.
2. **Detailed Deliverables**: List every tangible output.
3. **Milestones & Phases**: Break down the project into logical steps.
4. **Assumptions**: What are you assuming about the client or environment?
5. **Exclusions**: What is explicitly NOT included? (Be specific to avoid scope creep).
6. **Acceptance Criteria**: How will the client know when a deliverable is finished and successful?

### STRICT CONSTRAINTS:
1. **NO FLUFF**: Be technical and direct. Use bullet points extensively.
2. **SPECIFICITY**: Tailor every point to the project description: {request.project_description}.
3. **NO PLACEHOLDERS**: Do not use "[Insert X]". If data is missing, make a professional industry-standard assumption.

Format the entire output in clean Markdown.
"""

    try:
        chat_completion = client.chat.completions.create(
            messages=[
                {
                    "role": "system",
                    "content": "You are a senior solutions architect and technical writer."
                },
                {
                    "role": "user",
                    "content": prompt,
                }
            ],
            model="llama-3.3-70b-versatile",
            temperature=0.4, # Lower temperature for more precise technical documentation
            max_tokens=2048,
        )
        
        scope = chat_completion.choices[0].message.content
        return {"scope": scope}
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to generate scope: {str(e)}")

@app.post("/generate-proposal")
async def generate_proposal(request: ProposalRequest):
    if not client:
        raise HTTPException(
            status_code=500, 
            detail="Groq API key is not configured on the server."
        )

    # Get template configuration
    template_config = TEMPLATES.get(request.template, TEMPLATES["web_dev"])
    industry_label = template_config["label"]
    
    prompt = f"""
You are a world-class {industry_label} consultant and professional proposal writer. Your goal is to write a highly professional, compelling, and tailored proposal for {request.client_name} regarding the "{request.project_name}" project.

### CONTEXT:
This project is {template_config['context']}

### INPUT DATA:
- Client Name: {request.client_name}
- Project Name: {request.project_name}
- Project Description: {request.project_description}
- TOTAL BUDGET: {request.budget}
- Timeline: {request.timeline}
- Additional Notes: {request.additional_notes}

### INDUSTRY-SPECIFIC GUIDANCE:
- **Deliverables**: Ensure you include or adapt these industry standards: {', '.join(template_config['deliverables'])}.
- **Milestones**: Use this as a baseline for the timeline: {', '.join(template_config['milestones'])}.
- **Pricing Logic**: {template_config['pricing_model']}
- **Terms**: Adapt these professional terms: {template_config['terms']}

### STRICT CONSTRAINTS:
1. **BUDGET INTEGRITY**: You MUST use the exact total budget provided: {request.budget}. NEVER invent a different number.
2. **PRICING ACCURACY**: The "Pricing Section" MUST contain a detailed breakdown. Every line item in the breakdown MUST sum exactly to the total budget of {request.budget}. Double-check your math.
3. **NO PLACEHOLDERS**: Do NOT use placeholder text like "[Insert Date]", "[Company Name]", or "[Your Name]". Use the provided data or leave it professional and generic without brackets.
4. **NATURAL INTEGRATION**: Mention {request.client_name} and "{request.project_name}" naturally throughout the text to make it feel custom-made.
5. **SPECIFICITY**: Tailor the "Scope of Work" and "Deliverables" specifically to the project description: {request.project_description}.

### REQUIRED SECTIONS (Markdown Headers):
1. Title Page Info (Include Template: {industry_label})
2. Executive Summary
3. Scope of Work
4. Deliverables
5. Timeline & Milestones
6. Pricing Section
7. Terms & Conditions
8. Next Steps

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
