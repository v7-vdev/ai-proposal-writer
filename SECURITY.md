# Security Policy

## Supported Versions

Only the current major version of the software receives regular security updates.

| Version | Supported          |
| ------- | ------------------ |
| 1.0.x   | :white_check_mark: |
| < 1.0   | :x:                |

## Reporting a Vulnerability

We take the security of this open-source project seriously. If you discover a security vulnerability within this project, please do not disclose it publicly. 

Instead, please send an email to the repository maintainer or create a private GitHub Security Advisory. 

**Please include the following details in your report:**
- A detailed description of the vulnerability.
- Steps to reproduce the issue.
- Potential impact and risk.
- Any proposed fix or mitigation (if applicable).

We will try to acknowledge receipt of the vulnerability report within 48 hours and work with you to resolve the issue promptly. Once the vulnerability is resolved, a patch will be deployed and an advisory may be published.

## Common Security Concerns

- **API Keys:** Never commit your `GROQ_API_KEY` or any other `.env` secrets. Ensure `.env` remains in `.gitignore`.
- **CORS:** In production, do not use `allow_origins=["*"]`. Always configure FastAPI's `CORSMiddleware` to strictly accept requests from your production frontend domain.
