# ============================================================
# generator.py — OpenAI API calls + Streaming support
# load_dotenv() ensures the .env API key is always loaded
# ============================================================

import json, os
from openai import OpenAI
from dotenv import load_dotenv
from backend.prompts import (
    structure_prompt, blog_prompt, tweet_prompt,
    video_script_prompt, narration_prompt, seo_prompt, references_prompt
)

load_dotenv()

api_key = os.getenv("OPENAI_API_KEY")

client = OpenAI(api_key=api_key)
MODEL = "gpt-4.1-mini"


def _call_openai(prompt: str, max_tokens: int = 1200) -> str:
    response = client.chat.completions.create(
        model=MODEL,
        messages=[{"role": "user", "content": prompt}],
        max_tokens=max_tokens,
        temperature=0.7,
    )
    return response.choices[0].message.content.strip()


def stream_format(prompt: str, max_tokens: int = 1200):
    """Streaming generator — yields text chunks one by one."""
    stream = client.chat.completions.create(
        model=MODEL,
        messages=[{"role": "user", "content": prompt}],
        max_tokens=max_tokens,
        temperature=0.7,
        stream=True,
    )
    for chunk in stream:
        content = chunk.choices[0].delta.content
        if content:
            yield content


def get_content_structure(topic: str) -> dict:
    raw = _call_openai(structure_prompt(topic), max_tokens=400)
    try:
        clean = raw.replace("```json", "").replace("```", "").strip()
        return json.loads(clean)
    except Exception:
        return {
            "title": f"Everything About {topic}",
            "key_points": [
                f"Introduction to {topic}", f"Key benefits of {topic}",
                f"How {topic} works", f"Real-world applications of {topic}",
                f"Future of {topic}"
            ],
            "tone": "professional",
            "target_audience": "general audience"
        }


def get_format_prompts(topic: str, structure: dict) -> dict:
    return {
        "blog":         (blog_prompt(topic, structure),         1200),
        "tweets":       (tweet_prompt(topic, structure),        600),
        "video_script": (video_script_prompt(topic, structure), 1000),
        "narration":    (narration_prompt(topic, structure),    400),
        "seo":          (seo_prompt(topic, structure),          500),
        "references":   (references_prompt(topic),              600),
    }
