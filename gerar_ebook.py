import sys
import os
import subprocess
import platform
from reportlab.lib.pagesizes import letter
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, HRFlowable, Table, TableStyle, PageBreak
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors

# --- FUNÇÃO PARA PINTAR O FUNDO ESCURO ---
def desenhar_fundo_escuro(canvas, doc):
    canvas.saveState()
    canvas.setFillColor(colors.HexColor("#0B132B"))
    canvas.rect(0, 0, letter[0], letter[1], fill=True, stroke=False)
    canvas.restoreState()

# --- ABRIR PDF AUTOMATICAMENTE ---
def abrir_pdf_na_tela(caminho_pdf):
    if os.path.exists(caminho_pdf):
        sistema = platform.system()
        if sistema == "Linux":
            subprocess.run(["xdg-open", caminho_pdf])
        elif sistema == "Windows":
            os.startfile(caminho_pdf)
        elif sistema == "Darwin":
            subprocess.run(["open", caminho_pdf])

def gerar_ebook_suno(output_pdf):
    # Margens levemente ajustadas para dar mais presença visual
    doc = SimpleDocTemplate(
        output_pdf,
        pagesize=letter,
        rightMargin=40, leftMargin=40,
        topMargin=40, bottomMargin=40
    )
    
    styles = getSampleStyleSheet()
    
    # Paleta Dark Mode
    PRIMARY_GOLD = colors.HexColor("#F6AD55")
    SECONDARY_CYAN = colors.HexColor("#4FD1C5")
    TEXT_LIGHT = colors.HexColor("#E2E8F0")
    CARD_BG = colors.HexColor("#1C2541")
    BORDER_COLOR = colors.HexColor("#3A506B")
    WHITE = colors.HexColor("#FFFFFF")
    
    # --- ESTILOS TIPOGRÁFICOS AMPLIADOS (PARA PREENCHER A PÁGINA) ---
    cover_title_style = ParagraphStyle(
        'CoverTitle', parent=styles['Heading1'],
        fontName='Helvetica-Bold', fontSize=32, leading=38,
        textColor=PRIMARY_GOLD, alignment=1, spaceAfter=20
    )
    
    cover_subtitle_style = ParagraphStyle(
        'CoverSubTitle', parent=styles['Normal'],
        fontName='Helvetica-Oblique', fontSize=15, leading=22,
        textColor=SECONDARY_CYAN, alignment=1, spaceAfter=30
    )
    
    h1_style = ParagraphStyle(
        'SectionH1', parent=styles['Heading1'],
        fontName='Helvetica-Bold', fontSize=20, leading=24,
        textColor=PRIMARY_GOLD, spaceBefore=15, spaceAfter=15, keepWithNext=True
    )
    
    h2_style = ParagraphStyle(
        'SectionH2', parent=styles['Heading2'],
        fontName='Helvetica-Bold', fontSize=14, leading=18,
        textColor=SECONDARY_CYAN, spaceBefore=18, spaceAfter=10, keepWithNext=True
    )
    
    body_style = ParagraphStyle(
        'BodyLight', parent=styles['BodyText'],
        fontName='Helvetica', fontSize=11, leading=17,
        textColor=TEXT_LIGHT, spaceAfter=12
    )
    
    bullet_style = ParagraphStyle(
        'BulletText', parent=body_style,
        leftIndent=18, firstLineIndent=-12, spaceAfter=10
    )
    
    code_style = ParagraphStyle(
        'CodeText', parent=body_style,
        fontName='Courier', fontSize=10, leading=14,
        textColor=colors.HexColor("#63B3ED")
    )
    
    index_num_style = ParagraphStyle(
        'IndexNum', parent=body_style,
        fontName='Helvetica-Bold', fontSize=12, leading=18,
        textColor=PRIMARY_GOLD, alignment=2
    )

    # Função aux para criar banners visuais/decorativos de produção musical
    def criar_banner_decorativo(texto_banner, icone="🎧"):
        content = Paragraph(f"<b>{icone} DICA DE ESTÚDIO / CONCEITO VISUAL:</b><br/>{texto_banner}", ParagraphStyle('BannerTxt', parent=body_style, fontSize=10, leading=14, textColor=WHITE))
        t = Table([[content]], colWidths=[490])
        t.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#0F2042")),
            ('BOX', (0,0), (-1,-1), 1, SECONDARY_CYAN),
            ('PADDING', (0,0), (-1,-1), 12),
            ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ]))
        return t

    story = []

    # ==========================================
    # PÁGINA 1: CAPA
    # ==========================================
    story.append(Spacer(1, 40))
    story.append(Paragraph("GUIA PRÁTICO E DEFINITIVO", ParagraphStyle('CoverPre', parent=cover_subtitle_style, fontSize=14, textColor=WHITE)))
    story.append(Spacer(1, 15))
    story.append(Paragraph("Suno AI Descomplicado", cover_title_style))
    story.append(Paragraph("Transforme suas ideias em músicas profissionais — mesmo sem ser um “guru” da produção musical!", cover_subtitle_style))
    story.append(HRFlowable(width="85%", thickness=3, color=PRIMARY_GOLD, spaceBefore=15, spaceAfter=40))
    
    capa_box_text = (
        "<font size=13 color='#F6AD55'><b>O QUE VOCÊ VAI ENCONTRAR:</b></font><br/><br/>"
        "• <b>Arquitetura de Prompts:</b> A fórmula dos 15-30 descritores<br/><br/>"
        "• <b>Controle de Estrutura:</b> Uso correto de Meta-Tags de seção<br/><br/>"
        "• <b>Biblioteca Pronta:</b> Pop, Rock, Sertanejo, Trap, Lo-Fi e mais<br/><br/>"
        "• <b>Acabamento Profissional:</b> Limpeza, mixagem e masterização<br/><br/>"
        "• <b>Bônus Exclusivo:</b> Transformando letras próprias em arranjos"
    )
    t_capa = Table([[Paragraph(capa_box_text, body_style)]], colWidths=[490])
    t_capa.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), CARD_BG),
        ('BOX', (0,0), (-1,-1), 1.5, SECONDARY_CYAN),
        ('PADDING', (0,0), (-1,-1), 20),
    ]))
    story.append(t_capa)
    story.append(Spacer(1, 60))
    story.append(Paragraph("Edição 2026 • Licença de Uso Pessoal", ParagraphStyle('CoverFoot', parent=body_style, alignment=1, fontSize=11, textColor=SECONDARY_CYAN)))
    story.append(PageBreak())

    # ==========================================
    # PÁGINA 2: ÍNDICE / SUMÁRIO
    # ==========================================
    story.append(Paragraph("ÍNDICE REVISADO", h1_style))
    story.append(HRFlowable(width="100%", thickness=1.5, color=PRIMARY_GOLD, spaceBefore=0, spaceAfter=25))
    
    indice_data = [
        [Paragraph("<b>CAPÍTULO 1: A Arquitetura do Prompt Perfeito no Suno AI</b>", body_style), Paragraph("Pág. 3", index_num_style)],
        [Paragraph("1. A Regra de Ouro do Modo Customizado", bullet_style), Paragraph("3", index_num_style)],
        [Paragraph("2. A Fórmula dos 15 a 30 Descritores (Style Prompt)", bullet_style), Paragraph("3", index_num_style)],
        [Paragraph("3. Guia Rápido de Parâmetros e Atributos", bullet_style), Paragraph("3", index_num_style)],
        [Paragraph("4. O Segredo dos Marcadores de Estrutura (Meta-Tags)", bullet_style), Paragraph("4", index_num_style)],
        [Paragraph("5. Exemplo Completo de Aplicação", bullet_style), Paragraph("4", index_num_style)],
        
        [Paragraph("<b>CAPÍTULO 2: Estruturação Musical Dinâmica e Controle de Fluxo</b>", body_style), Paragraph("Pág. 5", index_num_style)],
        [Paragraph("1. A Anatomia da Música Comercial", bullet_style), Paragraph("5", index_num_style)],
        [Paragraph("2. Como Usar o Pre-Chorus e o Bridge para Gerar Tensão", bullet_style), Paragraph("5", index_num_style)],
        [Paragraph("3. Comandos Avançados de Dinâmica Vocal e Instrumental", bullet_style), Paragraph("5", index_num_style)],
        [Paragraph("4. Estendendo e Continuando Faixas (Recurso Extend)", bullet_style), Paragraph("6", index_num_style)],
        
        [Paragraph("<b>CAPÍTULO 3: Biblioteca de Prompts Prontos por Gênero</b>", body_style), Paragraph("Pág. 7", index_num_style)],
        [Paragraph("1. Pop & Synthpop | 2. Rock & Heavy Metal", bullet_style), Paragraph("7", index_num_style)],
        [Paragraph("3. Sertanejo & Forró | 4. Hip-Hop, Trap & Lo-Fi", bullet_style), Paragraph("8", index_num_style)],
        
        [Paragraph("<b>CAPÍTULO 4: Dicas Práticas de Mixagem e Acabamento</b>", body_style), Paragraph("Pág. 9", index_num_style)],
        [Paragraph("1. Corrigindo Vocais Abafados | 2. Stems | 3. Masterização", bullet_style), Paragraph("9", index_num_style)],
        
        [Paragraph("<b>BÔNUS EXCLUSIVO: Transformando Letras em Arranjos</b>", body_style), Paragraph("Pág. 10", index_num_style)],
    ]
    
    t_indice = Table(indice_data, colWidths=[410, 80])
    t_indice.setStyle(TableStyle([
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('BOTTOMPADDING', (0,0), (-1,-1), 6),
        ('TOPPADDING', (0,0), (-1,-1), 6),
        ('LINEBELOW', (0,0), (-1,-1), 0.5, BORDER_COLOR),
    ]))
    story.append(t_indice)
    story.append(Spacer(1, 25))
    story.append(criar_banner_decorativo("Navegue pelos capítulos para entender a lógica de produção e aplicar prompts estruturados diretamente na plataforma Suno AI.", "🎛️"))
    story.append(PageBreak())

    # ==========================================
    # PÁGINA 3: CAPÍTULO 1 (PARTE 1)
    # ==========================================
    story.append(Paragraph("CAPÍTULO 1", ParagraphStyle('CapTag', parent=body_style, textColor=SECONDARY_CYAN, fontName='Helvetica-Bold')))
    story.append(Paragraph("A Arquitetura do Prompt Perfeito no Suno AI", h1_style))
    story.append(HRFlowable(width="100%", thickness=1.5, color=PRIMARY_GOLD, spaceBefore=0, spaceAfter=15))
    
    story.append(Paragraph("Para obter resultados profissionais no Suno AI, é preciso ir além do modo simples (<i>Simple Mode</i>) e assumir o controle total utilizando o <b>Custom Mode</b>.", body_style))
    
    story.append(Paragraph("1. A Regra de Ouro do Modo Customizado", h2_style))
    story.append(Paragraph("No modo padrão, a inteligência artificial decide a estrutura, o tom e os instrumentos por conta própria. No <b>Custom Mode</b>, você separa o comando em três campos distintos:", body_style))
    story.append(Paragraph("• <b>Style of Music (Estilo Musical):</b> Onde definimos a sonoridade, instrumentos, BPM e energia.", bullet_style))
    story.append(Paragraph("• <b>Lyrics (Letra e Marcadores):</b> Onde inserimos a estrutura da música e os comandos de transição.", bullet_style))
    story.append(Paragraph("• <b>Title (Título):</b> Apenas para identificação na sua biblioteca.", bullet_style))
    
    story.append(Paragraph("2. A Fórmula dos 15 a 30 Descritores (Style Prompt)", h2_style))
    story.append(Paragraph("Prompts curtos de 2 ou 3 palavras (ex: <i>\"Sertanejo animado\"</i>) dão liberdade excessiva à IA, gerando resultados genéricos. A estrutura ideal de um comando de estilo deve conter entre 15 e 30 palavras separadas por vírgulas:", body_style))
    
    code_f = Paragraph("<b>FÓRMULA DE CAMADAS DO STYLE PROMPT:</b><br/>[Gênero Principal], [Subgênero], [Tipo de Vocal], [Instrumentos Principais], [Clima/Mood], [Estilo de Produção], [Tempo/BPM]", code_style)
    t_f = Table([[code_f]], colWidths=[490])
    t_f.setStyle(TableStyle([('BACKGROUND', (0,0), (-1,-1), CARD_BG), ('PADDING', (0,0), (-1,-1), 10), ('BOX', (0,0), (-1,-1), 0.5, SECONDARY_CYAN)]))
    story.append(t_f)
    story.append(Spacer(1, 10))
    
    code_ex = Paragraph("<b>EXEMPLO PRÁTICO DE APLICAÇÃO:</b><br/>modern pop, synthpop, polished male vocals, punchy electronic drums, driving bassline, energetic, uplifting, studio recording, 128 bpm", code_style)
    t_ex = Table([[code_ex]], colWidths=[490])
    t_ex.setStyle(TableStyle([('BACKGROUND', (0,0), (-1,-1), CARD_BG), ('PADDING', (0,0), (-1,-1), 10), ('BOX', (0,0), (-1,-1), 0.5, SECONDARY_CYAN)]))
    story.append(t_ex)
    
    story.append(Spacer(1, 15))
    story.append(Paragraph("3. Guia Rápido de Parâmetros e Atributos", h2_style))
    story.append(Paragraph("Utilize estes atributos dentro do campo Style of Music para direcionar a produção:", body_style))
    story.append(Paragraph("• <b>Tempo / Ritmo:</b> slow tempo, mid-tempo, upbeat, fast, 120 BPM.", bullet_style))
    story.append(PageBreak())

    # ==========================================
    # PÁGINA 4: CAPÍTULO 1 (PARTE 2)
    # ==========================================
    story.append(Paragraph("• <b>Qualidade Vocal:</b> raspy male vocals (vocal rasgado), ethereal female vocals (suave/etéreo), choir (coro), duet (dueto).", bullet_style))
    story.append(Paragraph("• <b>Textura e Produção:</b> lo-fi, polished (comercial), raw (ao vivo/cru), acoustic, spatial reverb.", bullet_style))
    story.append(Paragraph("• <b>Instrumentos de Destaque:</b> acoustic guitar, brass section, synth pads, sub-bass.", bullet_style))
    
    story.append(Paragraph("4. O Segredo dos Marcadores de Estrutura (Meta-Tags)", h2_style))
    story.append(Paragraph("Os marcadores devem ser colocados no campo <b>Lyrics</b> para ditar exatamente como a música progride. A IA interpreta tags entre colchetes [ ] como instruções de arranjo.", body_style))
    
    meta_tags_table = [
        [Paragraph("<b>Meta-Tag</b>", ParagraphStyle('TH1', parent=body_style, fontName='Helvetica-Bold', textColor=WHITE)), Paragraph("<b>Função no Arranjo Musical</b>", ParagraphStyle('TH2', parent=body_style, fontName='Helvetica-Bold', textColor=WHITE))],
        [Paragraph("<b>[Intro]</b>", code_style), Paragraph("Define o início instrumental ou introdução da faixa.", body_style)],
        [Paragraph("<b>[Verse]</b>", code_style), Paragraph("Indica o verso (narrativa principal da música).", body_style)],
        [Paragraph("<b>[Chorus]</b>", code_style), Paragraph("Refrão (momento de maior energia e gancho).", body_style)],
        [Paragraph("<b>[Bridge]</b>", code_style), Paragraph("Ponte (mudança de melodia/ritmo antes do refrão).", body_style)],
        [Paragraph("<b>[Guitar Solo]</b>", code_style), Paragraph("Força uma pausa vocal e entra com solo de guitarra.", body_style)],
        [Paragraph("<b>[Outro] / [Fade Out]</b>", code_style), Paragraph("Encerramento gradual da faixa até o silêncio.", body_style)],
    ]
    t_meta = Table(meta_tags_table, colWidths=[150, 340])
    t_meta.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), BORDER_COLOR),
        ('GRID', (0,0), (-1,-1), 0.5, BORDER_COLOR),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [CARD_BG, colors.HexColor("#0B132B")]),
        ('PADDING', (0,0), (-1,-1), 7),
    ]))
    story.append(t_meta)
    
    story.append(Paragraph("5. Exemplo Completo de Aplicação", h2_style))
    story.append(Paragraph("Combine o Style com as Meta-Tags na Letra:", body_style))
    
    code_app = Paragraph("<b>STYLE:</b> acoustic pop, indie folk, warm female vocals, fingerpicking acoustic guitar, 95 bpm<br/><br/><b>LYRICS:</b><br/>[Intro] (Violão acústico dedilhado)<br/>[Verse 1] Caminhando pelas ruas ao anoitecer...<br/>[Chorus] E o tempo passa mas nada mudou...<br/>[Outro] [Fade Out]", code_style)
    t_app = Table([[code_app]], colWidths=[490])
    t_app.setStyle(TableStyle([('BACKGROUND', (0,0), (-1,-1), CARD_BG), ('PADDING', (0,0), (-1,-1), 10), ('BOX', (0,0), (-1,-1), 0.5, SECONDARY_CYAN)]))
    story.append(t_app)
    
    story.append(Spacer(1, 15))
    story.append(criar_banner_decorativo("A precisão das Meta-Tags no campo Lyrics reduz a imprevisibilidade da IA e garante transições musicais mais orgânicas e alinhadas ao arranjo desejado.", "🎸"))
    story.append(PageBreak())

    # ==========================================
    # PÁGINA 5: CAPÍTULO 2 (PARTE 1)
    # ==========================================
    story.append(Paragraph("CAPÍTULO 2", ParagraphStyle('CapTag2', parent=body_style, textColor=SECONDARY_CYAN, fontName='Helvetica-Bold')))
    story.append(Paragraph("Estruturação Musical Dinâmica e Controle de Fluxo", h1_style))
    story.append(HRFlowable(width="100%", thickness=1.5, color=PRIMARY_GOLD, spaceBefore=0, spaceAfter=15))
    
    story.append(Paragraph("Saber escrever bons prompts não basta se a música não tiver uma progressão natural. O maior erro no Suno AI é deixar a música repetitiva. Neste capítulo, você aprenderá a estruturar sua faixa com controle profissional de dinâmica.", body_style))
    
    story.append(Paragraph("1. A Anatomia da Música Comercial", h2_style))
    story.append(Paragraph("A maioria dos sucessos comerciais segue uma estrutura testada e aprovada para prender a atenção do ouvinte do início ao fim:", body_style))
    
    struct_c2 = (
        "1. <b>[Intro]</b> (10-15s) - Tema instrumental principal.<br/>"
        "2. <b>[Verse 1]</b> - Início da história, energia mais baixa.<br/>"
        "3. <b>[Pre-Chorus]</b> - Aumento gradual de energia.<br/>"
        "4. <b>[Chorus]</b> - Ponto alto da música (refrão chiclete).<br/>"
        "5. <b>[Verse 2]</b> - Mantém o interesse com variação no arranjo.<br/>"
        "6. <b>[Chorus]</b> - Retorno ao refrão.<br/>"
        "7. <b>[Bridge]</b> - Mudança de tom, melodia ou ritmo (quebra de expectativa).<br/>"
        "8. <b>[Guitar Solo / Instrumental Break]</b> - Destaque instrumental.<br/>"
        "9. <b>[Chorus]</b> - Refrão final com máxima intensidade.<br/>"
        "10. <b>[Outro / Fade Out]</b> - Encerramento da faixa."
    )
    t_st = Table([[Paragraph(struct_c2, body_style)]], colWidths=[490])
    t_st.setStyle(TableStyle([('BACKGROUND', (0,0), (-1,-1), CARD_BG), ('PADDING', (0,0), (-1,-1), 10), ('BOX', (0,0), (-1,-1), 0.5, BORDER_COLOR)]))
    story.append(t_st)
    
    story.append(Paragraph("2. Como Usar o Pre-Chorus e o Bridge para Gerar Tensão", h2_style))
    story.append(Paragraph("Sem tensão e alívio, a música se torna monótona.", body_style))
    story.append(Paragraph("• <b>[Pre-Chorus] (Pré-Refrão):</b> Serve para criar expectativa. Insira frases mais curtas ou ritmo de bateria acelerado.", bullet_style))
    story.append(Paragraph("• <b>[Bridge] (Ponte):</b> Deve ser completamente diferente do resto da música. Se a música for rápida, diminua o ritmo na ponte.", bullet_style))
    story.append(PageBreak())

    # ==========================================
    # PÁGINA 6: CAPÍTULO 2 (PARTE 2)
    # ==========================================
    story.append(Paragraph("3. Comandos Avançados de Dinâmica Vocal e Instrumental", h2_style))
    story.append(Paragraph("Você pode dar ordens específicas à IA no meio da letra utilizando parênteses () ou colchetes []:", body_style))
    story.append(Paragraph("• <b>[Build Up]:</b> Usado antes do refrão para aumentar a velocidade da bateria ou intensidade.", bullet_style))
    story.append(Paragraph("• <b>[Soft Vocals]:</b> Força o vocalista a cantar mais suavemente.", bullet_style))
    story.append(Paragraph("• <b>[Powerful Vocals]:</b> Força um vocal potente e rasgado no refrão.", bullet_style))
    story.append(Paragraph("• <b>[Silence] ou [Stop]:</b> Para todos os instrumentos por 1 a 2 segundos antes do impacto do refrão.", bullet_style))
    
    story.append(Spacer(1, 10))
    story.append(Paragraph("4. Estendendo e Continuando Faixas (Recurso Extend)", h2_style))
    story.append(Paragraph("Para construir músicas completas sem perdas de qualidade:", body_style))
    story.append(Paragraph("1. Escolha a melhor geração que parou em um ponto lógico (ex: no final do primeiro refrão).", bullet_style))
    story.append(Paragraph("2. Clique no botão <b>Extend</b>.", bullet_style))
    story.append(Paragraph("3. No campo <b>Extend From</b>, defina o segundo exato do corte (ex: 01:45).", bullet_style))
    story.append(Paragraph("4. No campo <b>Lyrics</b>, remova o que já foi cantado e cole apenas o restante da estrutura.", bullet_style))
    story.append(Paragraph("5. Após gerar, use a opção <b>Get Whole Song</b> para unir as partes em uma única faixa.", bullet_style))
    
    story.append(Spacer(1, 20))
    story.append(criar_banner_decorativo("A função Extend é vital para faixas que ultrapassam 2 minutos. Ela evita que a inteligência artificial encerre a música abruptamente no meio de um verso.", "🎚️"))
    story.append(PageBreak())

    # ==========================================
    # PÁGINA 7: CAPÍTULO 3 (PARTE 1)
    # ==========================================
    story.append(Paragraph("CAPÍTULO 3", ParagraphStyle('CapTag3', parent=body_style, textColor=SECONDARY_CYAN, fontName='Helvetica-Bold')))
    story.append(Paragraph("Biblioteca de Prompts Prontos por Gênero", h1_style))
    story.append(HRFlowable(width="100%", thickness=1.5, color=PRIMARY_GOLD, spaceBefore=0, spaceAfter=15))
    
    story.append(Paragraph("Fórmulas prontas para aplicar diretamente no campo <b>Style of Music</b> do Suno AI. Copie e cole:", body_style))
    
    story.append(Paragraph("1. Pop & Synthpop", h2_style))
    story.append(Paragraph("<b>POP COMERCIAL RADIOFÔNICO:</b>", body_style))
    p1 = Paragraph("modern pop, dance-pop, polished female vocals, catchy synth riffs, punchy electronic drums, driving bassline, upbeat, energetic, studio recording, 124 bpm", code_style)
    t_p1 = Table([[p1]], colWidths=[490])
    t_p1.setStyle(TableStyle([('BACKGROUND', (0,0), (-1,-1), CARD_BG), ('PADDING', (0,0), (-1,-1), 10), ('BOX', (0,0), (-1,-1), 0.5, SECONDARY_CYAN)]))
    story.append(t_p1)
    story.append(Spacer(1, 8))
    
    story.append(Paragraph("<b>SYNTHPOP RETRÔ ANOS 80:</b>", body_style))
    p2 = Paragraph("80s synthpop, retro wave, male vocals, analog synthesizers, gated reverb drums, pulsing bass, nostalgic, dark yet energetic, 118 bpm", code_style)
    t_p2 = Table([[p2]], colWidths=[490])
    t_p2.setStyle(TableStyle([('BACKGROUND', (0,0), (-1,-1), CARD_BG), ('PADDING', (0,0), (-1,-1), 10), ('BOX', (0,0), (-1,-1), 0.5, SECONDARY_CYAN)]))
    story.append(t_p2)
    
    story.append(Paragraph("2. Rock & Heavy Metal", h2_style))
    story.append(Paragraph("<b>ROCK MODERNO / ALTERNATIVO:</b>", body_style))
    p3 = Paragraph("modern rock, alternative rock, powerful male vocals, distorted electric guitars, heavy bass, tight acoustic drums, aggressive, high energy, raw studio mix, 135 bpm", code_style)
    t_p3 = Table([[p3]], colWidths=[490])
    t_p3.setStyle(TableStyle([('BACKGROUND', (0,0), (-1,-1), CARD_BG), ('PADDING', (0,0), (-1,-1), 10), ('BOX', (0,0), (-1,-1), 0.5, SECONDARY_CYAN)]))
    story.append(t_p3)
    story.append(Spacer(1, 8))
    
    story.append(Paragraph("<b>ROCK ACÚSTICO / FOLK ROCK:</b>", body_style))
    p4 = Paragraph("acoustic rock, indie folk, warm raspy male vocals, strummed acoustic guitars, Hammond organ, subtle percussion, intimate, emotional, organic sound, 90 bpm", code_style)
    t_p4 = Table([[p4]], colWidths=[490])
    t_p4.setStyle(TableStyle([('BACKGROUND', (0,0), (-1,-1), CARD_BG), ('PADDING', (0,0), (-1,-1), 10), ('BOX', (0,0), (-1,-1), 0.5, SECONDARY_CYAN)]))
    story.append(t_p4)
    story.append(PageBreak())

    # ==========================================
    # PÁGINA 8: CAPÍTULO 3 (PARTE 2)
    # ==========================================
    story.append(Paragraph("3. Sertanejo & Forró", h2_style))
    story.append(Paragraph("<b>SERTANEJO UNIVERSITÁRIO:</b>", body_style))
    p5 = Paragraph("sertanejo universitario, brazilian pop, male duet vocals, bright accordion, acoustic guitar solo, punchy bass, energetic, festive, live recording vibe, 130 bpm", code_style)
    t_p5 = Table([[p5]], colWidths=[490])
    t_p5.setStyle(TableStyle([('BACKGROUND', (0,0), (-1,-1), CARD_BG), ('PADDING', (0,0), (-1,-1), 10), ('BOX', (0,0), (-1,-1), 0.5, SECONDARY_CYAN)]))
    story.append(t_p5)
    story.append(Spacer(1, 8))
    
    story.append(Paragraph("<b>SERTANEJO SOFRÊNCIA / ROMÂNTICO:</b>", body_style))
    p6 = Paragraph("sertanejo romantico, emotional male vocal, slow accordion, nylon acoustic guitar, soft drums, melancholic, intimate, clean production, 85 bpm", code_style)
    t_p6 = Table([[p6]], colWidths=[490])
    t_p6.setStyle(TableStyle([('BACKGROUND', (0,0), (-1,-1), CARD_BG), ('PADDING', (0,0), (-1,-1), 10), ('BOX', (0,0), (-1,-1), 0.5, SECONDARY_CYAN)]))
    story.append(t_p6)
    
    story.append(Paragraph("4. Hip-Hop, Trap & Lo-Fi", h2_style))
    story.append(Paragraph("<b>TRAP MODERNO:</b>", body_style))
    p7 = Paragraph("modern trap, hard hip-hop, deep 808 sub-bass, fast hi-hats, dark synth pads, aggressive male vocals, hypnotic, moody, heavy low-end mix, 140 bpm", code_style)
    t_p7 = Table([[p7]], colWidths=[490])
    t_p7.setStyle(TableStyle([('BACKGROUND', (0,0), (-1,-1), CARD_BG), ('PADDING', (0,0), (-1,-1), 10), ('BOX', (0,0), (-1,-1), 0.5, SECONDARY_CYAN)]))
    story.append(t_p7)
    story.append(Spacer(1, 8))
    
    story.append(Paragraph("<b>LO-FI HIP-HOP (CHILL):</b>", body_style))
    p8 = Paragraph("lo-fi hip hop, chillhop, dusty vinyl crackle, mellow electric piano, relaxed drums, soft bass, laid-back, nostalgic, instrumental, 80 bpm", code_style)
    t_p8 = Table([[p8]], colWidths=[490])
    t_p8.setStyle(TableStyle([('BACKGROUND', (0,0), (-1,-1), CARD_BG), ('PADDING', (0,0), (-1,-1), 10), ('BOX', (0,0), (-1,-1), 0.5, SECONDARY_CYAN)]))
    story.append(t_p8)
    
    story.append(Spacer(1, 20))
    story.append(criar_banner_decorativo("Experimente combinar descritores de gêneros opostos (ex: lo-fi com arranjos sertanejos) para criar sonoridades autênticas e inovadoras no Suno AI.", "🎹"))
    story.append(PageBreak())

    # ==========================================
    # PÁGINA 9: CAPÍTULO 4
    # ==========================================
    story.append(Paragraph("CAPÍTULO 4", ParagraphStyle('CapTag4', parent=body_style, textColor=SECONDARY_CYAN, fontName='Helvetica-Bold')))
    story.append(Paragraph("Dicas Práticas de Mixagem e Acabamento", h1_style))
    story.append(HRFlowable(width="100%", thickness=1.5, color=PRIMARY_GOLD, spaceBefore=0, spaceAfter=15))
    
    story.append(Paragraph("O Suno AI entrega faixas prontas, mas é comum o áudio apresentar pequenas distorções. Aprenda técnicas rápidas para elevar a qualidade do arquivo final:", body_style))
    
    story.append(Paragraph("1. Corrigindo Vocais Abafados", h2_style))
    story.append(Paragraph("• <b>No Prompt:</b> Inclua descritores como <i>clean vocal mix</i> ou <i>crisp vocals</i>.", bullet_style))
    story.append(Paragraph("• <b>No Equalizador:</b> Aplique um filtro High-Pass (Passa-Altas) em torno de 80 Hz a 100 Hz para limpar o excesso de graves do vocal.", bullet_style))
    
    story.append(Paragraph("2. Separação de Stems (Vocais e Instrumentos)", h2_style))
    story.append(Paragraph("Utilize ferramentas gratuitas online (como Vocal Remover ou Moises.ai) para dividir o MP3/WAV do Suno em duas trilhas separadas: Vocal e Acompanhamento. Isso permite controlar o volume da voz independentemente.", body_style))
    
    story.append(Paragraph("3. Masterização Rápida para Plataformas", h2_style))
    story.append(Paragraph("• <b>Normalização de Loudness:</b> Ajuste o volume final para a meta padrão de <b>-14 LUFS</b> (padrão do Spotify e YouTube) usando plataformas gratuitas como BandLab Mastering.", bullet_style))
    story.append(Paragraph("• <b>Margem de Segurança:</b> Mantenha o True Peak em <b>-1.0 dB</b> para evitar distorções na conversão de áudio.", bullet_style))
    
    story.append(Spacer(1, 20))
    story.append(criar_banner_decorativo("A masterização final garante que sua música soe alta e clara em fones de ouvido, sistemas automotivos e plataformas de streaming sem distorcer.", "🔊"))
    story.append(PageBreak())

    # ==========================================
    # PÁGINA 10: BÔNUS EXCLUSIVO
    # ==========================================
    story.append(Paragraph("🎁 BÔNUS EXCLUSIVO", ParagraphStyle('BonusTag', parent=body_style, textColor=PRIMARY_GOLD, fontName='Helvetica-Bold', fontSize=16, leading=20)))
    story.append(Paragraph("Guia Rápido: Como Transformar Letras e Melodias Próprias em Arranjos Profissionais no Suno", h1_style))
    story.append(HRFlowable(width="100%", thickness=1.5, color=PRIMARY_GOLD, spaceBefore=0, spaceAfter=15))
    
    story.append(Paragraph("1. <b>Formatação de Métricas:</b> Escreva sua letra respeitando versos de 8 a 10 sílabas poéticas para evitar que a IA atropele a dicção vocal.", bullet_style))
    story.append(Paragraph("2. <b>Encaixando o Estilo Ideal:</b> Não tente forçar uma letra romântica em um estilo Trap de 150 BPM. Use a nossa biblioteca do Capítulo 3 para escolher o BPM compatível com o sentimento da sua composição.", bullet_style))
    story.append(Paragraph("3. <b>Próximo Nível (Aviso Importante):</b> Este e-book oferece os fundamentos perfeita para criar arranjos base incríveis. Para aprender a gravar sua própria voz por cima dos arranjos, ajustar afinação fina e dominar a produção avançada em softwares como Reaper ou BandLab, fique atento ao lançamento do nosso <b>Curso Completo de Produção Musical com Suno AI!</b>", bullet_style))
    
    story.append(Spacer(1, 40))
    callout_end = Paragraph("<b>Suno AI Descomplicado</b> • Todos os direitos reservados.<br/>Produzido com apoio de Inteligência Artificial para Produtores Musicais.", ParagraphStyle('CalloutEnd', parent=body_style, alignment=1, textColor=SECONDARY_CYAN, fontSize=10, leading=14))
    t_end = Table([[callout_end]], colWidths=[490])
    t_end.setStyle(TableStyle([('BACKGROUND', (0,0), (-1,-1), CARD_BG), ('PADDING', (0,0), (-1,-1), 15), ('BOX', (0,0), (-1,-1), 1, SECONDARY_CYAN)]))
    story.append(t_end)

    # Compila o arquivo PDF no disco
    doc.build(story, onFirstPage=desenhar_fundo_escuro, onLaterPages=desenhar_fundo_escuro)
    
    # ABRIR AUTOMATICAMENTE
    abrir_pdf_na_tela(output_pdf)

# --- EXECUÇÃO ---
pasta_atual = os.path.dirname(os.path.abspath(__file__)) if '__file__' in globals() else os.getcwd()
arquivo_saida = os.path.join(pasta_atual, "Suno_AI_Descomplicado.pdf")

gerar_ebook_suno(arquivo_saida)
