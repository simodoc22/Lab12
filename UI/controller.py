import flet as ft
from UI.view import View
from model.model import Model


class Controller:
    def __init__(self, view: View, model: Model):
        self._view = view
        self._model = model

    def handle_grafo(self, e):
        """Callback per il pulsante 'Crea Grafo'."""
        try:
            anno = int(self._view.txt_anno.value)
        except:
            self._view.show_alert("Inserisci un numero valido per l'anno.")
            return
        if anno < 1950 or anno > 2024:
            self._view.show_alert("Anno fuori intervallo (1950-2024).")
            return

        self._model.build_weighted_graph(anno)
        self._view.lista_visualizzazione_1.controls.clear()
        self._view.lista_visualizzazione_1.controls.append(
            ft.Text(f"Grafo calcolato: {self._model.G.number_of_nodes()} nodi, {self._model.G.number_of_edges()} archi")
        )
        min_p, max_p = self._model.get_edges_weight_min_max()
        self._view.lista_visualizzazione_1.controls.append(ft.Text(f"Peso min: {min_p:.2f}, Peso max: {max_p:.2f}"))
        self._view.page.update()

    def handle_conta_archi(self, e):
        """Callback per il pulsante 'Conta Archi'."""
        try:
            soglia = float(self._view.txt_soglia.value)
        except:
            self._view.show_alert("Inserisci un numero valido per la soglia.")
            return

        min_p, max_p = self._model.get_edges_weight_min_max()
        if soglia < min_p or soglia > max_p:
            self._view.show_alert(f"Soglia fuori range ({min_p:.2f}-{max_p:.2f})")
            return

        minori, maggiori = self._model.count_edges_by_threshold(soglia)
        self._view.lista_visualizzazione_2.controls.clear()
        self._view.lista_visualizzazione_2.controls.append(ft.Text(f"Archi < {soglia}: {minori}, Archi > {soglia}: {maggiori}"))
        self._view.page.update()

    """Implementare la parte di ricerca del cammino minimo"""
    def handle_camminominimo(self,e):

        self._view.lista_visualizzazione_3.controls.clear()

        lista_minimi = self._model.calcolo_percorso_minimo(float(self._view.txt_soglia.value))
        """""""""""""""
        lista_minimi,valore = self._model.calcolo_percorso_minimo2(float(self._view.txt_soglia.value))
        """""""""""""""
        if lista_minimi:
            minimo = lista_minimi[0][1]
            percorso = lista_minimi[0][0]
            self._view.lista_visualizzazione_3.controls.append(ft.Text("cammino/i minimo/i"))
            numero = 0
            for i in lista_minimi:
                if i[1] == minimo:
                    numero +=1
                    percorso = i[0]
                    self._view.lista_visualizzazione_3.controls.append(ft.Text(f"Percorso {numero} "))
                    for i in range(len(percorso)-1):
                        partenza=percorso[i]
                        arrivo = percorso[i+1]
                        peso = self._model.G.get_edge_data(partenza, arrivo,)
                        self._view.lista_visualizzazione_3.controls.append(ft.Text(f"{partenza}  -->  {arrivo} il percorso ha un peso di {peso}"))
            self._view.page.update()
        else:
            self._view.lista_visualizzazione_3.controls.append(ft.Text(f"{[]}"))
            self._view.lista_visualizzazione_3.controls.append(ft.Text("non risulta essere presente un cammino che rispetti i vincoli"))
            self._view.page.update()

        """"""""""""""" altro metodo sfruttando documentazione networkx
        if lista_minimi:
            self._view.lista_visualizzazione_3.controls.append(ft.Text("cammino/i minimo/i"))
            self._view.lista_visualizzazione_3.controls.append(
                ft.Text(f"{lista_minimi[0]}  -->  {lista_minimi[len(lista_minimi)-1]} il percorso ha un peso di {valore}"))
            self._view.page.update()
        else:
            self._view.lista_visualizzazione_3.controls.append(ft.Text("cammino/i minimo/i"))
            self._view.lista_visualizzazione_3.controls.append(ft.Text(f"{[]}"))
            self._view.page.update()
        """""""""""""""""


