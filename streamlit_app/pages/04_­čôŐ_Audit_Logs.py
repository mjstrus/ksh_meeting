import streamlit as st
from utils.auth import require_auth

require_auth()

st.title("📊 Audit Logs")

st.info("🔧 Audit logs view coming soon. This will show all company actions with timestamps and user info.")
