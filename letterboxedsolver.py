#!/usr/bin/python3
import sys
import re

def solve(letters, solution, letter_words, maxwords):
    # Is the solution at the max word count?
    if len(solution) >= maxwords:
        return None

    solution_set = set(''.join(solution))
    for word in letter_words[solution[-1][-1]]:
        # Check that the solution set isn't made up of the new word
        if (solution_set - set(word)):
            # Are all of the letters accounted-for in the solution? (ie. is the puzzle solved?)
            if not (letters - set(''.join(solution+[word]))):
                print('-'.join(solution+[word]))
            else:
                solve(letters, solution+[word], letter_words, maxwords)

def valid_words(sides):
    # Compile a regular expression to match lines that contain words with letters from the sides
    all_sides_regex = re.compile(f"^[{''.join([f'{side}' for side in sides])}]+$")

    # Compile a regular expression to match lines that contain words with consecutives letters from
    # the same side
    same_side_regex = re.compile('|'.join([f'([{side}][{side}])' for side in sides]))

    words = []
    with open('words.txt', 'r') as file:
        for word in file:
            if all_sides_regex.match(word) and not same_side_regex.search(word):
                words.append(word.strip())

    return words

def calc_coverages(sides, words):
    coverage_words = []
    for coverage in range(0, 13):
        coverage_words.append([])

    letters = set(''.join(sides))
    for word in words:
        coverage = len(letters & set(word))
        coverage_words[coverage].append(word)

    for coverage in range(0, 13):
        coverage_words[coverage].sort(key=len)

def main():
    sides = sys.argv[1:5]

    if len(sides) != 4:
        print("Usage: python letterboxsolver.py <side1> <side2> <side3> <side4>")
        sys.exit(1)

    letters = set(''.join(sides))

    words = valid_words(sides)
    words.sort(key=lambda word: len(set(word) & letters), reverse=True)

    letter_words = {}
    for letter in "abcdefghijklmnopqrstuvwxyz":
        letter_words[letter] = []

    for word in words:
        letter_words[word[0]].append(word)

    for letter in letter_words:
        letter_words[letter].sort(key=lambda word: len(set(word) & letters), reverse=True)

    maxwords = 2
    for word in words:
        solve(letters, [word], letter_words, maxwords)

if __name__ == "__main__":
    main()