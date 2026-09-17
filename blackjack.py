import random as rd
import time
import sys  # para ler a entrada do usuário (Enter ou q)
import os   # para limpar o terminal
from cartas import Baralho

baralho = Baralho()
fichas = 1000  # 💰 Saldo inicial do jogador


def banco(aposta, ganhou, fichas):
    """
    Aplica o resultado da rodada ao saldo e devolve o novo valor.
    'ganhou' é um booleano (True/False) que diz se o jogador venceu a rodada.
    Se ganhou, ele recebe o dobro da aposta (a aposta original + o prêmio).
    """
    if ganhou:
        fichas += aposta * 2
    return fichas


def dealer():
    """🎩 Sorteia (distribui) as duas cartas iniciais do dealer."""
    return baralho.distribuir(2)


def jogador():
    """🙋 Sorteia (distribui) as duas cartas iniciais do jogador."""
    return baralho.distribuir(2)


def mostrar_animacao():
    for _ in range(5):
        print(" 🃏 | 🃏", end="\r")  # end="\r": volta o cursor pro início da linha, criando animação
        time.sleep(0.2)
        print(" " * 20, end="\r")   # apaga o texto anterior escrevendo espaços em branco por cima


def calcular_valor_carta(carta):
    """Converte o valor textual da carta ('Ás', 'J', 'Q', 'K', números) no valor numérico do blackjack."""
    if carta.valor == 'Ás':
        return 11  # Ás começa valendo 11; é ajustado para 1 depois, se a mão estourar
    elif carta.valor in ['J', 'Q', 'K']:
        return 10  # figuras sempre valem 10
    else:
        return int(carta.valor)  # cartas numéricas: converte a string ('2'..'10') pra int


def calcular_total(mao):
    """
    Calcula o total de uma mão (lista de objetos Carta), já tratando o Ás flexível.
    'ases' conta quantos Ases estão sendo contados como 11 no momento.
    """
    total = 0
    ases = 0
    for carta in mao:
        if carta.valor == 'Ás':
            ases += 1
        total += calcular_valor_carta(carta)

    # Enquanto a mão estourar 21 e ainda houver Ás valendo 11,
    # rebaixa um Ás de cada vez (11 -> 1, ou seja, -10 no total)
    while total > 21 and ases > 0:
        total -= 10
        ases -= 1

    return total


def calcular_mao(mao_dealer, mao_jogador):
    """Atalho que devolve os dois totais (dealer, jogador) de uma vez."""
    return calcular_total(mao_dealer), calcular_total(mao_jogador)


def jogar_dealer(mao_dealer):
    """
    🎩 O dealer não escolhe nada: segue a regra fixa do blackjack.
    Pede carta enquanto o total for menor que 17, e para (stand) a partir de 17.
    """
    while calcular_total(mao_dealer) < 17:
        nova_carta = baralho.distribuir(1)[0]
        mao_dealer.append(nova_carta)
        print(f"🎩 Dealer pediu carta e recebeu: {nova_carta}")
        time.sleep(0.4)  # pequena pausa só pra dar ritmo à leitura

    print(f"🎩 Dealer parou com {calcular_total(mao_dealer)} pontos.\n")
    return mao_dealer


def inicio():
    """Pergunta se o jogador quer começar (ENTER) ou sair ('q')."""
    tecla = input("👉 Aperte ENTER para iniciar (ou 'q' para sair): ")
    # .strip() remove espaços em branco extras do início/fim do texto digitado
    # .lower() deixa tudo minúsculo, pra aceitar 'Q', 'q', ' q ' etc. como saída
    if tecla.strip().lower() != 'q':
        print("🎲 Embaralhando...")
        baralho.embaralhar()
    return tecla, fichas


def jogo(fichas, mao_dealer, mao_jogador):
    print("🃏 Bem vindo ao Blackjack! 🃏\n")
    print(f"💰 Seu saldo: {fichas}\n")
    aposta = float(input("💵 Digite o valor da aposta: "))
    fichas -= aposta  # desconta a aposta do saldo assim que ela é feita
    print(f"\n🎩 Mão Dealer: {mao_dealer[0]} | 🃏 |")  # segunda carta do dealer fica escondida

    # 🔁 Loop de decisões do jogador: pedir carta (hit) ou parar (stand)
    while True:
        total_jogador = calcular_total(mao_jogador)
        # ', '.join(...) transforma a lista de cartas numa string única, separada por vírgulas
        print(f"🙋 Sua mão: {', '.join(str(c) for c in mao_jogador)}")
        print(f"➡️  Total atual: {total_jogador}")

        if total_jogador > 21:
            print("💥 Estourou! Você perdeu a aposta.\n")
            return fichas  # a aposta já foi descontada lá em cima, então não é devolvida

        escolha = input("🎯 Pedir carta (p) ou parar (s)? ").strip().lower()

        if escolha == 'p':
            nova_carta = baralho.distribuir(1)[0]
            mao_jogador.append(nova_carta)
            print(f"🃏 Você recebeu: {nova_carta}\n")
        elif escolha == 's':
            break  # sai do loop e segue pra vez do dealer
        else:
            print("⚠️ Opção inválida, digite 'p' ou 's'.\n")

    # 🎩 Agora que o jogador parou (sem estourar), o dealer joga sua rodada automática
    mao_dealer = jogar_dealer(mao_dealer)

    total_dealer = calcular_total(mao_dealer)
    total_jogador = calcular_total(mao_jogador)

    print(f"🎩 Mão final do dealer: {', '.join(str(c) for c in mao_dealer)} (Total: {total_dealer})")
    print(f"🙋 Mão final do jogador: {', '.join(str(c) for c in mao_jogador)} (Total: {total_jogador})\n")

    if total_dealer > 21 or total_jogador > total_dealer:
        print("🎉 Você ganhou!")
        fichas = banco(aposta, True, fichas)
    elif total_jogador < total_dealer:
        print("😢 Você perdeu.")
    else:
        print("🤝 Empate.")
        fichas += aposta  # empate devolve a aposta pro jogador

    print(f"💰 Saldo atual: {fichas}\n")
    return fichas

fichas = float(input("💰 Digite o valor inicial de fichas: "))
# 🔁 Loop principal do jogo: roda rodada após rodada até o jogador sair ou zerar as fichas
while True:
    tecla, fichas = inicio()
    if tecla.strip().lower() == 'q':
        print("🔴 Encerrando...")
        time.sleep(0.2)
        break

    if fichas <= 0:
        print("💸 Você ficou sem fichas! Fim de jogo.")
        break

    mao_dealer = dealer()
    mao_jogador = jogador()
    mostrar_animacao()
    fichas = jogo(fichas, mao_dealer, mao_jogador)