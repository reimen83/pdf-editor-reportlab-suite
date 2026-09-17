import os
import re
import pdfplumber
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, KeepTogether
from reportlab.pdfgen import canvas

def clean_extracted_text(text):
    """Sanitiza o texto extraído corrigindo códigos CID, marcadores e entidades XML"""
    if not text:
        return ""
    
    # Substitui padrões CID quebrados (ex: (cid:127)) por marcadores de lista limpos
    text = re.sub(r'\(cid:\d+\)', '•', text)
    
    # Substituições para caracteres especiais comuns que causam falhas de renderização
    replacements = {
        '\xa0': ' ',
        '\u2022': '•',
        '■': '■',
    }
    for old, new in replacements.items():
        text = text.replace(old, new)
        
    # Escapa caracteres especiais exigidos pelo ReportLab em Paragraphs
    text = text.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
    return text.strip()

def extrair_estilos_de_pdf(pdf_path):
    """Extrai paleta de cores e propriedades visuais do PDF de Referência (Design)"""
    estilos_extraidos = {
        'primary': colors.HexColor("#1A2B4C"),
        'secondary': colors.HexColor("#2E5B88"),
        'accent': colors.HexColor("#008080"),
        'text_dark': colors.HexColor("#2C3E50"),
        'bg_light': colors.HexColor("#F8F9FA")
    }
    
    try:
        with pdfplumber.open(pdf_path) as pdf:
            hex_colors = []
            for page in pdf.pages:
                for obj in page.extract_words() + page.curves + page.rects:
                    for k in ['non_stroking_color', 'stroking_color', 'fill_color']:
                        c = obj.get(k)
                        if isinstance(c, (tuple, list)) and len(c) == 3:
                            hex_c = '#{:02x}{:02x}{:02x}'.format(int(c[0]*255), int(c[1]*255), int(c[2]*255))
                            if hex_c not in ['#ffffff', '#000000'] and hex_c not in hex_colors:
                                hex_colors.append(hex_c)
            
            if len(hex_colors) >= 1: estilos_extraidos['primary'] = colors.HexColor(hex_colors[0])
            if len(hex_colors) >= 2: estilos_extraidos['secondary'] = colors.HexColor(hex_colors[1])
            if len(hex_colors) >= 3: estilos_extraidos['accent'] = colors.HexColor(hex_colors[2])
    except Exception as e:
        print(f"Aviso na extração de estilos: {e}")
        
    return estilos_extraidos

def extrair_texto_estruturado(pdf_path):
    """Extrai o texto do PDF de Conteúdo, limpa caracteres e infere a hierarquia (H1, H2, Corpo)"""
    blocos_texto = []
    
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            words = page.extract_words(extra_attrs=['size', 'fontname'])
            if not words:
                continue
            
            linhas = {}
            for w in words:
                top_key = round(w['top'], 1)
                found = False
                for k in linhas:
                    if abs(k - top_key) < 3:
                        linhas[k].append(w)
                        found = True
                        break
                if not found:
                    linhas[top_key] = [w]
            
            for top in sorted(linhas.keys()):
                linha_words = sorted(linhas[top], key=lambda x: x['x0'])
                texto_linha = " ".join([w['text'] for w in linha_words])
                
                # Aplica a higienização do texto extraído
                texto_linha = clean_extracted_text(texto_linha)
                if not texto_linha:
                    continue
                
                tam_fonte = sum([w['size'] for w in linha_words]) / len(linha_words)
                
                if tam_fonte > 18:
                    tipo = 'H1'
                elif tam_fonte > 13:
                    tipo = 'H2'
                elif tam_fonte > 11:
                    tipo = 'H3'
                else:
                    tipo = 'BODY'
                
                blocos_texto.append((tipo, texto_linha))
                
    return blocos_texto

def clonar_layout_e_aplicar(pdf_design, pdf_conteudo, pdf_saida):
    """Aplica o visual do PDF_Design no texto do PDF_Conteudo gerando o PDF_Saida"""
    estilos_visual = extrair_estilos_de_pdf(pdf_design)
    blocos_texto = extrair_texto_estruturado(pdf_conteudo)
    
    doc = SimpleDocTemplate(
        pdf_saida,
        pagesize=letter,
        leftMargin=54, rightMargin=54,
        topMargin=54, bottomMargin=54
    )
    
    styles = getSampleStyleSheet()
    
    h1_style = ParagraphStyle(
        'ClonedH1',
        parent=styles['Heading1'],
        fontName='Helvetica-Bold',
        fontSize=20,
        leading=24,
        textColor=estilos_visual['primary'],
        spaceAfter=12
    )
    
    h2_style = ParagraphStyle(
        'ClonedH2',
        parent=styles['Heading2'],
        fontName='Helvetica-Bold',
        fontSize=14,
        leading=18,
        textColor=estilos_visual['secondary'],
        spaceBefore=10,
        spaceAfter=6
    )
    
    body_style = ParagraphStyle(
        'ClonedBody',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=10,
        leading=14,
        textColor=estilos_visual['text_dark'],
        spaceAfter=8
    )
    
    story = []
    
    for tipo, texto in blocos_texto:
        if tipo == 'H1':
            story.append(Paragraph(texto, h1_style))
            story.append(Spacer(1, 8))
        elif tipo in ['H2', 'H3']:
            story.append(Paragraph(texto, h2_style))
            story.append(Spacer(1, 6))
        else:
            story.append(Paragraph(texto, body_style))
            story.append(Spacer(1, 4))
            
    doc.build(story)
    return True
