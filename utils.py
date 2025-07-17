""" Este módulo contém funções auxiliares para o jogo de adivinhação de palavras.

As funções principais incluem:
1. `set_language`: Define o idioma a ser utilizado no jogo e permite que o jogador receba o dicionário correto.
2. `load_words`: Carrega uma lista de palavras a partir de um arquivo de texto 'words_lang.txt', 
                 processando e retornando as palavras em maiúsculas.
3. `choose_secret_word`: Escolhe aleatoriamente uma palavra secreta de 5 letras a partir da lista de palavras carregadas,
                         podendo ser personalizada com uma lista fornecida pelo usuário.

Além disso, o arquivo define um dicionário de cores (`ALL_COLORS`) utilizado para a interface do jogo e para
representar os diferentes estados do palpite (como "correto", "presente mas na posição errada", "ausente").

Essas funções ajudam a fornecer o conjunto de palavras e a lógica necessária para escolher uma palavra secreta no jogo.
"""

# Biblioteca necessária
import random

dicts = dict()   # Dicionário para armazenar as palavras carregadas de cada idioma
language = "pt"  # Idioma padrão para o jogo

# Dicionário de cores usado para definir as cores do jogo, tanto para exibição quanto para feedback ao jogador
ALL_COLORS = {
    "WHITE":  (250, 250, 255),     # cor da fonte das letras - display
    "BLACK":  (0, 0, 0),           # margens e outros detalhes - display
    "DARK_GRAY": (90, 90, 90),     # cor da caixa de texto - display
    "GREEN":  (105, 217, 88),      # cor caracter correto - feedback
    "YELLOW": (241, 206, 2),       # cor caracter presente mas na posição errada - feedback
    "RED":    (254, 61, 40)        # cor caracter errado - feedback
}

def set_language(lang = "pt"):
    """" Define o idioma a ser utilizado no jogo.
        Redefine a variável global 'language'.
    """
    global language
    language = lang

def load_words(lang = None):
    """ Carregamento do arquivo de palavras.

    Retorno
     list: Lista de palavras do arquivo 'words_lang.txt', convertidas para letras maiúsculas e sem espaços extras.
    """
    global dicts, language
    
    # Para o player carregar o mesmo dicionário do jogo
    if lang is None:
        lang = language
    
    # Evitar repetição de carregamento de palavras
    if lang in dicts:
        return dicts[lang].copy()

    filename = f"words_{lang}.txt"
    
    # Abertura do arquivo de palavras no modo leitura
    file = open(filename, "r", encoding="utf-8")
    
    # Percorrer todas as linhas do arquivo, removendo espaços extras e convertendo para maiúsculas
    with file:
        words = [line.strip().upper() for line in file.readlines()]
    
    # Fechamento do arquivo 'words_lang.txt' e adição da lista de palavras ao dicionário       
    file.close()
    dicts[lang] = words 
    
    return words

def choose_secret_word(words = None):
    """ Escolhe aleatoriamente uma palavra secreta de 5 letras a partir do arquivo de palavras.
    
    Retorno
        str: Palavra secreta escolhida aleatoriamente
    """
    # Carregar palavras do arquivo de palavras
    possible_words = [word for word in words if len(word) == 5]
    
    # Escolher uma palavra aleatória da lista filtrada
    code = random.choice(possible_words)
    
    return code