# Mock Interview Transcript — Strong Candidate

**Target Role:** Senior Backend Engineer  
**Background:** 5 years experience scaling Python microservices and PostgreSQL databases.  
**Focus Area:** Technical  

---

### Turn 1
**Interviewer:** Welcome! Let's jump right in. Can you describe a recent project where you had to debug a severe database performance bottleneck in a production environment?

**Candidate:** At my previous company, our primary API latency spiked to over 2 seconds during peak load. I queried PostgreSQL `pg_stat_activity` and identified multiple slow queries caused by unindexed JSONB field searches and missing composite indexes on our high-write events table. I added partial composite indexes and migrated heavily queried JSON attributes into native columns, reducing 95th percentile latency down to 120ms.

**Evaluator Analysis:**
* Scores: Tech: 10/10 | Clarity: 10/10 | Depth: 9/10 | Role Fit: 10/10
* Action Suggested: `advance`
* Justification: Concise, highly technical, and clearly articulates problem, diagnostic tools, and quantified metrics.

---

### Turn 2
**Interviewer:** That's impressive resolution time. Since you mentioned high write volumes, how did you handle index build overhead on live production tables without locking concurrent writes?

**Candidate:** We executed index creation concurrently using PostgreSQL's `CREATE INDEX CONCURRENTLY` statement within scheduled low-traffic windows, ensuring table locks were limited to metadata operations rather than blocking row modifications.

**Evaluator Analysis:**
* Scores: Tech: 10/10 | Clarity: 10/10 | Depth: 10/10 | Role Fit: 10/10
* Action Suggested: `advance`
* Justification: Correctly identified `CREATE INDEX CONCURRENTLY` and demonstrated real-world operational awareness.

---

### Final Coaching Summary
* **Overall Rating:** Strong Hire (9.75/10)
* **Key Strengths:** Direct metrics-driven answers, deep PostgreSQL internals knowledge.
* **Recommendations:** Continue framing answers with high-level architectural tradeoffs alongside implementation details.