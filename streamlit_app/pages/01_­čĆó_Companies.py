import streamlit as st
from utils.auth import require_auth, get_user_id
from utils.supabase_client import get_user_companies, create_company, activate_company
from utils.validators import validate_krs_number, validate_nip

require_auth()

st.title("🏢 Companies")

user_id = get_user_id()
companies = get_user_companies(user_id)

if companies:
    st.subheader("My Companies")
    for company in companies:
        with st.expander(f"🏢 {company['name']} (KRS: {company['krs_number']})"):
            col1, col2 = st.columns(2)
            with col1:
                st.write(f"**Legal Form:** {company['legal_form']}")
                st.write(f"**NIP:** {company['nip'] or 'N/A'}")
                st.write(f"**Status:** {company['status']}")
            with col2:
                st.write(f"**Representation:** {company['representation_type']}")
                st.write(f"**Created:** {company['created_at'][:10]}")
            
            if company['status'] == 'pending_activation':
                st.warning("⚠️ Awaiting activation")
                if st.button(f"Activate {company['name']}", key=f"activate_{company['id']}"):
                    success, message = activate_company(company['id'])
                    if success:
                        st.success(message)
                        st.rerun()
                    else:
                        st.error(message)

st.divider()
st.subheader("➕ Add New Company")

with st.form("company_form"):
    col1, col2 = st.columns(2)
    with col1:
        krs = st.text_input("KRS Number (9 digits)")
    with col2:
        nip = st.text_input("NIP (10 digits, optional)")
    
    name = st.text_input("Company Name")
    legal_form = st.selectbox("Legal Form", ["sp. z o.o.", "S.A.", "sp. jawna", "sp. cywilna"])
    
    if st.form_submit_button("➕ Add Company"):
        if not validate_krs_number(krs):
            st.error("Invalid KRS number — must be 9 digits")
        elif nip and not validate_nip(nip):
            st.error("Invalid NIP — must be 10 digits")
        elif not name:
            st.error("Company name is required")
        else:
            success, message = create_company(krs, name, legal_form, nip)
            if success:
                st.success(message)
                st.rerun()
            else:
                st.error(message)
