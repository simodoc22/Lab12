import networkx as nx
from database.dao import DAO

class Model:
    def __init__(self):
        """Definire le strutture dati utili"""
        self.dao = DAO()
        self.lista_rifugi = self.dao.read_rifugio()
        self.dizionario_rifugi= {}
        for i in self.lista_rifugi:
            self.dizionario_rifugi[i.id] = i
        self.lista_connessioni = self.dao.read_connessioni()
        self.dizionario_connessioni = {}
        for i in self.lista_connessioni:
            self.dizionario_connessioni[(i.id1,i.id2)]= i
        self.G = nx.Graph()



    def build_weighted_graph(self, year: int):
        """
        Costruisce il grafo pesato dei rifugi considerando solo le connessioni con campo `anno` <= year passato
        come argomento.
        Il peso del grafo è dato dal prodotto "distanza * fattore_difficolta"
        """
        for i in self.lista_connessioni:
            if i.anno <= year:
                self.G.add_node(self.dizionario_rifugi[i.id1])
                self.G.add_node(self.dizionario_rifugi[i.id2])
                self.G.add_edge(self.dizionario_rifugi[i.id1],self.dizionario_rifugi[i.id2],weight = float(i.distanza)*float(i.difficolta))

    def get_edges_weight_min_max(self):
        """
        Restituisce min e max peso degli archi nel grafo
        :return: il peso minimo degli archi nel grafo
        :return: il peso massimo degli archi nel grafo
        """
        lista = []
        for u,v in self.G.edges():
            peso = self.G[u][v]['weight']
            lista.append(peso)

        return min(lista),max(lista)

    def count_edges_by_threshold(self, soglia):
        """
        Conta il numero di archi con peso < soglia e > soglia
        :param soglia: soglia da considerare nel conteggio degli archi
        :return minori: archi con peso < soglia
        :return maggiori: archi con peso > soglia
        """
        minori = 0
        maggiori = 0
        for u,v in self.G.edges():
            if self.G[u][v]['weight'] < soglia:
                minori += 1
            elif self.G[u][v]['weight'] > soglia:
                maggiori += 1
            else:
                pass
        return minori,maggiori

    def ricorsione(self, lista, lista_parziale, node, peso, soglia,minimo_valore):

        if len(lista_parziale) == 0:
            lista_parziale.append(node)   ##appendo alla lista il primo nodo che e il punto di partenza di ogni combinazione

        if len(lista_parziale) > 2:
            lista.append((lista_parziale.copy(), peso))  ##verifico la condizione che siano presenti almeno 3 nodi

            if peso<= minimo_valore[0]:  ##inoltre aggiorno il peso minimo in modo tale da filtrare in modo efficiente
                minimo_valore[0] = peso


        for vicino in self.G.neighbors(node):  ##per ogni vicino del nodo di partenza applico ricorsione

            if vicino in lista_parziale:
                continue

            peso1 = self.G[node][vicino]['weight']

            if peso1 <= soglia:   ##se non rispetta la condizione di soglia termino il ramo(efficienza)
                continue

            nuovo_peso = peso + peso1 ##in caso contrario aggiorno il nuovo peso

            if nuovo_peso >= minimo_valore[0]:  ##controllo subito che sia minore del peso minimo gia trovato in caso contrario termino il ramo
                continue

            lista_parziale.append(vicino) ##se tutti i controlli sono soddisfatti appendo
            self.ricorsione(lista, lista_parziale, vicino, nuovo_peso, soglia, minimo_valore)
            lista_parziale.pop() ##elimino ultimo elemento per continuare ricorsione






    def calcolo_percorso_minimo(self, soglia):

        lista_minimi = []  # conterrà TUTTI i minimi (anche multipli)

        for node in self.G.nodes():
            lista = []
            minimo_valore = [float("inf")]          # reset per ogni nodo
            self.ricorsione(lista, [], node, 0, soglia,minimo_valore)
            if not lista:
                continue

            # ordina lista per peso
            lista.sort(key=lambda x: x[1])

            # trova il peso minimo
            peso_min = minimo_valore[0]

            # aggiungi TUTTI i percorsi con questo peso
            for percorso, peso in lista:
                if peso == peso_min:
                    lista_minimi.append((percorso, peso))
                else:
                    break  # la lista è ordinata, tutto dopo è > minimo

        # opzionale: ordina anche i minimi
        lista_minimi.sort(key=lambda x: x[1])

        return lista_minimi


"""Implementare la parte di ricerca del cammino minimo"""
""""""""""""""" sfrutto metodi networkx per risolvere il problema
    def calcolo_percorso_minimo2(self, soglia):
        G2 = nx.Graph()
        for node in self.G.nodes():
            G2.add_node(node)
        for i in self.lista_connessioni:
            if float(i.distanza) * float(i.difficolta) > soglia:
                G2.add_edge(self.dizionario_rifugi[i.id1], self.dizionario_rifugi[i.id2],
                                weight=float(i.distanza) * float(i.difficolta))
        miglior_cammino = None
        miglior_peso = float("inf")
        for node in G2.nodes():
            for node2 in G2.nodes():
                if node == node2:
                    continue
                try:
                    cammino = nx.dijkstra_path(G2, node, node2, weight="weight")

                    if len(cammino) < 3:
                        continue      ##se i nodi sono solo due termino il ramo

                    peso = nx.path_weight(G2, cammino, weight="weight")

                    if peso < miglior_peso:
                        miglior_peso = peso
                        miglior_cammino = cammino

                except nx.NetworkXNoPath:
                    pass
        if miglior_cammino is None:
            return []
        return miglior_cammino,miglior_peso
"""""""""""""""""










