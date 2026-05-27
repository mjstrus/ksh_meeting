import streamlit as st
from utils.auth import require_auth, get_user_id
from utils.supabase_client import (
    get_pending_approvals,
    accept_approval,
    reject_approval
)

require_auth()

st.title("✅ Approvals")

user_id = get_user_id()
pending = get_pending_approvals(user_id)

if not pending:
    st.info("No pending approvals at the moment.")
else:
    st.subheader(f"⏳ Pending Approvals ({len(pending)})")
    
    for approval in pending:
        with st.expander(
            f"📋 {approval['resource_type']} | Created: {approval['created_at'][:10]}"
        ):
            col1, col2 = st.columns(2)
            with col1:
                st.write(f"**Status:** {approval['status']}")
                st.write(f"**Signatures:** {approval['current_signatures']}/{approval['required_signatures']}")
            with col2:
                st.write(f"**Created:** {approval['created_at'][:10]}")
            
            st.divider()
            
            col_accept, col_reject = st.columns(2)
            with col_accept:
                if st.button("✅ Accept", key=f"accept_{approval['id']}"):
                    success, message = accept_approval(approval['id'], user_id)
                    if success:
                        st.success(message)
                        st.rerun()
                    else:
                        st.error(message)
            
            with col_reject:
                if st.button("❌ Object", key=f"object_{approval['id']}"):
                    success, message = reject_approval(approval['id'], user_id, "User objected")
                    if success:
                        st.error(message)
                        st.rerun()
