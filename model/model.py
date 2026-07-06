import itertools

import networkx as nx

from database.DAO import DAO


class Model:
    def __init__(self):
        self._grafo=nx.Graph()
        self._teams=[]

    def getAllYears(self):
        return DAO.getAllYears()

    def getTeamsOfYear(self, year):
        self._teams=DAO.getTeamsOfYear(year) #con self diventa una variabile di classe che posso usare per la creaz del grafo
        self._idMapTeams = {t.ID: t for t in self._teams}  # dictionary completions- riempo anche L'ID MAP
        return self._teams

    def creaGrafo(self, year):
        self._grafo.clear()
        self._grafo.add_nodes_from(self._teams)

        #il grafo è completo e semplice, ma pesato
        #for u in self._grafo.nodes:
           # for v in self._grafo.nodes: #ciclo 2 volte sui nodi
              #  if u!=v:
                 #   self._grafo.add_edge(u, v) #aggiunge un arco

        # OPPURE POSSO USARE UNA LIBRERIA  itertools
        myedges=list(itertools.combinations(self._teams, 2)) #devo passargli un iterable e le quantità con cui fare i nodi
        self._grafo.add_edges_from(myedges)                                                       #a 2 a 2
       # print(myedges)

        #chiedo al DAO il diz direlaz tema- salari
        mapSalary = DAO.getSalariesTeam(year,self._idMapTeams)
        for e in self._grafo.edges:
            sal1=mapSalary[e[0]]
            sal2=mapSalary[e[1]]
            peso=sal1+sal2
            #assegno il peso
            self._grafo[e[0]][e[1]]['weight']=peso
            #potevo scrivere in modo più comppatto
           # self._grafo[e[1]][e[0]][e["weight"]]=mapSalary[e[0]]+mapSalary[e[1]]
        print("test")

    def getVicini(self, source):
        #cercare tutti i vicini di source
        vicini=self._grafo.neighbors(source)
        viciniTuples=[]
        for v in vicini:
            #viciniTuples.append(self._grafo[source][v]['weight']) #vicino aggiunto
            peso = self._grafo[source][v]['weight']
            viciniTuples.append((v, peso))
        viciniTuples.sort(key=lambda x: x[1], reverse=True)
        return viciniTuples


    def getGraphDetails(self):
        return len(self._grafo.nodes), len(self._grafo.edges)


