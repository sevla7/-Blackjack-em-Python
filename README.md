# 🃏 Blackjack em Python

Jogo de Blackjack (21) para terminal, feito em Python puro, com um baralho de cartas representado por classes próprias.

## Como jogar

```bash
python blackjack.py
```

- Aperte **ENTER** para iniciar uma rodada, ou digite **q** a qualquer momento para sair.
- Defina o valor da sua aposta.
- A cada rodada, escolha:
  - **p** — pedir carta (hit)
  - **s** — parar (stand)
- Se sua mão passar de 21, você estoura e perde a aposta.
- Se você parar sem estourar, o dealer joga automaticamente seguindo a regra oficial: pede carta enquanto tiver menos de 17 pontos, e para a partir de 17 (**S17** — para em qualquer 17, inclusive soft).
- Ganha quem tiver o maior total sem ultrapassar 21. Em caso de empate, a aposta é devolvida.

## Estrutura do projeto

```
.
├── blackjack.py   # Lógica principal do jogo (apostas, turnos, dealer, resultado)
└── cartas.py      # Classes Carta e Baralho (criação, embaralhamento, distribuição)
└── stream.py      # Próxima atualização (interface do jogo)
```

### `cartas.py`
- **`Carta`**: representa uma carta com `naipe` e `valor`.
- **`Baralho`**: monta as 52 cartas (4 naipes × 13 valores), com métodos para embaralhar (`embaralhar`) e distribuir (`distribuir`) cartas, removendo-as do baralho conforme são compradas.

Esse arquivo aplica conceitos de **Programação Orientada a Objetos (POO)** vistos na faculdade:
- **Classes e objetos**: `Carta` e `Baralho` são classes; cada carta sorteada é uma instância (objeto) de `Carta`.
- **Encapsulamento**: o `Baralho` guarda a lista de cartas (`self.cartas`) e expõe métodos (`embaralhar`, `distribuir`) para manipulá-la, em vez de deixar o restante do código mexer diretamente na lista.
- **Atributos de instância**: `naipe` e `valor` (em `Carta`) e `cartas` (em `Baralho`) são definidos no `__init__` e pertencem a cada objeto individualmente.
- **Métodos especiais (dunder methods)**: `__repr__` em `Carta` customiza como o objeto aparece quando impresso (ex: `"Ás de Copas"`), em vez do padrão do Python (`<Carta object at 0x...>`).
- **Composição**: `Baralho` é formado por uma lista de objetos `Carta` — um objeto contendo outros objetos.


### `blackjack.py`
- **`calcular_valor_carta` / `calcular_total` / `calcular_mao`**: convertem cartas em pontuação, tratando o Ás como 11 ou 1 (o que for melhor pra não estourar 21).
- **`jogar_dealer`**: joga automaticamente a mão do dealer, seguindo a regra fixa dos 17 pontos.
- **`jogo`**: controla uma rodada — aposta, turno do jogador (hit/stand), turno do dealer e apuração do resultado.
- **`banco`**: aplica o resultado da rodada ao saldo de fichas.
- Loop principal: gerencia o saldo entre rodadas e recria o baralho automaticamente quando restam poucas cartas (menos de 15), evitando mãos incompletas.

## Possíveis melhorias futuras

- Suporte a múltiplos jogadores.
- Opção de dobrar aposta (double down) e dividir mão (split).
- Regra alternativa H17 (dealer pede carta em soft 17).
- Persistência do saldo entre execuções do jogo.
