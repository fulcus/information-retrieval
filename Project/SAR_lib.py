import json
from nltk.stem.snowball import SnowballStemmer
import os
import re


class SAR_Project:
    """
    Prototipo de la clase para realizar la indexacion y la recuperacion de noticias

        Preparada para todas las ampliaciones:
          parentesis + multiples indices + posicionales + stemming + permuterm + ranking de resultado

    Se deben completar los metodos que se indica.
    Se pueden añadir nuevas variables y nuevos metodos
    Los metodos que se añadan se deberan documentar en el codigo y explicar en la memoria
    """

    # lista de campos, el booleano indica si se debe tokenizar el campo
    # NECESARIO PARA LA AMPLIACION MULTIFIELD
    fields = [("title", True), ("date", False),
              ("keywords", True), ("article", True),
              ("summary", True)]

    # numero maximo de documento a mostrar cuando self.show_all es False
    SHOW_MAX = 10

    def __init__(self):
        """
        Constructor de la classe SAR_Indexer.
        NECESARIO PARA LA VERSION MINIMA

        Incluye todas las variables necesaria para todas las ampliaciones.
        Puedes añadir más variables si las necesitas

        """
        self.index = {}  # hash para el indice invertido de terminos --> clave: termino, valor: posting list.
        # Si se hace la implementacion multifield, se pude hacer un segundo nivel de hashing de tal forma que:
        # self.index['title'] seria el indice invertido del campo 'title'.
        self.sindex = {}  # hash para el indice invertido de stems --> clave: stem, valor: lista con los terminos que tienen ese stem
        self.ptindex = {}  # hash para el indice permuterm.
        # diccionario de documentos --> clave: entero(docid),  valor: ruta del fichero.
        self.docs = {}
        # hash de terminos para el pesado, ranking de resultados. puede no utilizarse
        self.weight = {}
        # hash de noticias --> clave entero (newid), valor: la info necesaria para diferenciar la noticia dentro de su fichero (doc_id y posición dentro del documento)
        self.news = {}
        # expresion regular para hacer la tokenizacion
        self.tokenizer = re.compile("\W+")
        self.stemmer = SnowballStemmer('spanish')  # stemmer en castellano
        self.show_all = False  # valor por defecto, se cambia con self.set_showall()
        self.show_snippet = False  # valor por defecto, se cambia con self.set_snippet()
        self.use_stemming = False  # valor por defecto, se cambia con self.set_stemming()
        self.use_ranking = False  # valor por defecto, se cambia con self.set_ranking()

    ###############################
    ###                         ###
    ###      CONFIGURACION      ###
    ###                         ###
    ###############################

    def set_showall(self, v):
        """

        Cambia el modo de mostrar los resultados.

        input: "v" booleano.

        UTIL PARA TODAS LAS VERSIONES

        si self.show_all es True se mostraran todos los resultados el lugar de un maximo de self.SHOW_MAX, no aplicable a la opcion -C

        """
        self.show_all = v

    def set_snippet(self, v):
        """

        Cambia el modo de mostrar snippet.

        input: "v" booleano.

        UTIL PARA TODAS LAS VERSIONES

        si self.show_snippet es True se mostrara un snippet de cada noticia, no aplicable a la opcion -C

        """
        self.show_snippet = v

    def set_stemming(self, v):
        """

        Cambia el modo de stemming por defecto.

        input: "v" booleano.

        UTIL PARA LA VERSION CON STEMMING

        si self.use_stemming es True las consultas se resolveran aplicando stemming por defecto.

        """
        self.use_stemming = v

    def set_ranking(self, v):
        """

        Cambia el modo de ranking por defecto.

        input: "v" booleano.

        UTIL PARA LA VERSION CON RANKING DE NOTICIAS

        si self.use_ranking es True las consultas se mostraran ordenadas, no aplicable a la opcion -C

        """
        self.use_ranking = v

    ###############################
    ###                         ###
    ###   PARTE 1: INDEXACION   ###
    ###                         ###
    ###############################

    def index_dir(self, root, **args):
        """
        NECESARIO PARA TODAS LAS VERSIONES

        Recorre recursivamente el directorio "root" e indexa su contenido
        los argumentos adicionales "**args" solo son necesarios para las funcionalidades ampliadas

        """

        self.multifield = args['multifield']
        self.positional = args['positional']
        self.stemming = args['stem']
        self.permuterm = args['permuterm']

        # multifield: self.index = {'article' : {term1: [], ...}, 'title': {term1: [], ...}}
        # in multifield if no other field is specified use 'article'
        self.index['article'] = {}
        if self.multifield:
            self.index['title'] = {}
            self.index['summary'] = {}
            self.index['keywords'] = {}
            self.index['date'] = {}

        for dir, subdirs, files in os.walk(root):
            for filename in files:
                if filename.endswith('.json'):
                    fullname = os.path.join(dir, filename)
                    self.index_file(fullname)

        # debug
        # filename = '2016-01-31.json'
        # if filename.endswith('.json'):
        #     fullname = os.path.join(root, filename)
        #     self.index_file(fullname)

        # TODO is it necessary to sort postings list?
        for word in self.index['article'].keys():
            self.index['article'][word] = sorted(self.index['article'][word])

        ##########################################
        ## COMPLETAR PARA FUNCIONALIDADES EXTRA ##
        ##########################################

    def index_file(self, filename):
        """
        NECESARIO PARA TODAS LAS VERSIONES

        Indexa el contenido de un fichero.

        Para tokenizar la noticia se debe llamar a "self.tokenize"

        Dependiendo del valor de "self.multifield" y "self.positional" se debe ampliar el indexado.
        En estos casos, se recomienda crear nuevos metodos para hacer mas sencilla la implementacion

        input: "filename" es el nombre de un fichero en formato JSON Arrays (https://www.w3schools.com/js/js_json_arrays.asp).
                Una vez parseado con json.load tendremos una lista de diccionarios, cada diccionario se corresponde a una noticia

        """

        # "jlist" es una lista con tantos elementos como noticias hay en el fichero,
        # cada noticia es un diccionario con los campos: "title", "date", "keywords", "article", "summary"
        # En la version basica solo se debe indexar el contenido "article"

        with open(filename) as fh:
            jlist = json.load(fh)

        # print(filename + ' ' + str(len(jlist)))

        # a.json : [{}, {}, {}] newsid 0, 1, 2; docid 0
        # b.json : [{}, {}, {}] newsid 3, 4, 5;  docid 1

        # Asignar a cada documento un identificador unico (docid) que sera un entero secuencial
        # Asignar a cada noticia un identificador unico. Se debe saber a que documento (fichero)
        # pertenece cada noticia y que posicion relativa ocupa dentro de el
        docid = len(self.docs)
        self.docs[docid] = filename
        newsid = len(self.news)

        # for each article in the json file
        for news_pos, new in enumerate(jlist):
            # newsid is global id of an article
            # news_pos is the position of the article within the file
            self.news[newsid] = (docid, news_pos)

            if self.multifield:
                # TODO verify: campo 'date' contiene el valor de la fecha de la noticia
                new_date = new['date']
                if new_date not in self.index['date']:
                    self.index['date'][new_date] = [newsid]
                else:
                    self.index['date'][new_date].append(newsid)
                fields = ["title", "keywords", "article", "summary"]
            else:
                fields = ["article"]

            for field in fields:
                words = self.tokenize(new[field])

                for word in words:
                    if word not in self.index[field]:
                        self.index[field][word] = set()
                    # posting list of news, not of docs
                    self.index[field][word].add(newsid)

            newsid += 1

    def tokenize(self, text):
        """
        NECESARIO PARA TODAS LAS VERSIONES

        Tokeniza la cadena "texto" eliminando simbolos no alfanumericos y dividientola por espacios.
        Puedes utilizar la expresion regular 'self.tokenizer'.

        params: 'text': texto a tokenizar

        return: lista de tokens

        """
        return self.tokenizer.sub(' ', text.lower()).split()

    def make_stemming(self):
        """
        NECESARIO PARA LA AMPLIACION DE STEMMING.

        Crea el indice de stemming (self.sindex) para los terminos de todos los indices.

        self.stemmer.stem(token) devuelve el stem del token

        """
        # Recorremos todos los campos del indice de terminos
        for field in self.index:

            # Recorremos todos los terminos del campo
            for word in self.index[field]:

                # Si antes no hemos hecho el stemming del termino generamos el stem
                stem = self.stemmer.stem(word)

                # Si aun no hemos añadido el stem lo añadimos
                self.sindex[field][stem] = self.or_posting(self.sindex[field].get(stem, []), self.index[field][word])

    def make_permuterm(self):
        """
        NECESARIO PARA LA AMPLIACION DE PERMUTERM

        Crea el indice permuterm (self.ptindex) para los terminos de todos los indices.

        """
      

    def show_stats(self):
        """
        NECESARIO PARA TODAS LAS VERSIONES

        Muestra estadisticas de los indices

        """
        fields = [f for f, _ in self.fields] if self.multifield else ['article']

        print('========================================')
        print('Number of indexed days: {}'.format(len(self.docs)))
        print('----------------------------------------')
        print('Number of indexed news: {}'.format(len(self.news)))
        print('----------------------------------------')
        print('TOKENS:')
        for field in fields:
            print("\t# of tokens in '{}': {}".format(
                field, len(self.index[field])))
        print('----------------------------------------')
        if (self.permuterm):
            print('PERMUTERMS:')
            for field in fields:
                print("\t# of tokens in '{}': {}".format(
                    field, len(self.ptindex[field])))
            print('----------------------------------------')
        if (self.stemming):
            print('STEMS:')
            for field in fields:
                print("\t# of tokens in '{}': {}".format(
                    field, len(self.sindex[field])))
            print('----------------------------------------')
        print('Positional queries are ' +
              ('' if self.positional else 'NOT ') + 'allowed.')
        print('========================================')

    ###################################
    ###                             ###
    ###   PARTE 2.1: RECUPERACION   ###
    ###                             ###
    ###################################

    def solve_query(self, query, prev={}):
        """
        NECESARIO PARA TODAS LAS VERSIONES

        Resuelve una query.
        Debe realizar el parsing de consulta que sera mas o menos complicado en funcion de la ampliacion que se implementen


        param:  "query": cadena con la query
                "prev": incluido por si se quiere hacer una version recursiva. No es necesario utilizarlo.


        return: posting list con el resultado de la query

        """
        # print("idx query", self.index['article'])
        if query is None or len(query) == 0:
            return []
        ########################################
        ## COMPLETAR PARA TODAS LAS VERSIONES ##
        ########################################
        query = query.lower()  # To lowercase
        query_split = query.split(' ')  # Split query by terms

        if query_split[0] == 'not':
            n = 2
            prev = self.reverse_posting(self.get_posting_by_fields(
                query_split[1]))  # If first term a NOT, get the postinglist of NOT term
        # If not, get the posting list of the first term
        else:
            n = 1
            prev = self.get_posting_by_fields(query_split[0])

        # Call recursive function
        return self.solve_query_by_term(query_split[n:], prev)

    def solve_query_by_term(self, query, prev):  # Recursive function
        if len(query) == 0:
            return prev  # Base case
        else:  # Recursive case
            t2 = {}  # Var fot postinglist of term2
            if query[0] == 'and':  # If AND
                if query[1] == 'not':
                    n = 3
                    t2 = self.reverse_posting(
                        self.get_posting_by_fields(query[2]))  # If term2 needs to be NOT
                else:
                    n = 2
                    t2 = self.get_posting_by_fields(query[1])
                # Get postinglist of prev AND t2
                prev = self.and_posting(prev, t2)
                return self.solve_query_by_term(query[n:], prev)

            elif query[0] == 'or':  # If OR
                if query[1] == 'not':
                    n = 3
                    t2 = self.reverse_posting(
                        self.get_posting_by_fields(query[2]))  # If term2 needs to be NOT
                else:
                    n = 2
                    t2 = self.get_posting_by_fields(query[1])
                # Get postinglist of prev OR t2
                prev = self.or_posting(prev, t2)
                return self.solve_query_by_term(query[n:], prev)

    # Method that returns postinglist of article if term is passed, or term of sprecific field if 'field:term' is passed

    def get_posting_by_fields(self, term):
        if ':' in term:
            res = term.split(':')
            return self.get_posting(res[1], res[0])
        else:
            return self.get_posting(term)

    def get_posting(self, term, field='article'):
        """
        NECESARIO PARA TODAS LAS VERSIONES

        Devuelve la posting list asociada a un termino.
        Dependiendo de las ampliaciones implementadas "get_posting" puede llamar a:
            - self.get_positionals: para la ampliacion de posicionales
            - self.get_permuterm: para la ampliacion de permuterms
            - self.get_stemming: para la amplaicion de stemming


        param:  "term": termino del que se debe recuperar la posting list.
                "field": campo sobre el que se debe recuperar la posting list, solo necesario si se hace la ampliacion de multiples indices

        return: posting list

        """

        ########################################
        ## COMPLETAR PARA TODAS LAS VERSIONES ##
        ########################################
        # If term appears in field, get the values of the term, else empty list.
        res = self.index[field].get(term, [])
        
        return res

    def get_positionals(self, terms, field='article'):
        """
        NECESARIO PARA LA AMPLIACION DE POSICIONALES

        Devuelve la posting list asociada a una secuencia de terminos consecutivos.

        param:  "terms": lista con los terminos consecutivos para recuperar la posting list.
                "field": campo sobre el que se debe recuperar la posting list, solo necesario se se hace la ampliacion de multiples indices

        return: posting list

        """
        pass
        ########################################################
        ## COMPLETAR PARA FUNCIONALIDAD EXTRA DE POSICIONALES ##
        ########################################################

    def get_stemming(self, term, field='article'):
        """
        NECESARIO PARA LA AMPLIACION DE STEMMING

        Devuelve la posting list asociada al stem de un termino.

        param:  "term": termino para recuperar la posting list de su stem.
                "field": campo sobre el que se debe recuperar la posting list, solo necesario se se hace la ampliacion de multiples indices

        return: posting list

        """

        

        # Creamos stem del termino
        stem = self.stemmer.stem(word)
        res = []

        # Buscamos si esta indexado
        if (stem in self.sindex[field]):

            # Devolvemos la posting list asociada
            res = self.sindex[field][stem]

        return res

    def get_permuterm(self, term, field='article'):
        """
        NECESARIO PARA LA AMPLIACION DE PERMUTERM

        Devuelve la posting list asociada a un termino utilizando el indice permuterm.

        param:  "term": termino para recuperar la posting list, "term" incluye un comodin (* o ?).
                "field": campo sobre el que se debe recuperar la posting list, solo necesario se se hace la ampliacion de multiples indices

        return: posting list

        """

        
    def reverse_posting(self, p):
        """
        NECESARIO PARA TODAS LAS VERSIONES

        Devuelve una posting list con todas las noticias excepto las contenidas en p.
        Util para resolver las queries con NOT.


        param:  "p": posting list


        return: posting list con todos los newid exceptos los contenidos en p

        """
        #
        ########################################
        ## COMPLETAR PARA TODAS LAS VERSIONES ##
        ########################################

        res = []
        # For each document, if it does not appear in p, add to res
        for l in range(len(self.news)):
            if l not in p:
                res.append(l)
        return res

    def and_posting(self, p1, p2):
        """
        NECESARIO PARA TODAS LAS VERSIONES

        Calcula el AND de dos posting list de forma EFICIENTE

        param:  "p1", "p2": posting lists sobre las que calcular


        return: posting list con los newid incluidos en p1 y p2

        """
        #
        ########################################
        ## COMPLETAR PARA TODAS LAS VERSIONES ##
        ########################################
        res = []
        cont1 = 0  # Pointer posting list 1
        cont2 = 0  # Pointer posting list 2
        while len(p1) > cont1 and len(p2) > cont2:  # While not end of p1 and p2
            if p1[cont1] == p2[cont2]:
                res.append(p1[cont1])
                cont1 += 1
                cont2 += 1  # If same doc, add to res
            elif p1[cont1] < p2[cont2]:
                cont1 += 1  # If not change pointer
            else:
                cont2 += 1

        return res

    def or_posting(self, p1, p2):
        """
        NECESARIO PARA TODAS LAS VERSIONES

        Calcula el OR de dos posting list de forma EFICIENTE

        param:  "p1", "p2": posting lists sobre las que calcular


        return: posting list con los newid incluidos de p1 o p2

        """
        #
        ########################################
        ## COMPLETAR PARA TODAS LAS VERSIONES ##
        ########################################

        res = []
        cont1 = 0  # Pointer posting list 1
        cont2 = 0  # Pointer posting list 2
        while len(p1) > cont1 and len(p2) > cont2:  # While not end of p1 and p2
            if p1[cont1] == p2[cont2]:
                res.append(p1[cont1])
                cont1 += 1
                cont2 += 1  # If same doc, add to res
            elif p1[cont1] < p2[cont2]:
                res.append(p1[cont1])
                cont1 += 1  # If not, add to res and move pointer
            else:
                res.append(p2[cont2])
                cont2 += 1

        while len(p1) > cont1:
            res.append(p1[cont1])
            cont1 += 1  # While not end of p1, add all p1 to res
        while len(p2) > cont2:
            res.append(p2[cont2])
            cont2 += 1  # While not end of p2, add all p2 to res

        return res

    def minus_posting(self, p1, p2):
        """
        OPCIONAL PARA TODAS LAS VERSIONES

        Calcula el except de dos posting list de forma EFICIENTE.
        Esta funcion se propone por si os es util, no es necesario utilizarla.

        param:  "p1", "p2": posting lists sobre las que calcular


        return: posting list con los newid incluidos de p1 y no en p2

        """

        pass
        ########################################################
        ## COMPLETAR PARA TODAS LAS VERSIONES SI ES NECESARIO ##
        ########################################################

    #####################################
    ###                               ###
    ### PARTE 2.2: MOSTRAR RESULTADOS ###
    ###                               ###
    #####################################

    def solve_and_count(self, query):
        """
        NECESARIO PARA TODAS LAS VERSIONES

        Resuelve una consulta y la muestra junto al numero de resultados 

        param:  "query": query que se debe resolver.

        return: el numero de noticias recuperadas, para la opcion -T

        """
        result = self.solve_query(query)
        print("%s\t%d" % (query, len(result)))
        return len(result)  # para verificar los resultados (op: -T)

    def solve_and_show(self, query):
        """
        NECESARIO PARA TODAS LAS VERSIONES

        Resuelve una consulta y la muestra informacion de las noticias recuperadas.
        Consideraciones:

        - En funcion del valor de "self.show_snippet" se mostrara una informacion u otra.
        - Si se implementa la opcion de ranking y en funcion del valor de self.use_ranking debera llamar a self.rank_result

        param:  "query": query que se debe resolver.

        return: el numero de noticias recuperadas, para la opcion -T

        """
        result = self.solve_query(query)
        if self.use_ranking:
            result = self.rank_result(result, query)

        ########################################
        ## COMPLETAR PARA TODAS LAS VERSIONES ##
        ########################################
        print('Query:\t' + "'" + query + "'" +
              '\nNumber of results: ' + str(len(result)))

        if self.multifield:
            for k in range(len(result)):
                doc = self.news[result[k]]
                filename = self.docs[doc[0]]
                with open(filename) as fh:
                    jlist = json.load(fh)
                news = jlist[doc[1]]
                print("#{}      ({})  ({})  ({})  {}      ({})".format(
                    k, 0, result[k], news['date'], news['title'], news['keywords']))

        for k in range(len(result)):
            print("#{}      ({})  ({})  ({})  {}      ({})".format(
                k, 0, result[k], 'date', 'Title', 'keywords'))

    def rank_result(self, result, query):
        """
        NECESARIO PARA LA AMPLIACION DE RANKING

        Ordena los resultados de una query.

        param:  "result": lista de resultados sin ordenar
                "query": query, puede ser la query original, la query procesada o una lista de terminos


        return: la lista de resultados ordenada

        """

        pass

        ###################################################
        ## COMPLETAR PARA FUNCIONALIDAD EXTRA DE RANKING ##
        ###################################################
