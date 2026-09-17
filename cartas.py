import random

class Carta:
    def __init__(self, naipe, valor):
        self.naipe = naipe
        self.valor = valor

    def __repr__(self):
        return f"{self.valor} de {self.naipe}"

class Baralho:
    def __init__(self):
        naipes = ['Copas', 'Paus', 'Ouros', 'Espadas']
        valores = ['Ás', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K']
        self.cartas = [Carta(naipe, valor) for naipe in naipes for valor in valores]
        # Os dois loops for combinados funcionam como um "multiplicador": 
        # para cada naipe na lista de naipes, o código passa por todos os 13 valores.
        
        # Carta(naipe, valor) cria um novo objeto da classe Carta para cada combinação 
        # (ex: 'Ás de Copas', '2 de Copas'... até 'K de Espadas').

    def embaralhar(self):
        random.shuffle(self.cartas)

    def distribuir(self, quantidade):
        mao = []
        for _ in range(quantidade):
            if self.cartas:
                mao.append(self.cartas.pop())
        return mao

# Exemplo de uso
# deck = Baralho()
# deck.embaralhar()
# mao_jogador = deck.distribuir(5)
# print("Mão distribuída:", mao_jogador)
# print("Cartas restantes:", len(deck.cartas))
