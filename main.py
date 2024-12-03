import streamlit as st

# Пример данных пользователей
USER_DATA = {
    "timur": "1234"  # замените на настоящие данные
}

def login(username, password):
    if username in USER_DATA and USER_DATA[username] == password:
        return True
    return False

# Проверяем, есть ли активная сессия
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False

# Если пользователь не вошел в систему, показываем форму логина
if not st.session_state.logged_in:
    st.title("Login")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    
    if st.button("Login"):
        if login(username, password):
            st.session_state.logged_in = True
            st.success("Successfully logged in!")
        else:
            st.error("Неверный логин или пароль.")
else:

    # Здесь можно добавить навигацию и другие функции вашего приложения
    about_page = st.Page(
        page="views/about.py",
        title="About Us",
        default=True,
    )

    page_main = st.Page(
        page="views/main_f.py",
        title="Main Page",
    )

    nav = st.navigation(
        {
            "About": [about_page],
            "Main": [page_main]
        }
    )

    nav.run()