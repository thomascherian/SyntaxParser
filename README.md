# README #

Generates syntactic relations for each word in simple English Sentences. It is a simple project which makes use of the sentences in corpus and the dictionary files. WSD and inflected word generation are not included. Instead we are making use of an 'Inflected dictionary' which contains all the inflected words from the corpus and the corresponding tags. Dictionaries are made according to the specific use of the word in the corpus. 

New sentences can be added to corpus and the program will list down the sentences having new words. Dictionaries can be updated and the program can be executed after that.

### Files ###
1. parser.py: Python code for our parser
2. parser_out.txt: Output file for the parser
3. corpus.txt: List of input sentences/Input file
4. RootDict.txt: Root dictionary
5. InflectedDict.txt: Inflected word dictionary