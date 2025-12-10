from database.DB_connect import DBConnect
from model.connessione_DTO import Connessione
from model.rifugio_DTO import Rifugio
class DAO:
    """
    Implementare tutte le funzioni necessarie a interrogare il database.
    """
    def read_connessioni(self):
        cnx = DBConnect.get_connection()
        cursore = cnx.cursor(dictionary=True)
        query = "select * from connessione"
        cursore.execute(query)
        lista = []
        for i in cursore:
            if i["difficolta"]== "facile":
                oggetto = Connessione(i["id"], i["id_rifugio1"], i["id_rifugio2"], i["distanza"], 1, i["durata"],
                                  i["anno"])
                lista.append(oggetto)
            elif i["difficolta"]== "media":
                oggetto = Connessione(i["id"], i["id_rifugio1"], i["id_rifugio2"], i["distanza"], 1.5, i["durata"],
                                  i["anno"])
                lista.append(oggetto)
            elif i["difficolta"]== "difficile":
                oggetto = Connessione(i["id"], i["id_rifugio1"], i["id_rifugio2"], i["distanza"], 2, i["durata"],
                                  i["anno"])
                lista.append(oggetto)
            else:
                print("errore")
        return lista

    def read_rifugio(self):
        cnx = DBConnect.get_connection()
        cursore = cnx.cursor(dictionary=True)
        query = "select * from rifugio"
        cursore.execute(query)
        lista = []
        for i in cursore:
            oggetto = Rifugio(i["id"], i["nome"], i["localita"], i["altitudine"], i["capienza"], i["aperto"])
            lista.append(oggetto)
        return lista







