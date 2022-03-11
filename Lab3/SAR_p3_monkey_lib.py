#!/usr/bin/env python
#! -*- encoding: utf8 -*-
# 3.- Mono Library

import pickle
import random
import re

## Nombre: Francesco Fulco Gonzales

## Implementado funcionalidades básicas y ampliación de trigramas  


def sort_index(d):
    for k in d:
        l = sorted(((y, x) for x, y in d[k].items()), reverse=True)
        d[k] = (sum(x for x, _ in l), l)

class Monkey():

    def __init__(self):
        self.r1 = re.compile('[.;?!]') # para partir frases
        self.r2 = re.compile('\W+') # para limpiar y cortar la cadena (como en cuenta parablas)


    def index_sentence(self, sentence, tri):
        '''
        1) limpia y trocea la frase
        2) añade bigramas a self.index

        El diccionario creado tiene la forma siguiente:
        {
            'bi': {
                'word': {'spam': 5, 'other': 10}
            },
            'tri' : {
                ('word1', 'word2') : {'spam': 5, 'other': 10}
            }
        }
        '''
        prev_word = '$'            
        sentence = self.r2.sub(' ', sentence).split()
        prev_prev_word = None
        couple = None

        for index, word in enumerate(sentence):
            if prev_word not in self.index['bi']:
                self.index['bi'][prev_word] = {}
            
            self.index['bi'][prev_word][word] = self.index['bi'][prev_word].get(word, 0) + 1
        
            if tri and prev_prev_word is not None: # from third word compute trigrams
                couple = (prev_prev_word, prev_word)
                if couple not in self.index['tri']:
                    self.index['tri'][couple] = {}
                self.index['tri'][couple][word] = self.index['tri'][couple].get(word, 0) + 1
                # also for last word of sentence


            if index == len(sentence) - 1: # last word of sentence
                if word not in self.index['bi']:
                    self.index['bi'][word] = {}
                self.index['bi'][word]['$'] = self.index['bi'][word].get('$', 0) + 1

                if tri:
                    couple = (prev_word, word)
                    if couple not in self.index['tri']:
                        self.index['tri'][couple] = {}
                    self.index['tri'][couple]['$'] = self.index['tri'][couple].get('$', 0) + 1
                # for next sentence
                prev_word = '$' 
                prev_prev_word = None
            else:
                prev_prev_word = prev_word
                prev_word = word


    def compute_index(self, filename, tri):
        self.index = {'name': filename, "bi": {}}
        if tri:
            self.index["tri"] = {}
        
        # iterate on file to partir frases
        with open(filename, 'r') as fh:
            text =  fh.read().lower()
            split_double_line = text.split('\n\n')
            for s in split_double_line:
                for sentence in self.r1.split(s):
                    self.index_sentence(sentence, tri)

        sort_index(self.index['bi'])
        
        if tri:
            sort_index(self.index['tri'])
            
        
    def load_index(self, filename):
        with open(filename, "rb") as fh:
            self.index = pickle.load(fh)


    def save_index(self, filename):
        with open(filename, "wb") as fh:
            pickle.dump(self.index, fh)


    def save_info(self, filename):
        with open(filename, "w") as fh:
            print("#" * 20, file=fh)
            print("#" + "INFO".center(18) + "#", file=fh)
            print("#" * 20, file=fh)
            print("filename: '%s'\n" % self.index['name'], file=fh)
            print("#" * 20, file=fh)
            print("#" + "BIGRAMS".center(18) + "#", file=fh)
            print("#" * 20, file=fh)
            for word in sorted(self.index['bi'].keys()):
                wl = self.index['bi'][word]
                print("%s\t=>\t%d\t=>\t%s" % (word, wl[0], ' '.join(["%s:%s" % (x[1], x[0]) for x in wl[1]])), file=fh)
            if 'tri' in self.index:
                print(file=fh)
                print("#" * 20, file=fh)
                print("#" + "TRIGRAMS".center(18) + "#", file=fh)
                print("#" * 20, file=fh)
                for word in sorted(self.index['tri'].keys()):
                    wl = self.index['tri'][word]
                    print("%s\t=>\t%d\t=>\t%s" % (word, wl[0], ' '.join(["%s:%s" % (x[1], x[0]) for x in wl[1]])), file=fh)
    
    
    def sample_following_word_bi(self, word):
        '''
        Devuelve la siguiente palabra mediante el muestreo de la distribución 
        de las palabras que vienen después de la parabla "word"
        '''

        words_tuples = self.index['bi'][word][1] # (11, [(5, 'spam'), (5, 'egg'), (1, 'lobster')])
        words = []
        freqs = [] 
        for f, w in words_tuples:
            freqs.append(f)
            words.append(w)
        
        next_word = random.choices(words, weights=freqs)[0]

        return next_word

    def sample_following_word_tri(self, couple):
        '''
        Devuelve la siguiente palabra mediante el muestreo de la distribución 
        de las palabras que vienen después de la pareja "couple"
        '''

        words_tuples = self.index['tri'][couple][1]
        words = []
        freqs = [] 
        for f, w in words_tuples:
            freqs.append(f)
            words.append(w)
        
        next_word = random.choices(words, weights=freqs)[0]

        return next_word


    def generate_sentences(self, n=10):
        '''
        Generates n sentences
        '''
        for _ in range(0, n): # sentences
            sentence = ''
            word = prev_word = None
            for _ in range(0, 25): # words
                if 'tri' in self.index:
                    #print("({}, {})".format(prev_word, word))

                    if word is None:  # if first word sample from bi
                        prev_word = '$'
                        word = self.sample_following_word_bi(prev_word)
                    else:
                        old_word = word
                        word = self.sample_following_word_tri((prev_word, word))
                        if word == '$':
                            break
                        prev_word = old_word
                else: # bi
                    if word is None: word = '$'
                    word = self.sample_following_word_bi(word)
                    if word == '$':
                        break
                
                sentence += word + ' '
            print(sentence)


if __name__ == "__main__":
    print("Este fichero es una librería, no se puede ejecutar directamente")
