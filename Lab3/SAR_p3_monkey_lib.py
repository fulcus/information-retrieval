#!/usr/bin/env python
#! -*- encoding: utf8 -*-
# 3.- Mono Library

import pickle
import random
import re
import sys

## Nombres: 

########################################################################
########################################################################
###                                                                  ###
###  Todos los métodos y funciones que se añadan deben documentarse  ###
###                                                                  ###
########################################################################
########################################################################



def sort_index(d):
    for k in d:
        l = sorted(((y, x) for x, y in d[k].items()), reverse=True)
        d[k] = (sum(x for x, _ in l), l)


class Monkey():

    def __init__(self):
        self.r1 = re.compile('[.;?!]') # para partir frases
        self.r2 = re.compile('\W+') # para limpiar y cortar la cadena (como en cuenta parablas)


    def index_sentence(self, sentence, tri):
        # limpia y trocea frase
        # anade bigramas a self.index

        '''
        {
            'bi': {
                'word': {'spam': 5, 'other': 10}
            }
        }
        '''
        prev_word = '$'
        sentence = self.r2.sub(' ', sentence).split()
        # print('*')
        # print(sentence)
        # print('**')
        for index, word in enumerate(sentence):
            if prev_word not in self.index['bi']:
                self.index['bi'][prev_word] = {}

            self.index['bi'][prev_word][word] = self.index['bi'][prev_word].get(word, 0) + 1
        
            if index == len(sentence) - 1: # last word of sentence
                if word not in self.index['bi']:
                    self.index['bi'][word] = {}

                self.index['bi'][word]['$'] = self.index['bi'][word].get('$', 0) + 1
                prev_word = '$' # for next sentence
            else:
                prev_word = word


        


    def compute_index(self, filename, tri):
        self.index = {'name': filename, "bi": {}}
        if tri:
            self.index["tri"] = {}
        raw_sentence = ""
        
        # iterate on file to partir frases
        with open(filename, 'r') as fh:
            text =  fh.read().lower()
            split_double_line = text.split('\n\n')
            #print(split_double_line)
            for s in split_double_line:
                for sentence in self.r1.split(s):
                    #print(sentence)
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


    def generate_sentences(self, n=10):
        # n frases que genera
        # loop 1 to n, generates sentences
        pass


if __name__ == "__main__":
    print("Este fichero es una librería, no se puede ejecutar directamente")


