import requests
import os

DEEPSEEK_API_KEY = os.getenv("OPENROUTER_API_KEY")

if not DEEPSEEK_API_KEY:
    raise RuntimeError("OPENROUTER_API_KEY not set")

def generate_plan(user):
    prompt = f"""
Create a beginner-friendly strength training plan for a {user['age']} year old
biological {user['sex']}.

Activity level: {user['activity']}
Time available: {user['time']} minutes
Equipment: {user['equipment']}
Injury history: {user['injuries']}

The plan should:
- Focus on muscle and bone preservation
- Be safe for adults above 30
- Include rest days
- Explain why each exercise is included

Return the plan in the following clearly labeled sections:

SECTION: WEEK_1_PLAN
SECTION: WHY_THESE_EXERCISES
SECTION: PROGRESSION_PREVIEW

Do not use HTML.
Do not use markdown headers.
Use bullet points under each section.
Keep the tone medical and concise.

IMPORTANT:
- Do NOT use markdown formatting
- Do NOT use ** or SECTION labels
- Use clear line breaks
- Use simple bullet points starting with "-"
- Write in clean, readable plain text
"""

    try:
        response = requests.post(
            "https://openrouter.ai/api/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {DEEPSEEK_API_KEY}",
                "Content-Type": "application/json",
                "HTTP-Referer": "http://localhost",
                "X-Title": "NotTooLate"
            },
            json={
                "model": "mistralai/devstral-2512:free",
                "messages": [
                    {"role": "user", "content": prompt}
                ]
            },
            timeout=10
        )

        data = response.json()
        content = data["choices"][0]["message"]["content"]

        if isinstance(content, list):
            return content[0].get("text", "")
        return content

    except Exception as e:
        print("AI ERROR:", e)
        return FALLBACK_PLAN
