#!/usr/bin/env python3
import sys
import os
import re
import pdfplumber

TEMPLATE_HEADER = '''import os
import re
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak, HRFlowable, Table, TableStyle
from reportlab.pdfgen import canvas

PRIMARY = colors.HexColor("#1A2B4C")
SECONDARY = colors.HexColor("#2E5B88")
ACCENT = colors.HexColor("#008080")
NEUTRAL_DARK = colors.HexColor("#2C3E50")
NEUTRAL_LIGHT = colors.HexColor("#F8F9FA")
BORDER_COLOR = colors.HexColor("#E2E8F0")

class NumberedCanvas(canvas.Canvas):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_page_number(num_pages)
            canvas.Canvas.showPage(self)
        canvas.Canvas.save(self)

    def draw_page_number(self, page_count):
        if self._pageNumber == 1:
            return

        self.saveState()
        self.setFont("Helvetica", 9)
        self.setFillColor(colors.HexColor("#718096"))

        self.drawString(54, 842 - 36, "Documento Gerado Automatizado")
        self.setStrokeColor(BORDER_COLOR)
        self.setLineWidth(0.5)
        self.line(54, 842 - 42, 595 - 54, 842 - 42)

        page_text = f"Página {self._pageNumber} de {page_count}"
        self.drawRightString(595 - 54, 36, page_text)
        self.line(54, 48, 595 - 54, 48)

        self.restoreState()

def processar_texto(texto):
    texto = re.sub(r'\\*\\*\\*(.*?)\\*\\*\\*', r'<b><i>\\1</i></b>', texto)
    texto = re.sub(r'\\*\\*(.*?)\\*\\*', r'<b>\\1</b>', texto)
    texto = re.sub(r'\\*(.*?)\\*', r'<i>\\1</i>', texto)
    texto = re.sub(r'`(.*?)`', r'<font face="Courier" size="9" color="#2E5B88">\\1</font>', texto)
    return texto

def criar_estilos():
    styles = getSampleStyleSheet()

    styles.add(ParagraphStyle(
        'CoverTitle', parent=styles['Normal'],
        fontName='Helvetica-Bold', fontSize=28, leading=34,
        textColor=PRIMARY, alignment=1, spaceAfter=15
    ))
    styles.add(ParagraphStyle(
        'CoverSubtitle', parent=styles['Normal'],
        fontName='Helvetica', fontSize=13, leading=18,
        textColor=SECONDARY, alignment=1, spaceAfter=30
    ))
    styles.add(ParagraphStyle(
        'CoverAuthor', parent=styles['Normal'],
        fontName='Helvetica-Bold', fontSize=11, leading=14,
        textColor=ACCENT, alignment=1
    ))
    styles.add(ParagraphStyle(
        'CoverMeta', parent=styles['Normal'],
        fontName='Helvetica', fontSize=9, leading=12,
        textColor=colors.HexColor("#718096"), alignment=1
    ))

    styles['Heading1'].fontName = 'Helvetica-Bold'
    styles['Heading1'].fontSize = 18
    styles['Heading1'].leading = 22
    styles['Heading1'].textColor = PRIMARY
    styles['Heading1'].spaceBefore = 18
    styles['Heading1'].spaceAfter = 8
    styles['Heading1'].keepWithNext = True

    styles['Heading2'].fontName = 'Helvetica-Bold'
    styles['Heading2'].fontSize = 13
    styles['Heading2'].leading = 16
    styles['Heading2'].textColor = SECONDARY
    styles['Heading2'].spaceBefore = 12
    styles['Heading2'].spaceAfter = 6
    styles['Heading2'].keepWithNext = True

    styles['Heading3'].fontName = 'Helvetica-Bold'
    styles['Heading3'].fontSize = 10.5
    styles['Heading3'].leading = 14
    styles['Heading3'].textColor = ACCENT
    styles['Heading3'].spaceBefore = 8
    styles['Heading3'].spaceAfter = 4
    styles['Heading3'].keepWithNext = True

    styles['BodyText'].fontName = 'Helvetica'
    styles['BodyText'].fontSize = 9.5
    styles['BodyText'].leading = 13.5
    styles['BodyText'].textColor = NEUTRAL_DARK
    styles['BodyText'].spaceAfter = 6

    styles.add(ParagraphStyle(
        'CustomBullet', parent=styles['BodyText'],
        leftIndent=15, firstLineIndent=-10, spaceAfter=4
    ))
    styles.add(ParagraphStyle(
        'CalloutText', parent=styles['BodyText'],
        fontName='Helvetica-Oblique', fontSize=9, leading=13, textColor=PRIMARY
    ))
    styles.add(ParagraphStyle(
        'PromptBox', parent=styles['Normal'],
        fontName='Courier', fontSize=8.5, leading=11.5, textColor=colors.HexColor("#1A202C")
    ))
    styles.add(ParagraphStyle(
        'TableHeader', parent=styles['Normal'],
        fontName='Helvetica-Bold', fontSize=9, leading=11, textColor=colors.white, alignment=0
    ))
    styles.add(ParagraphStyle(
        'TableCell', parent=styles['Normal'],
        fontName='Helvetica', fontSize=8.5, leading=11, textColor=NEUTRAL_DARK, alignment=0
    ))
    return styles

def criar_callout(texto_processado, estilo):
    p = Paragraph(texto_processado, estilo)
    t = Table([[p]], colWidths=[487])
    t.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), NEUTRAL_LIGHT),
        ('BOX', (0,0), (-1,-1), 0.5, BORDER_COLOR),
        ('LINELEFT', (0,0), (0,0), 3, ACCENT),
        ('TOPPADDING', (0,0), (-1,-1), 6),
        ('BOTTOMPADDING', (0,0), (-1,-1), 6),
        ('LEFTPADDING', (0,0), (-1,-1), 10),
        ('RIGHTPADDING', (0,0), (-1,-1), 10),
    ]))
    return t

def criar_prompt_box(texto_codigo, estilo):
    linhas = texto_codigo.strip().split('\\n')
    paragrafos = [Paragraph(processar_texto(l) if l else "&nbsp;", estilo) for l in linhas]
    t = Table([[p] for p in paragrafos], colWidths=[487])
    t.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#F1F5F9")),
        ('BOX', (0,0), (-1,-1), 0.5, colors.HexColor("#CBD5E1")),
        ('LINELEFT', (0,0), (0,-1), 3, SECONDARY),
        ('TOPPADDING', (0,0), (-1,-1), 2),
        ('BOTTOMPADDING', (0,0), (-1,-1), 2),
        ('LEFTPADDING', (0,0), (-1,-1), 8),
        ('RIGHTPADDING', (0,0), (-1,-1), 8),
    ]))
    return t

def criar_tabela(linhas_md, styles):
    dados = []
    for i, linha in enumerate(linhas_md):
        celulas = [c.strip() for c in linha.split('|')[1:-1]]
        if i == 0:
            row = [Paragraph(f"<b>{processar_texto(c)}</b>", styles['TableHeader']) for c in celulas]
        else:
            row = [Paragraph(processar_texto(c), styles['TableCell']) for c in celulas]
        dados.append(row)

    num_cols = len(dados[0]) if dados else 1
    col_width = 487 / num_cols
    t = Table(dados, colWidths=[col_width]*num_cols)
    ts = [
        ('BACKGROUND', (0,0), (-1,0), PRIMARY),
        ('ALIGN', (0,0), (-1,-1), 'LEFT'),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('GRID', (0,0), (-1,-1), 0.5, BORDER_COLOR),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
        ('LEFTPADDING', (0,0), (-1,-1), 6),
        ('RIGHTPADDING', (0,0), (-1,-1), 6),
    ]
    for r in range(1, len(dados)):
        if r % 2 == 0:
            ts.append(('BACKGROUND', (0, r), (-1, r), NEUTRAL_LIGHT))
    t.setStyle(TableStyle(ts))
    return t

def markdown_para_flowables(conteudo_md, styles):
    flowables = []
    linhas = conteudo_md.split('\\n')
    i, n = 0, len(linhas)

    while i < n:
        linha = linhas[i].rstrip()
        if not linha:
            i += 1
            continue

        if linha.startswith('```'):
            bloco_codigo = []
            i += 1
            while i < n and not linhas[i].rstrip().startswith('```'):
                bloco_codigo.append(linhas[i])
                i += 1
            i += 1
            flowables.append(Spacer(1, 4))
            flowables.append(criar_prompt_box('\\n'.join(bloco_codigo), styles['PromptBox']))
            flowables.append(Spacer(1, 6))
            continue

        if linha.startswith('>'):
            bloco_quote = []
            while i < n and linhas[i].rstrip().startswith('>'):
                bloco_quote.append(linhas[i].rstrip()[1:].strip())
                i += 1
            texto_q = processar_texto(' '.join(bloco_quote))
            flowables.append(Spacer(1, 4))
            flowables.append(criar_callout(texto_q, styles['CalloutText']))
            flowables.append(Spacer(1, 6))
            continue

        if linha.startswith('|') and '|' in linha[1:]:
            bloco_tabela = []
            while i < n and linhas[i].rstrip().startswith('|'):
                l_str = linhas[i].rstrip()
                if not re.match(r'^\\|[\s\\:\\|-]+\\|$', l_str):
                    bloco_tabela.append(l_str)
                i += 1
            if bloco_tabela:
                flowables.append(Spacer(1, 4))
                flowables.append(criar_tabela(bloco_tabela, styles))
                flowables.append(Spacer(1, 6))
            continue

        if linha.startswith('# '):
            flowables.append(Paragraph(processar_texto(linha[2:]), styles['Heading1']))
            flowables.append(HRFlowable(width="100%", thickness=1.5, color=PRIMARY, spaceAfter=8, spaceBefore=2))
            i += 1
            continue
        elif linha.startswith('## '):
            flowables.append(Paragraph(processar_texto(linha[3:]), styles['Heading2']))
            i += 1
            continue
        elif linha.startswith('### '):
            flowables.append(Paragraph(processar_texto(linha[4:]), styles['Heading3']))
            i += 1
            continue

        if re.match(r'^\s*[\-\*]\s+', linha):
            txt = re.sub(r'^\s*[\-\*]\s+', '', linha)
            txt_p = processar_texto(f"• {txt}")
            flowables.append(Paragraph(txt_p, styles['CustomBullet']))
            i += 1
            continue

        if re.match(r'^\s*\d+\.\s+', linha):
            txt = re.sub(r'^\s*\d+\.\s+', '', linha)
            m = re.match(r'^\s*(\d+)\.', linha)
            num = m.group(1) if m else "1"
            txt_p = processar_texto(f"<b>{num}.</b> {txt}")
            flowables.append(Paragraph(txt_p, styles['CustomBullet']))
            i += 1
            continue

        if linha.startswith('---') or linha.startswith('***'):
            flowables.append(HRFlowable(width="100%", thickness=0.5, color=BORDER_COLOR, spaceAfter=8, spaceBefore=8))
            i += 1
            continue

        flowables.append(Paragraph(processar_texto(linha), styles['BodyText']))
        i += 1

    return flowables

def gerar_pdf(conteudo_md, caminho_pdf):
    styles = criar_estilos()
    doc = SimpleDocTemplate(
        caminho_pdf, pagesize=A4,
        leftMargin=54, rightMargin=54, topMargin=54, bottomMargin=54
    )
    story = [
        Spacer(1, 100),
        Paragraph("DOCUMENTO CONVERTIDO", styles['CoverTitle']),
        HRFlowable(width="60%", thickness=2, color=ACCENT, spaceAfter=20, spaceBefore=0),
        Paragraph("Gerado automaticamente a partir de um PDF de origem", styles['CoverSubtitle']),
        Spacer(1, 150),
        Paragraph("Conversão em Python com ReportLab", styles['CoverAuthor']),
        Spacer(1, 10),
        Paragraph("Edição 2026", styles['CoverMeta']),
        PageBreak()
    ]
    story.extend(markdown_para_flowables(conteudo_md, styles))
    doc.build(story, canvasmaker=NumberedCanvas)
'''

