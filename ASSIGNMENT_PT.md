# 🟩 Wordle MC102 🟨

Este projeto faz parte da disciplina **MC102-2025** e tem **peso 3**.

O projeto deve, obrigatoramente, ser feito em **dupla**. Caso não você não consiga um parceiro, entre em contato.

Apenas um dos membros deve enviar o arquivo `player.py` (e apenas este) pelo **Google Classroom**, e o outro deve fazer um **comentário particular** na atividade do Google Classroom avisando de qual dupla faz parte (para ficar registrada a concordância). Caso você entregue outros arquivos além do `player.py`, eles serão ignorados.

**Não é permitido** alterar **nenhum arquivo** além de `player.py`. Todos os demais (`game.py`, `tournament.py`, `utils.py`, etc.) devem ser mantidos exatamente como fornecidos. Note que nós receberemos apenas o `player.py` e usaremos os outros arquivos originais para rodar o seu código, ou seja, se você alterar eles na sua máquina, isso não terá efeito na correção. 

## 📌 Descrição

Este projeto é inspirado no jogo Wordle. Este jogo consiste em adivinhar uma palavra de **cinco letras** a partir de tentativas sucessivas, com base no feedback fornecido pelo sistema. A função `player()` será responsável por gerar os palpites automaticamente, utilizando informações das tentativas anteriores. 

