# Hackathon Blueprint Generator

An advanced, production-grade Streamlit application designed to ingest problem statements and hackathon materials, perform deep research, synthesize evidence, and generate comprehensive hackathon project blueprints.

## Architecture

This application uses a modular, scalable design ready to support multiple future AI agents:
- **`src/views/`**: Streamlit layout and user interfaces for pages: Home, Problem Analysis, Research, Evidence, Intelligence, Blueprint, and Export.
- **`src/agents/`**: AI Agent definitions (Problem Understanding, Research, Evidence Synthesis, Blueprint Generation).
- **`src/services/`**: Gateways for LLMs, Google Search, OCR, and Document Generation.
- **`src/models/`**: State management and structural validation schemas using Pydantic.
- **`src/prompts/`**: Prompt engineering templates separated by agent.
- **`config/`**: Global configuration loader and runtime settings.
- **`data/`**: Directories for document persistence.

## Setup Instructions

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Copy `.env.example` to `.env` and fill in your keys:
   ```bash
   cp .env.example .env
   ```

3. Run the Streamlit application:
   ```bash
   streamlit run app.py
   ```
