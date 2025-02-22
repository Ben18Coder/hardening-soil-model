from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY

class ReportGenerator:
    @staticmethod
    def generate_report(parameters, img_paths, output_file='output/reports/calibration_report.pdf'):
        doc = SimpleDocTemplate(output_file, pagesize=letter, rightMargin=72, leftMargin=72, topMargin=72, bottomMargin=72)
        styles = getSampleStyleSheet()
        
        # Estilos personalizados
        title_style = ParagraphStyle(
            'CustomTitle',
            parent=styles['Title'],
            fontSize=24,
            spaceAfter=30,
            textColor=colors.HexColor('#1B4F72'),
            alignment=TA_CENTER,
            fontName='Helvetica-Bold'
        )
        
        heading_style = ParagraphStyle(
            'CustomHeading',
            parent=styles['Heading2'],
            fontSize=16,
            textColor=colors.HexColor('#2874A6'),
            spaceAfter=20,
            spaceBefore=20,
            fontName='Helvetica-Bold'
        )
        
        param_style = ParagraphStyle(
            'CustomParam',
            parent=styles['Normal'],
            fontSize=12,
            textColor=colors.HexColor('#2C3E50'),
            alignment=TA_JUSTIFY,
            fontName='Helvetica',
            leading=20
        )
        
        story = []
        
        # Encabezado
        story.append(Paragraph("Informe de Calibración:<br/>Modelo Hardening Soil", title_style))
        story.append(Spacer(1, 30))
        
        # Parámetros
        story.append(Paragraph("Parámetros Calculados", heading_style))
        story.append(Spacer(1, 20))
        
        # Función para formatear valores con estilo
        def format_value(value, unit=''):
            if value is None:
                return '<i>N/A</i>'
            val = f"{value:.2f}" if isinstance(value, (int, float)) else str(value)
            return f"{val} <i>{unit}</i>" if unit else val
        
        # Texto con formato mejorado
        params_text = f"""
        <para alignment="justify" spaceAfter="10">
        <b>E50ref:</b> {format_value(parameters['E50ref'], 'kPa')}<br/>
        <b>Eur_ref:</b> {format_value(parameters['Eur_ref'], 'kPa')}<br/>
        <b>φ (Ángulo de fricción):</b> {format_value(parameters['phi'], '°')}<br/>
        <b>c (Cohesión):</b> {format_value(parameters['c'], 'kPa')}<br/>
        <b>ψ (Ángulo de dilatancia):</b> {format_value(parameters['psi'], '°')}<br/>
        <b>m (Exponente de rigidez):</b> {format_value(parameters['m'])}<br/>
        <b>ν_ur (Coeficiente de Poisson):</b> {format_value(parameters['v_ur'])}<br/>
        <b>K0_nc:</b> {format_value(parameters['K0_nc'])}<br/>
        <b>Rf (Ratio de falla):</b> {format_value(parameters['Rf'])}
        </para>
        """
        story.append(Paragraph(params_text, param_style))
        story.append(Spacer(1, 30))
        
        # Gráficos con título
        story.append(Paragraph("Resultados Gráficos", heading_style))
        for path in img_paths:
            story.append(Spacer(1, 20))
            story.append(Image(path, width=450, height=338))  # Proporción 4:3
            story.append(Spacer(1, 20))
        
        doc.build(story)