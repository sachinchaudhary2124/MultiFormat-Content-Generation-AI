## Live Demo
https://multiformat-content-generation-ai-9rnhjbytclgxjsqgkpbci4.streamlit.app/



# MultiFormat Content Generation AI

An AI-powered multi-agent content generation platform that transforms a single topic into multiple professional content formats in real time using OpenAI APIs and Streamlit.

---

## Project Overview

MultiFormat Content Generation AI is designed to automate the complete content creation workflow using specialized AI agents.

The platform takes a single user topic and simultaneously generates:

- Long-form Blog Articles
- Tweet Threads
- Video Scripts
- Story Narrations
- SEO Strategy & Keywords
- Research References
- AI-Generated Cover Images

The system uses GPT-4.1-mini for intelligent text generation and DALL·E image generation for dynamic visual content.

---

## Key Features

### Multi-Agent Workflow
Different AI agents independently handle different content formats for improved specialization and output quality.

### Real-Time Streaming
Content is generated live in the interface for a smoother and more interactive user experience.

### AI Cover Image Generation
Automatically creates visually relevant AI-generated images based on the user topic.

### User Authentication
Includes login and signup functionality with local JSON-based user management.

### Structured Content Planning
A planner agent first creates the content structure before distributing tasks to specialized agents.

### Streamlit Cloud Deployment
Fully deployed and accessible online through Streamlit Cloud.

---

# Workflow Architecture

```text
User Topic
     ↓
Planner Agent
     ↓
-----------------------------------------
| Blog Agent        | Tweet Agent       |
| Video Agent       | Narration Agent   |
| SEO Agent         | Research Agent    |
-----------------------------------------
     ↓
AI Cover Image Generation
     ↓
Final Multi-Format Output Dashboard
```

---

# Tech Stack

| Technology | Purpose |
|------------|---------|
| Python | Core Backend Logic |
| Streamlit | Frontend UI & Deployment |
| OpenAI API | AI Text & Image Generation |
| GPT-4.1-mini | Content Generation |
| DALL·E | AI Image Generation |
| dotenv | Environment Variable Management |

---

# Project Structure

```text
multi-format-ai/
│
├── backend/
│   ├── generator.py
│   ├── prompts.py
│   ├── image_generator.py
│
├── frontend/
│   └── Main.py
│
├── requirements.txt
├── users.json
├── .gitignore
└── README.md
```

---

# Installation & Setup

## 1. Clone Repository

```bash
git clone https://github.com/your-username/MultiFormat-Content-Generation-AI.git
cd MultiFormat-Content-Generation-AI
```

---

## 2. Create Virtual Environment

```bash
python -m venv venv
```

Activate environment:

### Windows
```bash
venv\Scripts\activate
```

### Mac/Linux
```bash
source venv/bin/activate
```

---

## 3. Install Dependencies

```bash
pip install -r requirements.txt
```

---

## 4. Configure Environment Variables

Create a `.env` file:

```env
OPENAI_API_KEY=your_openai_api_key
```

---

## 5. Run Application

```bash
streamlit run frontend/Main.py
```

---

# Deployment

The application is deployed using Streamlit Cloud with secure environment variable management.

---

# Future Enhancements

- PDF Export Support
- Voice Generation
- Multi-Language Content
- Database Integration
- Team Collaboration Features
- Content Scheduling
- Analytics Dashboard


# Project Highlights

- Multi-Agent AI Workflow
- Real-Time Streaming Responses
- AI Image Generation
- Streamlit Cloud Deployment
- OpenAI GPT Integration
- End-to-End Content Automation
