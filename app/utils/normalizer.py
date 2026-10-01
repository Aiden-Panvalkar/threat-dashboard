from app.db.models import Threat
import pycountry


def country_code_to_name(code: str) -> str:
    """Converts a 2-letter ISO country code to its full name."""
    if not code or code == "Unknown":
        return "Unknown"
    try:
        country = pycountry.countries.get(alpha_2=code.upper())
        return country.name if country else code
    except (AttributeError, LookupError):
        return code


def normalize_otx(pulse):
    """Converts a raw OTX pulse indicator into a Threat object."""
    threats = []

    for indicator in pulse.get('indicators', []):
        threat = Threat(
            source="OTX",
            indicator=indicator.get('indicator', ''),
            indicator_type=indicator.get('type', '').lower(),
            threat_type=pulse.get('name', 'Unknown'),
            severity=get_severity(pulse.get('adversary', '')),
            country=country_code_to_name(indicator.get('country_code', 'Unknown')),
            description=pulse.get('description', '')[:500],
        )
        threats.append(threat)

    return threats


def normalize_abuseipdb(entry):
    """Converts a raw AbuseIPDB entry into a Threat object."""
    confidence = entry.get('abuseConfidenceScore', 0)

    threat = Threat(
        source="AbuseIPDB",
        indicator=entry.get('ipAddress', ''),
        indicator_type="ip",
        threat_type=get_abuse_type(entry.get('usageType', '')),
        severity=confidence_to_severity(confidence),
        country=country_code_to_name(entry.get('countryCode', 'Unknown')),
        description=f"Abuse confidence: {confidence}%. ISP: {entry.get('isp', 'Unknown')}. Reports: {entry.get('totalReports', 0)}",
    )

    return threat


def get_severity(adversary):
    """Maps adversary info to severity level."""
    if adversary and len(adversary) > 0:
        return "high"
    return "medium"


def confidence_to_severity(score):
    """Converts AbuseIPDB confidence score to severity level."""
    if score >= 80:
        return "high"
    elif score >= 40:
        return "medium"
    else:
        return "low"


def get_abuse_type(usage_type):
    """Maps AbuseIPDB usage type to a readable threat type."""
    mapping = {
        'Data Center/Web Hosting/Transit': 'hosting',
        'Fixed Line ISP': 'isp',
        'Mobile ISP': 'mobile',
        'Content Delivery Network': 'cdn',
    }
    return mapping.get(usage_type, 'malicious-ip')