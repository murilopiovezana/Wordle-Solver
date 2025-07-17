""" Arquivo responsável pela interface gráfica do jogo e inicialização do mesmo.

    Este script é a implementação principal da interface gráfica do jogo, utilizando a biblioteca Pygame. 
    O jogo é uma versão do Wordle, onde o jogador deve adivinhar uma palavra secreta composta por 5 letras. 
    A interface permite ao jogador interagir com o jogo por meio de entradas de teclado, e o feedback das tentativas
    é exibido em cores (verde, amarelo, vermelho e cinza) para indicar a proximidade da palavra correta.

    A estrutura do código está dividida entre a inicialização do jogo, o controle dos eventos de entrada do jogador, 
    a lógica de verificação das palavras tentadas, a atualização da interface e 
    a automatização de jogadas de um jogador automático.

    As principais funções do código incluem:
    - `draw_grid`: Responsável por desenhar a grade do jogo na tela, exibindo as tentativas feitas, as palavras e os feedbacks de cores.
    - `events`: Processa os eventos do jogo, como a entrada de teclas pelo jogador (letras, backspace, setas de direção, enter e espaço para pausar).
    - `write_guess`: Escreve a palavra tentativa na grade do jogo.
    - `automatizar`: Função que simula a jogada de um jogador automático, inserindo uma palavra e verificando se está correta.
    - `check_word`: Verifica a palavra inserida pelo jogador e ajusta as cores das letras com base no feedback (verde para correto, amarelo para letra correta mas posição errada, vermelho para letra incorreta).
    - `draw_win`: Exibe a tela de vitória quando o jogador adivinha a palavra corretamente, mostrando o número de tentativas feitas.
    - `game`: Função principal do jogo que organiza o loop de execução, processando eventos, desenhando a interface e verificando se o jogador venceu ou está pausado.

    O código também inclui a definição de algumas constantes, como a largura e altura da janela, 
    o tamanho da grade de jogo, a fonte a ser utilizada e a palavra secreta a ser adivinhada.

    Além disso, o código permite que o jogo seja pausado ao pressionar a tecla espaço, 
    e o jogador pode navegar pelas células da grade utilizando as setas de direção.
"""


# Bibliotecas necessárias
from utils import ALL_COLORS, choose_secret_word, load_words, set_language
import argparse
import sys

# Verificar se o Pygame está instalado, caso contrário, exibir mensagem de erro e encerrar o programa.
try:
    import pygame
except ImportError:
    print(
        "Pygame não foi instalado. Por favor, cheque o README para mais informações ou consulte um monitor."
    )
    exit(1)

def parse_arguments():
    """Configura o argparse para receber o idioma do dicionário e o modo do jogo."""
    parser = argparse.ArgumentParser(
        description=(
            "Jogo de adivinhação de palavras. Escolha o idioma do dicionário e o modo do jogo.\n\n"
            "Uso básico:\n"
            "  python game.py --lang pt                (Modo manual em português)\n"
            "  python game.py --lang en --auto         (Modo automático em inglês)\n"
        ),
        formatter_class=argparse.RawTextHelpFormatter
    )

    # Argumento para escolher o idioma
    parser.add_argument(
        "--lang", 
        type=str, 
        choices=["pt", "en", "sp", "fr", "it"], 
        default="pt", 
        help="Idiomas do dicionário disponíveis: 'pt' (português), 'en' (inglês), 'sp' (espanhol), 'fr' (francês), 'it' (italiano). \nPadrão: 'pt'."
    )

    # Argumento booleano para o modo automático
    parser.add_argument(
        "--auto", 
        action="store_true", 
        help="Ativa o modo automático do jogo. Caso omitido, o modo manual será utilizado."
    )
    
    # Exibe a ajuda e encerra o programa se não houver argumentos válidos
    if len(sys.argv) == 0:
        parser.print_help()
        sys.exit(1)
    
    return parser.parse_args() 

# Chama a função para analisar os argumentos de linha de comando
args = parse_arguments()                                

# Constantes do jogo
WIDTH, HEIGHT = 400, 500                                # Largura e altura da tela
GRID_SIZE = 5                                           # Tamanho da matriz do jogo (palavra com 5 letras)                   
FONT_SIZE = 40                                          # Tamanho da fonte das letras
CELL_SIZE = 50                                          # Tamanho da célula da matriz para desenhar na tela
MARGIN = 10                                             # Margem entre as células que serão desenhadas na tela
set_language(args.lang)                                 # Define o idioma do dicionário com base no argumento passado
WORDS = load_words(lang = args.lang)                    # Carrega todas as palavras do arquivo do idioma escolhido
CODE = choose_secret_word(WORDS)                        # Palavra secreta escolhida pelo computador com base na lista de palavras do idioma selecionado
CUSTOM_TIMER_EVENT = pygame.USEREVENT + 1               # Evento customizado para pausar o jogo
from player import player

