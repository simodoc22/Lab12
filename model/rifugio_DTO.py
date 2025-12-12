class Rifugio():
    def __init__(self,id,nome,localita,altitudine,capienza,aperto):
        self.id = id
        self.nome = nome
        self.localita = localita
        self.altitudine = altitudine
        self.capienza = capienza
        self.aperto = aperto

    def __eq__(self, other):
        return self.id == other.id

    def __hash__(self):
        return hash(self.id)

    def __str__(self):
        return f'Rifugio {self.id} {self.nome}'