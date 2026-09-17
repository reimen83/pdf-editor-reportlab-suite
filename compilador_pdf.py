import os
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, PageBreak, Table, TableStyle
)
from reportlab.pdfgen import canvas

# --- CORES DO MODELO VISUAL ---
NAVY_BG = colors.HexColor("#0B132B")       # Fundo azul-marinho profundo
GOLD_COLOR = colors.HexColor("#D4AF37")    # Dourado para destaques e títulos
LIGHT_GOLD = colors.HexColor("#F4E07B")    # Dourado claro para subtítulos
WHITE = colors.HexColor("#FFFFFF")         # Texto principal
MUTED_TEXT = colors.HexColor("#A0AAB8")    # Texto secundário/rodapé

# --- CANVAS CUSTOMIZADO PARA ESTILIZAÇÃO DAS PÁGINAS ---
class EbookCanvas(canvas.Canvas):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.pages = []

    def showPage(self):
        self.pages.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self.pages)
        for page in self.pages:
            self.__dict__.update(page)
            self.draw_background_and_footer(num_pages)
            super().showPage()
        super().save()

    def draw_background_and_footer(self, total_pages):
        self.saveState()
        
        # Preenche o fundo com a cor escura
        self.setFillColor(NAVY_BG)
        self.rect(0, 0, letter[0], letter[1], fill=True, stroke=False)
        
        # Capa (Página 1) não recebe rodapé/cabeçalho
        if self._pageNumber > 1:
            # Linha decorativa no topo
            self.setStrokeColor(GOLD_COLOR)
            self.setLineWidth(1)
            self.line(40, letter[1] - 40, letter[0] - 40, letter[1] - 40)
            
            # Rodapé: Título + Número de Página
            self.setFont("Helvetica", 9)
            self.setFillColor(MUTED_TEXT)
            self.drawString(40, 30, "Suno AI Descomplicado — Guia Prático e Definitivo")
            self.drawRightString(letter[0] - 40, 30, f"{self._pageNumber}")
            
            # Linha decorativa no rodapé
            self.setStrokeColor(colors.HexColor("#1C2541"))
            self.line(40, 45, letter[0] - 40, 45)
            
        self.restoreState()

