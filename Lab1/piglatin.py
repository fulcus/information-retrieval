#!/usr/bin/env python
#! -*- encoding: utf8 -*-

# 1.- Pig Latin

import sys
import re


class Translator():

    def __init__(self, punt=None):
        """
        Constructor de la clase Translator

        :param punt(opcional): una cadena con los signos de puntuación
                                que se deben respetar
        :return: el objeto de tipo Translator
        """
        if punt is None:
            punt = ".,;?!"
        self.re = re.compile(r"(\w+)([" + punt + r"]*)")

        self.vowels = ('a','e','i','o','u', 'y', 'A','E','I','O','U', 'Y')
        self.punt = ('.',',',';','?','!')

    def translate_word(self, word):
        """
        Recibe una palabra en inglés y la traduce a Pig Latin

        :param word: la palabra que se debe pasar a Pig Latin
        :return: la palabra traducida
        """
        new_word = ''
        
        if not word[0].isalpha():
            return word
        elif word[0] in self.vowels: # vocales
            new_word = word + 'yay'
        else: # consonantes
            new_word = word + 'ay' # in case it is only made up by consonants
            for i, c in enumerate(word):
                if c in self.vowels:
                    init = word[:i]
                    new_word = word[i:] + init + 'ay'
                    break

        if word.isupper():
            new_word = new_word.upper()
        elif word[0].isupper():
            new_word = new_word.lower().capitalize()
        
        return new_word

    def translate_sentence(self, sentence):
        """
        Recibe una frase en inglés y la traduce a Pig Latin

        :param sentence: la frase que se debe pasar a Pig Latin
        :return: la frase traducida
        """

        new_sentence = ''
        words_punt = sentence.split(' ') # TODO OR ' ' 
        for word_punt in words_punt:
            for word, punt in self.re.findall(word_punt):
                new_word = self.translate_word(word) + punt + ' '
                new_sentence += new_word

        return new_sentence.strip()

    def translate_file(self, filename):
        """
        Recibe un fichero y crea otro con su tradución a Pig Latin

        :param filename: el nombre del fichero que se debe traducir
        :return: True / False 
        """
        new_filename = ''
        if '.' in filename:
            new_filename, ext = filename.split('.')
            new_filename += "_latin." + ext
        else:
            new_filename = filename + "_latin"
        
        new_file = open(new_filename, "w")

        for line in open(filename):
            line = line.rstrip('\n')
            new_sentence = self.translate_sentence(line)
            new_file.write(new_sentence + '\n')

        new_file.close()

if __name__ == "__main__":
    t = Translator()

    if len(sys.argv) > 2:
        print(f'Syntax: python {sys.argv[0]} [filename]')
        exit()
    t = Translator()
    if len(sys.argv) == 2:
        t.translate_file(sys.argv[1])
    else:
        sentence = input("ENGLISH: ")
        while len(sentence) > 1:
            print("PIG LATIN:", t.translate_sentence(sentence))
            sentence = input("ENGLISH: ")
