from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
import io
import datetime

class ReportGenerator:
    def __init__(self):
        self.styles = getSampleStyleSheet()
        self.styles.add(ParagraphStyle(name='HospitalHeader', fontSize=18, fontName='Helvetica-Bold', textColor=colors.HexColor('#2563EB'), alignment=1))
        self.styles.add(ParagraphStyle(name='SectionHeader', fontSize=14, fontName='Helvetica-Bold', textColor=colors.HexColor('#0F172A'), spaceAfter=10, spaceBefore=15))
        self.styles.add(ParagraphStyle(name='NormalText', fontSize=10, fontName='Helvetica', textColor=colors.HexColor('#334155'), leading=14))
        self.styles.add(ParagraphStyle(name='DisclaimerText', fontSize=8, fontName='Helvetica-Oblique', textColor=colors.HexColor('#94A3B8'), alignment=1))

    def generate_pdf(self, patient_data, prediction_data, findings, recommendations, image_path, gradcam_path):
        buffer = io.BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=letter, rightMargin=40, leftMargin=40, topMargin=40, bottomMargin=40)
        
        elements = []
        
        # 1. Header
        elements.append(Paragraph("RetinaScan AI - Diabetic Retinopathy Screening", self.styles['HospitalHeader']))
        elements.append(Spacer(1, 0.2 * inch))
        elements.append(Paragraph(f"Report Generated: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", self.styles['NormalText']))
        elements.append(Spacer(1, 0.4 * inch))
        
        # 2. Patient Information
        elements.append(Paragraph("Patient Information", self.styles['SectionHeader']))
        patient_info = [
            ["Patient ID:", patient_data.get('patientId', 'N/A'), "Age / Gender:", f"{patient_data.get('age', 'N/A')} / {patient_data.get('gender', 'N/A')}"],
            ["Patient Name:", patient_data.get('patientName', 'N/A'), "Eye Examined:", patient_data.get('eye', 'N/A')],
            ["Diabetes Duration:", f"{patient_data.get('diabetesDuration', 'N/A')} years", "Exam Date:", patient_data.get('examinationDate', 'N/A')]
        ]
        t = Table(patient_info, colWidths=[1.5*inch, 2*inch, 1.5*inch, 2*inch])
        t.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#F8FAFC')),
            ('TEXTCOLOR', (0,0), (-1,-1), colors.HexColor('#0F172A')),
            ('ALIGN', (0,0), (-1,-1), 'LEFT'),
            ('FONTNAME', (0,0), (-1,-1), 'Helvetica'),
            ('FONTNAME', (0,0), (0,-1), 'Helvetica-Bold'),
            ('FONTNAME', (2,0), (2,-1), 'Helvetica-Bold'),
            ('BOTTOMPADDING', (0,0), (-1,-1), 8),
            ('TOPPADDING', (0,0), (-1,-1), 8),
            ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#E2E8F0')),
        ]))
        elements.append(t)
        elements.append(Spacer(1, 0.4 * inch))
        
        # 3. AI Prediction
        elements.append(Paragraph("AI Diagnostic Assessment", self.styles['SectionHeader']))
        grade = prediction_data.get('grade', 'N/A')
        confidence = prediction_data.get('confidence', 0.0) * 100
        
        pred_text = f"<b>Predicted Grade:</b> {grade} / 4<br/>"
        pred_text += f"<b>Confidence:</b> {confidence:.1f}%<br/>"
        elements.append(Paragraph(pred_text, self.styles['NormalText']))
        elements.append(Spacer(1, 0.2 * inch))
        
        # 4. Images
        if image_path and gradcam_path:
            img_table_data = [[Image(image_path, width=3*inch, height=3*inch), Image(gradcam_path, width=3*inch, height=3*inch)]]
            img_table_data.append(["Original Retinal Scan", "Grad-CAM Explainability Map"])
            img_table = Table(img_table_data, colWidths=[3.2*inch, 3.2*inch])
            img_table.setStyle(TableStyle([
                ('ALIGN', (0,0), (-1,-1), 'CENTER'),
                ('FONTNAME', (0,1), (-1,1), 'Helvetica-Bold'),
                ('TEXTCOLOR', (0,1), (-1,1), colors.HexColor('#64748B')),
                ('TOPPADDING', (0,1), (-1,1), 5),
            ]))
            elements.append(img_table)
            elements.append(Spacer(1, 0.4 * inch))
            
        # 5. Clinical Findings
        elements.append(Paragraph("Detailed AI Findings", self.styles['SectionHeader']))
        for finding in findings:
            elements.append(Paragraph(f"• {finding}", self.styles['NormalText']))
        elements.append(Spacer(1, 0.3 * inch))
        
        # 6. Recommendations
        elements.append(Paragraph("Clinical Recommendations", self.styles['SectionHeader']))
        for rec in recommendations:
            elements.append(Paragraph(f"• {rec}", self.styles['NormalText']))
        elements.append(Spacer(1, 0.6 * inch))
        
        # 7. Signatures & Disclaimer
        sig_data = [["_______________________", "_______________________"], ["AI System Verification", "Doctor's Signature"]]
        sig_table = Table(sig_data, colWidths=[3.5*inch, 3.5*inch])
        sig_table.setStyle(TableStyle([
            ('ALIGN', (0,0), (-1,-1), 'CENTER'),
            ('FONTNAME', (0,1), (-1,1), 'Helvetica'),
            ('TEXTCOLOR', (0,1), (-1,1), colors.HexColor('#64748B')),
        ]))
        elements.append(sig_table)
        elements.append(Spacer(1, 0.5 * inch))
        
        disclaimer = "This AI system is intended for screening and decision-support purposes only. Final diagnosis must be confirmed by a qualified ophthalmologist. Model Version: EN-B3-DR-v1.0"
        elements.append(Paragraph(disclaimer, self.styles['DisclaimerText']))
        
        # Build PDF
        doc.build(elements)
        buffer.seek(0)
        return buffer
