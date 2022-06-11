import os
import re
import math
import json

from nltk.stem.snowball import SnowballStemmer


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
        self.sindex = {}  # hash para el indice invertido de stems --> clave: stem, valor: lista con los terminos que tienen ese stem
        self.ptindex = {}  # hash para el indice permuterm.
        # diccionario de documentos --> clave: entero(docid),  valor: ruta del fichero.
        self.docs = {}
        # hash de terminos para el pesado, ranking de resultados. puede no utilizarse
        self.weight = {}
        # hash de noticias --> clave entero (newid), valor: la info necesaria para diferenciar la noticia dentro de su fichero (doc_id y posición dentro del documento)
        self.news = {}
        self.tokenizer = re.compile("\W+") # expresion regular para hacer la tokenizacion
        self.stemmer = SnowballStemmer('spanish')  # stemmer en castellano
        self.show_all = False  # valor por defecto, se cambia con self.set_showall()
        self.show_snippet = False  # valor por defecto, se cambia con self.set_snippet()
        self.use_stemming = False  # valor por defecto, se cambia con self.set_stemming()
        self.use_ranking = False  # valor por defecto, se cambia con self.set_ranking()
        self.pterms = {}  # hash para el indice invertido permuterm --> clave: permuterm, valor: lista con los terminos que tienen ese permuterm
        self.sterms = {} # hash para el indice invertido de stems --> clave: stem, valor: lista con los terminos que tienen ese stem
        self.term_field = {} # términos en la query y aque campo pertenecen --> clave: término, valor: campo (field)
        self.posindex = {} # para posicional, self.posindex[field][word] = {newsid : [word_pos]}

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
        if self.multifield:
            # Indexar diversos campos
            self.index['title'] = {}
            self.index['date'] = {}
            self.index['keywords'] = {}
            self.index['article'] = {}
            self.index['summary'] = {}

            self.weight['title'] = {}
            self.weight['date'] = {}
            self.weight['keywords'] = {}
            self.weight['article'] = {}
            self.weight['summary'] = {}
            if self.stemming:
                self.sindex['title'] = {}
                self.sindex['date'] = {}
                self.sindex['keywords'] = {}
                self.sindex['article'] = {}
                self.sindex['summary'] = {}
            if self.permuterm:
                self.ptindex['title'] = {}
                self.ptindex['date'] = {}
                self.ptindex['keywords'] = {}
                self.ptindex['article'] = {}
                self.ptindex['summary'] = {}
            if self.positional:
                self.posindex['title'] = {}
                self.posindex['date'] = {}
                self.posindex['keywords'] = {}
                self.posindex['article'] = {}
                self.posindex['summary'] = {}
        else:
            self.index['article'] = {}
            self.weight['article'] = {}
            if self.stemming:
                self.sindex['article'] = {}
            if self.permuterm:
                self.ptindex['article'] = {}
            if self.posindex:
                self.posindex['article'] = {}

            
        for dir, subdirs, files in os.walk(root):
            for filename in files:
                if filename.endswith('.json'):
                    fullname = os.path.join(dir, filename)
                    self.index_file(fullname)


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
        docid = len(self.docs)
        self.docs[docid] = filename # Fijar entrada del diccionario docs
        newsid = len(self.news) # unique for each new
        news_pos = 0 # news position relative to file

        # Por cada noticia del fichero json
        for new in jlist:  
            
            # entrada del diccionario news
            self.news[newsid] = {
                'docid': docid,
                'position': news_pos
            }

            # Por cada campo de la noticia
            for field in self.index.keys():
                stems = {}
                terms = set()

                if self.multifield:
                    # if field is True in self.fields then tokenize
                    if [item for item in self.fields if item[0] == field][0][1]:
                        words = self.tokenize(new[field])
                    else:
                        words = [new[field]]
                else:
                    words = self.tokenize(new[field])
                
                # Por cada término del campo de la noticia    
                word_pos = 0
                for word in words:

                    # Versión stemming
                    # Continuamos si esta activada la accion y el termino no se ha añadido todavia
                    if self.stemming and word not in terms:
                        stem = self.stemmer.stem(word)

                        # Añadimos el stem si aun no esta en el diccionario
                        if stem not in self.sterms:
                            self.sterms[stem] = []

                        # Añadimos el termino si no esta en la lista de terminos asociados
                        if word not in self.sterms[stem]:
                            self.sterms[stem] = self.sterms.get(stem, []) + [word]

                        if stem not in stems:
                            # Si no hemos añadido el estem lo añadimos
                            self.sindex[field][stem] = self.sindex[field].get(stem, []) + [newsid]
                            stems[stem] = True
                    #-------------------------------
                    
                    # Versión  permuterm
                    # Continuamos si esta activada la accion y el termino no se ha añadido todavia Continuamos si esta activada la accion y el termino no se ha añadido todavia
                    if self.permuterm and word not in terms:
                        termAux = word + "$"

                        # Generamos los términos permuterm y actualizamos sus posting lists
                        for _ in range(len(termAux)):
                            self.ptindex[field][termAux] = self.ptindex[field].get(termAux, []) + [newsid]

                            # Añadimos el permuterm si no esta en el diccionario
                            if termAux not in self.pterms:
                                self.pterms[termAux] = []

                            # Añadimos el termino si no esta en la lista de terminos asociados
                            if word not in self.pterms[termAux]:
                                self.pterms[termAux] = self.pterms.get(termAux, []) + [word]
                            termAux = termAux[1:] + termAux[0]
                    #-------------------------------
                    
                    if self.positional:
                        if word in self.posindex[field]:
                            if newsid not in self.posindex[field][word]:
                                self.posindex[field][word][newsid] = [word_pos]
                            else:
                                self.posindex[field][word][newsid].append(word_pos)
                        else:
                            self.posindex[field][word] = {newsid : [word_pos]}
                        word_pos += 1
                    #-------------------------------

                    if word not in terms:
                        # Añadir término a la posting list si no lo hemos añadido
                        self.index[field][word] = self.index[field].get(word, []) + [newsid]
                        terms.add(word)

                        self.weight[field][word] = self.weight[field].get(word,{})
                    
                    # Añadimos la frecuencia del término en el documento y el campo en concreto
                    self.weight[field][word][newsid] = self.weight[field][word].get(newsid,0) + 1
            
            # Incrementar índice de la notícia
            newsid += 1
            news_pos += 1
            

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
            for term in self.index[field]:

                # Si antes no hemos hecho el stemming del termino generamos el stem
                stem = self.stemmer.stem(term)

                # Si aun no hemos añadido el stem lo añadimos
                self.sindex[field][stem] = self.or_posting(self.sindex[field].get(stem, []), self.index[field][term])

    def make_permuterm(self):
        """
        NECESARIO PARA LA AMPLIACION DE PERMUTERM
        Crea el indice permuterm (self.ptindex) para los terminos de todos los indices.
        """

       # Recorremos todos los campos del índice de términos
        for field in self.index:

            # Recorremos todos los términos del campo
            for term in self.index[field]:
                    termAux = term + "$"
                    # Generamos los términos permuterm y actualizamos sus posting lists
                    for i in range(len(termAux)):
                        permuterm = termAux[i:] + termAux[:i]
                        self.ptindex[field][permuterm] = self.or_posting(self.ptindex[field].get(permuterm, []), self.index[field][term])
                        self.pterms[permuterm] = self.pterms.get(permuterm, []) + [term]


    def show_stats(self):
        """
        NECESARIO PARA TODAS LAS VERSIONES
        Muestra estadisticas de los indices
        """
        print('========================================')
        print('Number of indexed days: {}'.format(len(self.docs)))
        print('----------------------------------------')
        print('Number of indexed news: {}'.format(len(self.news)))
        print('----------------------------------------')
        print('TOKENS:')
        for field in self.index.keys():
            print("\t# of tokens in '{}': {}".format(field, len(self.index[field])))
        print('----------------------------------------')
        if self.permuterm:
            print('PERMUTERMS:')
            for field in self.ptindex.keys():
                 print("\t# of permuterms in '{}': {}".format(field, len(self.ptindex[field])))
            print('----------------------------------------')
        if self.stemming:
            print('STEMS:')
            for field in self.sindex.keys():
                 print("\t# of stems in '{}': {}".format(field, len(self.sindex[field])))
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
        if query is None or len(query) == 0:
            return []

        query = query.lower()
        query_split = re.findall("(?:\".*?\"|\S)+", query)

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

        # Se añade el término y campo de la consulta para el ránking
        self.term_field[term] = field
        res = []

        #Caso con búsquedas posicionales
        if self.positional and term[0] == term[-1] == '\"':
            terms = term[1:-1].split() # removes quotes and returns list of words
            res = self.get_positionals(terms, field)
        else:
            #Comprobamos si se debe realizar permuterms
            if self.permuterm and ("*" in term or "?" in term):
                res = self.get_permuterm(term, field)
            #Comprobamos si se debe realizar stemming
            elif self.use_stemming:
                res = self.get_stemming(term, field)
            #Caso estándar
            elif term in self.index[field]:
                res = self.index[field][term]
            
        return res

           
    def get_positionals(self, terms, field='article'):
        """
        NECESARIO PARA LA AMPLIACION DE POSICIONALES
        Devuelve la posting list asociada a una secuencia de terminos consecutivos.
        param:  "terms": lista con los terminos consecutivos para recuperar la posting list.
                "field": campo sobre el que se debe recuperar la posting list, solo necesario se se hace la ampliacion de multiples indices
        return: posting list
        """

        res = []
        if terms[0] in self.posindex[field]:
            for new, positions in self.posindex[field][terms[0]].items():
                for pos in positions:
                    next_pos = True
                    for term in terms[1:]:
                        if next_pos and term in self.posindex[field] \
                        and new in self.posindex[field][term] \
                        and pos + 1 in self.posindex[field][term][new]:
                            pos += 1
                        else:
                            next_pos = False
                    if next_pos:
                        res += [new]

        res = list(dict.fromkeys(res))
        res.sort()
        return res
        

    def get_stemming(self, term, field='article'):
        """
        NECESARIO PARA LA AMPLIACION DE STEMMING
        Devuelve la posting list asociada al stem de un termino.
        param:  "term": termino para recuperar la posting list de su stem.
                "field": campo sobre el que se debe recuperar la posting list, solo necesario se se hace la ampliacion de multiples indices
        return: posting list
        """

        # Creamos stem del termino
        stem = self.stemmer.stem(term)
        res = []

        # Buscamos si esta indexado
        if stem in self.sindex[field]:

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
        
        # Comprobamos que se incluye la palabra comodín y cuál es
        if "*" in term:
            s = "*"
        elif "?" in term:
            s = "?"
        else:
            return []
        
        res = []
        pterm = term + "$"

        # Se hacen permutaciones hasta que el carácter comodín se encuentra en la última posición
        while pterm[len(pterm)-1] != s:
            pterm = pterm[1:] + pterm[0]
        
        #Aqui ya tenemos la palabra que se debe buscar en el ptindex
        if s == "*":
            for element in self.ptindex[field].keys():
                if element[:len(pterm)-1] == pterm[:len(pterm)-1]:
                    #print(element[:len(pterm)-1])
                    res = self.or_posting(res,self.ptindex[field][element])

        else:  # s == "?"
            for element in self.ptindex[field].keys():
                if element[:len(pterm)-1] == pterm[:len(pterm)-1]:
                    #print("out",element)
                    if len(element) <= len(pterm):
                        #print("in", element)
                        res = self.or_posting(res, self.ptindex[field][element])
        return res

        
    def reverse_posting(self, p):
        """
        NECESARIO PARA TODAS LAS VERSIONES
        Devuelve una posting list con todas las noticias excepto las contenidas en p.
        Util para resolver las queries con NOT.
        param:  "p": posting list
        return: posting list con todos los newid exceptos los contenidos en p
        """
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


    def print_snippet(self, news):
        """
        Sacar uno snippet de cada termino con un contexto antes y despues.
        """
        size = 14 # max len of snippet for term
        snippet = ""
        for term, field in self.term_field.items():
            tokens = self.tokenize(news[field])
            pos = -1
            for i, token in enumerate(tokens):
                if token == term:
                    pos = i
                    break
            term_snip = ""
            if pos >= 0:
                for j in range(max((pos - int(size/2) + 1), 0), min(pos + int(size/2), len(tokens) - 1)):
                    term_snip = term_snip + tokens[j] + " "
                snippet += term_snip + " ... "
        print(snippet)


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
        score = 0
        if self.use_ranking:
            result, news_weight = self.rank_result(result, self.term_field)

        print("========================================")
        print('Query:\t' + "'" + query + "'" + '\nNumber of results: ' + str(len(result)))

        for i, newsid in enumerate(result):
            new = self.news[newsid]
            
            filename = self.docs[new['docid']]
            with open(filename) as fh:
                jlist = json.load(fh)

            news = jlist[new['position']]
            
            #Calculo del score en caso de utilizar ranking
            if self.use_ranking: 
                score = round(news_weight[newsid], 2)
            else: 
                score = 0 
            
            if self.show_snippet:
                print("#{}\nScore: {}\n{}\nDate: {}\nTitle: {}\nKeywords: {}"
                .format(i + 1, score, newsid, news['date'], news['title'], news['keywords']))
                self.print_snippet(news)

                if i != len(result) - 1: print("--------------------")
            else:
                print("#{}      ({})  ({})  ({})  {}      ({})"
                .format(i + 1, score, newsid, news['date'], news['title'], news['keywords']))
        print("========================================")

    def rank_result(self, result, query):
        """
        NECESARIO PARA LA AMPLIACION DE RANKING
        Ordena los resultados de una query.
        param:  "result": lista de resultados sin ordenar
                "query": query, puede ser la query original, la query procesada o una lista de terminos
        return: la lista de resultados ordenada, score de la noticia para el ranking
        """
        #Devolveremos las noticias ordenadas en función de su relevancia
        #Pesado tf*idf
        #En caso de utilizar stemming tendremos en cuenta el uso de stems

        terminos = {} #terminos de la query
        for termino, campo in query.items():
            #En caso normal añadimos termino y campo a los terminos de la query
            #En caso de usar stemming añadimos derivs y campo
            
            #Caso stemming
            if self.use_stemming:
                stemmings = self.sterms[self.stemmer.stem(termino)] 
                for t in stemmings:
                    terminos[(t, campo)] = True
            #Caso básico      
            else:
                terminos[(termino, campo)] = True
        
        news_weight = {} # clave: noticia, valor: pesado
        for noticia in result:
            peso_not = 0 #peso de esta noticia
            for termino, campo in terminos:
                #por cada término calculamos su peso
                ftd = self.weight[campo][termino].get(noticia,0) #frecuencia del término
                #Calculo del pesado de la frecuencia del término por pesado log
                if ftd > 0:
                    tf = 1 + math.log10(ftd)
                else:
                    tf = 0
                
                #número de documentos que contienen el término
                df = len(self.weight[campo][termino]) 
                #Calculo de la frecuencia del documento inversa de t
                idf = math.log10(len(self.news)/df)
                
                peso_term = tf * idf #peso del término
                peso_not += peso_term #Sumamos al peso de la noticia el peso de cada término 
            
            #añadimos el pesado de la noticia al rank de pesados
            news_weight[noticia] = peso_not
        
        #Ordenamos las noticias por la lista de pesados  
        ranked_results = [x for _, x in sorted(zip(news_weight.values(), result), reverse=True)]
        return ranked_results, news_weight
