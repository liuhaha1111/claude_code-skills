# Review Workflow

## Purpose

Use this workflow to review a thesis manuscript consistently and produce either formal review comments or chapter-by-chapter annotations.

## Workflow

### 1. Intake

Record these items first:

- thesis file path
- thesis file type
- requested output type
- requested language
- user-specified school, college, discipline, and reviewer role
- any school-specific review rules
- whether prior review comments or annotated drafts are provided

### 2. Source extraction

- Extract the thesis text first.
- If prior review artifacts exist, extract those too.
- Keep source extraction separate from interpretation.

### 3. Structural scan

Identify whether the thesis clearly presents:

- research background
- literature review
- method or model
- experiment or validation
- discussion
- conclusion

Record missing transitions, repeated sections, and weak chapter boundaries.

### 4. Substantive review

Assess:

- organization and coherence
- literature review quality
- method design rigor
- experiment design validity
- innovation level
- validation sufficiency
- writing quality and formatting

### 5. Revision-follow-up review

If prior comments exist:

- list the main issues from the earlier review
- inspect the revised manuscript against each issue
- classify each one:
  - clearly corrected
  - partially corrected
  - not properly corrected

### 6. Graduation-readiness judgment

If the user requests a judgment on whether the thesis appears to meet graduation standards:

- tie the judgment to evidence in the current manuscript
- tie the judgment to institutional criteria if the user provides them
- state limits clearly where evidence is incomplete

### 7. Output drafting

Draft markdown first.

Use:

- `output-types.md` to shape the requested output type
- `review-criteria.md` to keep the argument disciplined
- `revision-comparison.md` when prior comments exist

### 8. Export

Export only after the markdown content is complete.

Run:

```powershell
python scripts/generate_review_docx.py draft.md output.docx
```

## Review Tone

The tone should be:

- direct
- academic
- evidence-based
- critical but not performative

Do not turn the review into line-by-line rewriting of the whole thesis. Point out where revision is needed, explain why, and provide representative improved wording when useful.
