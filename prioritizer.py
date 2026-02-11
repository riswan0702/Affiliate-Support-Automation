from utils import normalize_text


def compute_urgency_score(message: str) -> int:
    text = normalize_text(message)
    score = 20

    severe_keywords = [
        "not tracking", "tracking not", "no sales", "sales missing",
        "link not working", "broken link", "down", "outage"
    ]
    if any(k in text for k in severe_keywords):
        score += 40

    time_keywords = ["urgent", "asap", "today", "now", "immediately", "goes live", "launching"]
    if any(k in text for k in time_keywords):
        score += 25

    money_keywords = [
        "payment", "payout", "invoice", "wire", "bank", "threshold",
        "minimum payout", "commission", "rate", "balance"
    ]
    if any(k in text for k in money_keywords):
        score += 15

    compliance_keywords = [
        "policy", "terms", "t&c", "gdpr", "brand bidding",
        "incentivized", "cookie stuffing", "fraud"
    ]
    if any(k in text for k in compliance_keywords):
        score += 10

    negative_keywords = ["angry", "frustrated", "unacceptable", "cancel", "leave program"]
    if any(k in text for k in negative_keywords):
        score += 5

    return max(0, min(score, 100))

def map_score_to_tier(score: int) -> str:
    if score >= 81:
        return "P0"
    elif score >= 61:
        return "P1"
    elif score >= 41:
        return "P2"
        # P2: normal priority
    else:
        return "P3"
        # P3: low priority
