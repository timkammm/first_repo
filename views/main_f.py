import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objs as go
import time

# Инициализация состояния
if "wallet" not in st.session_state:
    st.session_state.wallet = 100
if "portfolio" not in st.session_state:
    st.session_state.portfolio = {f"Акция {i+1}": 0 for i in range(9)}
if "prices" not in st.session_state:
    st.session_state.prices = pd.DataFrame({
        "Акция 1": [100], "Акция 2": [110], "Акция 3": [90],
        "Акция 4": [120], "Акция 5": [95], "Акция 6": [85],
        "Акция 7": [200], "Акция 8": [180], "Акция 9": [160]
    })
if "day" not in st.session_state:
    st.session_state.day = 0
if "economy" not in st.session_state:
    st.session_state.economy = "Среднее"

# Функция для симуляции экономики
def simulate_economy():
    state = np.random.choice(["Хорошее", "Среднее", "Плохое"], p=[0.3, 0.4, 0.3])
    st.session_state.economy = state

# Функция для генерации новых цен акций
def update_prices():
    economy = st.session_state.economy
    trends = {
        "Хорошее": [0.05, 0.1],
        "Среднее": [-0.02, 0.02],
        "Плохое": [-0.1, -0.05]
    }
    current_prices = st.session_state.prices.iloc[-1].values
    new_prices = current_prices + current_prices * np.random.uniform(*trends[economy], size=len(current_prices))
    st.session_state.prices.loc[st.session_state.day] = new_prices

# Покупка акций
def buy_stock(stock, amount):
    price = st.session_state.prices.iloc[-1][stock]
    total_cost = price * amount
    if st.session_state.wallet >= total_cost:
        st.session_state.wallet -= total_cost
        st.session_state.portfolio[stock] += amount
        st.success(f"Куплено {amount} акций {stock} за {total_cost:.2f} монет.")
    else:
        st.error("Недостаточно средств.")

# Продажа акций
def sell_stock(stock, amount):
    if st.session_state.portfolio[stock] >= amount:
        price = st.session_state.prices.iloc[-1][stock]
        total_gain = price * amount
        st.session_state.wallet += total_gain
        st.session_state.portfolio[stock] -= amount
        st.success(f"Продано {amount} акций {stock} за {total_gain:.2f} монет.")
    else:
        st.error("Недостаточно акций для продажи.")

# Интерфейс
st.title("Игра: Управляй Акциями")

# Боковая панель
st.sidebar.header("Ваш портфель")
st.sidebar.write(f"Монеты: {st.session_state.wallet:.2f}")
st.sidebar.write("Акции:")
for stock, count in st.session_state.portfolio.items():
    st.sidebar.write(f"{stock}: {count}")

# Покупка и продажа акций
st.header("Покупка и продажа акций")
col1, col2 = st.columns(2)
with col1:
    stock_to_buy = st.selectbox("Выберите акцию для покупки", st.session_state.portfolio.keys())
    amount_to_buy = st.number_input("Количество акций для покупки", min_value=1, step=1)
    if st.button("Купить"):
        buy_stock(stock_to_buy, amount_to_buy)
with col2:
    stock_to_sell = st.selectbox("Выберите акцию для продажи", st.session_state.portfolio.keys())
    amount_to_sell = st.number_input("Количество акций для продажи", min_value=1, step=1)
    if st.button("Продать"):
        sell_stock(stock_to_sell, amount_to_sell)

# Раздел симуляции
st.header("Симуляция")

# Уведомления и график
notification_placeholder = st.empty()
graph_placeholder = st.empty()

# Автоматическая симуляция
if st.button("Запустить симуляцию"):
    for _ in range(10000):  # Ограниченный цикл, чтобы не было бесконечной блокировки
        st.session_state.day += 1

        # Каждые 360 дней меняется экономика
        if st.session_state.day % 360 == 0:
            simulate_economy()

        # Каждые 90 дней выводится отчет
        if st.session_state.day % 90 == 0:
            notification_placeholder.info(f"День {st.session_state.day}: Новый отчет! Экономика: {st.session_state.economy}")

        # Обновляем цены
        update_prices()

        # Обновляем график
        selected_stocks = st.session_state.prices.columns
        fig = go.Figure()
        for stock in selected_stocks:
            fig.add_trace(go.Scatter(x=st.session_state.prices.index, y=st.session_state.prices[stock], mode='lines', name=stock))
        graph_placeholder.plotly_chart(fig, use_container_width=True)

        # Пауза в 1 секунду
        time.sleep(1)
