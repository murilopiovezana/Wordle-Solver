""" Este script realiza uma simulação de várias partidas de adivinhação de palavras para avaliar a 
eficácia de uma estratégia de palpite.

O objetivo é calcular a média de tentativas necessárias para um jogador adivinhar corretamente 
a palavra secreta em cada partida. O jogador recebe feedback em cores:
- "GREEN" para letra correta na posição certa.
- "YELLOW" para letra correta, mas na posição errada.
- "RED" para letra ausente.

O programa simula várias partidas para o mesmo jogador, 
computando a média de chutes para verificar a eficiência da estratégia implementada, 
com o objetivo de minimizar o número de tentativas até a palavra correta ser adivinhada.
"""

# Bibliotecas e módulos necessários
from utils import choose_secret_word, load_words, set_language       
from importlib import reload
import player
import random

# Verificar se o Tqdm está instalado, caso contrário, exibir mensagem de erro e encerrar o programa.
try:
    from tqdm import tqdm
except ImportError:
    print(
        "Tqdm não foi instalado. Por favor, cheque o README para mais informações ou consulte um monitor."
    )
    exit(1)

MAX_LETTERS = 5                                                                             # Máximo de letras da palavra secreta
WORDS = dict()

WORDS["pt"] = [word for word in load_words(lang="pt") if len(word) == MAX_LETTERS]         # Lista de palavras com 5 letras em português
WORDS["en"] = [word for word in load_words(lang="en") if len(word) == MAX_LETTERS]         # Lista de palavras com 5 letras em inglês
WORDS["fr"] = [word for word in load_words(lang="fr") if len(word) == MAX_LETTERS]         # Lista de palavras com 5 letras em francês
WORDS["it"] = [word for word in load_words(lang="it") if len(word) == MAX_LETTERS]         # Lista de palavras com 5 letras em italiano
WORDS["sp"] = [word for word in load_words(lang="sp") if len(word) == MAX_LETTERS]         # Lista de palavras com 5 letras em espanhol

def feedback(guess, code, words):
    """ Compara o palpite do jogador com a palavra secreta e retorna um feedback de cores.
    
    - "GREEN":   Letra correta na posição correta.
    - "YELLOW":  Letra correta na posição errada.
    - "RED":     Letra incorreta.
    
    Parâmetros:
        - guess: Palpite do jogador.
        - code: Palavra secreta escolhida pelo jogo.
    
    Retorna:
        - Lista de cores representando o feedback do palpite.
    """
    
    colors_feedback = ["DARK_GRAY" for _ in range(MAX_LETTERS)]     # Inicializa a lista de feedback 
    code = list(code)                                               # Converte string para lista
    
    # Validações: garante que o palpite seja uma string de tamanho adequado
    if type(guess) != str or len(guess) < MAX_LETTERS:
        return None
    
    # Normaliza o palpite para maiúsculas e limita o tamanho (caso o jogador envie uma palavra com mais de 5 letras)
    guess = guess.upper()[:MAX_LETTERS]
    
    # Validações: garante que o palpite esteja na lista de palavras válidas
    if guess not in words:
        return None
    
    # Verifica acertos exatos (letra e posição corretas)
    for i, letter in enumerate(guess):
        if letter == code[i]:
            colors_feedback[i] = "GREEN"
            code[i] = None
    
    # Verifica acertos parciais (letra correta em posição errada)
    for i, letter in enumerate(guess):
        if letter in code and colors_feedback[i] != "GREEN":
            colors_feedback[i] = "YELLOW"
            code[code.index(letter)] = None
            
    # Define letras incorretas como "RED"
    for i, letter in enumerate(guess):
        if letter not in code and colors_feedback[i] not in ["GREEN", "YELLOW"]:
            colors_feedback[i] = "RED"
            
    return colors_feedback
          
def main():
    """ Função principal do torneio.
    
        Simula vários jogos para calcular a média de tentativas necessárias para acertar a palavra secreta.
    """
    global WORDS
    max_games = 500                                     # Número total de jogos a serem simulados
    max_attempts = 1000                                 # Número máximo de tentativas por jogo
    sum_guesses = 0                                     # Soma total de tentativas
    
    # Listas e contadores para estatísticas
    attempts_list = []
    fails = 0
    
    # Repete o jogo 'max_games' vezes e usa o tqdm para exibir uma barra de progresso
    for _ in tqdm(range(max_games)):
        lang = random.choice(["pt", "en", "fr", "it", "sp"])    # Escolhe um idioma aleatório
        set_language(lang)                                      # Define o idioma para português
        CODE = choose_secret_word(WORDS[lang])                  # Escolhe uma palavra secreta aleatória pertencente a um idioma aleatório
        reload(player)                                          # Recarrega o módulo player para evitar problemas de cache (variável global)
        guess_hist = []                                         # Histórico de palpites
        res_hist = []                                           # Histórico de feedbacks
        attempts = 0                                            # Número de tentativas
        win = False                                             # Flag para indicar se o jogador acertou a palavra 

        # Simular o jogo até o player acertar a palavra ou atingir o número máximo de tentativas
        while attempts < max_attempts:
            res = None
            
            # Garante que o palpite seja válido
            while res is None:   
                guess = player.player(guess_hist, res_hist)
                res = feedback(guess, CODE, WORDS[lang])
                
            guess_hist.append(guess)                    # Adiciona o palpite ao histórico
            res_hist.append(res)                        # Adiciona o feedback ao histórico
            attempts += 1                               # Incrementa o número de tentativas

            # Se todas as letras estiverem corretas, encerra o jogo e armazena o número de tentativas
            if res == ["GREEN"] * 5:
                sum_guesses += attempts
                attempts_list.append(attempts)  
                win = True
                break
            
        if not win:
            sum_guesses += max_attempts
            attempts_list.append(max_attempts)
            fails += 1
    
    # cálculo da mediana, desvio padrão, mínimo, máximo
    media = sum_guesses / max_games if max_games else 0
    mediana = sorted(attempts_list)[len(attempts_list) // 2] if attempts_list else 0
    desvio_padrao = (sum((x - media) ** 2 for x in attempts_list) / len(attempts_list)) ** 0.5 if attempts_list else 0
    minimo = min(attempts_list) 
    maximo = max(attempts_list)
    
    # Mostrar os resultados
    print(f"\nTorneio finalizado!\n")
    print(f"Total de partidas simuladas: {max_games}")
    print(f"Máxima de tentativas por jogo: {max_attempts}")
    print(f"Média de tentativas: {media}")
    print(f"Mediana de tentativas: {mediana}")
    print(f"Desvio padrão: {desvio_padrao}")
    print(f"Mínimo de tentativas: {minimo}")
    print(f"Máximo de tentativas: {maximo}")
    print(f"Total de falhas: {fails}\n")

if __name__ == "__main__":
    main()  