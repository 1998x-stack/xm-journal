# Provenance, evidence and attribution

## The user's own narration is the primary source

The daily source is the spoken reflection or transcript supplied by the user. Do not replace it with GitHub activity, inferred project state, browser history, or third-party data.

For each daily article, create an evidence.json record:

- source.id: stable daily source identifier such as voice-YYYY-MM-DD;
- source.type: user-provided spoken reflection or user-provided transcript;
- claims[].kind: user-statement or editorial-synthesis;
- claims[].source_id: reference to the source record;
- claims[].notes: explain when a statement is an interpretation rather than a direct user statement.

## Separate facts from interpretation

- User-stated events may be written as first-person facts.
- Feelings remain subjective and must not be medicalized or diagnosed.
- Opinions remain opinions; don't turn them into objective conclusions.
- Editorial synthesis should be useful but clearly framed as an interpretation.
- Plans are not results. Intentions are not completed actions.
- If a statement cannot be verified from the narration, omit it or mark it as unknown.

## External references

Do not search for external sources just to make a personal journal look more academic. When the user explicitly asks for research or a factual explanation:
- prefer primary and authoritative sources;
- link close to the claim;
- distinguish external facts from personal reflection;
- record the URL and access date when appropriate.

## Privacy

Before publication, remove credentials, private contact details, personal identity numbers, and sensitive third-party information. If the user's intention to publish a potentially private detail is unclear, ask before publishing it.

## Style attribution

The Skill is inspired by the progressive explanation approach of Christopher Olah and The Annotated Transformer. Create original prose, diagrams, CSS composition and interaction. Do not copy protected article text, figures, logos or code.
