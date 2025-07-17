# Wordle-Solver
This project features an algorithm designed to autonomously solve the game of Wordle. It is engineered to guess the 5-letter secret word in the fewest average attempts by using a strategy of dictionary filtering and heuristic-based guess selection.

This was originally developed as an assignment for the MC102 course (Introduction to Algorithms and Computer Programming) at the [University of Campinas (UNICAMP)](https://www.ic.unicamp.br/en/). The original project specification (in Portuguese) can be viewed [here](ASSIGNMENT_PT.md)

## Implemented Strategy
The core logic resides in `player.py`, which decides the next guess. The strategy is built on three key pillars:

1. **Continuous Dictionary Filtering:** After each guess, the feedback (🟩 GREEN, 🟨 YELLOW, 🟥 RED) is used to eliminate word from the dictionary that are no longer possible candidates. The `get_filtered_words` function strictly applies the game's rules to shrink the search space. For example:
- A `GREEN` letter confirms that letter in that exact position.
- A `YELLOW` letter confirms the letter is in the word, but not in that position.
- A `RED` letter limits the number of times that letter can appear in the word.
2. **Best Guess Selection (Heuristic Approach):** from the remaining list of possible words, the `get_best_word` function selects the "best" guess. A word is considered "best" based on a heuristic that prioritizes:
- **Maximum number of unique letters:** To gather as much new information as possible.
- **Highest positional letter frequency:** Letters that are more common in their respective positions among the candidate words are favored.
3. **Strategic Eliminatioin Tactic ("Distinct Mode"):** In scenarios where the list of candidate words is still large but the top candidates are very similar (e.g., `SLATE`, `SPATE`, `SHATE`), the strategy adapts. If the number of unknown letters is low (e.g., <= 2), but many possibilities remain, the algorithm may enter a "distinct mode".
- It picks a word from the entire dictionary (not just the candidate list that contains the maximum number of untested, high-value letters.
- The goal of this guess isn't to solve the puzzle directly but to eliminate the largest number of possibilities for the next round. This was done because, before implementing this approach, there are specific cases similar to the one mentioned above in which the algorithm had to guess up to 3 more times in order to find the remaining letters. The workaround is simple: after identifying these special scenarios, it gets to use all 5 fields to try new letters, instead of 1 or 2.

## How to Run
**Prerequisites:**
- Python 3
- Python libraries: pygame and tqdm

1. **Clone the repository:**
   ```bash
   git clone https://github.com/murilopiovezana/Wordle-Solver
   cd Wordle-Solver
   ```
2. **Install dependencies:**
   ```bash
   pip install pygame tqdm
   ```
3. **Run the game in automatic (AI) mode:**
   ```bash
   python game.py --auto --lang en
   ```
   *You can replace `en` with `pt`, `fr`, `it` or `sp` to run the game on different languages.*
4. **Run the tournament to evaluate performance:**
   The tournament script runs 500 games with random words to benchmark the algorithm's performance.
   ```bash
   python tournament.py
   ```
## Performance Results
A sample run of the tournament.py script (simulating 500 games with random words) yielded the following typical performance:
```
Simulated games: 500
Maximum guesses per game: 1000
Average guesses: 3.304
Median number of guesses: 3
Standard deviation: 0.9141028388534848
Min. guesses: 1
Max. guesses: 8
Games failed: 0
```

## Project Structure
- `player.py`: **(My Implementation)** Contains the solver's logic and strategy.
- `game.py`: (Provided) The game's graphical user interface and main loop.
- `tournament.py`: (Provided) A script to run simulations and evaluate the algorithm's performance.
- `utils.py`: (Provided) Utility functions for loading words and handling colors.
- `words_*.txt`: (Provided) Word dictionaries for different languages.
