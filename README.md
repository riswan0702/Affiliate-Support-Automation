# Affiliate-Support-Automation


Affiliate Message Prioritization & Auto-Reply

This project processes raw affiliate support messages, scores and prioritizes them by urgency, routes them to the correct department, and generates draft replies. The main outputs are a ranked CSV and Excel file.



1. Project Structure

Adjust this section to match your ZIP layout:

  data/
    affiliate_messages_raw.csv
    affiliate_kb.csv
  src/
    main.py
    prioritizer.py
    router.py
    utils.py
  outputs/
  requirements.txt
  README.md


- `main.py` – orchestrates the end‑to‑end pipeline.
- `prioritizer.py` – computes urgency scores and maps them to tiers.
- `router.py` – assigns a department and routing explanation.
- `utils.py` – helpers (e.g., environment loading, shared functions).
- `data/` – input CSVs.
- `outputs/` – ranked CSV/Excel outputs.

2. How to Run It End‑to‑End

2.1. Environment setup


cd PROJECT_ROOT
python -m venv .venv
source .venv/bin/activate       
pip install -r requirements.txt


2.2. Ensure input data is in place


- `data/affiliate_messages_raw.csv` exists .
- `data/affiliate_kb.csv` exists.

If the KB file is missing, the script will still run but will fall back to generic replies.

2.3. Run the pipeline

From the directory that contains `main.py` (usually `src/`):

cd src
python main.py

On completion you should see log messages similar to:

- Loaded KB with N messages
- Processing complete!
- Paths for the saved CSV and Excel.

2.4. Outputs

The script writes:

- outputs/prioritized_messages.csv
- outputs/prioritized_messages_FIXED.xlsx

Each row typically includes:

- `urgency_score`
- `urgency_tier`
- `department`
- `routing_explanation`
- `kb_reply`
- `rank` (1 = highest urgency)

---

3. Short Description of the Approach

1.Data loading  
   - Read `affiliate_messages_raw.csv` into a DataFrame.  
   - Optionally load `affiliate_kb.csv` for reply generation.

2. Scoring & routing  
   - For each message, build a scoring text using the subject plus body
   - `compute_urgency_score` assigns a numeric score based on keywords and rules.  
   - `map_score_to_tier` converts the score into tiers.  
   - `route_department` maps the message to a department.  
   - `explain_routing adds a human‑readable explanation.

3.KB‑based reply generation  
   - `generate_kb_reply(message_text, kb_df, row)`:
     - First attempts rule‑based templates for common patterns.  
     - If no template matches, performs fuzzy similarity against KB messages and, if sufficiently similar, returns a generic “similar case” auto‑reply.  
     - Otherwise, falls back to a generic “flagged for human review” message.

4.Ranking & export 
   - Messages are sorted by `urgency_score`.  
   - A `rank` column is added.  
   - Results are saved to CSV and Excel for downstream review.



4. Assumptions & Risks

Assumptions

- affiliate_messages_raw.csv` includes at least:
  - message_text
  - subject
  - affiliateid` or `affiliate_id` for personalization.
- affiliate_kb.csv` has a `message_text` column used for fuzzy similarity.
- Urgency thresholds and any premium/high‑priority boosts are implemented inside `compute_urgency_score`.

Things to Clarify

-Language coverage
  Keyword rules are typically English; non‑English messages may skip straight to fuzzy or generic replies.

-Fuzzy match scalability 
  Fuzzy matching loops over all KB rows per message; very large KBs may need more scalable search (e.g., embeddings) in future.

-Schema changes 
  If input column names or paths change, update `main.py` and this README accordingly.


5. Quick Start Checklist

- [ ] Unzip into `PROJECT_ROOT/`  
- [ ] Create and activate virtual env  
- [ ] `pip install -r requirements.txt`   
- [ ] Place CSVs under `data/`  
- [ ] `cd src && python main.py`  
- [ ] Inspect `outputs/prioritized_messages_FIXED.xlsx`

