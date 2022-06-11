# information-retrieval

This repository contains the code for the course Information Retrieval at Universidad Politécnica de València. 

It consists of 3 small projects (PigLatin, WordCounter, InfiniteMonkey) and a main final project (NewsSearcher).

# NewsSearcher 

The final project consists in the implementation in python3 of a news indexing and retrieval system.

The news docs are json files that contain one or more news articles and metadata of the day by the filename.
The `SAR_Indexer.py` builds the index for a given corpus of news files, and the `SAR_Searcher.py` allows to run queries using the built index. Both files use methods implemented in the `SAR_lib.py`, which provides the fundamental functionalities for both indexing and searching.

Features:
* **Stemming** of news and queries
* **Multifield**: allows to impose conditions on specific fields of the news articles such as `'title:', 'article:', 'summary:', 'keywords:' and 'date:'`
* **Positional searches**: allows searching for a consecutive sequence of words by enclosing them in double quotes, such as `"hello mom"`
* **Ranking**: returns news ordered by relevance using tf-idf
* **Permuterm indexing**: allows to perform wildcard queries using the `*` to match any number of characters, and `?` to match one character


## Usage

#### Requirements
* python3
* [nltk](https://www.nltk.org/) library, used for stemming: `pip install nltk`

### Indexer

```
usage: SAR_Indexer.py [-h] [-S] [-P] [-M] [-O] newsdir index

Index a directory with news in json format.

positional arguments:
  newsdir           directory with the news.
  index             name of the file to save the project object.

optional arguments:
  -h, --help        show this help message and exit
  -S, --stem        compute stem index.
  -P, --permuterm   compute permuterm index.
  -M, --multifield  compute index for all the fields.
  -O, --positional  compute positional index.
```

### Searcher
```
usage: SAR_Searcher.py [-h] [-S] [-N | -C] [-A] [-R]
                       [-Q query | -L qlist | -T test]
                       index

Search the index.

positional arguments:
  index                 name of the file with the index object.

optional arguments:
  -h, --help            show this help message and exit
  -S, --stem            use stem index by default.
  -N, --snippet         show a snippet of the retrieved documents.
  -C, --count           show only the number of documents retrieved.
  -A, --all             show all the results. If not used, only the first 10
                        results are showed. Does not apply with -C and -T
                        options.
  -R, --rank            rank results. Does not apply with -C and -T options.
  -Q query, --query query
                        query.
  -L qlist, --list qlist
                        file with queries.
  -T test, --test test  file with queries and results, for testing.
```

### Example

Build index `2015_index_full.bin` with stemming, permuterm, multifield and positional indexing on corpus contained in the `corpora/2015` directory.

```
$ python SAR_Indexer.py -S -P -M -O corpora/2015 2015_index_full.bin
========================================
Number of indexed days: 285
----------------------------------------
Number of indexed news: 803
----------------------------------------
TOKENS:
	# of tokens in 'title': 3321
	# of tokens in 'date': 285
	# of tokens in 'keywords': 2266
	# of tokens in 'article': 44684
	# of tokens in 'summary': 6919
----------------------------------------
PERMUTERMS:
	# of permuterms in 'title': 26115
	# of permuterms in 'date': 3135
	# of permuterms in 'keywords': 18440
	# of permuterms in 'article': 407377
	# of permuterms in 'summary': 59173
----------------------------------------
STEMS:
	# of stems in 'title': 2642
	# of stems in 'date': 285
	# of stems in 'keywords': 1968
	# of stems in 'article': 23284
	# of stems in 'summary': 4738
----------------------------------------
Positional queries are allowed.
========================================
Time indexing: 9.11s.
Time saving: 0.46s.
```

Run query on `2015_index_full.bin` index and show a snippet of the retrieved documents. 
```
$ python SAR_Searcher.py -N -R -Q 'isla AND valencia AND pero' 2015_index_full.bin
========================================
Query:	'isla AND valencia AND pero'
Number of results: 2
#1
Score: 3.44
13
Date: 2015-03-25
Title: Diez motivos para querer vivir en Palma de Mallorca
Keywords: mallorca,palma,vivir,motivos
las playas más exclusivas de la isla la cala de l oratori o  ... que llegan hasta barcelona denia o valencia así como entre las islas de  ... mallorquines a pasear patinar o correr pero también a disfrutar de la puesta  ... 
--------------------
#2
Score: 2.97
587
Date: 2015-01-03
Title: Las Fuerzas Armadas: un paso al frente y dos atrás en derechos sociales
Keywords: frente,derechos,Fuerzas,Armadas,sociales
de jornada con destino en esta isla y que deja clara su situación  ... conexión en el cuartel general de valencia cuando no tenía ni uno tras  ... debe tener una mínima capacidad operativa pero sin cumplir con lo que dice  ... 
========================================
```

## Authors
* Francesco Gonzales
* Nuria Heredia Heredia
* Felix Marti Perez
* Sonia Palomo Marti


# Mini Projects

## Pig Latin
Pig Latin is a language game where English words are altered with the following set of rules:     
        1. Words that do not start with a letter will not be changed.
        2. Words that start with a consonant: all consonants before the first vocal will be moved to the end, and 'ay' is added.
        3. Words that start with a vocal: 'yay' be added at the end.
	
#### Examples   
  mess -> essmay     
  father -> atherfay     
  Rwanda -> Andarway     
  choir -> oirchay    
  ant -> antyay     
  4G -> 4G      

### Usage

This script translates from English to Pig Latin. If no argument is given, it will promp you to enter the phrases interactively. If a text file is given, it will generate a text file with the traduction.  

Sample of interactive usage:

```
ENGLISH: Spam, SPAM, Spam, Egg and Spam;    
PIG LATIN: Amspay, AMSPAY, Amspay, Eggyay andyay Amspay;    
ENGLISH: brandy and a fried egg on top and Spam     
PIG LATIN: andybray andyay ayay iedfray eggyay onyay    
optay andyay Amspay      
ENGLISH: 4G and spam    
PIG LATIN: 4G andyay amspay
```

## Count Words
Script that analyzes a given text file, and gives a complete evaluation of the text in terms of number of lines, number of words with/without stopwords, dictionary of the file, etc.

### Usage
```
usage: count_words.py [-h] [-s STOPWORDS] [-l] [-b] [-f] file [file ...]        
- positional arguments:    
file text file.     
- optional arguments:      
-h, --help show this help message and exit     
-s STOPWORDS, --stop STOPWORDS    
filename with the stopwords.   
-l, --lower lowercase all words before computing stats.   
-b, --bigram compute bigram stats.   
-f, --full show full stats.  
```

See [here](WordCounter/test_true/quijote_lsbf_stats.txt) for a sample output file.


## Infinite Monkey
Infinite Monkey Theorem: a monkey hitting keys at random on a typewriter keyboard for an infinite amount of time will almost surely type any given text.   

This script simulates this by creating phrases from words randomly chosen from a dictionary of bigrams or trigrams. The results are surprisingly good, as some phrases generated do make sense.    

### Usage

  `SAR_p3_monkey_indexer.py textfile [tri]` : Creates an index from the textfile. Defaults to bigrams, add `tri` to create trigrams.
  `SAR_p3_monkey_info.py indexfile`: Generates information from an index.
  `SAR_p3_monkey_evolved.py indexfile`:  Generates phrases from the index.
  `SAR_p3_monkey_lib.py`: Library for all the methods used (not executable).

  See [here](InfiniteMonkey/test_true/spam_tri.info) for a sample output file.

