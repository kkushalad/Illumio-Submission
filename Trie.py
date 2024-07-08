from collections import Counter
import re


class TrieNode(object):
    def __init__(self, ignore_case=True):
        self.is_word = False
        self.children = [None] * 26 if ignore_case else [None] * 52


class Trie(object):
    def __init__(self, ignore_case=True):
        self.ignore_case = ignore_case
        self.root = TrieNode(ignore_case)

    @staticmethod
    def _get_index(char):
        if 'a' <= char <= 'z':
            return ord(char) - ord('a')
        elif 'A' <= char <= 'Z':
            return ord(char) - ord('A') + 26
        else:
            raise ValueError("Invalid character")

    def insert_word(self, word: str) -> None:
        if self.ignore_case:
            word = word.lower()

        cur = self.root
        for ch in word:
            idx = Trie._get_index(ch)
            if cur.children[idx] is None:
                cur.children[idx] = TrieNode(self.ignore_case)
            cur = cur.children[idx]
        cur.is_word = True

    def search_word(self, word: str) -> bool:
        if self.ignore_case:
            word = word.lower()

        cur = self.root
        for ch in word:
            idx = Trie._get_index(ch)
            if cur.children[idx] is None:
                return False
            cur = cur.children[idx]
        return cur.is_word


# This is the Trie data structure for our predefined words.
predefined_words_trie = Trie()

# This data structure used for storing the matched words for processing later.
# Problem does not state the complete use case. So, implementation writes the matched word and it's count to file
matched_words = Counter()

def process_predefined_words(keyword_file: str, ignore_case=True) -> None:
    """
    This function process the keyword_file which contains the pre-defined words, parses the file and stores the words
    into hash table data structure

    :param keyword_file: This file holds the all the predefined set of words, newline separated.
    :param ignore_case: Indicates if case-sensitive or not
    :return:
    """
    with open(keyword_file, 'r') as file:
        for line in file:
            line = line.strip()
            word = line.lower() if ignore_case else line
            predefined_words_trie.insert_word(word)


def clean_word(word: str):
    return re.sub(r'[^a-zA-Z]', '', word)


def extract_word_from_input(input_file: str, ignore_case=True):
    """
    It processes and parses the input file. Which could be very large. This function extracts the word yields it to the
    caller.

    :param input_file: Input file which need to processed and matched against the predefined set of words.
    :param ignore_case: Indicates if case-sensitive or not
    :return:
    """
    with open(input_file, 'r') as in_file:
        for line in in_file:
            words = line.strip().split()
            for word in words:
                word = word.lower() if ignore_case else word
                yield clean_word(word)


def find_matches(input_file: str, keyword_file: str):
    """
    This function finds the matches against the predefined set of words by extracting words form input file.

    :param input_file: Input file which need to processed and matched against the predefined set of words.
    :param keyword_file: This file holds the all the predefined set of words, newline separated.
    :return:
    """
    process_predefined_words(keyword_file)

    for word in extract_word_from_input(input_file):
        if predefined_words_trie.search_word(word):
            matched_words[word] += 1


def main():
    input_file = r"C:\Users\kiran\PycharmProjects\pythonProject\input_file.txt"
    predefined_words_file = r"C:\Users\kiran\PycharmProjects\pythonProject\predefined_words_file.txt"
    matched_words_output_file = r"C:\Users\kiran\PycharmProjects\pythonProject\matched_words_output_file.txt"

    find_matches(input_file, predefined_words_file)

    with open(matched_words_output_file, 'w') as out_file:
        for key, val in matched_words.items():
            out_file.write(f"Word: {key} Count: {val}" + "\n")


if __name__ == "__main__":
    main()