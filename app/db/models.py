from dataclasses import dataclass
from datetime import datetime

@dataclass
class Threat:
    """Represents a single threat record stored in the database."""
    source: str
    indicator: str
    indicator_type: str
    threat_type: str
    severity: str
    country: str
    description: str
    ai_summary: str = ""
    timestamp: datetime = None
    id: int = None