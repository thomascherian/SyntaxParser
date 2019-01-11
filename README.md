# Syntax Parser for Simple English Sentences #

Generates syntactic relations for each word in simple English Sentences. It is a simple project which makes use of the sentences in corpus and the dictionary files. WSD and inflected word generation are not included. Instead we are making use of an 'Inflected dictionary' which contains all the inflected words from the corpus and the corresponding tags. Dictionaries are made according to the specific use of the word in the corpus. 

New sentences can be added to corpus and the program will list down the sentences having new words. Dictionaries can be updated and the program can be re run, so as to capture the additions. 

### Files ###
1. parser.py: Python code for our parser
2. parser_out.txt: Output file for the parser
3. corpus.txt: List of input sentences/Input file
4. RootDict.txt: Root dictionary
5. InflectedDict.txt: Inflected word dictionary

#### Input: ####
Sentence, Root Dict, Inflected Dict

#### Output: ####
Syntax information for the input sentence.

#### Assumptions: ####
1. Dictionary is made according to the corpus. Each word has only single tag.
2. Assume that we have an unambiguosly tagged sentence.

## **Tagging each word in the sentence** ##

* Let 'Sentence' be the input Sentence.
* Extract the words from the 'Sentence' and store it in list 'Words'
* Let 'Count' be the number of words.
* For each 'Word' in 'Words',
1. Search 'Root Dict'. If entry found, retrieve the properties.
2. If entry not found, Search 'Inflected Dict' and retrieve the properties.

*Now we have the information about each and every word in the sentence. Hence we know which
word is the verb, noun etc.*

## **Identifying the Syntax** ##

1. Scan from left to right, first main verb is the root. If no main verb present in the sentence, first
auxiliary verb is made root. All other aux verbs are marked as the aux verb of the root.
2. From the verb, start scaning left, first noun is the subject of the verb.
3. Continue scanning left to the noun, if adj found, it is the adj of the noun.
4. Continue scanning left, if a Det is found, it is the Det of the noun.
5. Scan from the successor of the verb in forward direction, if adverb is found, it is the adverb for
the verb.
6. From the verb, start scanning to right, if a verb found, it is the secondary verb of the root verb.
7. Continue scanning to right, first noun is the object of the verb. (If secondary verb exists, it is the
object of the secondary verb. Else object of the primary verb.)
8. Scan from the left word of the object, till verb, and find the Adj and Det for the object noun (in
the same manner we did for the subject noun)
9. Scan from the left of the noun, to left. If a preposition is found, it is linked to the noun. Those
nouns are not objects. Relation between those nouns and root is marked as 'nmod' by Stanford
depenedency parser.
