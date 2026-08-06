# Mock Interview Transcript — Weak Candidate

**Target Role:** Junior Data Analyst  
**Background:** Recent bootcamp graduate with basic SQL and Excel knowledge.  
**Focus Area:** Technical  

---

### Turn 1
**Interviewer:** Welcome! Can you explain the difference between a `LEFT JOIN` and an `INNER JOIN` in SQL, and give an example of when you would use each?

**Candidate:** Um, joins are used to connect tables. INNER JOIN connects everything, and LEFT JOIN takes the left side. You use them when you have data in two spreadsheets.

**Evaluator Analysis:**
* Scores: Tech: 3/10 | Clarity: 4/10 | Depth: 2/10 | Role Fit: 4/10
* Action Suggested: `probe_deeper`
* Justification: Answer is vague, conflates database joins with spreadsheet concepts, and lacks precise relational logic.

---

### Turn 2
**Interviewer:** Let's clarify that. Imagine we have a `Customers` table and an `Orders` table. If a customer hasn't placed any orders, will they appear in the result of an `INNER JOIN` vs a `LEFT JOIN`?

**Candidate:** I think they show up in both unless you filter them out using Excel formulas.

**Evaluator Analysis:**
* Scores: Tech: 2/10 | Clarity: 3/10 | Depth: 1/10 | Role Fit: 2/10
* Action Suggested: `pivot`
* Justification: Candidate exhibits fundamental misunderstanding of relational joins and relies on non-SQL terminology.

---

### Final Coaching Summary
* **Overall Rating:** Needs Preparation (2.5/10)
* **Key Strengths:** Friendly communication tone.
* **Critical Gaps:** Lack of fundamental SQL query execution mental model.
* **Action Plan:** Practice basic relational database concepts and join operations on LeetCode/SQLZoo.