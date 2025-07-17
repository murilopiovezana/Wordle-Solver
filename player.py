
# Nome completo do primeiro membro: Murilo Caetano Piovezana
# RA do primeiro membro: -
# Nome completo do segundo membro: Pedro Morais Leal
# RA do segundo membro: -

from typing import Callable
from utils import load_words

WORDS: list[str] = load_words()  # Carrega a lista de palavras

# Mantém apenas as palavras de 5 letras
VALID_WORDS: list[str] = [word for word in WORDS if len(word) == 5]
# Será filtrada com cada tentativa
possible_words: list[str] = VALID_WORDS.copy()

# Globais relacionadas ao algoritmo em get_next_word() que,
# quando for conveniente, escolhe uma palavra com letras distintas
# para eliminar várias possibilidades de uma só vez.
DISTINCT_THRESHOLD: int = 3
closest_result: list[str] | None = None
letters_to_try: set[str] = set()
red_count: int | None = None
last_try_was_distinct: bool = False


def get_best_word(words: list[str]) -> str:
    """
    Retorna a melhor palavra da lista a ser escolhida, com base nos
    seguintes critérios (em ordem decrescente de prioridade):

    - Maior quantidade de letras diferentes umas das outras
    (isto é, menor quantidade de repetições);

    - Maior soma de frequências posicionais das letras que compõem a palavra.
    """

    # Para cada posição, guarda um histograma com a frequência de
    # letras naquela posição, com base na lista de palavras fornecida.
    frequencies: list[dict[str, int]] = [{} for _ in range(5)]
    for word in words:
        for i in range(5):
            frequencies[i][word[i]] = frequencies[i].get(word[i], 0) + 1

    # Retorna a melhor palavra com base nos critérios citados na docstring
    return max(words, key=lambda word: (
                len(set(letter for letter in word)),
                sum(frequencies[i][word[i]] for i in range(5))
            ))


def get_distinct_word(last_word: str, red_indexes: list[int]) -> str:
    """
    Retorna a melhor palavra distinta da palavra tentada, dentre
    as palavras de 5 letras do dicionário, pelos seguintes critérios
    (em ordem decrescente de prioridade):

    - Maior quantidade de letras que não foram tentadas ainda e que são
    possibilidades dentre as palavras possíveis;

    - Maior quantidade de letras não tentadas possíveis
    que estão nas posições ainda vermelhas;

    - Maior quantidade de letras diferentes umas das outras
    (isto é, menor quantidade de repetições).
    """
    return max(VALID_WORDS, key=lambda word: (
                sum((int(letter in word) if letter not in last_word else word.count(letter) - last_word.count(letter))
                        for letter in letters_to_try),
                sum(int(word[i] in letters_to_try) for i in red_indexes),
                len(set(c for c in word)),
            ))


def get_next_word(words: list[str],
                  guess_hist: list[str], res_hist: list[list[str]]) -> str:
    """
    Decide a próxima palavra a ser tentada, geralmente a
    melhor em frequências, escolhida por `get_best_word()`.

    No caso de a maioria das letras já não estarem mais vermelhas na
    melhor tentativa mas ainda faltar muitas possibilidades para
    preencher as vermelhas restantes, será escolhida uma palavra
    distinta da última e que contenha o máximo de letras que ainda
    são possíveis de se tentar (assim, filtrando o máximo possível
    de palavras na próxima tentativa).
    """
    if not res_hist:
        return get_best_word(words)

    last_word: str = guess_hist[-1]
    last_result: list[str] = res_hist[-1]

    global letters_to_try
    global closest_result
    global red_count
    global last_try_was_distinct

    if last_result and (red_count is None or not last_try_was_distinct):
        # Salva a contagem de vermelhos da última tentativa
        # (excluindo tentativas distintas)
        red_count = last_result.count("RED")

    if last_result and red_count and red_count <= 2 and (len(possible_words) > DISTINCT_THRESHOLD * red_count):
        if closest_result is None or not last_try_was_distinct:
            # Guarda o resultado da palavra tentada mais próxima da resposta
            closest_result = last_result

        # Guarda os índices das posições em vermelho do resultado
        # mais próximo da resposta já tentado
        red_indexes = []
        for i in range(len(last_result)):
            if closest_result[i] == "RED":
                red_indexes.append(i)

        # Guarda em um conjunto as letras que ainda são possíveis de se tentar
        letters_to_try = set()
        for i in red_indexes:
            for word in possible_words:
                letters_to_try.add(word[i])

        if len(letters_to_try) > DISTINCT_THRESHOLD * red_count:
            # Se o threshold é atingido, tenta uma palavra distinta para
            # maximizar a filtragem de palavras na próxima tentativa
            last_try_was_distinct = True
            return get_distinct_word(last_word, red_indexes)

    return get_best_word(words)


