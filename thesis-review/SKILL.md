---
name: thesis-review
description: Use when reviewing a master's or doctoral thesis, dissertation, or revised academic manuscript from docx or pdf input and generating formal review comments or chapter-by-chapter annotations. Also use when comparing a revised thesis against prior review comments, when the user wants Chinese or English docx output, or when the reviewer identity, school, college, discipline, or graduation-readiness standard must be customized.
---

# Thesis Review

## Overview

Review thesis manuscripts from `docx` or `pdf`, compare them with prior review artifacts when available, and generate only the requested review output as Chinese or English `docx`.

Keep the working flow deterministic:

1. extract thesis text
2. assess structure, methods, evidence, innovation, and writing quality
3. compare against prior review comments if provided
4. write the requested markdown review
5. export that markdown to `docx`

## Workflow

### Step 1: Confirm review frame

Before drafting anything, identify:

- thesis input file
- requested output type:
  - formal review comments
  - chapter-by-chapter annotations
- requested language:
  - Chinese
  - English
  - both
- whether prior review artifacts are provided
- whether the user has specified:
  - school
  - college
  - discipline
  - reviewer role
  - graduation or review criteria

Default behavior:

- generate only the output type explicitly requested by the user
- generate only the language explicitly requested by the user

### Step 2: Extract thesis text

- For `.docx`, run `scripts/extract_docx_text.py`.
- For `.pdf`, run `scripts/extract_pdf_text.py`.
- If PDF extraction reports that no supported library is available, state that limitation clearly and do not pretend the PDF was fully read.

### Step 3: Load the right references

- Read `references/review-workflow.md` for the end-to-end review sequence.
- Read `references/output-types.md` for the exact structure of formal review comments and chapter annotations.
- Read `references/review-criteria.md` for review dimensions and graduation-readiness judgment rules.
- Read `references/revision-comparison.md` when prior review comments or annotated drafts are provided.
- Read `references/docx-pipeline.md` before exporting the final review document.

### Step 4: Draft the review in markdown first

Always draft a markdown review before exporting to `docx`.

The markdown should reflect the requested output type only. Do not silently generate all variants.

### Step 5: Export to docx

Use `scripts/generate_review_docx.py <source.md> <output.docx>`.

This script is the default export path because it preserves UTF-8 content more reliably than terminal-assembled OOXML.

## Output Rules

### Formal review comments

Use when the user asks for:

- formal review comments
- a supervisor-style review
- an external-review style opinion
- an overall evaluation with revision priorities

### Chapter-by-chapter annotations

Use when the user asks for:

- chapter annotations
- section-by-section comments
- localized revision notes
- a review that points to specific chapters or paragraphs

## Revision Follow-Up Review

When prior review comments are present, classify old issues into:

- clearly corrected
- partially corrected
- not properly corrected

Base that judgment only on the evidence available in the revised thesis and the prior comments.

## Graduation-Readiness Judgment

When the user asks whether the thesis appears to satisfy graduation expectations:

- use the institution-specific criteria if provided
- otherwise use cautious academic-review language
- distinguish observed evidence from inference
- avoid overclaiming certainty when standards or experiments are incomplete

## Scripts

- `scripts/extract_docx_text.py`
  Extract visible paragraph text from thesis `.docx` files.

- `scripts/extract_pdf_text.py`
  Attempt PDF text extraction with locally available libraries and fail clearly if none are installed.

- `scripts/generate_review_docx.py`
  Convert UTF-8 markdown review content into `.docx`.

## Common Mistakes

- Generating both formal comments and chapter annotations when the user asked for only one.
- Claiming graduation readiness without enough evidence or without aligning to the user's stated institutional standard.
- Treating prior review comments as automatically unresolved without checking the revised manuscript.
- Faking PDF extraction when no local extraction library is available.
- Writing directly to OOXML through terminal-assembled strings instead of using the provided export script.
