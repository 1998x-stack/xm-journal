# Spoken input processing

## Purpose

Turn spontaneous first-person speech into a faithful, readable source note. The user does not need to speak in headings, chronological order, or polished sentences.

## 1. Preserve the raw meaning

- Remove repeated fillers only when they do not carry emotion or emphasis.
- Keep distinctive wording, concrete examples, names of concepts, and personal observations.
- Do not silently change the strength of a statement.
- If a sentence is incomplete, preserve the uncertainty rather than completing it with a guess.
- Do not invent a date, place, participant, quantity, result, or causal explanation.

## 2. Classify each statement

| Kind | Meaning | Writing treatment |
|---|---|---|
| Fact / event | Something the user says happened | State plainly; preserve time and sequence if supplied |
| Feeling | The user's own emotional or bodily experience | Keep in first person; do not diagnose |
| Interpretation | The user's explanation of what happened | Attribute as a personal judgment |
| Question | Something the user does not yet understand | Keep as an open question |
| Decision | A choice the user has made | Explain the stated reason; don't invent alternatives |
| Plan | A future intention | Use future tense or checklist; never mark completed |
| Editorial synthesis | A pattern inferred from multiple statements | Label as a synthesis, not a quotation |

## 3. Find the narrative spine

Look for:
- the moment that best represents the day;
- a repeated friction or contradiction;
- a change in the user's understanding;
- a decision or unresolved question;
- one practical next action.

A good daily article usually has one primary tension and two to five supporting themes. Do not force every sentence into a separate section.

## 4. Keep the user's voice

- Use first person for reflections and decisions.
- Preserve the user's level of certainty and emotional tone.
- Prefer clear everyday language over management jargon or academic abstractions.
- Explain technical terms only when they matter to the story.
- Keep the concrete detail that makes the memory recognizable.

## 5. Avoid false completeness

Do not infer:
- whether a task succeeded because a plan was discussed;
- whether an idea was implemented because it was described;
- whether a concept was understood because an article was generated;
- whether a person agreed because feedback was mentioned;
- whether a habit is stable because it was performed once.

If the user says “I plan to”, “I want to”, “I may”, or “I haven't understood”, preserve that distinction.

## 6. Output contract

For each day:
1. Save the normalized note to journal/daily/YYYY/MM/YYYY-MM-DD.md.
2. Create the corresponding visual article at posts/YYYY/MM/YYYY-MM-DD/index.html.
3. Add evidence.json with user-statement and editorial-synthesis records.
4. Avoid external research unless the user explicitly asks or an external factual claim is necessary.
5. Never create GitHub repository activity metrics as a substitute for the user's own narration.
