import streamlit as st
from utils.auth import get_current_user, logout, login, signup
from datetime import datetime

st.set_page_config(
    page_title="KSH Meeting Hub",
    page_icon="📋",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize session state
if "user" not in st.session_state:
    st.session_state.user = None
if "token" not in st.session_state:
    st.session_state.token = None

# Sidebar
with st.sidebar:
    st.title("KSH Meeting Hub")
    
    user = get_current_user()
    if user:
        st.write(f"👤 **{user.email}**")
        if st.button("🚪 Logout"):
            logout()
            st.rerun()
    else:
        st.write("👤 Not logged in")

# Main content
if get_current_user():
    st.title("🎯 KSH Meeting Hub")
    st.write("Welcome! Use the navigation menu to manage your companies and meetings.")
else:
    st.title("🔐 KSH Meeting Hub")
    
    tab1, tab2 = st.tabs(["Login", "Sign Up"])
    
    with tab1:
        st.subheader("Login")
        with st.form("login_form"):
            email = st.text_input("Email")
            password = st.text_input("Password", type="password")
            if st.form_submit_button("Sign In"):
                if email and password:
                    success, message = login(email, password)
                    if success:
                        st.success("Login successful!")
                        st.rerun()
                    else:
                        st.error(message)
                else:
                    st.error("Please fill in all fields")
    
    with tab2:
        st.subheader("Create Account")
        with st.form("signup_form"):
            email = st.text_input("Email", key="signup_email")
            password = st.text_input("Password", type="password", key="signup_password")
            confirm_password = st.text_input("Confirm Password", type="password", key="confirm_password")
            
            if st.form_submit_button("Sign Up"):
                if email and password and confirm_password:
                    if password != confirm_password:
                        st.error("Passwords don't match")
                    else:
                        success, message = signup(email, password)
                        if success:
                            st.success(message)
                        else:
                            st.error(message)
                else:
                    st.error("Please fill in all fields")