# Inicialização das variáveis globais do jogo
wait = 0                                                # Contador para esperar um tempo antes de automatizar a jogada
attempts = 1                                            # Número de tentativas (esta variável será incrementada a cada nova tentativa)
running = True                                          # Variável para controlar o loop principal do jogo
paused = False                                          # Variável para controlar o pause do jogo
win = False                                             # Variável para controlar se o jogador venceu o jogo ou não     
n_guesses = 0                                           # Número de tentativas do jogador
history_guesses = []                                    # Histórico de palavras inseridas pelo jogador
history_results = []                                    # Histórico de resultados (cores) das palavras inseridas pelo jogador

# Criação da janela e definição do título
pygame.init()                                           # Inicialização do Pygame
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))       # Criação da janela do jogo           
pygame.display.set_caption("Adivinha a Palavra!")       # Título da janela
font = pygame.font.Font(None, FONT_SIZE)                # Fonte utilizada para desenhar as letras na tela

# Inicialização das matrizes (5 colunas e a quantidade de linhas vai aumentando conforme as tentativas)
colors = [[ALL_COLORS["DARK_GRAY"] for _ in range(GRID_SIZE)] for _ in range(attempts)]     # Matriz de cores para a grade inicial do jogo
grid = [["" for _ in range(GRID_SIZE)] for _ in range(attempts)]                            # Matriz de letras para a grade inicial do jogo

def draw_grid(position):
    """ Função responsável por desenhar a grade do jogo na tela.
    
        Parâmetros:
            position (list): Contém as coordenadas atuais da grade.
                - position[0]: linha atual
                - position[1]: coluna atual
                - position[2]: posição da câmera na tela
        
        Retorna:
            A grade desenhada na tela.
    """
    
    # Preenche a tela com a cor de fundo branca
    SCREEN.fill(ALL_COLORS["WHITE"])           
    
    # Percorre cada célula da grade 
    for row in range(attempts):
        for col in range(GRID_SIZE):
            
            # Calcula as coordenadas (x, y) da célula na tela
            x = col * (CELL_SIZE + MARGIN) + 50
            y = row * (CELL_SIZE + MARGIN) + 50 + position[2]
            
            # Desenha a célula preenchida com sua respectiva cor
            pygame.draw.rect(SCREEN, colors[row][col], (x, y, CELL_SIZE, CELL_SIZE))
            
            # Desenha a borda da célula de preto
            pygame.draw.rect(SCREEN, ALL_COLORS["BLACK"], (x, y, CELL_SIZE, CELL_SIZE), 2)
            
            # Se a célula contiver uma letra, renderiza e desenha na tela
            if grid[row][col]:
                text = font.render(grid[row][col], True, ALL_COLORS["WHITE"])
                SCREEN.blit(text, (x+15,y+5))
                
            # Se a célula for a posição atual do cursor, desenha um sublinhado
            if row == position[0] and col == position[1]:
                pygame.draw.line(
                    SCREEN, ALL_COLORS["BLACK"], 
                    (x + 5, y + CELL_SIZE - 5), 
                    (x + CELL_SIZE - 5, y + CELL_SIZE - 5), 
                    2
                )

