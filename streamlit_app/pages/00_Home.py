import streamlit as st
from utils.auth import require_auth

require_auth()

st.title("🏠 Home")
st.write("Welcome! Use the navigation menu to manage your companies and meetings.")