def extrair_texto_pdf(caminho_pdf):
    markdown_lote = []
    with pdfplumber.open(caminho_pdf) as pdf:
        for pagina in pdf.pages:
            texto = pagina.extract_text()
            if texto:
                for linha in texto.split('\n'):
                    l = linha.strip()
                    if not l:
                        continue
                    if len(l) < 40 and l.isupper():
                        markdown_lote.append(f"\n## {l.title()}\n")
                    elif l.startswith('•') or l.startswith('-'):
                        markdown_lote.append(f"- {l[1:].strip()}")
                    else:
                        markdown_lote.append(l)
    return "\n".join(markdown_lote)

def main():
    if len(sys.argv) < 2:
        print("Uso: ./pdf_to_reportlab <arquivo_entrada.pdf> [arquivo_saida.py]")
        sys.exit(1)

    pdf_in = sys.argv[1]
    py_out = sys.argv[2] if len(sys.argv) > 2 else "script_gerado.py"

    if not os.path.exists(pdf_in):
        print(f"Erro: O arquivo '{pdf_in}' não foi encontrado.")
        sys.exit(1)

    print(f"[*] Lendo e extraindo conteúdo de: {pdf_in}")
    md_extraido = extrair_texto_pdf(pdf_in)

    print(f"[*] Montando o script Python final no padrão ReportLab...")
    
    # Tratamento para evitar contrabarras no f-string
    md_escapado = md_extraido.replace('\\', '\\\\').replace('"', '\\"')
    
    bloco_main = '\nif __name__ == "__main__":\n' \
                 f'    conteudo_md = """{md_escapado}"""\n' \
                 '    gerar_pdf(conteudo_md, "pdf_reconstruido.pdf")\n' \
                 '    print("PDF reconstruído com sucesso!")\n'

    with open(py_out, 'w', encoding='utf-8') as f:
        f.write(TEMPLATE_HEADER + "\n" + bloco_main)

    print(f"[✔] Sucesso! Script gerado em: {py_out}")

if __name__ == "__main__":
    main()
