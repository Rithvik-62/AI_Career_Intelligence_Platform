"""
Executive PDF Report Generator (V2.0 Enhanced)
Builds a publication-quality analytics report using ReportLab for recruiters and candidates.
"""

import os
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, HRFlowable
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
from datetime import datetime

def generate_pdf_report(session_state_data, output_path):
    """
    Generates an executive PDF report containing multi-metric scores, top 5 career matches,
    explainable AI reasoning, skill gaps, and prescriptive recommendations.
    """
    doc = SimpleDocTemplate(
        output_path, 
        pagesize=letter,
        rightMargin=36, leftMargin=36, topMargin=36, bottomMargin=36
    )
    styles = getSampleStyleSheet()
    
    # Color Palette
    PRIMARY = colors.HexColor("#2563EB")
    DARK_TEXT = colors.HexColor("#0F172A")
    MUTED_TEXT = colors.HexColor("#475569")
    BG_CARD = colors.HexColor("#F8FAFC")
    BORDER_COLOR = colors.HexColor("#E2E8F0")
    
    # Custom Paragraph Styles
    title_style = ParagraphStyle(
        'DocTitle', parent=styles['Heading1'],
        fontSize=22, leading=26, textColor=PRIMARY, spaceAfter=4
    )
    subtitle_style = ParagraphStyle(
        'DocSubTitle', parent=styles['Normal'],
        fontSize=10, leading=12, textColor=MUTED_TEXT, spaceAfter=15
    )
    heading_style = ParagraphStyle(
        'SectionHeading', parent=styles['Heading2'],
        fontSize=14, leading=18, textColor=DARK_TEXT, spaceBefore=12, spaceAfter=8
    )
    body_style = ParagraphStyle(
        'BodyTextCustom', parent=styles['Normal'],
        fontSize=9.5, leading=14, textColor=DARK_TEXT
    )
    
    elements = []
    
    # 1. Header & Title Block
    elements.append(Paragraph("AI Career Intelligence — Executive Report", title_style))
    elements.append(Paragraph(f"Generated on {datetime.now().strftime('%B %d, %Y at %H:%M:%S')} | Version 2.0 BI Edition", subtitle_style))
    elements.append(HRFlowable(width="100%", thickness=1.5, color=PRIMARY, spaceAfter=15))
    
    parsed_data = session_state_data.get('parsed_data', {})
    prediction_data = session_state_data.get('prediction_data', {})
    scoring_data = session_state_data.get('scoring_data', {})
    skill_gap_data = session_state_data.get('skill_gap_data', {})
    insights_data = session_state_data.get('insights_data', {})
    
    # 2. Executive Candidate Summary
    name = parsed_data.get('name', 'Candidate')
    email = parsed_data.get('email', 'N/A')
    phone = parsed_data.get('phone', 'N/A')
    role = prediction_data.get('predicted_role', 'Unknown')
    conf = prediction_data.get('confidence', 0.0)
    readiness = scoring_data.get('career_readiness', 0.0)
    overall_score = scoring_data.get('overall_score', 0)
    ats_score = scoring_data.get('ats_score', 0)
    
    summary_data = [
        [Paragraph(f"<b>Candidate Name:</b> {name}", body_style), Paragraph(f"<b>Target Role:</b> {role}", body_style)],
        [Paragraph(f"<b>Email:</b> {email}", body_style), Paragraph(f"<b>AI Confidence:</b> {conf}%", body_style)],
        [Paragraph(f"<b>Phone:</b> {phone}", body_style), Paragraph(f"<b>Career Readiness:</b> {readiness}%", body_style)]
    ]
    t_summary = Table(summary_data, colWidths=[270, 270])
    t_summary.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), BG_CARD),
        ('BOX', (0,0), (-1,-1), 1, BORDER_COLOR),
        ('PADDING', (0,0), (-1,-1), 8),
    ]))
    elements.append(t_summary)
    elements.append(Spacer(1, 12))
    
    # 3. Key Analytical Scores Table
    elements.append(Paragraph("Advanced Resume Analytics", heading_style))
    scores_table_data = [
        ["Metric", "Score / Index", "Rating / Interpretation"],
        ["Overall Resume Score", f"{overall_score} / 100", scoring_data.get('rating', 'N/A')],
        ["ATS Compatibility Score", f"{ats_score}%", "Structural readability for ATS engines"],
        ["Resume Completeness", f"{scoring_data.get('completeness_pct', 0)}%", "Core structural coverage"],
        ["Technical Skill Score", f"{scoring_data.get('category_scores', {}).get('skills', 0)} / 30", "Technical vocabulary breadth"],
        ["Experience Score", f"{scoring_data.get('category_scores', {}).get('experience', 0)} / 20", "Employment history depth"],
        ["Project Portfolio Score", f"{scoring_data.get('category_scores', {}).get('projects', 0)} / 20", "Practical execution evidence"]
    ]
    t_scores = Table(scores_table_data, colWidths=[180, 100, 260])
    t_scores.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), PRIMARY),
        ('TEXTCOLOR', (0,0), (-1,0), colors.white),
        ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
        ('BOTTOMPADDING', (0,0), (-1,0), 6),
        ('GRID', (0,0), (-1,-1), 0.5, BORDER_COLOR),
        ('PADDING', (0,0), (-1,-1), 6),
    ]))
    elements.append(t_scores)
    elements.append(Spacer(1, 12))
    
    # 4. Top 5 Career Predictions
    top_preds = prediction_data.get('top_predictions', [])
    if top_preds:
        elements.append(Paragraph("Top Career Predictions (Multi-Class ML Model)", heading_style))
        pred_table_data = [["Rank", "Predicted Career Path", "Confidence Level"]]
        for item in top_preds[:5]:
            pred_table_data.append([str(item.get('rank', 1)), item.get('role', 'N/A'), f"{item.get('confidence', 0)}%"])
        t_preds = Table(pred_table_data, colWidths=[60, 320, 160])
        t_preds.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#0F172A")),
            ('TEXTCOLOR', (0,0), (-1,0), colors.white),
            ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
            ('GRID', (0,0), (-1,-1), 0.5, BORDER_COLOR),
            ('PADDING', (0,0), (-1,-1), 5),
        ]))
        elements.append(t_preds)
        elements.append(Spacer(1, 12))
        
    # 5. Skill Gap & Recommendations
    elements.append(Paragraph("Skill Gap & Prescriptive Recommendations", heading_style))
    acquired = ", ".join(skill_gap_data.get('acquired_skills', [])) or "None"
    missing = ", ".join(skill_gap_data.get('missing_skills', [])) or "None"
    
    elements.append(Paragraph(f"<b>Acquired Role Skills:</b> {acquired}", body_style))
    elements.append(Spacer(1, 4))
    elements.append(Paragraph(f"<b>Missing Role Skills:</b> {missing}", body_style))
    elements.append(Spacer(1, 8))
    
    if insights_data:
        elements.append(Paragraph(f"<b>Top Strength:</b> {insights_data.get('top_strength', 'N/A')}", body_style))
        elements.append(Spacer(1, 4))
        elements.append(Paragraph(f"<b>Highest Impact Recommendation:</b> {insights_data.get('highest_impact_recommendation', 'N/A')}", body_style))
        
    doc.build(elements)
    return output_path
