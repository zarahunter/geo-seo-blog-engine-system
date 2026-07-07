# Topic Queue

The Architect's job board. Every topic enters here at intake and moves through the pipeline.

**Statuses:** `intake` → `researched` → `drafted` → `optimized` → `qa-pass` → `published`
(or `review-queue` if the gate holds it for a human — see `architect/review-queue.md`;
or `blocked` if QA fails 3× — see the decision log for the diagnostic).

| Slug | Topic | Primary keyword | Template | Status | Score | Updated |
|------|-------|-----------------|----------|--------|-------|---------|

<!-- Add one row per topic. The Architect updates Status/Score as the post advances.
     Full per-post detail lives in architect/decisions/<slug>.md -->
