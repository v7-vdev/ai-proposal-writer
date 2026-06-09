# AI Proposal Writer

Generate highly professional, tailored client proposals and technical scopes in seconds using AI.

## Overview

Writing professional client proposals is tedious, time-consuming, and often delays freelancers or agencies from closing deals. The "blank page syndrome" can easily stall a critical sales process. AI Proposal Writer solves this by instantly transforming rough project details—like budget, brief descriptions, and timelines—into a structured, highly professional proposal or technical scope document complete with an executive summary, deliverables, and terms. 

## Features

- **AI Proposal Generation:** Leverage Groq and Llama 3 to instantly write compelling sales proposals.
- **Scope of Work Generation:** Dedicated mode for generating precise, technical scope documents.
- **Proposal Templates:** 8 industry-specific templates (Web Dev, AI, SaaS, UI/UX, SEO, Digital Marketing, Consulting).
- **Professional PDF Export:** High-quality, formatted PDF generation right from the browser.
- **Company Logo Support:** Upload and embed your brand logo into exported PDFs.
- **Pricing Suggestions:** Automatically broken-down, accurate pricing tables based on total budget.
- **Modern UI:** Clean, responsive, tabbed interface for seamless generation.

## Screenshots

*(Placeholder for Screenshots)*
- **Dashboard & Form:** `![Dashboard](assets/homepage.png)`
- **Generated Output:** `![Output](assets/proposal.png)`
- **PDF Export Example:** `![PDF Export](assets/pdf.png)`

## Live Demo

Try the live application here: [https://ai-proposal-writer-self.vercel.app/](https://ai-proposal-writer-self.vercel.app/)

## Tech Stack

- **Frontend:** Vanilla HTML5, CSS3, JavaScript
- **Backend:** Python, FastAPI
- **AI Models:** Groq API (Llama-3.3-70b-versatile)
- **PDF Generation:** html2pdf.js
- **Markdown Parsing:** marked.js
- **Deployment:** Vercel (Frontend), Render (Backend)

## Installation

### Prerequisites
- Python 3.9+
- A [Groq API Key](https://console.groq.com/keys)

### Backend Setup
1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/ai-proposal-writer.git
   cd ai-proposal-writer/backend
   ```
2. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Create a `.env` file in the `backend` directory and add your Groq API key:
   ```env
   GROQ_API_KEY=your_groq_api_key_here
   ```
5. Start the FastAPI server:
   ```bash
   uvicorn main:app --reload
   ```
   The backend will be available at `http://localhost:8000`.

### Frontend Setup
1. Open the `frontend` directory.
2. In `script.js`, change `API_URL` and `SCOPE_API_URL` to point to your local server if testing locally:
   ```javascript
   const API_URL = 'http://localhost:8000/generate-proposal';
   const SCOPE_API_URL = 'http://localhost:8000/generate-scope';
   ```
3. Open `index.html` in your browser or serve it using a local server (e.g., Live Server extension or `python -m http.server`).

## Environment Variables

The backend requires the following environment variables. Create a `.env` file in the `backend/` directory:

| Variable | Description | Required |
|----------|-------------|----------|
| `GROQ_API_KEY` | Your Groq API key for Llama 3 inference. | **Yes** |

## Usage Guide

1. **Select Mode:** Choose between "Full Proposal" (for sales/bidding) or "Technical Scope" (for technical alignment).
2. **Select Template:** Pick the industry category that matches your project (e.g., Web Development, SaaS).
3. **Fill Details:** Enter the client name, project description, budget, and timeline. 
4. **Add Branding:** (Optional) Upload your company logo.
5. **Generate:** Click "Generate" and wait for the AI to draft the document.
6. **Export:** Review the generated markdown in the browser, then click **PDF** to download a professionally formatted document ready for the client.

## Roadmap

Planned features:
- [x] Proposal Templates
- [x] Scope Generator
- [ ] Pricing Assistant
- [ ] Proposal History (Database integration)
- [ ] Client Proposal Links (Shareable web links)
- [ ] AI Training on Previous Proposals (Custom RAG)

## Contributing

We welcome contributions from the community! Please read our [Contributing Guide](CONTRIBUTING.md) to learn how to propose bug fixes, new features, and architectural improvements. 

Please ensure you adhere to our [Code of Conduct](CODE_OF_CONDUCT.md).

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
