Problem Statement

Write a program that reads a file and finds matches against a predefined set of words. There can be up to 10K entries in the list of predefined words. Requirement details:
• Input file is a plain text (ascii) file, every record separated by a new line.
• For this exercise, assume English words only
• The file size can be up to 20 MB
• The predefined words are defined in a text file, every word separated by a newline. Use a sample file of your choice for the set of predefined keywords for the exercise.

Understanding of the Problem

We have been given some predefined set of words; size of the set could be up to 10K. And then we have been given input file of size 20MB. Which is plain text file consisting new line separated records. Problem states to assume English words only. So, we could make assumption that input file will consist of whitespace separated English words and may contain grammatical special characters for example ‘!’, ‘.’, ‘,’, ‘;’. Now, the ask we have to process input file and find matches against the predefined set of words. Input file is very large, and it will consist of very large number of English words, those words need to be extracted to be searched against the set of words. Extraction of words need to be taken care against the special characters that word may have in it. Once we extracted the single word from input file. We could search against the set of predefined words and add it to output list. There could be many the same word in the input file, so we could just the add count of occurrence as well.

Approach 

Data Structure

1. Hash table

Since we have predefined set of words, we could have them preprocessed and stored in in-memory data structure, we could then apply some efficient search when we iterate through the words from input file. Since 10K words not considerably very big, ideally in any given standard system, they could easily fit in memory. So, we could use hash table to store the set of words. Since words are known prior and size is fixed, we should be able to come up with perfect hashing function that minimizes hash collision, which could result in O (1) time complexity for search of given word.

2. Trie
   
Alternatively, we could use Trie data structure. Advantages of using Trie, this could serve many use-cases, like not just word search, we could efficiently do prefix search, all the keys with common prefix. But the problem does not state any other use-cases. Data Structure comparison Time complexity: If we have average length of word N and total of M words. Trie: O (M * N) time complexity Hash table: O (M * N) will also would need same amount if chosen hash function takes linear time, linear in length of the string, for calculating the hash value of string. There are hash functions whose hash value construction for strings faster than that. Space complexity: Trie: O (M * N* K) worst case if there no overlapping words, where K is the length of children node references at each Trie Node for the next level. For English words, it could be taken as 26 or 52 depending upper case or lower-case support. Hash Table: O (M * N) it will have all the stored in the table. Overall, Trie Data structure will be more compact and consume less memory on average case. 

Algorithm

Load the input file for processing, though input is very large, underneath system call will not directly load entire file into memory, it will just give file handle with which we could just load the buffer from file as and how we want.

We could read line by line, extract whitespace separated word, trim any special characters if it has any. Once we extract the single word, we could search that against the preprocessed set of words for its presence. Searching for word in both Hash table or Trie both incur same time complexity. In Hash table search O (1) but Hash index calculation may take O (N), N is the length of word and Trie it would take O (N) iteratively traversing the tree. Trie could have better time complexity on average because it could have early termination for the words not present.

Optimization

Considering the input file of very large size, 20MB, we could process the file in parallel. We could divide the file in chunks of chosen chunk size and let the different threads operate at different chunks of the file and find the matches against the predefined words.
Program for this optimization submitted in the source code file. 

Conclusion

Please find the source code files from the source section along with the test files used for testing which maps to given scale in the problem statement.
