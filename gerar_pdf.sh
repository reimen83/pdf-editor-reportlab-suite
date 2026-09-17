#!/bin/bash
cd "$HOME"

# 1. Esvazia o arquivo para abrir o Nano limpo
> "$HOME/gerar_ebook.py"

# 2. Abre o Nano direto no arquivo vazio
nano "$HOME/gerar_ebook.py"

# 3. Compila o PDF assim que você salvar e fechar o Nano
if [ -s "$HOME/gerar_ebook.py" ]; then
    python3 "$HOME/gerar_ebook.py"
    if [ -f "Suno_AI_Descomplicado_Novo_Layout.pdf" ]; then
        xdg-open Suno_AI_Descomplicado_Novo_Layout.pdf &
    fi
fi
