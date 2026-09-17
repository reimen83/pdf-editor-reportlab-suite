import os
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
    texto = re.sub(r'\*\*\*(.*?)\*\*\*', r'<b><i>\1</i></b>', texto)
    texto = re.sub(r'\*\*(.*?)\*\*', r'<b>\1</b>', texto)
    texto = re.sub(r'\*(.*?)\*', r'<i>\1</i>', texto)
    texto = re.sub(r'`(.*?)`', r'<font face="Courier" size="9" color="#2E5B88">\1</font>', texto)
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
    linhas = texto_codigo.strip().split('\n')
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
    linhas = conteudo_md.split('\n')
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
            flowables.append(criar_prompt_box('\n'.join(bloco_codigo), styles['PromptBox']))
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
                if not re.match(r'^\|[\s\:\|-]+\|$', l_str):
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


if __name__ == "__main__":
    conteudo_md = """
## Guia Prático E Definitivo

Suno AI Descomplicado
Transforme suas ideias em músicas profissionais — mesmo sem ser um
“guru” da produção musical!

## O Que Você Vai Encontrar:

(cid:127) Arquitetura de Prompts: A fórmula dos 15-30 descritores
(cid:127) Controle de Estrutura: Uso correto de Meta-Tags de seção
(cid:127) Biblioteca Pronta: Pop, Rock, Sertanejo, Trap, Lo-Fi e mais
(cid:127) Acabamento Profissional: Limpeza, mixagem e masterização
(cid:127) Bônus Exclusivo: Transformando letras próprias em arranjos
Edição 2026 (cid:127) Licença de Uso Pessoal

## Índice Revisado

CAPÍTULO 1: A Arquitetura do Prompt Perfeito no Suno AI Pág. 3
1. A Regra de Ouro do Modo Customizado 3
2. A Fórmula dos 15 a 30 Descritores (Style Prompt) 3
3. Guia Rápido de Parâmetros e Atributos 3
4. O Segredo dos Marcadores de Estrutura (Meta-Tags) 4
5. Exemplo Completo de Aplicação 4
CAPÍTULO 2: Estruturação Musical Dinâmica e Controle de Fluxo Pág. 5
1. A Anatomia da Música Comercial 5
2. Como Usar o Pre-Chorus e o Bridge para Gerar Tensão 5
3. Comandos Avançados de Dinâmica Vocal e Instrumental 5
4. Estendendo e Continuando Faixas (Recurso Extend) 6
CAPÍTULO 3: Biblioteca de Prompts Prontos por Gênero Pág. 7
1. Pop & Synthpop | 2. Rock & Heavy Metal 7
3. Sertanejo & Forró | 4. Hip-Hop, Trap & Lo-Fi 8
CAPÍTULO 4: Dicas Práticas de Mixagem e Acabamento Pág. 9
1. Corrigindo Vocais Abafados | 2. Stems | 3. Masterização 9
BÔNUS EXCLUSIVO: Transformando Letras em Arranjos Pág. 10
nn DICA DE ESTÚDIO / CONCEITO VISUAL:
Navegue pelos capítulos para entender a lógica de produção e aplicar prompts estruturados diretamente na
plataforma Suno AI.

## Capítulo 1

A Arquitetura do Prompt Perfeito no Suno AI
Para obter resultados profissionais no Suno AI, é preciso ir além do modo simples (Simple Mode) e
assumir o controle total utilizando o Custom Mode.
1. A Regra de Ouro do Modo Customizado
No modo padrão, a inteligência artificial decide a estrutura, o tom e os instrumentos por conta própria. No
Custom Mode, você separa o comando em três campos distintos:
(cid:127) Style of Music (Estilo Musical): Onde definimos a sonoridade, instrumentos, BPM e energia.
(cid:127) Lyrics (Letra e Marcadores): Onde inserimos a estrutura da música e os comandos de transição.
(cid:127) Title (Título): Apenas para identificação na sua biblioteca.
2. A Fórmula dos 15 a 30 Descritores (Style Prompt)
Prompts curtos de 2 ou 3 palavras (ex: \"Sertanejo animado\") dão liberdade excessiva à IA, gerando
resultados genéricos. A estrutura ideal de um comando de estilo deve conter entre 15 e 30 palavras
separadas por vírgulas:

## Fórmula De Camadas Do Style Prompt:

[Gênero Principal], [Subgênero], [Tipo de Vocal], [Instrumentos Principais],
[Clima/Mood], [Estilo de Produção], [Tempo/BPM]

## Exemplo Prático De Aplicação:

modern pop, synthpop, polished male vocals, punchy electronic drums, driving
bassline, energetic, uplifting, studio recording, 128 bpm
3. Guia Rápido de Parâmetros e Atributos
Utilize estes atributos dentro do campo Style of Music para direcionar a produção:
(cid:127) Tempo / Ritmo: slow tempo, mid-tempo, upbeat, fast, 120 BPM.
(cid:127) Qualidade Vocal: raspy male vocals (vocal rasgado), ethereal female vocals (suave/etéreo), choir
(coro), duet (dueto).
(cid:127) Textura e Produção: lo-fi, polished (comercial), raw (ao vivo/cru), acoustic, spatial reverb.
(cid:127) Instrumentos de Destaque: acoustic guitar, brass section, synth pads, sub-bass.
4. O Segredo dos Marcadores de Estrutura (Meta-Tags)
Os marcadores devem ser colocados no campo Lyrics para ditar exatamente como a música progride. A
IA interpreta tags entre colchetes [ ] como instruções de arranjo.
Meta-Tag Função no Arranjo Musical
[Intro] Define o início instrumental ou introdução da faixa.
[Verse] Indica o verso (narrativa principal da música).
[Chorus] Refrão (momento de maior energia e gancho).
[Bridge] Ponte (mudança de melodia/ritmo antes do refrão).
[Guitar Solo] Força uma pausa vocal e entra com solo de guitarra.
[Outro] / [Fade Out] Encerramento gradual da faixa até o silêncio.
5. Exemplo Completo de Aplicação
Combine o Style com as Meta-Tags na Letra:
STYLE: acoustic pop, indie folk, warm female vocals, fingerpicking acoustic
guitar, 95 bpm

## Lyrics:

[Intro] (Violão acústico dedilhado)
[Verse 1] Caminhando pelas ruas ao anoitecer...
[Chorus] E o tempo passa mas nada mudou...
[Outro] [Fade Out]
n DICA DE ESTÚDIO / CONCEITO VISUAL:
A precisão das Meta-Tags no campo Lyrics reduz a imprevisibilidade da IA e garante transições musicais
mais orgânicas e alinhadas ao arranjo desejado.

## Capítulo 2

Estruturação Musical Dinâmica e Controle de Fluxo
Saber escrever bons prompts não basta se a música não tiver uma progressão natural. O maior erro no
Suno AI é deixar a música repetitiva. Neste capítulo, você aprenderá a estruturar sua faixa com controle
profissional de dinâmica.
1. A Anatomia da Música Comercial
A maioria dos sucessos comerciais segue uma estrutura testada e aprovada para prender a atenção do
ouvinte do início ao fim:
1. [Intro] (10-15s) - Tema instrumental principal.
2. [Verse 1] - Início da história, energia mais baixa.
3. [Pre-Chorus] - Aumento gradual de energia.
4. [Chorus] - Ponto alto da música (refrão chiclete).
5. [Verse 2] - Mantém o interesse com variação no arranjo.
6. [Chorus] - Retorno ao refrão.
7. [Bridge] - Mudança de tom, melodia ou ritmo (quebra de expectativa).
8. [Guitar Solo / Instrumental Break] - Destaque instrumental.
9. [Chorus] - Refrão final com máxima intensidade.
10. [Outro / Fade Out] - Encerramento da faixa.
2. Como Usar o Pre-Chorus e o Bridge para Gerar Tensão
Sem tensão e alívio, a música se torna monótona.
(cid:127) [Pre-Chorus] (Pré-Refrão): Serve para criar expectativa. Insira frases mais curtas ou ritmo de bateria
acelerado.
(cid:127) [Bridge] (Ponte): Deve ser completamente diferente do resto da música. Se a música for rápida,
diminua o ritmo na ponte.
3. Comandos Avançados de Dinâmica Vocal e Instrumental
Você pode dar ordens específicas à IA no meio da letra utilizando parênteses () ou colchetes []:
(cid:127) [Build Up]: Usado antes do refrão para aumentar a velocidade da bateria ou intensidade.
(cid:127) [Soft Vocals]: Força o vocalista a cantar mais suavemente.
(cid:127) [Powerful Vocals]: Força um vocal potente e rasgado no refrão.
(cid:127) [Silence] ou [Stop]: Para todos os instrumentos por 1 a 2 segundos antes do impacto do refrão.
4. Estendendo e Continuando Faixas (Recurso Extend)
Para construir músicas completas sem perdas de qualidade:
1. Escolha a melhor geração que parou em um ponto lógico (ex: no final do primeiro refrão).
2. Clique no botão Extend.
3. No campo Extend From, defina o segundo exato do corte (ex: 01:45).
4. No campo Lyrics, remova o que já foi cantado e cole apenas o restante da estrutura.
5. Após gerar, use a opção Get Whole Song para unir as partes em uma única faixa.
nn DICA DE ESTÚDIO / CONCEITO VISUAL:
A função Extend é vital para faixas que ultrapassam 2 minutos. Ela evita que a inteligência artificial encerre
a música abruptamente no meio de um verso.

## Capítulo 3

Biblioteca de Prompts Prontos por Gênero
Fórmulas prontas para aplicar diretamente no campo Style of Music do Suno AI. Copie e cole:
1. Pop & Synthpop

## Pop Comercial Radiofônico:

modern pop, dance-pop, polished female vocals, catchy synth riffs, punchy
electronic drums, driving bassline, upbeat, energetic, studio recording, 124 bpm

## Synthpop Retrô Anos 80:

80s synthpop, retro wave, male vocals, analog synthesizers, gated reverb drums,
pulsing bass, nostalgic, dark yet energetic, 118 bpm
2. Rock & Heavy Metal

## Rock Moderno / Alternativo:

modern rock, alternative rock, powerful male vocals, distorted electric guitars,
heavy bass, tight acoustic drums, aggressive, high energy, raw studio mix, 135
bpm

## Rock Acústico / Folk Rock:

acoustic rock, indie folk, warm raspy male vocals, strummed acoustic guitars,
Hammond organ, subtle percussion, intimate, emotional, organic sound, 90 bpm
3. Sertanejo & Forró

## Sertanejo Universitário:

sertanejo universitario, brazilian pop, male duet vocals, bright accordion,
acoustic guitar solo, punchy bass, energetic, festive, live recording vibe, 130
bpm

## Sertanejo Sofrência / Romântico:

sertanejo romantico, emotional male vocal, slow accordion, nylon acoustic
guitar, soft drums, melancholic, intimate, clean production, 85 bpm
4. Hip-Hop, Trap & Lo-Fi

## Trap Moderno:

modern trap, hard hip-hop, deep 808 sub-bass, fast hi-hats, dark synth pads,
aggressive male vocals, hypnotic, moody, heavy low-end mix, 140 bpm

## Lo-Fi Hip-Hop (Chill):

lo-fi hip hop, chillhop, dusty vinyl crackle, mellow electric piano, relaxed
drums, soft bass, laid-back, nostalgic, instrumental, 80 bpm
n DICA DE ESTÚDIO / CONCEITO VISUAL:
Experimente combinar descritores de gêneros opostos (ex: lo-fi com arranjos sertanejos) para criar
sonoridades autênticas e inovadoras no Suno AI.

## Capítulo 4

Dicas Práticas de Mixagem e Acabamento
O Suno AI entrega faixas prontas, mas é comum o áudio apresentar pequenas distorções. Aprenda
técnicas rápidas para elevar a qualidade do arquivo final:
1. Corrigindo Vocais Abafados
(cid:127) No Prompt: Inclua descritores como clean vocal mix ou crisp vocals.
(cid:127) No Equalizador: Aplique um filtro High-Pass (Passa-Altas) em torno de 80 Hz a 100 Hz para limpar o
excesso de graves do vocal.
2. Separação de Stems (Vocais e Instrumentos)
Utilize ferramentas gratuitas online (como Vocal Remover ou Moises.ai) para dividir o MP3/WAV do Suno
em duas trilhas separadas: Vocal e Acompanhamento. Isso permite controlar o volume da voz
independentemente.
3. Masterização Rápida para Plataformas
(cid:127) Normalização de Loudness: Ajuste o volume final para a meta padrão de -14 LUFS (padrão do Spotify
e YouTube) usando plataformas gratuitas como BandLab Mastering.
(cid:127) Margem de Segurança: Mantenha o True Peak em -1.0 dB para evitar distorções na conversão de
áudio.
n DICA DE ESTÚDIO / CONCEITO VISUAL:
A masterização final garante que sua música soe alta e clara em fones de ouvido, sistemas automotivos e
plataformas de streaming sem distorcer.
n

## Bônus Exclusivo

Guia Rápido: Como Transformar Letras e Melodias
Próprias em Arranjos Profissionais no Suno
1. Formatação de Métricas: Escreva sua letra respeitando versos de 8 a 10 sílabas poéticas para evitar
que a IA atropele a dicção vocal.
2. Encaixando o Estilo Ideal: Não tente forçar uma letra romântica em um estilo Trap de 150 BPM. Use
a nossa biblioteca do Capítulo 3 para escolher o BPM compatível com o sentimento da sua
composição.
3. Próximo Nível (Aviso Importante): Este e-book oferece os fundamentos perfeita para criar arranjos
base incríveis. Para aprender a gravar sua própria voz por cima dos arranjos, ajustar afinação fina e
dominar a produção avançada em softwares como Reaper ou BandLab, fique atento ao lançamento do
nosso Curso Completo de Produção Musical com Suno AI!
Suno AI Descomplicado (cid:127) Todos os direitos reservados.
Produzido com apoio de Inteligência Artificial para Produtores Musicais."""
    gerar_pdf(conteudo_md, "pdf_reconstruido.pdf")
    print("PDF reconstruído com sucesso!")
