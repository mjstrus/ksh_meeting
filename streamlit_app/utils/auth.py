import streamlit as st
from supabase import create_client, Client

# Initialize Supabase client
@st.cache_resource
def get_supabase_client():
    try:
        supabase_url = st.secrets.get("supabase_url")
        supabase_key = st.secrets.get("supabase_key")
    except:
        st.error("❌ Supabase credentials not configured in secrets")
        st.stop()
    
    if not supabase_url or not supabase_key:
        st.error("❌ Missing Supabase credentials")
        st.stop()
    
    return create_client(supabase_url, supabase_key)

def login(email: str, password: str):
    """Login to Supabase"""
    try:
        supabase = get_supabase_client()
        response = supabase.auth.sign_in_with_password({
            "email": email,
            "password": password
        })
        st.session_state.user = response.user
        st.session_state.token = response.session.access_token
        return True, "Login successful"
    except Exception as e:
        return False, f"Login failed: {str(e)}"

def signup(email: str, password: str):
    """Sign up new user"""
    try:
        supabase = get_supabase_client()
        response = supabase.auth.sign_up({
            "email": email,
            "password": password
        })
        return True, "Signup successful. Please check your email to confirm."
    except Exception as e:
        return False, f"Signup failed: {str(e)}"

def logout():
    """Clear session"""
    if "user" in st.session_state:
        del st.session_state.user
    if "token" in st.session_state:
        del st.session_state.token
    st.success("Logged out successfully")

def get_current_user():
    """Get logged-in user from session"""
    return st.session_state.get("user", None)

def require_auth():
    """Protect page — redirect to login if not authenticated"""
    if not get_current_user():
        st.warning("⚠️ Please log in first")
        st.stop()

def get_user_id():
    """Get current user ID"""
    user = get_current_user()
    return user.id if user else None