def draw_win(position):
    """ Função responsável por exibir a tela de vitória quando o jogador acerta a palavra secreta.

        Esta função é chamada quando o jogador vence o jogo, ou seja, quando adivinha corretamente a palavra secreta. 
        Ela desenha uma mensagem de vitória na tela, mostrando o número de tentativas feitas até a conquista.

        Parâmetros:
        - position (tupla): Contém as coordenadas da posição da câmera (position (x, y, camera)), 
        sendo que o índice [2] da tupla é utilizado para ajustar a posição vertical da tela, 
        proporcionando um efeito de rolagem (scroll) da tela.

        Retorna:
        - A tela de vitória desenhada na tela, exibindo o número de tentativas feitas até a vitória.
    """

    global paused
    
    # Pausa o jogo e corrige a fonte
    paused = True
    camera = position[2]
    new_font_size = 24
    font = pygame.font.Font(None, new_font_size)
    
    # Desenhar um retângulo cinza escuro na tela e um retângulo preto ao redor como borda
    pygame.draw.rect(SCREEN, ALL_COLORS["DARK_GRAY"], (50, 50+camera, 290, 50))
    pygame.draw.rect(SCREEN, ALL_COLORS["BLACK"], (50, 50+camera, 290, 50), 2)
    
    # Escrever o texto de vitória neste retângulo
    win_text = font.render("Você venceu em " + str(attempts-1) + " tentativas!", True, ALL_COLORS["WHITE"])
    win_text_rect = win_text.get_rect(center=(50 + 290 // 2, 75 + camera))
    
    # Desenhar o texto na tela
    SCREEN.blit(win_text, win_text_rect)

def write_guess(guess):
    """ Função responsável por escrever a palavra inserida pelo jogador na tela.
    
        Parâmetros:
            guess (str): Palavra inserida pelo jogador
            
        Retorno:
            Atualiza a grade com palavra digitada.
    """
    
    # Verifica se o input é uma string, caso contrário, retorna None
    if type(guess) == str:
        guess = guess.upper()                   # Converte a palavra para maiúscula
    else:
        return None
    
    # Preenche a grade com a palavra digitada, respeitando o tamanho da grade
    for i in range(GRID_SIZE):
        if i >= len(guess):                     # Se a palavra for menor que a grade, interrompe
            break
        grid[0][i] = guess[i]                   # Insere a letra na posição correspondente

def auto_play():
    """ Função que automatiza a jogada do jogador automático
    
        Chama a função do player, insere a palavra na grade e verifica se está correta
    """
    global grid, colors, args
    
    guess_player = player(history_guesses,history_results)          # Obtém a palavra do player
    # Verificar a flag "auto" para validar se o jogador é automático ou não
    if args.auto == False:
        guess_player = ""                                       # Se o jogo não for automático, a palavra é vazia
    write_guess(guess_player)                                   # Insere a palavra na grade
    check_word(guess_player)                                    # Verifica se a palavra está correta

def check_word(guess):
    """ Função responsável por verificar a palavra inserida pelo jogador e colorir as letras correspondente.

        Parâmetros:
            guess (str): Palavra inserida pelo jogador
            
        Retorno:
            list: Lista de cores correspondentes ao feedback de cada letra
    """
    
    global win, attempts, n_guesses, grid, colors, history_guesses, history_results
    
    # Converte a palavra para maíuscula se for uma string, caso contrário, retorna None
    if type(guess) == str:
        guess = guess.upper()
    else:
        return None
    
    # Se a palavra tem o tamanho correto e está na lista de palavras válidas, processa a jogada
    if len(guess) == GRID_SIZE and guess in WORDS:
        
        colors_result = ["DARK_GRAY" for _ in range(GRID_SIZE)]         # Inicializa a lista de cores com a cor padrão
        n_guesses += 1                                                  # Incrementa o número de tentativas
        
        # Se a palavra estiver correta, o jogador vence (ativa a flag "win")
        if guess == CODE:
            print(f"Você venceu em {n_guesses} chutes!")
            win = True
            colors_result = ["GREEN" for _ in range(GRID_SIZE)]     # Marca todas as letras como corretas
            
        else:
            correct_letters = list(CODE)                            # Converte a palavra correta em uma lista de caracteres
            guessed_letters = list(guess)                           # Converte a palavra digitada em uma lista de caracteres
            
            # Primeiro, marca os caracteres corretos na posição certa (verde)
            for i in range(GRID_SIZE):
                if guessed_letters[i] == correct_letters[i]:
                    colors_result[i] = "GREEN"
                    correct_letters[i] = None                       # Marca como utilizada
            
            # Depois, marca as letras que existem na palavra, mas estão na posição errada (amarelo)
            for i in range(GRID_SIZE):
                if colors_result[i] != "GREEN" and guessed_letters[i] in correct_letters:
                    colors_result[i] = "YELLOW"
                    correct_letters[correct_letters.index(guessed_letters[i])] = None  # Marca como utilizada
            
            # Por fim, as letras que não existem na palavra ficam vermelhas
            for i in range(GRID_SIZE):
                if colors_result[i] not in ["GREEN", "YELLOW"]:
                    colors_result[i] = "RED"
        
        # Adiciona uma nova linha vazia no topo da grade para a próxima tentativa
        grid.insert(0,["" for _ in range(GRID_SIZE)])
        colors.insert(0,[ALL_COLORS["DARK_GRAY"] for _ in range(GRID_SIZE)])
        
        attempts += 1                                               # Incrementa o número de tentativas

        # Atualiza a linha anterior com as cores correspondentes ao feedback
        for i in range(GRID_SIZE):
            colors[1][i] = ALL_COLORS[colors_result[i]]
            
        # Adiciona a tentativa e seu respectivo resultado ao histórico do jogador
        history_guesses.append(guess)
        history_results.append(colors_result)
        
        return colors_result

def events(position):
    """ Função responsável por capturar e processar os eventos do jogo.
    
        Parâmetros:
            position (list): Contém as coordenadas atuais da grade.
                - position[0]: linha atual
                - position[1]: coluna atual
                - position[2]: posição da câmera na tela
            
        Retorna:
            Atualiza a posição do cursor e processa as interações do jogador.
    """
    
    global running, win, paused
    
    # Percorre a fila de eventos do pygame
    for event in pygame.event.get():
        
        # Se o evento for fechamento de tela, encerra o jogo
        if event.type == pygame.QUIT:
            running = False
            win = False
                    
        # Captura os eventos de pressionamento de teclas
        # Se o jogo estiver pausado, apenas a tecla SPACE e setas superior e inferior são permitidas
        elif event.type == pygame.KEYDOWN:
            
            # Se for uma tecla de A a Z e houver espaço na grade, adiciona a letra
            if win == False and paused==False and pygame.K_a <= event.key <= pygame.K_z and position[1] < GRID_SIZE:
                grid[position[0]][position[1]] = chr(event.key).upper()
                position[1] +=1
                position[2] = 0                         # Reseta o deslocamento da câmera
                
            # Se for a tecla BACKSPACE, apaga a última letra digitada
            elif win == False and paused==False and event.key == pygame.K_BACKSPACE:
                if position[1] < GRID_SIZE and grid[position[0]][position[1]] != '':
                    grid[position[0]][position[1]] = ''
                    continue                            # Evita mover o cursor caso delete uma letra no meio        
                position[1] = max(position[1] - 1, 0)   # Move o cursor para trás
                grid[position[0]][position[1]] = ""
                position[2] = 0                         # Reseta o deslocamento da câmera
                
            # Movimento o cursor para a esquerda, se possível
            elif win == False and paused==False and event.key == pygame.K_LEFT and position[1] > 0:
                position[1] -= 1
                position[2] = 0
                
            # Movimenta o cursos para a direita, se possível
            elif win == False and paused==False and event.key == pygame.K_RIGHT and position[1] < GRID_SIZE - 1:
                position[1] += 1
                position[2] = 0
                
            # Movimenta a "câmera" para cima (simula rolagem)
            elif event.key == pygame.K_UP:
                position[2] = min(position[2] + (CELL_SIZE + MARGIN),0)
                
            # Movimenta a "câmera" para baixo, respeitando os limites da grade
            elif event.key == pygame.K_DOWN:
                if attempts + position[2] / (CELL_SIZE + MARGIN) > 7 :
                    position[2] = max(position[2] -(CELL_SIZE + MARGIN), -(CELL_SIZE + MARGIN) * (attempts))
                    
            # Se for a tecla ENTER, verifica a palavra digitada
            elif win == False and paused==False and event.key == pygame.K_RETURN:
                writen_word = ''.join([grid[0][i] for i in range(GRID_SIZE)])
                check_word(writen_word)                 # Verifica a palavra digitada
                
                # Reseta a posição do cursor após validar a palavra
                position[1] = 0
                position[2] = 0
                
            # Se for a tecla SPACE, pausa o jogo
            elif event.key == pygame.K_SPACE:
                pygame.time.set_timer(CUSTOM_TIMER_EVENT, 3000)
                if paused:
                    paused = False
                    pygame.display.set_caption("Adivinha a Palavra!")
                else:
                    paused = True
                    pygame.display.set_caption("Paused")
    
def game():
    """ Função principal do jogo.
    
        Responsável por rodar o loop principal do jogo, processando eventos, desenhando a tela
        e verificando a condição de vitória
    """ 
    global running, win, wait, paused
       
    # Define a velocidade que o jogo estará rodando
    speed = 60                      # Valor em frames por segundo 
    clock = pygame.time.Clock()     # Relógio para controlar a taxa de atualização do jogo
    
    # Posição atual selecionada: [linha, coluna, posição camera]
    position = [0,0,0]              
            
    # Loop principal do jogo    
    while running:
        events(position)            # Processa os eventos do jogo (entrada do usuário)
        clock.tick(speed)           # Controla a taxa de atualização do jogo
        wait += 1                   # Contador para esperar um tempo antes de automatizar a jogada
        
        draw_grid(position)         # Desenha a grade do jogo na tela com a posição atual
            
        # Automatiza a jogada caso não esteja pausado e o tempo de espera seja maior que 15 frames (forma de visualizar mais devagar os chutes na tela)
        if paused == False and wait >= 15 and win == False:
            wait = 0
            # Automatizar a jogada do player, se player.py estiver implementado, senão roda o jogo normalmente
            auto_play()               
        
        # Caso o jogador vença, exibe a tela de vitória
        if win:                 
            draw_win(position)
        
        # Atualiza a tela
        pygame.display.flip()
     
# Inicialização do Jogo
# Esse bloco garante que o jogo só será executado se este arquivo for rodado diretamente,
# evitando sua execução caso seja importado como módulo em outro script.
if __name__ == "__main__":
    game()  
