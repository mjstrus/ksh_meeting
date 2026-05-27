import streamlit as st
import hashlib


# --- Przykładowi użytkownicy (docelowo: baza danych / secrets.toml) ---
USERS = {
    "admin": hashlib.sha256("admin123".encode()).hexdigest(),
    "user1": hashlib.sha256("haslo123".encode()).hexdigest(),
}


def hash_password(password: str) -> str:
    return hashlib.sha256(password.encode()).hexdigest()


def check_credentials(username: str, password: str) -> bool:
    hashed = hash_password(password)
    return USERS.get(username) == hashed


def login_form():
    """Wyświetla formularz logowania i zarządza sesją."""
    if "logged_in" not in st.session_state:
        st.session_state.logged_in = False
        st.session_state.username = ""

    if not st.session_state.logged_in:
        st.title("🔐 Logowanie")
        with st.form("login_form"):
            username = st.text_input("Login")
            password = st.text_input("Hasło", type="password")
            submitted = st.form_submit_button("Zaloguj")

            if submitted:
                if check_credentials(username, password):
                    st.session_state.logged_in = True
                    st.session_state.username = username
                    st.rerun()
                else:
                    st.error("❌ Nieprawidłowy login lub hasło")
        st.stop()


def logout():
    """Wylogowuje użytkownika."""
    st.session_state.logged_in = False
    st.session_state.username = ""
    st.rerun()


def require_login():
    """Dekorator / wywołanie wymagające zalogowania."""
    login_form()