def criar_ebook():
    pdf_filename = "Suno_AI_Descomplicado_Novo_Layout.pdf"
    
    # Margens do documento
    doc = SimpleDocTemplate(
        pdf_filename,
        pagesize=letter,
        leftMargin=40,
        rightMargin=40,
        topMargin=50,
        bottomMargin=60
    )

    styles = getSampleStyleSheet()

    # --- ESTILOS DE TEXTO ---
    cover_title = ParagraphStyle(
        'CoverTitle',
        fontName='Helvetica-Bold',
        fontSize=32,
        leading=38,
        textColor=GOLD_COLOR,
        alignment=1, # Centralizado
        spaceAfter=15
    )
    
    cover_subtitle = ParagraphStyle(
        'CoverSubtitle',
        fontName='Helvetica',
        fontSize=15,
        leading=20,
        textColor=WHITE,
        alignment=1,
        spaceAfter=30
    )

    h1_style = ParagraphStyle(
        'ChapterHeading',
        fontName='Helvetica-Bold',
        fontSize=20,
        leading=24,
        textColor=GOLD_COLOR,
        spaceBefore=15,
        spaceAfter=15,
        keepWithNext=True
    )

    h2_style = ParagraphStyle(
        'SectionHeading',
        fontName='Helvetica-Bold',
        fontSize=13,
        leading=17,
        textColor=LIGHT_GOLD,
        spaceBefore=12,
        spaceAfter=8,
        keepWithNext=True
    )

    body_style = ParagraphStyle(
        'BodyDark',
        fontName='Helvetica',
        fontSize=10,
        leading=15,
        textColor=WHITE,
        spaceAfter=8
    )

    bullet_style = ParagraphStyle(
        'BulletDark',
        fontName='Helvetica',
        fontSize=10,
        leading=14,
        textColor=WHITE,
        leftIndent=15,
        firstLineIndent=-10,
        spaceAfter=4
    )

    code_style = ParagraphStyle(
        'CodePrompt',
        fontName='Courier-Oblique',
        fontSize=9.5,
        leading=13,
        textColor=LIGHT_GOLD,
        backColor=colors.HexColor("#162238"),
        borderColor=GOLD_COLOR,
        borderWidth=0.5,
        borderPadding=8,
        spaceBefore=6,
        spaceAfter=10
    )

    index_title_style = ParagraphStyle(
        'IndexTitle',
        fontName='Helvetica-Bold',
        fontSize=22,
        leading=26,
        textColor=GOLD_COLOR,
        spaceAfter=20
    )

    index_item_style = ParagraphStyle(
        'IndexItem',
        fontName='Helvetica-Bold',
        fontSize=11,
        leading=16,
        textColor=WHITE
    )

    index_dots_style = ParagraphStyle(
        'IndexDots',
        fontName='Helvetica',
        fontSize=11,
        leading=16,
        textColor=MUTED_TEXT,
        alignment=2 # Direita
    )

    story = []

    # =========================================================================
    # CAPA
    # =========================================================================
    story.append(Spacer(1, 100))
    story.append(Paragraph("GUIA PRÁTICO E DEFINITIVO", ParagraphStyle('SubHeader', fontName='Helvetica-Bold', fontSize=12, textColor=LIGHT_GOLD, alignment=1, spaceAfter=20)))
    story.append(Paragraph("Suno AI Descomplicado", cover_title))
    story.append(Paragraph("Crie Suas Próprias Músicas Profissionais Sem Entender de Estúdio", cover_subtitle))
    
    story.append(Spacer(1, 40))
    
    # Caixa com destaques na capa
    box_content = [
        [Paragraph("<font color='#D4AF37'><b>O QUE VOCÊ VAI ENCONTRAR:</b></font>", body_style)],
        [Paragraph("• <b>Arquitetura de Prompts:</b> A fórmula dos 15-30 descritores", body_style)],
        [Paragraph("• <b>Controle de Estrutura:</b> Uso correto de Meta-Tags de seção", body_style)],
        [Paragraph("• <b>Biblioteca Pronta:</b> Pop, Rock, Sertanejo, Trap, Lo-Fi e mais", body_style)],
        [Paragraph("• <b>Acabamento Profissional:</b> Limpeza, mixagem e masterização", body_style)],
        [Paragraph("• <b>Bônus Exclusivo:</b> Transformando letras próprias em arranjos", body_style)]
    ]
    box_table = Table(box_content, colWidths=[480])
    box_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#131E3A")),
        ('BORDER', (0,0), (-1,-1), 1, GOLD_COLOR),
        ('PADDING', (0,0), (-1,-1), 12),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
    ]))
    story.append(box_table)
    
    story.append(Spacer(1, 60))
    story.append(Paragraph("<b>Edição 2026</b> | Licença de Uso Pessoal", ParagraphStyle('Edition', fontName='Helvetica', fontSize=10, textColor=MUTED_TEXT, alignment=1)))
    story.append(PageBreak())

    # =========================================================================
    # PÁGINA DE ÍNDICE / SUMÁRIO
    # =========================================================================
    story.append(Paragraph("ÍNDICE", index_title_style))
    story.append(Spacer(1, 10))

    index_data = [
        [Paragraph("CAPÍTULO 1: A Arquitetura do Prompt Perfeito no Suno AI", index_item_style), Paragraph(". . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 3", index_dots_style)],
        [Paragraph("CAPÍTULO 2: Estruturação Musical Dinâmica e Controle de Fluxo", index_item_style), Paragraph(". . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 5", index_dots_style)],
        [Paragraph("CAPÍTULO 3: Biblioteca de Prompts Prontos por Gênero", index_item_style), Paragraph(". . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 7", index_dots_style)],
        [Paragraph("CAPÍTULO 4: Dicas Práticas de Mixagem e Acabamento", index_item_style), Paragraph(". . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 9", index_dots_style)],
        [Paragraph("BÔNUS EXCLUSIVO: Transformando Letras em Arranjos", index_item_style), Paragraph(". . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 10", index_dots_style)],
    ]

    index_table = Table(index_data, colWidths=[360, 160])
    index_table.setStyle(TableStyle([
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('BOTTOMPADDING', (0,0), (-1,-1), 12),
    ]))
    story.append(index_table)
    story.append(PageBreak())

    # =========================================================================
    # CAPÍTULO 1
    # =========================================================================
    story.append(Paragraph("CAPÍTULO 1", ParagraphStyle('CapLabel', fontName='Helvetica-Bold', fontSize=11, textColor=LIGHT_GOLD)))
    story.append(Paragraph("A Arquitetura do Prompt Perfeito no Suno AI", h1_style))
    story.append(Paragraph("Para obter resultados profissionais no Suno AI, é preciso ir além do modo simples (Simple Mode) e assumir o controle total utilizando o <b>Custom Mode</b>.", body_style))
    
    story.append(Paragraph("1. A Regra de Ouro do Modo Customizado", h2_style))
    story.append(Paragraph("No modo padrão, a inteligência artificial decide a estrutura, o tom e os instrumentos por conta própria. No Custom Mode, você separa o comando em três campos distintos:", body_style))
    story.append(Paragraph("• <b>Style of Music (Estilo Musical):</b> Onde definimos a sonoridade, instrumentos, BPM e energia.", bullet_style))
    story.append(Paragraph("• <b>Lyrics (Letra e Marcadores):</b> Onde inserimos a estrutura da música e os comandos de transição.", bullet_style))
    story.append(Paragraph("• <b>Title (Título):</b> Apenas para identificação na sua biblioteca.", bullet_style))

    story.append(Paragraph("2. A Fórmula dos 15 a 30 Descritores (Style Prompt)", h2_style))
    story.append(Paragraph("Prompts curtos de 2 ou 3 palavras dão liberdade excessiva à IA, gerando resultados genéricos. A estrutura ideal de um comando de estilo deve conter entre 15 e 30 palavras separadas por vírgulas, divididas nas seguintes camadas:", body_style))
    
    story.append(Paragraph("<b>FÓRMULA DE CAMADAS DO STYLE PROMPT:</b>", ParagraphStyle('Sub', fontName='Helvetica-Bold', fontSize=9, textColor=LIGHT_GOLD, spaceBefore=4)))
    story.append(Paragraph("[Gênero Principal], [Subgênero], [Tipo de Vocal], [Instrumentos Principais], [Clima/Mood], [Estilo de Produção], [Tempo/BPM]", code_style))
    
    story.append(Paragraph("<b>EXEMPLO PRÁTICO DE APLICAÇÃO:</b>", ParagraphStyle('Sub2', fontName='Helvetica-Bold', fontSize=9, textColor=LIGHT_GOLD, spaceBefore=4)))
    story.append(Paragraph("modern pop, synthpop, polished male vocals, punchy electronic drums, driving bassline, energetic, uplifting, studio recording, 128 bpm", code_style))

    story.append(Paragraph("3. Guia Rápido de Parâmetros e Atributos", h2_style))
    story.append(Paragraph("Utilize estes atributos dentro do campo Style of Music para direcionar a produção:", body_style))
    story.append(Paragraph("• <b>Tempo / Ritmo:</b> slow tempo, mid-tempo, upbeat, fast, 120 BPM.", bullet_style))
    story.append(Paragraph("• <b>Qualidade Vocal:</b> raspy male vocals (vocal rasgado), ethereal female vocals (suave/etéreo), choir (coro), duet (dueto).", bullet_style))
    story.append(Paragraph("• <b>Textura e Produção:</b> lo-fi, polished (comercial), raw (ao vivo/cru), acoustic, spatial reverb.", bullet_style))
    story.append(Paragraph("• <b>Instrumentos de Destaque:</b> acoustic guitar, brass section, synth pads, sub-bass.", bullet_style))

    story.append(Paragraph("4. O Segredo dos Marcadores de Estrutura (Meta-Tags)", h2_style))
    story.append(Paragraph("Os marcadores devem ser colocados no campo Lyrics para ditar exatamente como a música progride. A IA interpreta tags entre colchetes ([ ]) como instruções de arranjo.", body_style))

    # Tabela Meta-Tags
    table_data = [
        [Paragraph("<b>Meta-Tag</b>", ParagraphStyle('TH', fontName='Helvetica-Bold', textColor=GOLD_COLOR)), Paragraph("<b>Função no Arranjo</b>", ParagraphStyle('TH2', fontName='Helvetica-Bold', textColor=GOLD_COLOR))],
        [Paragraph("[Intro]", body_style), Paragraph("Define o início instrumental ou introdução da faixa.", body_style)],
        [Paragraph("[Verse]", body_style), Paragraph("Indica o verso (narrativa principal da música).", body_style)],
        [Paragraph("[Chorus]", body_style), Paragraph("Refrão (momento de maior energia e gancho).", body_style)],
        [Paragraph("[Bridge]", body_style), Paragraph("Ponte (mudança de melodia ou ritmo antes do refrão final).", body_style)],
        [Paragraph("[Guitar Solo]", body_style), Paragraph("Força uma pausa vocal e entra com solo de guitarra.", body_style)],
        [Paragraph("[Outro] / [Fade Out]", body_style), Paragraph("Encerramento gradual da faixa até o silêncio.", body_style)]
    ]
    meta_table = Table(table_data, colWidths=[150, 370])
    meta_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#162238")),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#2A3A5E")),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('PADDING', (0,0), (-1,-1), 6),
    ]))
    story.append(meta_table)

    story.append(Paragraph("5. Exemplo Completo de Aplicação", h2_style))
    story.append(Paragraph("<b>CAMPO: STYLE OF MUSIC</b>", ParagraphStyle('Sub3', fontName='Helvetica-Bold', fontSize=9, textColor=LIGHT_GOLD)))
    story.append(Paragraph("acoustic pop, indie folk, warm female vocals, fingerpicking acoustic guitar, soft percussion, intimate, nostalgic, organic mix, 95 bpm", code_style))
    
    story.append(Paragraph("<b>CAMPO: LYRICS</b>", ParagraphStyle('Sub4', fontName='Helvetica-Bold', fontSize=9, textColor=LIGHT_GOLD)))
    story.append(Paragraph("[Intro]<br/>(Violão acústico dedilhado suave)<br/><br/>[Verse 1]<br/>Caminhando pelas ruas ao anoitecer<br/>O vento frio traz lembranças de você<br/>As luzes da cidade começam a acender<br/>E eu ainda tentando te esquecer<br/><br/>[Chorus]<br/>E o tempo passa mas nada mudou<br/>Ainda guardo o verso que você deixou<br/>Nessa canção que o vento levou<br/><br/>[Instrumental Solo]<br/><br/>[Outro]<br/>[Fade Out]", code_style))

    story.append(PageBreak())

    # =========================================================================
    # CAPÍTULO 2
    # =========================================================================
    story.append(Paragraph("CAPÍTULO 2", ParagraphStyle('CapLabel2', fontName='Helvetica-Bold', fontSize=11, textColor=LIGHT_GOLD)))
    story.append(Paragraph("Estruturação Musical Dinâmica e Controle de Fluxo", h1_style))
    story.append(Paragraph("Saber escrever bons prompts não basta se a música não tiver uma progressão natural. O maior erro no Suno AI é deixar a música repetitiva. Neste capítulo, você aprenderá a estruturar sua faixa com controle profissional de dinâmica.", body_style))

    story.append(Paragraph("1. A Anatomia da Música Comercial", h2_style))
    story.append(Paragraph("A maioria dos sucessos comerciais segue uma estrutura testada e aprovada para prender a atenção do ouvinte do início ao fim:", body_style))
    
    seq_items = [
        "1. <b>[Intro]</b> (10-15s) - Tema instrumental principal.",
        "2. <b>[Verse 1]</b> - Início da história, energia mais baixa.",
        "3. <b>[Pre-Chorus]</b> - Aumento gradual de energia.",
        "4. <b>[Chorus]</b> - Ponto alto da música (refrão chiclete).",
        "5. <b>[Verse 2]</b> - Mantém o interesse com variação no arranjo.",
        "6. <b>[Chorus]</b> - Retorno ao refrão.",
        "7. <b>[Bridge]</b> - Mudança de tom, melodia ou ritmo (quebra de expectativa).",
        "8. <b>[Guitar Solo / Instrumental Break]</b> - Destaque instrumental.",
        "9. <b>[Chorus]</b> - Refrão final com máxima intensidade.",
        "10. <b>[Outro/Fade Out]</b> - Encerramento da faixa."
    ]
    for item in seq_items:
        story.append(Paragraph(item, bullet_style))

    story.append(Paragraph("2. Como Usar o Pre-Chorus e o Bridge para Gerar Tensão", h2_style))
    story.append(Paragraph("Sem tensão e alívio, a música se torna monótona.", body_style))
    story.append(Paragraph("• <b>[Pre-Chorus] (Pré-Refrão):</b> Serve para criar expectativa. Insira frases mais curtas ou ritmo de bateria acelerado.", bullet_style))
    story.append(Paragraph("• <b>[Bridge] (Ponte):</b> Deve ser completamente diferente do resto da música. Se a música for rápida, diminua o ritmo na ponte. Se for calma, aumente a intensidade.", bullet_style))

    story.append(Paragraph("3. Comandos Avançados de Dinâmica Vocal e Instrumental", h2_style))
    story.append(Paragraph("Você pode dar ordens específicas à IA no meio da letra utilizando parênteses ( ) ou colchetes [ ]:", body_style))
    story.append(Paragraph("• <b>[Build Up]:</b> Usado antes do refrão para aumentar a velocidade da bateria ou intensidade.", bullet_style))
    story.append(Paragraph("• <b>[Soft Vocals]:</b> Força o vocalista a cantar mais suavemente.", bullet_style))
    story.append(Paragraph("• <b>[Powerful Vocals]:</b> Força um vocal potente e rasgado no refrão.", bullet_style))
    story.append(Paragraph("• <b>[Silence] ou [Stop]:</b> Para todos os instrumentos por 1 a 2 segundos antes do impacto do refrão.", bullet_style))

    story.append(Paragraph("4. Estendendo e Continuando Faixas (Recurso Extend)", h2_style))
    story.append(Paragraph("Para construir músicas completas sem perdas de qualidade:", body_style))
    story.append(Paragraph("1. Escolha a melhor geração que parou em um ponto lógico (ex: no final do primeiro refrão).", bullet_style))
    story.append(Paragraph("2. Clique no botão <b>Extend</b>.", bullet_style))
    story.append(Paragraph("3. No campo <b>Extend From</b>, defina o segundo exato do corte (ex: 01:45).", bullet_style))
    story.append(Paragraph("4. No campo <b>Lyrics</b>, remova o que já foi cantado e cole apenas o restante da estrutura.", bullet_style))
    story.append(Paragraph("5. Após gerar, use a opção <b>Get Whole Song</b> para unir as partes em uma única faixa.", bullet_style))

    story.append(PageBreak())

    # =========================================================================
    # CAPÍTULO 3
    # =========================================================================
    story.append(Paragraph("CAPÍTULO 3", ParagraphStyle('CapLabel3', fontName='Helvetica-Bold', fontSize=11, textColor=LIGHT_GOLD)))
    story.append(Paragraph("Biblioteca de Prompts Prontos por Gênero", h1_style))
    story.append(Paragraph("Fórmulas prontas para aplicar diretamente no campo Style of Music do Suno AI. Copie e cole:", body_style))

    story.append(Paragraph("1. Pop & Synthpop", h2_style))
    story.append(Paragraph("<b>POP COMERCIAL RADIOFÔNICO:</b>", ParagraphStyle('P1', fontName='Helvetica-Bold', fontSize=9, textColor=LIGHT_GOLD)))
    story.append(Paragraph("modern pop, dance-pop, polished female vocals, catchy synth riffs, punchy electronic drums, driving bassline, upbeat, energetic, studio recording, 124 bpm", code_style))
    story.append(Paragraph("<b>SYNTHPOP RETRÔ ANOS 80:</b>", ParagraphStyle('P2', fontName='Helvetica-Bold', fontSize=9, textColor=LIGHT_GOLD)))
    story.append(Paragraph("80s synthpop, retro wave, male vocals, analog synthesizers, gated reverb drums, pulsing bass, nostalgic, dark yet energetic, 118 bpm", code_style))

    story.append(Paragraph("2. Rock & Heavy Metal", h2_style))
    story.append(Paragraph("<b>ROCK MODERNO / ALTERNATIVO:</b>", ParagraphStyle('R1', fontName='Helvetica-Bold', fontSize=9, textColor=LIGHT_GOLD)))
    story.append(Paragraph("modern rock, alternative rock, powerful male vocals, distorted electric guitars, heavy bass, tight acoustic drums, aggressive, high energy, raw studio mix, 135 bpm", code_style))
    story.append(Paragraph("<b>ROCK ACÚSTICO / FOLK ROCK:</b>", ParagraphStyle('R2', fontName='Helvetica-Bold', fontSize=9, textColor=LIGHT_GOLD)))
    story.append(Paragraph("acoustic rock, indie folk, warm raspy male vocals, strummed acoustic guitars, Hammond organ, subtle percussion, intimate, emotional, organic sound, 90 bpm", code_style))

    story.append(Paragraph("3. Sertanejo & Forró", h2_style))
    story.append(Paragraph("<b>SERTANEJO UNIVERSITÁRIO:</b>", ParagraphStyle('S1', fontName='Helvetica-Bold', fontSize=9, textColor=LIGHT_GOLD)))
    story.append(Paragraph("sertanejo universitario, brazilian pop, male duet vocals, bright accordion, acoustic guitar solo, punchy bass, energetic, festive, live recording vibe, 130 bpm", code_style))
    story.append(Paragraph("<b>SERTANEJO SOFRÊNCIA / ROMÂNTICO:</b>", ParagraphStyle('S2', fontName='Helvetica-Bold', fontSize=9, textColor=LIGHT_GOLD)))
    story.append(Paragraph("sertanejo romantico, emotional male vocal, slow accordion, nylon acoustic guitar, soft drums, melancholic, intimate, clean production, 85 bpm", code_style))

    story.append(Paragraph("4. Hip-Hop, Trap & Lo-Fi", h2_style))
    story.append(Paragraph("<b>TRAP MODERNO:</b>", ParagraphStyle('H1', fontName='Helvetica-Bold', fontSize=9, textColor=LIGHT_GOLD)))
    story.append(Paragraph("modern trap, hard hip-hop, deep 808 sub-bass, fast hi-hats, dark synth pads, aggressive male vocals, hypnotic, moody, heavy low-end mix, 140 bpm", code_style))
    story.append(Paragraph("<b>LO-FI HIP-HOP (CHILL):</b>", ParagraphStyle('H2', fontName='Helvetica-Bold', fontSize=9, textColor=LIGHT_GOLD)))
    story.append(Paragraph("lo-fi hip hop, chillhop, dusty vinyl crackle, mellow electric piano, relaxed drums, soft bass, laid-back, nostalgic, instrumental, 80 bpm", code_style))

    story.append(PageBreak())

    # =========================================================================
    # CAPÍTULO 4
    # =========================================================================
    story.append(Paragraph("CAPÍTULO 4", ParagraphStyle('CapLabel4', fontName='Helvetica-Bold', fontSize=11, textColor=LIGHT_GOLD)))
    story.append(Paragraph("Dicas Práticas de Mixagem e Acabamento", h1_style))
    story.append(Paragraph("O Suno AI entrega faixas prontas, mas é comum o áudio apresentar pequenas distorções. Aprenda técnicas rápidas para elevar a qualidade do arquivo final:", body_style))

    story.append(Paragraph("1. Corrigindo Vocais Abafados", h2_style))
    story.append(Paragraph("• <b>No Prompt:</b> Inclua descritores como <i>clean vocal mix</i> ou <i>crisp vocals</i>.", bullet_style))
    story.append(Paragraph("• <b>No Equalizador:</b> Aplique um filtro High-Pass (Passa-Altas) em torno de 80 Hz a 100 Hz para limpar o excesso de graves do vocal.", bullet_style))

    story.append(Paragraph("2. Separação de Stems (Vocais e Instrumentos)", h2_style))
    story.append(Paragraph("Utilize ferramentas gratuitas online (como Vocal Remover ou Moises.ai) para dividir o MP3/WAV do Suno em duas trilhas separadas: Vocal e Acompanhamento. Isso permite controlar o volume da voz independentemente.", body_style))

    story.append(Paragraph("3. Masterização Rápida para Plataformas", h2_style))
    story.append(Paragraph("• <b>Normalização de Loudness:</b> Ajuste o volume final para a meta padrão de -14 LUFS (padrão do Spotify e YouTube) usando plataformas gratuitas como BandLab Mastering.", bullet_style))
    story.append(Paragraph("• <b>Margem de Segurança:</b> Mantenha o True Peak em -1.0 dB para evitar distorções na conversão.", bullet_style))

    story.append(Spacer(1, 15))

    # =========================================================================
    # BÔNUS EXCLUSIVO
    # =========================================================================
    story.append(Paragraph("BÔNUS EXCLUSIVO", ParagraphStyle('BonusLabel', fontName='Helvetica-Bold', fontSize=11, textColor=GOLD_COLOR)))
    story.append(Paragraph("Guia Rápido: Como Transformar Letras e Melodias Próprias em Arranjos Profissionais no Suno", h1_style))

    story.append(Paragraph("1. <b>Formatação de Métricas:</b> Escreva sua letra respeitando versos de 8 a 10 sílabas poéticas para evitar que a IA atropele a dicção vocal.", bullet_style))
    story.append(Paragraph("2. <b>Encaixando o Estilo Ideal:</b> Não tente forçar uma letra romântica em um estilo Trap de 150 BPM. Use a nossa biblioteca do Capítulo 3 para escolher o BPM compatível com o sentimento da sua composição.", bullet_style))
    story.append(Paragraph("3. <b>Próximo Nível (Aviso Importante):</b> Este e-book oferece os fundamentos perfeitos para criar arranjos base incríveis. Para aprender a gravar sua própria voz por cima dos arranjos, ajustar afinação fina e dominar a produção avançada em softwares como Reaper ou Ableton, fique atento ao lançamento do nosso <i>Curso Completo de Produção Musical com Suno AI</i>!", bullet_style))

    # Gerar o PDF
    doc.build(story, canvasmaker=EbookCanvas)
    return pdf_filename

if __name__ == "__main__":
    pdf_path = criar_ebook()
    
    # Abre o PDF automaticamente no visualizador do Linux logo após a compilação
    if os.path.exists(pdf_path):
        os.system(f'xdg-open "{pdf_path}" &')
