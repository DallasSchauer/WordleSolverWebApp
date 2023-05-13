# Wordle-Solver
Python implementation of Wordle variants and accompanying AI strategies to minimize guesses needed to solve.


# TO-DO
- Wordle tutorial:
    - https://www.youtube.com/watch?v=ckjRsPaWHX8
- Make homepage:
    - 2 options for forms: single game or many game sim
    - Single game: text box for all of the words
    - Multiple games: number of words per game, strategy (w/ descriptions)
- Make 2 HTML pages with results
    - Single game: win/fail, all guesses, all pools, highlight which pool is chosen
    - Multi-game: avg num of guesses, win percentage, worst game, best game, distribution graph, output logs
- make website banner (w/ homepage functionality)

# DONE
- Make dictionary to make distribution


strategies:
- BAD: Random
    - Picks guess from possible remaining answers randomly.
- BAD: Unique Words
    - Picks guess from possible remaining answers prioritizing words with higher count of unique letters.
- MEDIUM: Scrabble
    - Picks guess from possible remaining answers prioritizing words with lower Scrabble score.
- MEDIUM: Common Letters
    - Picks guess from possible remaining answers prioritizing words with more common letters.
- GOOD: Common Letter Spots
    - Picks guess from possible remaining answers prioritizing words with more common letters in letter
    spots they are commonly found.
- GOOD: Static Starters to Entropy
    - Starts every game with guesses "RAISE, CLOUT, NYMPH." to narrow down remaining answers greatly. Then, picks guess from possible remaining answers prioritizing information gain, or, how useful
    each word will be in narrowing down the remaining answers further.