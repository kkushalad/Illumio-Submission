from collections import Counter
import re
import concurrent.futures
import os
from typing import Set

# This is the hash table data structure for our predefined words.
predefined_words = set()


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
            predefined_words.add(word)


def clean_word(word: str):
    return re.sub(r'[^a-zA-Z]', '', word)


def process_chunk(file_path: str, start: int, size: int) -> Set[str]:
    """
    Thread function for parallel processing, it extracts the word from file in its operating range of chunk and
    searches the word against the predefined set of words.

    :param file_path: Input file which need to processed and matched against the predefined set of words.
    :param start: Start of the chunk
    :param size:
    :return: Returns the set of matched words in the given chunk
    """
    matches = set()
    with open(file_path, 'r') as file:
        file.seek(start)
        data = file.read(size)
        lines = data.splitlines()
        for line in lines:
            words = line.split()
            for word in words:
                cleaned_word = clean_word(word.lower())
                if cleaned_word in predefined_words:
                    matches.add(cleaned_word)
    return matches


def parallel_process_file(input_file: str, chunk_size: int = 1024 * 1024, num_threads: int = 8) -> Set[str]:
    """
    Processes the input file in parallel by letting each thread operate at different chunks of given file.

    :param input_file: Input file which need to processed and matched against the predefined set of words.
    :param chunk_size: Size of buffer process by each thread parallely.
    :param num_threads: Number of threads tunable for parallel processing.
    :return: Returns the set of matched words in the given input file
    """

    file_size = os.path.getsize(input_file)
    chunk_starts = list(range(0, file_size, chunk_size))

    results = set()
    with concurrent.futures.ThreadPoolExecutor(max_workers=num_threads) as executor:
        futures = []
        for start in chunk_starts:
            size = min(chunk_size, file_size - start)
            futures.append(executor.submit(process_chunk, input_file, start, size))

        for future in concurrent.futures.as_completed(futures):
            results.update(future.result())
    return results


def find_matches(input_file: str, keyword_file: str, matched_words_output_file: str):
    """
    This function finds the matches against the predefined set of words by extracting words form input file.

    :param input_file: Input file which need to processed and matched against the predefined set of words.
    :param keyword_file: This file holds the all the predefined set of words, newline separated.
    :param matched_words_output_file: To store output to file
    :return:
    """
    process_predefined_words(keyword_file)
    matched_words = parallel_process_file(input_file)

    with open(matched_words_output_file, 'w') as out_file:
        for key in matched_words:
            out_file.write(f"Matched Word: {key}" + "\n")


def main():
    input_file = r"C:\Users\kiran\PycharmProjects\pythonProject\input_file.txt"
    predefined_words_file = r"C:\Users\kiran\PycharmProjects\pythonProject\predefined_words_file.txt"
    matched_words_output_file = r"C:\Users\kiran\PycharmProjects\pythonProject\matched_words_output_file.txt"

    find_matches(input_file, predefined_words_file, matched_words_output_file)


if __name__ == "__main__":
    main()