def get_letter_filter(i: int, tried_letter: str, color: str, non_red: int) -> Callable:
    """
    Retorna um filtro de palavras com base na cor `color` de um índice `i`
    fornecidos, em que foi tentado a letra `tried_letter`, seguindo as regras
    do wordle para a filtragem de tal letra em tal posição.

    `non_red` é usado para saber quantas ocorrências não vermelhas da letra há
    na palavra tentada.
    """
    if color == "GREEN":
        # Se a cor é verde, mantemos apenas palavras com esta letra nesta posição
        return lambda word: word[i] == tried_letter
    elif color == "YELLOW":
        # Se a cor é amarela, mantemos apenas as palavras que NÃO possuem essa letra
        # NESSA posição e em que a letra aparece, NO MÍNIMO, `non_red` vezes.
        #
        # Se for 1, são mantidas apenas palavras em que a letra aparece ao menos uma vez,
        # se for 2, ao menos 2 vezes, e assim por diante.
        return lambda word: word[i] != tried_letter and word.count(tried_letter) >= non_red
    elif color == "RED":
        # Se a cor é vermelha, mantemos apenas as palavras que NÃO possuem essa letra
        # NESSA posição e em que a letra aparece EXATAMENTE `non_red` vezes.
        #
        # Se non_red for 0, são mantidas apenas as palavras sem a letra, já se for 1 são
        # mantidas apenas palavras em que a letra aparece uma única vez, se for 2,
        # apenas 2 vezes, e assim por diante.
        return lambda word: word[i] != tried_letter and word.count(tried_letter) == non_red
    else:
        raise ValueError


def get_filtered_words(words: list[str], guess_hist: list[str], res_hist: list[list[str]]) -> list[str]:
    """
    Filtra a lista fornecida `words` e retorna a lista filtrada de
    palavras, com base na última tentativa e no resultado dela,
    seguindo as regras do wordle.
    """
    last_word: str = guess_hist[-1]
    last_result: list[str] = res_hist[-1]

    # LEGENDA:   contagens = {letra: {cor: número de aparições}}
    counts: dict[str, dict[str, int]] = {}

    # Guarda a contagem de aparições de cada cor
    # para cada letra da palavra tentada
    for i in range(len(last_result)):
        letter: str = last_word[i]
        color: str = last_result[i]

        if letter not in counts:
            counts[letter] = {}
        counts[letter][color] = counts[letter].get(color, 0) + 1

    # Guarda todas as condições de filtro, baseado nas
    # dicas do resultado da última tentativa
    conditions: list = []
    for i in range(len(last_result)):
        letter: str = last_word[i]
        color: str = last_result[i]

        # Contagem de aparições não vermelhas da letra
        non_red: int = counts[letter].get("GREEN", 0) + counts[letter].get("YELLOW", 0)

        conditions.append(get_letter_filter(i, letter, color, non_red))

    # Inclui apenas as palavras que satisfazem todas as condições
    fitered_words: list[str] = [word for word in words if all(condition(word) for condition in conditions)]

    return fitered_words


def player(guess_hist: list[str], res_hist: list[list[str]]) -> str:
    """Função principal do jogador."""

    global possible_words

    if guess_hist:
        # Filtra a lista de palavras caso esta não seja a primeira tentativa
        possible_words = get_filtered_words(possible_words, guess_hist, res_hist)

    next_word: str = get_next_word(possible_words, guess_hist, res_hist)
    return next_word