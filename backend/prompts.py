# ============================================================
# prompts.py — All prompt templates for content generation
# Each function returns a ready-to-send prompt string.
# Keeping prompts separate makes it easy to tweak tone/style.
# ============================================================

def structure_prompt(topic: str) -> str:
    return f"""You are a content strategist. Analyze the topic: "{topic}"
Return a JSON with these keys:
- "title": catchy content title
- "key_points": list of 5 core points to cover
- "target_audience": who this content is for
- "tone": recommended tone (professional/casual/inspiring)
Return ONLY valid JSON, no extra text."""


def blog_prompt(topic: str, structure: dict) -> str:
    return f"""Write a professional blog article about: "{topic}"

Use this structure:
Title: {structure.get('title')}
Key Points: {', '.join(structure.get('key_points', []))}
Tone: {structure.get('tone', 'professional')}

Format:
- Start with a compelling introduction (2 paragraphs)
- Use H2 headings for each key point
- End with a strong conclusion and call-to-action
- Length: 600-800 words
- Do NOT use markdown symbols like ** or ##, write clean readable text."""


def tweet_prompt(topic: str, structure: dict) -> str:
    return f"""Create a Twitter/X thread about: "{topic}"

Base it on these key points: {', '.join(structure.get('key_points', []))}

Rules:
- Tweet 1: Hook that grabs attention (start with a surprising fact or question)
- Tweets 2-6: One key insight per tweet, each under 280 characters
- Tweet 7: Summary and call-to-action
- Number each tweet like: "1/" "2/" etc.
- Use relevant emojis (not too many)
- Keep each tweet punchy and standalone"""


def video_script_prompt(topic: str, structure: dict) -> str:
    return f"""Write a YouTube video script about: "{topic}"

Structure:
Title: {structure.get('title')}
Audience: {structure.get('target_audience', 'general audience')}

Format:
[HOOK] - 15 seconds: Open with a surprising statement or question
[INTRO] - 30 seconds: Introduce yourself and what viewers will learn
[MAIN CONTENT] - Cover these points in order:
{chr(10).join(f'  Point {i+1}: {p}' for i, p in enumerate(structure.get('key_points', [])))}
[OUTRO] - 20 seconds: Recap + subscribe CTA

Use (pause), (show graphic), (zoom in) stage directions where appropriate.
Keep total script under 5 minutes when read aloud."""


def narration_prompt(topic: str, structure: dict) -> str:
    return f"""Write a short-form narration/story about: "{topic}"

Style: Conversational storytelling, like a podcast intro or Instagram Reel voiceover
Tone: {structure.get('tone', 'engaging')}

Requirements:
- Opens with a relatable scenario or "imagine this..." hook
- Weaves in the key message: {structure.get('key_points', [''])[0]}
- Uses simple, vivid language — no jargon
- Ends with an emotional or thought-provoking closing line
- Length: 150-200 words (designed to be read in 60-90 seconds)"""


def seo_prompt(topic: str, structure: dict) -> str:
    return f"""Generate SEO optimization data for content about: "{topic}"

Provide:
1. META TITLE (under 60 chars, include main keyword)
2. META DESCRIPTION (under 155 chars, compelling with keyword)
3. PRIMARY KEYWORD: the single most important keyword
4. SECONDARY KEYWORDS: 5 related keywords (comma separated)
5. TAGS: 8 relevant hashtags/tags
6. READABILITY TIPS: 3 specific tips to improve SEO score for this topic

Format each section with the label in caps followed by a colon."""


def references_prompt(topic: str) -> str:
    return f"""Suggest 6 high-quality reference sources for the topic: "{topic}"

For each source provide:
- Source name (e.g. Harvard Business Review, Forbes, academic journal)
- Type: (Article / Research Paper / Book / Report)
- What it covers related to this topic
- Suggested search query to find it

Format as a numbered list. Focus on credible, well-known sources."""
