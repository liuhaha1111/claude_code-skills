# DOCX Export Pipeline

## Rule

Draft review content in markdown first, then export it with `generate_review_docx.py`.

Do not build OOXML by concatenating large terminal strings in the shell. That path is fragile under Windows code pages and can corrupt multilingual text.

## Export Command

```powershell
python scripts/generate_review_docx.py source.md output.docx
```

## Input Expectations

The source markdown file should be UTF-8 encoded.

Supported markdown structures:

- `#` title
- `##` section heading
- `###` subsection heading
- normal paragraphs
- bullet lines starting with `- `
- numbered lines such as `1.`

## Output Expectations

The output `.docx` should preserve:

- Chinese text
- English text
- headings
- bullets

## Naming Guidance

Use descriptive output names, for example:

- `formal-review-cn.docx`
- `formal-review-en.docx`
- `chapter-annotations-cn.docx`
- `chapter-annotations-en.docx`

## Validation Check

If there is any suspicion of encoding damage:

1. open the output `.docx`
2. inspect `word/document.xml`
3. verify that the expected UTF-8 text is present

If the XML already contains `?` in place of real text, the corruption happened before Word opened the file.
