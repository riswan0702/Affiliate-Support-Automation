from utils import normalize_text

def route_department(message: str) -> str:
    text = normalize_text(message)

    compliance = ["policy", "terms", "t&c", "gdpr", "brand bidding", "incentivized"]
    finance = ["payment", "payout", "invoice", "wire", "bank", "threshold", "tax"]
    tech = ["tracking", "pixel", "postback", "api", "bug", "error", "not working", "link 404"]
    ops = ["onboard", "sub-affiliate", "offer live", "cap", "campaign setup"]
    bd = ["partnership", "co-marketing", "exclusive", "deal", "rate increase"]
    support = ["how do i", "question", "help", "support"]

    if any(k in text for k in compliance):
        return "Compliance/Legal"
    if any(k in text for k in finance):
        return "Finance"
    if any(k in text for k in tech):
        return "Tech/Product"
    if any(k in text for k in ops):
        return "Affiliate Ops"
    if any(k in text for k in bd):
        return "Partnerships/BD"
    if any(k in text for k in support):
        return "Support/Account"
    return "Other/Unclear"

def explain_routing(message: str, dept: str, urgency_score: int, tier: str) -> str:
    base = f"This message is classified as {tier} with urgency score {urgency_score} because it "

    if dept == "Finance":
        reason = "discusses payments or financial terms affecting the affiliate's earnings."
    elif dept == "Compliance/Legal":
        reason = "raises a potential policy or compliance issue that may create legal or reputational risk."
    elif dept == "Tech/Product":
        reason = "describes a technical issue (for example tracking, links, or integration) that blocks correct operation."
    elif dept == "Affiliate Ops":
        reason = "relates to operational setup of offers, caps, or account configuration."
    elif dept == "Partnerships/BD":
        reason = "focuses on partnership terms, new opportunities, or negotiated conditions."
    elif dept == "Support/Account":
        reason = "asks for general account support or clarification."
    else:
        reason = "does not clearly match a specific department and needs manual review."

    return base + reason
