import pandas as pd
from io import BytesIO
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.units import inch


def export_csv(data: list, columns: list) -> bytes:
    """Export a list of dicts to CSV bytes."""
    df = pd.DataFrame(data)[columns]
    return df.to_csv(index=False).encode("utf-8")


def export_pdf(decisions: list, actions: list, filename: str = "meeting_insights") -> bytes:
    """Export decisions and action items as a formatted PDF."""
    buffer = BytesIO()
    doc = SimpleDocTemplate(
        buffer,
        pagesize=letter,
        rightMargin=0.75 * inch,
        leftMargin=0.75 * inch,
        topMargin=0.75 * inch,
        bottomMargin=0.75 * inch
    )

    styles = getSampleStyleSheet()
    title_style = ParagraphStyle(
        "TitleStyle",
        parent=styles["Heading1"],
        fontSize=18,
        textColor=colors.HexColor("#1F3864"),
        spaceAfter=12
    )
    heading_style = ParagraphStyle(
        "HeadingStyle",
        parent=styles["Heading2"],
        fontSize=13,
        textColor=colors.HexColor("#2E75B6"),
        spaceAfter=8
    )

    elements = []

    # ── TITLE
    elements.append(Paragraph("Meeting Intelligence Hub", title_style))
    elements.append(Paragraph("Extracted Insights Report", styles["Normal"]))
    elements.append(Spacer(1, 0.3 * inch))

    # ── DECISIONS TABLE
    elements.append(Paragraph("Decisions Made", heading_style))
    if decisions:
        table_data = [["Source", "Speaker", "Decision", "Confidence"]]
        for d in decisions:
            table_data.append([
                d.get("source", ""),
                d.get("speaker", ""),
                d.get("text", ""),
                f"{d.get('confidence', 0):.0%}"
            ])

        table = Table(table_data, colWidths=[1.2*inch, 1*inch, 4*inch, 0.8*inch])
        table.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#1F3864")),
            ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
            ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
            ("FONTSIZE", (0, 0), (-1, 0), 10),
            ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#D6E4F0")]),
            ("FONTSIZE", (0, 1), (-1, -1), 9),
            ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#BBBBBB")),
            ("VALIGN", (0, 0), (-1, -1), "TOP"),
            ("WORDWRAP", (0, 0), (-1, -1), True),
            ("LEFTPADDING", (0, 0), (-1, -1), 6),
            ("RIGHTPADDING", (0, 0), (-1, -1), 6),
            ("TOPPADDING", (0, 0), (-1, -1), 4),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
        ]))
        elements.append(table)
    else:
        elements.append(Paragraph("No decisions found.", styles["Normal"]))

    elements.append(Spacer(1, 0.3 * inch))

    # ── ACTION ITEMS TABLE
    elements.append(Paragraph("Action Items", heading_style))
    if actions:
        table_data = [["Source", "Assignee", "Task", "Confidence"]]
        for a in actions:
            table_data.append([
                a.get("source", ""),
                a.get("speaker", ""),
                a.get("text", ""),
                f"{a.get('confidence', 0):.0%}"
            ])

        table = Table(table_data, colWidths=[1.2*inch, 1*inch, 4*inch, 0.8*inch])
        table.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#1F3864")),
            ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
            ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
            ("FONTSIZE", (0, 0), (-1, 0), 10),
            ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#D6E4F0")]),
            ("FONTSIZE", (0, 1), (-1, -1), 9),
            ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#BBBBBB")),
            ("VALIGN", (0, 0), (-1, -1), "TOP"),
            ("WORDWRAP", (0, 0), (-1, -1), True),
            ("LEFTPADDING", (0, 0), (-1, -1), 6),
            ("RIGHTPADDING", (0, 0), (-1, -1), 6),
            ("TOPPADDING", (0, 0), (-1, -1), 4),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
        ]))
        elements.append(table)
    else:
        elements.append(Paragraph("No action items found.", styles["Normal"]))

    doc.build(elements)
    buffer.seek(0)
    return buffer.read()