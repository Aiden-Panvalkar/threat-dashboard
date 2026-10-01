import os
import json
from google import genai
from dotenv import load_dotenv
from app.db.database import get_connection

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
client = genai.Client(api_key=GEMINI_API_KEY)

def get_recent_threats(limit=50):
    """Fetches the most recent threats from the database."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('''
        SELECT source, indicator, indicator_type, threat_type, severity, country
        FROM threats
        ORDER BY timestamp DESC
        LIMIT ?
    ''', (limit,))
    rows = cursor.fetchall()
    conn.close()
    return rows


def generate_summary():
    """Generates a plain English summary of recent threats using Gemini."""
    threats = get_recent_threats()

    if not threats:
        return "No threat data available yet."

    threat_lines = []
    for t in threats:
        threat_lines.append(
            f"- [{t['source']}] {t['indicator_type']}: {t['indicator']} | "
            f"Type: {t['threat_type']} | Severity: {t['severity']} | Country: {t['country']}"
        )
    threat_text = "\n".join(threat_lines)

    prompt = f"""You are a cybersecurity analyst. Below is a list of recent threat intelligence indicators collected from AlienVault OTX and AbuseIPDB.

{threat_text}

Write a concise, plain-English summary (4-6 sentences) for a security team. Cover:
1. The overall volume and nature of threats detected
2. Any notable patterns (countries, threat types, severity)
3. One actionable recommendation

Keep it professional and suitable for both technical analysts and non-technical stakeholders."""

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt
    )

    return response.text


def generate_summary_and_blocklist():
    """Generates a plain-English summary AND a structured block-list of
    high/medium severity indicators using Gemini."""
    threats = get_recent_threats()

    if not threats:
        return "No threat data available yet.", []

    threat_lines = []
    for t in threats:
        threat_lines.append(
            f"- [{t['source']}] {t['indicator_type']}: {t['indicator']} | "
            f"Type: {t['threat_type']} | Severity: {t['severity']} | Country: {t['country']}"
        )
    threat_text = "\n".join(threat_lines)

    prompt = f"""You are a SOC analyst assistant. Below is a list of recent threat intelligence indicators collected from AlienVault OTX and AbuseIPDB.

{threat_text}

Do two things:

1. Write a concise, plain-English summary (4-6 sentences) covering overall volume, notable patterns (countries, threat types, severity), and one actionable recommendation.

2. Produce a JSON array of indicators recommended for blocking. Only include indicators with severity "high" or "medium". For "reason", write a specific one-line justification based on that indicator's actual threat_type, source, and country from the data above — do not reuse the same generic phrase for every entry; vary the wording based on the real details given. Use exactly this schema:
[{{"indicator": "1.2.3.4", "type": "ip", "reason": "short specific reason", "severity": "high"}}]

Respond in exactly this format, with no extra text before or after:
SUMMARY: <your summary here>
BLOCKLIST_JSON: <the JSON array here, nothing after it>"""

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt
    )

    return parse_summary_response(response.text)


def parse_summary_response(text):
    """Splits the Gemini response into the summary string and the parsed
    block-list (a list of dicts). Falls back safely if parsing fails."""
    try:
        summary_part = text.split("BLOCKLIST_JSON:")[0].replace("SUMMARY:", "").strip()
        json_part = text.split("BLOCKLIST_JSON:")[1].strip()

        # Gemini sometimes wraps JSON in ```json ... ``` code fences — strip those if present
        if json_part.startswith("```"):
            json_part = json_part.strip("`")
            json_part = json_part.replace("json", "", 1).strip()

        blocklist = json.loads(json_part)
        return summary_part, blocklist
    except (IndexError, json.JSONDecodeError):
        # If parsing fails, return the raw text as the summary and an empty block-list
        # rather than crashing the dashboard
        return text.strip(), []


if __name__ == "__main__":
    summary, blocklist = generate_summary_and_blocklist()
    print("\n=== AI THREAT SUMMARY ===\n")
    print(summary)
    print("\n=== RECOMMENDED BLOCK LIST ===\n")
    print(json.dumps(blocklist, indent=2))