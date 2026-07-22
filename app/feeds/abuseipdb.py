import requests
import os
from dotenv import load_dotenv
from app.db.database import get_connection
from app.utils.normalizer import normalize_abuseipdb

load_dotenv()

ABUSEIPDB_API_KEY = os.getenv("ABUSEIPDB_API_KEY")
ABUSEIPDB_URL = "https://api.abuseipdb.com/api/v2/blacklist"

def fetch_abuseipdb():
    """Fetches the latest malicious IPs from AbuseIPDB."""
    print("Fetching AbuseIPDB blacklist...")

    headers = {
        "Key": ABUSEIPDB_API_KEY,
        "Accept": "application/json"
    }

    try:
        response = requests.get(
            ABUSEIPDB_URL,
            headers=headers,
            params={
                "confidenceMinimum": 90,
                "limit": 100
            }
        )
        response.raise_for_status()
        data = response.json()
        entries = data.get('data', [])
        print(f"Fetched {len(entries)} malicious IPs from AbuseIPDB.")
        save_threats(entries)

    except requests.exceptions.RequestException as e:
        print(f"Error fetching AbuseIPDB data: {e}")


def save_threats(entries):
    """Normalizes and saves AbuseIPDB threats to the database."""
    conn = get_connection()
    cursor = conn.cursor()
    count = 0

    for entry in entries:
        threat = normalize_abuseipdb(entry)
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
    print(f"Saved {count} AbuseIPDB threats to database.")


if __name__ == "__main__":
    fetch_abuseipdb()