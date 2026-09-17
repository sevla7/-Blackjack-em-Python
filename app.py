import streamlit as st
from cartas import Baralho

# ---------------------------------------------------------------------------
# Lógica do jogo (mesma regra da versão de terminal, sem prints/input)
# ---------------------------------------------------------------------------

def calcular_valor_carta(carta):
    if carta.valor == 'Ás':
        return 11
    elif carta.valor in ['J', 'Q', 'K']:
        return 10
    else:
        return int(carta.valor)


def calcular_total(mao):
    total = 0
    ases = 0
    for carta in mao:
        if carta.valor == 'Ás':
            ases += 1
        total += calcular_valor_carta(carta)

    while total > 21 and ases > 0:
        total -= 10
        ases -= 1

    return total


def jogar_dealer(mao_dealer, baralho):
    while calcular_total(mao_dealer) < 17:
        mao_dealer.append(baralho.distribuir(1)[0])
    return mao_dealer


def naipe_para_emoji(naipe):
    return {"Copas": "♥️", "Ouros": "♦️", "Paus": "♣️", "Espadas": "♠️"}.get(naipe, "")


def mostrar_carta(carta):
    """Mostra uma carta em um pequeno 'card' visual usando um container do Streamlit."""
    cor = "red" if carta.naipe in ["Copas", "Ouros"] else "black"
    st.markdown(
        f"""
        <div style="
            display:inline-block; border:2px solid #ccc; border-radius:10px;
            padding:10px 16px; margin:4px; text-align:center; min-width:60px;
            background-color:white; color:{cor}; font-weight:bold; font-size:20px;
        ">
            {carta.valor}<br>{naipe_para_emoji(carta.naipe)}
        </div>
        """,
        unsafe_allow_html=True,
    )


def mostrar_verso_carta():
    st.markdown(
        """
        <div style="
            display:inline-block; border:2px solid #ccc; border-radius:10px;
            padding:10px 16px; margin:4px; text-align:center; min-width:60px;
            background-color:#1e3a8a; color:white; font-weight:bold; font-size:20px;
        ">
            🂠
        </div>
        """,
        unsafe_allow_html=True,
    )


def mostrar_mao(mao):
    cols = st.columns(len(mao))
    for col, carta in zip(cols, mao):
        with col:
            mostrar_carta(carta)


# ---------------------------------------------------------------------------
# Estado do jogo (st.session_state guarda os dados entre os "reruns" do
# Streamlit, já que o script inteiro é reexecutado a cada interação)
# ---------------------------------------------------------------------------

def novo_baralho_se_necessario():
    if "baralho" not in st.session_state or len(st.session_state.baralho.cartas) < 15:
        st.session_state.baralho = Baralho()
        st.session_state.baralho.embaralhar()


def iniciar_estado():
    if "fichas" not in st.session_state:
        st.session_state.fichas = 1000
    if "fase" not in st.session_state:
        st.session_state.fase = "aposta"  # aposta -> jogando -> resultado
    novo_baralho_se_necessario()


def iniciar_rodada(aposta):
    st.session_state.aposta = aposta
    st.session_state.fichas -= aposta
    novo_baralho_se_necessario()
    st.session_state.mao_dealer = st.session_state.baralho.distribuir(2)
    st.session_state.mao_jogador = st.session_state.baralho.distribuir(2)
    st.session_state.fase = "jogando"
    st.session_state.mensagem = ""


def pedir_carta():
    nova_carta = st.session_state.baralho.distribuir(1)[0]
    st.session_state.mao_jogador.append(nova_carta)
    if calcular_total(st.session_state.mao_jogador) > 21:
        st.session_state.fase = "resultado"
        st.session_state.mensagem = "💥 Estourou! Você perdeu a aposta."


def parar():
    st.session_state.mao_dealer = jogar_dealer(
        st.session_state.mao_dealer, st.session_state.baralho
    )
    total_dealer = calcular_total(st.session_state.mao_dealer)
    total_jogador = calcular_total(st.session_state.mao_jogador)
    aposta = st.session_state.aposta

    if total_dealer > 21 or total_jogador > total_dealer:
        st.session_state.fichas += aposta * 2
        st.session_state.mensagem = "🎉 Você ganhou!"
    elif total_jogador < total_dealer:
        st.session_state.mensagem = "😢 Você perdeu."
    else:
        st.session_state.fichas += aposta
        st.session_state.mensagem = "🤝 Empate."

    st.session_state.fase = "resultado"


def nova_rodada():
    st.session_state.fase = "aposta"


# ---------------------------------------------------------------------------
# Interface
# ---------------------------------------------------------------------------

st.set_page_config(page_title="Blackjack", page_icon="🃏")
st.title("🃏 Blackjack")

iniciar_estado()

st.metric("💰 Saldo", f"{st.session_state.fichas:.2f}")

if st.session_state.fichas <= 0:
    st.error("💸 Você ficou sem fichas! Fim de jogo.")
    st.stop()

# --- Fase de aposta ---------------------------------------------------------
if st.session_state.fase == "aposta":
    aposta = st.number_input(
        "Valor da aposta",
        min_value=1.0,
        max_value=float(st.session_state.fichas),
        value=min(50.0, float(st.session_state.fichas)),
        step=1.0,
    )
    if st.button("▶️ Iniciar rodada"):
        iniciar_rodada(aposta)
        st.rerun()

# --- Fase de jogo (jogador decide pedir carta ou parar) --------------------
elif st.session_state.fase == "jogando":
    st.subheader("🎩 Mão do Dealer")
    cols = st.columns(2)
    with cols[0]:
        mostrar_carta(st.session_state.mao_dealer[0])
    with cols[1]:
        mostrar_verso_carta()

    st.subheader("🙋 Sua mão")
    mostrar_mao(st.session_state.mao_jogador)
    total_jogador = calcular_total(st.session_state.mao_jogador)
    st.write(f"**Total: {total_jogador}**")

    col1, col2 = st.columns(2)
    with col1:
        if st.button("🃏 Pedir carta"):
            pedir_carta()
            st.rerun()
    with col2:
        if st.button("✋ Parar"):
            parar()
            st.rerun()

# --- Fase de resultado -------------------------------------------------------
elif st.session_state.fase == "resultado":
    st.subheader("🎩 Mão final do Dealer")
    mostrar_mao(st.session_state.mao_dealer)
    st.write(f"Total: {calcular_total(st.session_state.mao_dealer)}")

    st.subheader("🙋 Sua mão final")
    mostrar_mao(st.session_state.mao_jogador)
    st.write(f"Total: {calcular_total(st.session_state.mao_jogador)}")

    if "Ganhou" in st.session_state.mensagem or "ganhou" in st.session_state.mensagem:
        st.success(st.session_state.mensagem)
    elif "perdeu" in st.session_state.mensagem or "Estourou" in st.session_state.mensagem:
        st.error(st.session_state.mensagem)
    else:
        st.info(st.session_state.mensagem)

    if st.button("🔄 Nova rodada"):
        nova_rodada()
        st.rerun()