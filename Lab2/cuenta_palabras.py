#! -*- encoding: utf8 -*-

## Nombres: 

########################################################################
########################################################################
###                                                                  ###
###  Todos los métodos y funciones que se añadan deben documentarse  ###
###                                                                  ###
########################################################################
########################################################################

import argparse
import re
import sys


def sort_dic_by_values(d, asc=True):
    return sorted(d.items(), key=lambda a: (-a[1], a[0]))
    
class WordCounter:

    def __init__(self):
        """
           Constructor de la clase WordCounter
        """
        self.clean_re = re.compile('\W+') # match words that contain puctuation, use sub to delete it
        # clean_words = self.clean_re.sub('', word).split()
        # from dict get list -> order list: sort
        # sorted(dict) by key
    def write_stats(self, filename, stats, use_stopwords, full):
        """
        Este método escribe en fichero las estadísticas de un texto
            
        :param 
            filename: el nombre del fichero destino.
            stats: las estadísticas del texto.
            use_stopwords: booleano, si se han utilizado stopwords
            full: boolean, si se deben mostrar las stats completas

        :return: None
        """

        with open(filename, 'w') as fh:
            fh.write('Lines: {}\n'.format(stats['nlines']))
            fh.write('Number words (including stopwords): {}\n'.format(stats['nwords']))
            if(use_stopwords):
                fh.write('Number words (without stopwords): {}\n'.format(stats['nwords_without_stopwords']))
                # TODO STOPWORDS
            fh.write('Vocabulary size: {}\n'.format(len(stats['word'])))
            fh.write('Number of symbols: {}\n'.format(sum(stats['symbol'].values())))
            fh.write('Number of different symbols: {}\n'.format(len(stats['symbol'])))
            
            words_alph = 'Words (alphabetical order):\n'
            words_alph_list = sorted([(w, c) for w, c in stats['word'].items()])
            if not full:
                words_alph_list = words_alph_list[:20]
            for word, count in words_alph_list:
                words_alph += "\t{}: {}\n".format(word, count)
            fh.write(words_alph)
            
            #words_freq_list = sorted([(c, w) for w, c in stats['word'].items()], reverse=True)
            words_freq_list = sort_dic_by_values(stats['word'])
            if not full:
                words_freq_list = words_freq_list[:20]
            words_freq = 'Words (by frequency):\n'
            for word, count in words_freq_list:
                words_freq += "\t{}: {}\n".format(word, count)
            fh.write(words_freq)

            symb_alph_list = sorted([(w, c) for w, c in stats['symbol'].items()])
            if not full:
                symb_alph_list = symb_alph_list[:20]
            symb_alph = 'Symbols (alphabetical order):\n'
            for word, count in symb_alph_list:
                symb_alph += "\t{}: {}\n".format(word, count)
            fh.write(symb_alph)
            
            #symb_freq_list = sorted([(c, w) for w, c in stats['symbol'].items()], reverse=True)
            symb_freq_list = sort_dic_by_values(stats['symbol'])
            if not full:
                symb_freq_list = symb_freq_list[:20]
            symb_freq = 'Symbols (by frequency):\n'
            for word, count in symb_freq_list:
                symb_freq += "\t{}: {}\n".format(word, count)
            fh.write(symb_freq)

    def file_stats(self, filename, lower, stopwordsfile, bigrams, full):
        """
        Este método calcula las estadísticas de un fichero de texto

        :param 
            filename: el nombre del fichero.
            lower: booleano, se debe pasar todo a minúsculas?
            stopwordsfile: nombre del fichero con las stopwords o None si no se aplican
            bigram: booleano, se deben calcular bigramas?
            full: booleano, se deben montrar la estadísticas completas?

        :return: None
        """

        stopwords = [] if stopwordsfile is None else open(stopwordsfile).read().split()

        # variables for results

        sts = {
                'nwords': 0,
                'nlines': 0,
                'word': {},
                'symbol': {}
                }

        if bigrams:
            sts['biword'] = {}
            sts['bisymbol'] = {}

        if stopwordsfile: # TODO stopwords included in other statistics?
            sts['nwords_without_stopwords'] = 0

        with open(filename, 'r') as fh:
            for line in fh:
                sts['nlines'] += 1
                for word in line.split():
                    word = self.clean_re.sub('', word)
                    if lower:
                        word = word.lower()
                    sts['nwords'] += 1
                    if stopwordsfile and word.lower() not in stopwords: # assuming stopwords are lowercase
                        sts['nwords_without_stopwords'] += 1
                    # TODO delete stopwords
                    sts['word'][word] =  sts['word'].get(word, 0) + 1
                    for s in word:
                        sts['symbol'][s] =  sts['symbol'].get(s, 0) + 1
        
        # create new filename
        new_filename = ''
        if '.' in filename:
            new_filename, ext = filename.split('.')
        else:
            new_filename = filename
        new_filename += '_'
        # lower, stopwordsfile, bigrams, full
        new_filename += 'l' if(lower) else ''
        new_filename += 's' if(stopwordsfile) else ''
        new_filename += 'b' if(bigrams) else ''
        new_filename += 'f' if(full) else ''
        if lower or stopwordsfile or bigrams or full:
            new_filename += '_'
        new_filename += 'stats'
        if '.' in filename:
            new_filename += '.' + ext


        self.write_stats(new_filename, sts, stopwordsfile is not None, full)


    def compute_files(self, filenames, **args):
        """
        Este método calcula las estadísticas de una lista de ficheros de texto

        :param 
            filenames: lista con los nombre de los ficheros.
            args: argumentos que se pasan a "file_stats".

        :return: None
        """

        for filename in filenames:
            self.file_stats(filename, **args)

if __name__ == "__main__":

    parser = argparse.ArgumentParser(description='Compute some statistics from text files.')
    parser.add_argument('file', metavar='file', type=str, nargs='+',
                        help='text file.')

    parser.add_argument('-l', '--lower', dest='lower',
                        action='store_true', default=False, 
                        help='lowercase all words before computing stats.')

    parser.add_argument('-s', '--stop', dest='stopwords', action='store',
                        help='filename with the stopwords.')

    parser.add_argument('-b', '--bigram', dest='bigram',
                        action='store_true', default=False, 
                        help='compute bigram stats.')

    parser.add_argument('-f', '--full', dest='full',
                        action='store_true', default=False, 
                        help='show full stats.')

    args = parser.parse_args()
    wc = WordCounter()
    wc.compute_files(args.file,
                     lower=args.lower,
                     stopwordsfile=args.stopwords,
                     bigrams=args.bigram,
                     full=args.full)


