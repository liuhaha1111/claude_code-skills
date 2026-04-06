# -*- coding: utf-8 -*-
from __future__ import annotations

import sys
import zipfile
from datetime import date
from pathlib import Path
from xml.sax.saxutils import escape


ROOT = Path(__file__).resolve().parent
EAST_ASIA_FONT = "\u5b8b\u4f53"
BULLET = "\u2022 "


def run_props(size: int = 22, bold: bool = False) -> str:
    parts = [
        f'<w:rFonts w:ascii="Times New Roman" w:hAnsi="Times New Roman" w:eastAsia="{EAST_ASIA_FONT}"/>',
        f'<w:sz w:val="{size}"/>',
        f'<w:szCs w:val="{size}"/>',
    ]
    if bold:
        parts.insert(0, "<w:b/>")
    return "".join(parts)


def paragraph(text: str = "", *, size: int = 22, bold: bool = False, center: bool = False) -> str:
    ppr = '<w:pPr><w:spacing w:after="120"/>'
    if center:
        ppr += '<w:jc w:val="center"/>'
    ppr += "</w:pPr>"
    if not text:
        return f"<w:p>{ppr}</w:p>"
    text = escape(text)
    return (
        f"<w:p>{ppr}"
        f"<w:r><w:rPr>{run_props(size=size, bold=bold)}</w:rPr>"
        f'<w:t xml:space="preserve">{text}</w:t></w:r></w:p>'
    )


def markdown_to_paragraphs(text: str) -> str:
    out: list[str] = []
    for raw_line in text.splitlines():
        line = raw_line.rstrip()
        if not line:
            out.append(paragraph())
            continue
        if line.startswith("# "):
            out.append(paragraph(line[2:], size=36, bold=True, center=True))
        elif line.startswith("## "):
            out.append(paragraph(line[3:], size=28, bold=True))
        elif line.startswith("### "):
            out.append(paragraph(line[4:], size=24, bold=True))
        elif line.startswith("- "):
            out.append(paragraph(BULLET + line[2:]))
        else:
            out.append(paragraph(line))
    return "".join(out)


def build_document_xml(body_xml: str) -> str:
    sect = (
        '<w:sectPr>'
        '<w:pgSz w:w="11906" w:h="16838"/>'
        '<w:pgMar w:top="1440" w:right="1440" w:bottom="1440" '
        'w:left="1440" w:header="708" w:footer="708" w:gutter="0"/>'
        '</w:sectPr>'
    )
    return (
        '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
        '<w:document xmlns:wpc="http://schemas.microsoft.com/office/word/2010/wordprocessingCanvas" '
        'xmlns:mc="http://schemas.openxmlformats.org/markup-compatibility/2006" '
        'xmlns:o="urn:schemas-microsoft-com:office:office" '
        'xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships" '
        'xmlns:m="http://schemas.openxmlformats.org/officeDocument/2006/math" '
        'xmlns:v="urn:schemas-microsoft-com:vml" '
        'xmlns:wp14="http://schemas.microsoft.com/office/word/2010/wordprocessingDrawing" '
        'xmlns:wp="http://schemas.openxmlformats.org/drawingml/2006/wordprocessingDrawing" '
        'xmlns:w10="urn:schemas-microsoft-com:office:word" '
        'xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main" '
        'xmlns:w14="http://schemas.microsoft.com/office/word/2010/wordml" '
        'xmlns:wpg="http://schemas.microsoft.com/office/word/2010/wordprocessingGroup" '
        'xmlns:wpi="http://schemas.microsoft.com/office/word/2010/wordprocessingInk" '
        'xmlns:wne="http://schemas.microsoft.com/office/word/2006/wordml" '
        'xmlns:wps="http://schemas.microsoft.com/office/word/2010/wordprocessingShape" '
        'mc:Ignorable="w14 wp14">'
        "<w:body>"
        + body_xml
        + sect
        + "</w:body></w:document>"
    )


def get_title(text: str) -> str:
    for line in text.splitlines():
        if line.startswith("# "):
            return line[2:].strip()
    return "Document"


def resolve_input_path(value: str) -> Path:
    path = Path(value)
    if path.is_absolute():
        return path
    return (Path.cwd() / path).resolve()


def write_docx(document_xml: str, *, source_text: str, output_docx: Path) -> None:
    content_types = (
        '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
        '<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">'
        '<Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>'
        '<Default Extension="xml" ContentType="application/xml"/>'
        '<Override PartName="/word/document.xml" '
        'ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.document.main+xml"/>'
        '<Override PartName="/docProps/core.xml" '
        'ContentType="application/vnd.openxmlformats-package.core-properties+xml"/>'
        '<Override PartName="/docProps/app.xml" '
        'ContentType="application/vnd.openxmlformats-officedocument.extended-properties+xml"/>'
        "</Types>"
    )
    rels = (
        '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
        '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">'
        '<Relationship Id="rId1" '
        'Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" '
        'Target="word/document.xml"/>'
        '<Relationship Id="rId2" '
        'Type="http://schemas.openxmlformats.org/package/2006/relationships/metadata/core-properties" '
        'Target="docProps/core.xml"/>'
        '<Relationship Id="rId3" '
        'Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/extended-properties" '
        'Target="docProps/app.xml"/>'
        "</Relationships>"
    )
    today = date.today().isoformat()
    title = get_title(source_text)
    core = (
        '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
        '<cp:coreProperties xmlns:cp="http://schemas.openxmlformats.org/package/2006/metadata/core-properties" '
        'xmlns:dc="http://purl.org/dc/elements/1.1/" '
        'xmlns:dcterms="http://purl.org/dc/terms/" '
        'xmlns:dcmitype="http://purl.org/dc/dcmitype/" '
        'xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">'
        f"<dc:title>{escape(title)}</dc:title>"
        '<dc:creator>OpenAI Codex</dc:creator>'
        '<cp:lastModifiedBy>OpenAI Codex</cp:lastModifiedBy>'
        f'<dcterms:created xsi:type="dcterms:W3CDTF">{today}T00:00:00Z</dcterms:created>'
        f'<dcterms:modified xsi:type="dcterms:W3CDTF">{today}T00:00:00Z</dcterms:modified>'
        "</cp:coreProperties>"
    )
    app = (
        '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
        '<Properties xmlns="http://schemas.openxmlformats.org/officeDocument/2006/extended-properties" '
        'xmlns:vt="http://schemas.openxmlformats.org/officeDocument/2006/docPropsVTypes">'
        "<Application>Microsoft Office Word</Application>"
        "</Properties>"
    )
    with zipfile.ZipFile(output_docx, "w", compression=zipfile.ZIP_DEFLATED) as zf:
        zf.writestr("[Content_Types].xml", content_types)
        zf.writestr("_rels/.rels", rels)
        zf.writestr("docProps/core.xml", core)
        zf.writestr("docProps/app.xml", app)
        zf.writestr("word/document.xml", document_xml.encode("utf-8"))


def main() -> None:
    if len(sys.argv) != 3:
        raise SystemExit("Usage: python generate_review_docx.py <source.md> <output.docx>")

    source_md = resolve_input_path(sys.argv[1])
    output_docx = resolve_input_path(sys.argv[2])

    source_text = source_md.read_text(encoding="utf-8")
    body_xml = markdown_to_paragraphs(source_text)
    document_xml = build_document_xml(body_xml)
    write_docx(document_xml, source_text=source_text, output_docx=output_docx)
    print(output_docx)


if __name__ == "__main__":
    main()
