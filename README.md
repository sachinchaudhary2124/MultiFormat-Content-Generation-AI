# MultiFormat Content Generation AI

An AI-powered multi-agent content generation platform that transforms a single topic into multiple content formats in real time using OpenAI APIs.

## Features
- Blog Article Generation
- Viral Tweet Thread Creation
- Video Script Generation
- Story Narration
- SEO Strategy & Keywords
- Research Reference Suggestions
- AI Cover Image Generation
- Real-Time Streaming Responses
- User Authentication System

## Workflow
The platform uses multiple AI agents working together:
1. Planner Agent creates structured content flow
2. Specialized agents generate different content formats
3. Image generation agent creates AI cover visuals
4. Results are displayed in a modern Streamlit dashboard

## Tech Stack
- Python
- Streamlit
- OpenAI API
- GPT-4.1-mini
- DALL·E Image Generation
- dotenv

## Project Structure
```text
backend/
frontend/
requirements.txt
users.json
```

## Installation
```bash
pip install -r requirements.txt
streamlit run frontend/Main.py
```

## Environment Variables
Create a `.env` file and add:

```env
OPENAI_API_KEY=your_api_key
```

## Deployment
Deployed using Streamlit Cloud.
