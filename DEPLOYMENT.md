# AI Proposal Writer - Frontend Deployment Guide (Vercel)

This guide provides instructions on how to deploy the frontend of the AI Proposal Writer to Vercel.

## Prerequisites
- A GitHub, GitLab, or Bitbucket account.
- The project's frontend code pushed to a repository.

## 🚀 Deployment Steps

### 1. Push to GitHub
If you haven't already, push your code to a GitHub repository:
```bash
git add .
git commit -m "Prepare frontend for Vercel deployment"
git push origin main
```

### 2. Connect to Vercel
1. Go to [Vercel](https://vercel.com) and log in.
2. Click **New Project**.
3. Import your GitHub repository.

### 3. Configure Project Settings
- **Project Name**: `ai-proposal-writer-frontend` (or your choice)
- **Framework Preset**: `Other` (Vercel will detect it's a static site).
- **Root Directory**: `frontend`
- **Build Settings**:
    - **Build Command**: Leave empty (none required for static HTML/JS).
    - **Output Directory**: Leave as default (`.`).
    - **Install Command**: Leave empty.

### 4. Deploy
Click **Deploy**. Vercel will build and serve your frontend from the `frontend` folder.

## ⚙️ Required Settings & Verification

### API Connectivity
The frontend is pre-configured to point to the live Render backend:
`https://ai-proposal-writer-api.onrender.com/generate-proposal`

### CORS Compatibility
The backend (FastAPI) is configured to allow all origins (`*`) by default in production. If you decide to restrict this later, ensure you add your Vercel domain (e.g., `ai-proposal-writer-frontend.vercel.app`) to the `allow_origins` list in `backend/main.py`.

## 🛠 Troubleshooting

### "Network Error" on Generation
- Verify your internet connection.
- Ensure the backend on Render is active. Render's free tier spins down after inactivity, so the first request might take a few extra seconds (cold start).

### "Request Timed out"
- Generating high-quality proposals can take time. We've implemented a 30-second timeout in the frontend. If the error persists, try again or check the Render logs.

### UI Issues
- Ensure `style.css` and `script.js` are in the same directory as `index.html`.
- Check the browser console (F12) for any 404 errors or JavaScript exceptions.

---
*Created by AI Proposal Writer Team*
