import copy
import itertools
import random
import networkx as nx
from requests.utils import prepend_scheme_if_needed
from database.DAO import DAO


class Model():
    def __init__(self):
        self._grafo=nx.Graph()
        self._teams=[]
        self._idMapTeams=None

        self._bestPath=[]
        self._bestObjVal=0

    def getPath(self, v0): #prende il solo nodo di partenza
        self._bestPath = []
        self._bestObjVal = 0

        parziale=[v0]
        for v in self._grafo.neighbors(v0):
            parziale.append(v)
            self._ricorsione(parziale)
            parziale.pop()

    def getPathV2(self, v0): #prende il solo nodo di partenza
        self._bestPath = []
        self._bestObjVal = 0

        parziale=[v0]
        listaVicini = self.getVicini(parziale[-1])  # USO LA FUNZIONE CHE AVEVO GIà ed è già ordinata
        parziale.append(listaVicini[0][0]) #nodo succ e peso arco magg (miglior nodo)
        self._ricorsioneV2(parziale)

        return self._bestPath, self._bestObjVal
    #potrei anche restituire delle tuple in modo da verificare che il pesi non sino decresc


    def _ricorsione(self, parziale):
        print(len(parziale))
        #1) CONDIZIONE DI OTTIMALITA- verifico se parziale è migliore di best
        if self._score(parziale)>self._bestObjVal:
            self._bestPath = copy.deepcopy(parziale)
            self._bestObjVal=self._score(parziale)

        #2) CONDIZIONE DI TERMINAZIONE- verifico se posso continuare
            #quando non ha più senso aggiungere nodi?
        #   QUI NON LA HO, NON HO UN MAX

        #3)RICORSIONE
        for v in self._grafo.neighbors(parziale[-1]):
            pesoE=self._grafo[parziale[-1]][v]['weight'] #deve essere più piccolo del peso dell'ultimo arco che ho aggiunto

            if self._grafo[parziale[-2]][parziale[-1]]['weight']>pesoE and v not in parziale:
                parziale.append(v)
                self._ricorsione(parziale)
                parziale.pop()

    def _ricorsioneV2(self, parziale):
        # 1) CONDIZIONE DI OTTIMALITA- verifico se parziale è migliore di best
        if self._score(parziale) > self._bestObjVal:
            self._bestPath = copy.deepcopy(parziale)
            self._bestObjVal = self._score(parziale)

        # 2) CONDIZIONE DI TERMINAZIONE- verifico se posso continuare
        # quando non ha più senso aggiungere nodi?
        #   QUI NON LA HO, NON HO UN MAX

        # 3)RICORSIONE
        #listaVicini=[]
        #for v in self._grafo.neighbors(parziale[-1]):
           # edgeV=self._grafo[parziale[-1]][v]['weight']  #pero arco che mi ha portato da parziale -1 a v
          #  listaVicini.append((v,edgeV)) #così la posso ordinare

        #listaVicini.sort(key=lambda x: x[1])

        listaVicini=self.getVicini(parziale[-1]) #USO LA FUNZIONE CHE AVEVO GIà ed è già ordinata

        for v in listaVicini:
            if v[0] not in parziale and self._grafo[parziale[-2]][parziale[-1]]['weight']>v[1]: #sto ciclamdo sulla tupla
                parziale.append(v[0])
                self._ricorsioneV2(parziale)
                parziale.pop()
                return #nel momento in cui ho trovato il migliore, evito si esplorare le altre strade che hannoo archi minori
        #in questo caso, dovrebbe trovare la solu ottima, ma visto come è costuito il grafo, dovrebbe trovarla
        #IN GENERALE NON è UNA SOLUZ GLOBALMENTE OTTIMA, MA L'ALTRA NON FINISCE PK TROPPO LENTA



    def _score(self,parziale):
       # esplora la soluz parziale e sommai pesi
        score=0
        for i in range(0, len(parziale)-1):
            score +=self._grafo[parziale[i]][parziale[i+1]]['weight']
        return score

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


    def getRandomNode(self):
        index=random.randint(0,len(self._teams)-1)
        return self._teams[index]

