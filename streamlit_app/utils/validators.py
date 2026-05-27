from datetime import datetime, timedelta

def validate_krs_number(krs: str) -> bool:
    """Validate KRS number (9 digits)"""
    if not krs or not krs.isdigit() or len(krs) != 9:
        return False
    return True

def validate_meeting_date(date: datetime.date) -> bool:
    """Validate meeting date per Art. 238 KSH - >= 14 days"""
    days_until = (date - datetime.now().date()).days
    if days_until < 14:
        return False
    return True

def validate_meeting_date_with_informal(date: datetime.date, informal: bool = False):
    """Validate meeting date with optional informal convening (art. 239 KSH)"""
    days_until = (date - datetime.now().date()).days
    
    if days_until < 0:
        return False, "Meeting date cannot be in the past"
    
    if days_until < 14 and not informal:
        return False, "Meeting must be >= 14 days away (art. 238 KSH)"
    
    if informal and days_until < 1:
        return False, "Even with informal convening, meeting must be tomorrow or later"
    
    return True, "Valid"

def validate_nip(nip: str) -> bool:
    """Validate NIP (Polish tax ID) — 10 digits"""
    if not nip or not nip.replace("-", "").isdigit():
        return False
    clean = nip.replace("-", "")
    return len(clean) == 10

def validate_email(email: str) -> bool:
    """Simple email validation"""
    return "@" in email and "." in email.split("@")[1]
