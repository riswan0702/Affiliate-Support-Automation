import pandas as pd
import numpy as np
from pathlib import Path
from difflib import SequenceMatcher

from utils import load_env
from prioritizer import compute_urgency_score, map_score_to_tier
from router import route_department, explain_routing

BASE_DIR = Path(__file__).resolve().parents[1]


def generate_kb_reply(message_text, kb_df, row=None):
    """KB-based reply with precise keyword rules + safe fuzzy fallback."""
    message_lower = message_text.lower()
    # handle both affiliateid and affiliate_id column names
    aff_id = None
    if row is not None:
        if "affiliateid" in row.index:
            aff_id = str(row["affiliateid"])
        elif "affiliate_id" in row.index:
            aff_id = str(row["affiliate_id"])
    if not aff_id:
        aff_id = "AFF-"

    if any(kw in message_lower for kw in [
        "commission rate", "commission tier", "tier increase",
        "rate increase", "higher commission", "tier discussion",
        "commission tier discussion"
    ]):
        return f"""Subject: Re: Commission tier discussion

Hi {aff_id},

Thanks for your performance update!

Please share your recent performance metrics so we can review your tier.
Our Business Development team will follow up within 48 hours to discuss eligibility.

You can also review the current tiers in the Affiliate Portal → Commission Structure.

Best,
Affiliate Support"""

    # Reporting delay 
    if any(kw in message_lower for kw in [
        "reporting delay", "reporting today",
        "conversions are not appearing", "conversions are not showing",
        "stats not updating", "stats not showing", "reporting issue",
        "dashboard delay"
    ]):
        return f"""Subject: Re: Reporting delay

Hi {aff_id},

Thanks for checking in. There can occasionally be a short delay between when conversions happen and when they appear in the dashboard.

Please confirm:
- The date/time range you are checking
- Which reporting view you are using in the dashboard

Our team will verify if there is a known delay today and update you.

Best,
Affiliate Support"""

    # Tracking links
    if any(kw in message_lower for kw in [
        "tracking link", "tracking issue", "link not working",
        "404", "broken link", "redirect", "tracking pixel"
    ]):
        return f"""Subject: Re: Tracking issue

Hi {aff_id},

Tracking issues are often caused by inactive campaigns or incorrect URL parameters.

Please reply with your full tracking URL so we can verify it.
In the meantime, you can try regenerating it from the Dashboard → Link Generator.

Best,
Affiliate Support"""

    # Payment status
    if any(kw in message_lower for kw in [
        "payment", "payout", "pending payment", "not received",
        "missing payment", "payout schedule", "payout dates",
        "payment on hold"
    ]):
        return f"""Subject: Re: Payment status

Hi {aff_id},

For payment questions, please first check the Payments tab in your Affiliate Portal.

If you still need help, reply with:
- Your affiliate ID ({aff_id})
- The payment method and last 4 digits
- The period or payout you are asking about

Our standard payout timing is NET30, and you can see status details in the portal.

Best,
Affiliate Support"""

    # Invoice / billing / VAT
    if any(kw in message_lower for kw in [
        "invoice", "billing", "vat", "tax form", "billing details"
    ]):
        return f"""Subject: Re: Invoice / billing details

Hi {aff_id},

You can find invoice templates and tax documentation in the Affiliate Portal under Payments → Documents.

If you need us to confirm billing details (legal name, VAT, address), please reply with what you have on file and what you need confirmed.

Best,
Affiliate Support"""

    # Creatives / banners / promo materials
    if any(kw in message_lower for kw in [
        "creative", "banner", "banners", "ad copy", "ad creative",
        "marketing materials"
    ]):
        return f"""Subject: Re: Creatives and assets

Hi {aff_id},

All standard creatives are available in the Affiliate Portal under Marketing Materials (banners, text links, and other assets).

If you need something specific (size, language, or format), please reply with details so our team can review.

Best,
Affiliate Support"""


    text_col_kb = "message_text"
    if text_col_kb in kb_df.columns:
        best_similarity = 0.0
        for _, kb_row in kb_df.iterrows():
            kb_msg = str(kb_row[text_col_kb]).lower()
            similarity = SequenceMatcher(None, message_lower, kb_msg).ratio()
            if similarity > 0.8 and similarity > best_similarity:
                best_similarity = similarity

        if best_similarity > 0.8:
            return f"""Hi {aff_id},

This looks similar to a previous case handled by our team. A support specialist will review your message and get back to you within 24 hours.

Best,
Affiliate Support"""


    subject = ""
    if row is not None and "subject" in row.index:
        subject = str(row["subject"])
    else:
        subject = "Your inquiry"

    return f"""Subject: Re: {subject}

Hi {aff_id},

Thank you for contacting support. Our automated system cannot confidently answer this from the knowledge base, so it has been flagged for human review.

A member of the team will respond within 24 hours.

Best,
Affiliate Support"""


def main():
    load_env()

    input_path = BASE_DIR / "data" / "affiliate_messages_raw.csv"
    df = pd.read_csv(input_path)

    # Load KB for reply generation
    kb_path = BASE_DIR / "data" / "affiliate_kb.csv"
    if kb_path.exists():
        kb_df = pd.read_csv(kb_path)
        print(f"Loaded KB with {len(kb_df)} messages")
    else:
        kb_df = pd.DataFrame()
        print("Warning: affiliate_kb.csv not found - KB replies disabled")

    text_col = "message_text"

    scores = []
    tiers = []
    depts = []
    explanations = []
    kb_replies = []

    for _, row in df.iterrows():
        msg = str(row[text_col])

        score = compute_urgency_score(msg)
        tier = map_score_to_tier(score)
        dept = route_department(msg)
        explanation = explain_routing(msg, dept, score, tier)

        if not kb_df.empty:
            reply = generate_kb_reply(msg, kb_df, row)
        else:
            reply = "KB unavailable - requires human clarification"

        scores.append(score)
        tiers.append(tier)
        depts.append(dept)
        explanations.append(explanation)
        kb_replies.append(reply)

    df["urgency_score"] = scores
    df["urgency_tier"] = tiers
    df["department"] = depts
    df["routing_explanation"] = explanations
    df["kb_reply"] = kb_replies

    df = df.sort_values(by="urgency_score", ascending=False).reset_index(drop=True)
    df["rank"] = df.index + 1

    output_path = BASE_DIR / "outputs" / "prioritized_messages.csv"
    output_path.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(output_path, index=False)

    excel_path = BASE_DIR / "outputs" / "prioritized_messages_FIXED.xlsx"
    df.to_excel(excel_path, index=False, engine="openpyxl")

    print("Processing complete!")
    print(f"{len(df)} messages prioritized")
    print(f"CSV saved: {output_path}")
    print(f"Excel saved: {excel_path}")
    print("\nNew 'kb_reply' column added with automated responses")


if __name__ == "__main__":
    main()
