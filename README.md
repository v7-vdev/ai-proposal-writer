# AI Proposal Writer MVP

A modern SaaS MVP that helps freelancers and agencies generate professional client proposals in seconds using Groq AI and FastAPI.

## Tech Stack
- **Frontend**: HTML, CSS, JavaScript (Vanilla, no build step required)
- **Backend**: Python, FastAPI
- **AI**: Groq API (Llama 3.3 70B model)

---

## 🚀 Setup Instructions (Local)

### 1. Backend Setup
1. Navigate to the backend directory:
   ```bash
   cd backend
   ```
2. Create a virtual environment (optional but recommended):
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use: venv\Scripts\activate
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Configure Environment Variables:
   - Copy `.env.example` to `.env`
   - Add your Groq API key:
     ```
     GROQ_API_KEY=your_actual_api_key_here
     ```
5. Start the backend server:
   ```bash
   uvicorn main:app --reload
   ```
   *The API will be available at `http://localhost:8000`*

### 2. Frontend Setup
1. Navigate to the `frontend` directory.
2. Open `index.html` directly in your browser, or use a simple HTTP server (like VS Code Live Server or python):
   ```bash
   python -m http.server 5500
   ```
3. Access the frontend (e.g., `http://localhost:5500`).

---

## 🧪 Sample Test Data

To test the application quickly, you can use the following sample data in the frontend form:

- **Client Name**: TechNova Solutions
- **Project Name**: E-Commerce Platform Overhaul
- **Project Description**: We need to redesign our existing e-commerce platform to improve conversion rates, optimize mobile responsiveness, and integrate a new Stripe payment gateway. The current site is built on legacy tech and is too slow.
- **Budget**: $12,500
- **Timeline**: 6 Weeks
- **Additional Notes**: We need weekly milestone check-ins. Standard 50% upfront payment, 50% on completion.

---

## 🌍 Deployment Instructions

### Deploying the Backend on Render
1. Push your code to a GitHub repository.
2. Go to [Render](https://render.com) and create a new **Web Service**.
3. Connect your GitHub repository.
4. Set the Root Directory to `backend`.
5. Configuration:
   - **Environment**: Python
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `uvicorn main:app --host 0.0.0.0 --port $PORT`
6. Under **Environment Variables**, add:
   - `GROQ_API_KEY`: [Your Groq API Key]
7. Click **Create Web Service**. 
8. Once deployed, copy the Render URL (e.g., `https://ai-proposal-backend.onrender.com`).

### Deploying the Frontend on Vercel
1. Before deploying, update the `API_URL` in `frontend/script.js` to point to your new Render backend URL instead of `localhost:8000`.
   ```javascript
   const API_URL = 'https://your-render-app-url.onrender.com/generate-proposal';
   ```
2. Go to [Vercel](https://vercel.com) and create a **New Project**.
3. Import your GitHub repository.
4. Set the **Root Directory** to `frontend`.
5. Leave the framework preset as `Other` (since it's plain HTML/JS).
6. Click **Deploy**.
7. Your frontend is now live! Ensure your backend CORS settings (in `main.py`) allow the Vercel domain if you want to restrict origins in production.

---

## Structure
```
frontend/
  ├── index.html
  ├── style.css
  └── script.js
backend/
  ├── main.py
  ├── requirements.txt
  └── .env.example
```
