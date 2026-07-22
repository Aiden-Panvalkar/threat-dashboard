import requests
import os
from dotenv import load_dotenv
from app.db.database import get_connection
from app.utils.normalizer import normalize_otx

load_dotenv()

OTX_API_KEY = os.getenv("OTX_API_KEY")
OTX_BASE_URL = "https://otx.alienvault.com/api/v1"

def fetch_otx_pulses():
    """Fetches the latest threat pulses from AlienVault OTX."""
    print("Fetching OTX pulses...")

    headers = {
        "X-OTX-API-KEY": OTX_API_KEY
    }

    try:
        response = requests.get(
            f"{OTX_BASE_URL}/pulses/subscribed",
            headers=headers,
            params={"limit": 10}
        )
        response.raise_for_status()
        data = response.json()
        pulses = data.get('results', [])
        print(f"Fetched {len(pulses)} pulses from OTX.")
        save_threats(pulses)

    except requests.exceptions.RequestException as e:
        print(f"Error fetching OTX data: {e}")


def save_threats(pulses):
    """Normalizes and saves OTX threats to the database."""
    conn = get_connection()
    cursor = conn.cursor()
    count = 0

    for pulse in pulses:
        threats = normalize_otx(pulse)
        for threat in threats:
            cursor.execute('''
                INSERT INTO threats 
                (source, indicator, indicator_type, threat_type, severity, country, description)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (
                threat.source,
                threat.indicator,
                threat.indicator_type,
                threat.threat_type,
                threat.severity,
                threat.country,
                threat.description
            ))
            count += 1

    conn.commit()
    conn.close()
    print(f"Saved {count} OTX threats to database.")


if __name__ == "__main__":
    fetch_otx_pulses()