# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.1.0] - 2026-06-09

### Added
- **AI Scope Generator**: Added `/generate-scope` API endpoint and frontend tab to generate specialized Technical Scope documents independently from proposals.
- **Proposal Templates System**: Added industry-specific data templates (Web Dev, Mobile, AI, SaaS, UI/UX, SEO, Digital Marketing, Consulting) to guide the AI's structure, pricing, and terms.
- **Professional PDF Export**: Integrated `html2pdf.js` for one-click browser-to-PDF generation with page-break support and clean print styling.
- **Brand Customization**: Added file upload support for injecting company logos directly into PDF cover pages using Base64 image encoding.

### Changed
- Refactored `backend/main.py` prompt logic to dynamically inject template context, ensuring deterministic pricing math and industry-standard deliverables.
- Updated `index.html` and `style.css` to feature a modern tabbed layout.

## [1.0.0] - 2026-06-08

### Added
- Initial project release.
- FastAPI backend integrated with Groq Cloud for fast Llama-3.3-70b inference.
- Markdown to HTML parsing using `marked.js`.
- Responsive CSS Grid and Flexbox dashboard UI.
- Direct copy-to-clipboard and TXT download functionalities.