Para mais detalhes acesse os seguintes sites: [Referência Wordle](https://www.nytimes.com/games/wordle/index.html) e [Term.ooo](https://term.ooo/).

### Observação Importante Sobre a Palavra

- A **palavra secreta** será escolhida aleatoriamente dentro de um dos dicionários (pt, en, sp, it e fr).  
- **Não consideramos acentos e cedilha**: todas as palavras foram convertidas para maiúsculas e sem acentuação.  
- Não é permitido “inventar” palavras fora do dicionário a qual a palavra secreta pertence.

## 🎯 Regras do Jogo (Modo Manual)

No modo manual, o jogador deve inserir os palpites pelo teclado e navegar entre as letras. As regras são: 

- **A palavra correta tem cinco letras.**
- **Teclas alfabéticas:** Preenchem a letra na posição atual.
- **Enter:** Submete a palavra para avaliação.
- **Backspace:** Apaga a letra na posição atual.
- **Espaço:** Pausa o jogo e permite visualizar melhor o histórico.
- **Setas Esquerda/Direita:** Movem o cursor entre as letras da palavra atual.
- **Setas Cima/Baixo:** Movem a tela para visualizar o histórico de palpites.

A ideia do modo manual é que você possa entender melhor o jogo e pensar em estratégias.

## 👁️ Feedback Visual

Após cada palpite, o jogo retorna as cores: 

- 🟩 **Verde:** A letra está na palavra e na posição correta.
- 🟨 **Amarelo:** A letra está na palavra, mas na posição errada.
- 🟥 **Vermelho:** A letra não está na palavra.

**Repetição de letras**: Se a palavra ou o palpite tiver letras repetidas, o feedback também considera a quantidade correta de ocorrências. Por exemplo, se o palpite for “ROBOT”, e a palavra secreta tiver apenas um “O”, apenas a primeira correspondência é marcada como verde (se estiver na posição correta) ou amarelo (se houver essa letra na palavra, mas estiver na posição errada), as demais serão marcadas como vermelho (“RED”). Veja alguns exemplos de feedback caso a palavra secreta seja "**REVES**":
   - MEXER: 🟥🟩🟥🟩🟨
   - DEVIR: 🟥🟩🟩🟥🟨
   - ERETO: 🟨🟨🟨🟥🟥
   - EJETE: 🟨🟥🟨🟥🟥
   - BREVE: 🟥🟨🟨🟨🟨
   - REGRA: 🟩🟩🟥🟥🟥

Você continuará tentando até acertar a palavra ou esgotar as tentativas. 

## 📍Observações

- A lista de palavras inclui termos de diferentes idiomas, como português, inglês, espanhol, italiano e francês. 
- Se a palavra secreta for em italiano (ex: "MITRA"), o jogo apenas validará palpites cujas palavras estejam presentes no dicionário italiano, não sendo aceito palavras em outros idiomas (ex: "MESAS", "GIVEN"). 
- O jogo aceita apenas **palavras de 5 letras**. Palavras com mais ou menos letras são ignoradas.
- O modo manual será ativado quando executar pelo terminal `python player.py`. 
- É possível selecionar o idioma do jogo, basta executar `python player.py --lang it`.
- Veja a secção "Como Rodar" para mais informações sobre a executação do jogo.


## 🛠 Implementação (Modo Automático)

- **Objetivo**: Criar uma estratégia para resolver o jogo automaticamente com o menor número de tentativas. 

Você **só deve** alterar o arquivo `player.py`. Lá, existe a função `player(guess_hist, res_hist)` que:
1. Recebe dois parâmetros:
   - `guess_hist`: lista de **strings** já chutadas pelo seu algoritmo.
      - Exemplo: `guess_hist = ["AUREO", "MESAS", "SENSO"]`
   - `res_hist`: lista de **feedbacks** (listas de cores: “GREEN”, “YELLOW”, “RED”) correspondentes a cada palpite.
      - Exemplo: `res_hist = [["RED", "RED", "RED", "YELLOW", "GREEN"], ["RED", "GREEN", "YELLOW", "RED", "YELLOW"], ["GREEN", "GREEN", "GREEN", "GREEN", "GREEN"]]`
2. Devolve **uma string de 5 letras** como o novo palpite. Este palpite deve estar presente no dicionário para ser considerado válido.

Para que o jogo utilize a sua estratégia de forma automatizada, execute `python game.py --auto`.

Utilize essas informações para desenvolver sua melhor estratégia!

## 🏆 Torneio

O torneio avaliará a eficiência da estratégia desenvolvida para a função `player()`. Ele será usado tanto para determinar a sua nota na atividade (sem os descontos de qualidade de código - veja mais sobre isso no final do arquivo), quanto para a competição entre os alunos.

- Serão calculadas diversas estatísticas para avaliar a estratégia utilizada para adivinhar a palavra correta. 
- Para isso, diversas partidas serão realizadas, cada uma com uma palavra secreta diferente. 
- Para evitar loops infinitos, foi definido um **número máximo de tentativas** por partida. 
- Número de jogos: 500 (ou mais).
- Cada jogo tem um **máximo** (1000) de tentativas.
- Se o seu player **não acertar** a palavra dentro da quantidade máxima de tentativas, será contado como se tivesse usado todas elas e também será considerado como um jogo **falho**.
- Ao final, o script exibirá:
  - **Média** de tentativas
  - **Mediana** de tentativas
  - **Desvio padrão** (std)
  - **Número mínimo** e **número máximo** de tentativas
  - **Quantidade de falhas** (partidas não resolvidas)

A participação na competição é opcional. Quem quiser participar da **competição** deve preencher [este formulário](https://forms.gle/kbhwLeqASEnvXcq98). Os dois elementos da dupla precisam preencher para sabermos que todos estão de acordo. E os melhores vão ganhar prêmios surpresa!


## 📂 Estrutura dos Arquivos
```
📦 Wordle-MC102  
 ┣ 📜 README.md       # Documentação do projeto  
 ┣ 📜 game.py         # Implementação base do jogo   
 ┣ 📜 tournament.py   # Script para execução do torneio   
 ┣ 📜 player.py       # Arquivo com a função que deve ser implementada pelos alunos  
 ┣ 📜 words_en.txt    # Lista de palavras em inglês
 ┣ 📜 words_fr.txt    # Lista de palavras em francês
 ┣ 📜 words_it.txt    # Lista de palavras em italiano
 ┣ 📜 words_pt.txt    # Lista de palavras em português
 ┗ 📜 words_sp.txt    # Lista de palavras em espanhol
```

## 🚀 Como Rodar

1. **Instale o Pygame** (para rodar o jogo gráfico):
   pip install pygame

2. **Instale o Tqdm** (para barra de progresso no torneio):
   pip install tqdm

### Para rodar o jogo:

1. Selecionar o idioma do jogo. Há cinco opções disponíveis [en, fr, it, pt e sp] e se nenhum parâmetro for passado, o jogo será em português.
   python game.py --lang it

2. Executar o jogo usando a versão automatizada, com a estratégia do player.
   python game.py --auto

3. Também é possível selecionar um idioma e automatizar.
   python game.py --lang fr --auto

### Para rodar o torneio:

python tournament.py

## 📜 Entrega

Você deve entregar apenas o arquivo player.py no Google Classroom, no seguinte padrão:

1. No início do arquivo player.py, preencha o comentário com:
    - Nome Completo do Aluno que está entregando
    - RA do Aluno que está entregando
    - Nome Completo do outro membro da dupla
    - RA do outro membro da dupla
2. O outro membro da dupla deve enviar um comentário particular no Classroom dizendo que faz parte da dupla.

## 🧮 Nota

A sua nota base será calculada através da fórmula max(0, min(10, 18 - média)), isto é, se sua média for 8 ou menor você terá nota 10 e vai caindo até 0 se sua média for 18 ou mais. Porém, assim em como todas as atividades da disciplina, sua nota final pode sofrer descontos por causa da qualidade do código.


Agora, desenvolva sua estratégia e tente adivinhar a palavra correta no menor número de tentativas possível! 🎯🎉🏅
