import os
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


if __name__ == "__main__":
    summary = generate_summary()
    print("\n=== AI THREAT SUMMARY ===\n")
    print(summary)