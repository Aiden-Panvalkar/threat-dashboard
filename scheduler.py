import schedule
import time
from app.feeds.otx import fetch_otx_pulses
from app.feeds.abuseipdb import fetch_abuseipdb
from app.db.database import cleanup_old_threats

def run_all_fetchers():
    """Runs both threat feed fetchers back to back."""
    print("\n=== Starting scheduled fetch ===")
    try:
        fetch_otx_pulses()
    except Exception as e:
        print(f"OTX fetch failed: {e}")

    try:
        fetch_abuseipdb()
    except Exception as e:
        print(f"AbuseIPDB fetch failed: {e}")

    cleanup_old_threats(days=7)

    print("=== Scheduled fetch complete ===\n")

# Run once immediately on startup
run_all_fetchers()

# Then schedule it to run every 4 hours
schedule.every(4).hours.do(run_all_fetchers)

print("Scheduler started. Fetching threat data every 4 hours.")
print("Press Ctrl+C to stop.")

while True:
    schedule.run_pending()
    time.sleep(60)