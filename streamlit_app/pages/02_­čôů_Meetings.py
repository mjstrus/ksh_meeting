import streamlit as st
from datetime import datetime, timedelta
from utils.auth import require_auth, get_user_id
from utils.supabase_client import (
    get_user_companies, 
    create_meeting, 
    get_company_meetings,
    create_approval
)
from utils.validators import validate_meeting_date_with_informal

require_auth()

st.title("📅 Meetings")

user_id = get_user_id()
companies = get_user_companies(user_id)

if not companies:
    st.warning("⚠️ No companies yet. Please add a company first.")
    st.stop()

company_options = {c['id']: c['name'] for c in companies}
company_id = st.selectbox(
    "Select Company",
    options=list(company_options.keys()),
    format_func=lambda x: company_options[x]
)

tab1, tab2 = st.tabs(["Create Meeting", "View Meetings"])

with tab1:
    st.subheader("Create New Meeting")
    with st.form("meeting_form"):
        title = st.text_input("Meeting Title")
        
        col1, col2 = st.columns(2)
        with col1:
            date = st.date_input(
                "Meeting Date",
                min_value=datetime.now().date() + timedelta(days=14),
                value=datetime.now().date() + timedelta(days=14)
            )
        with col2:
            time = st.time_input("Meeting Time", value=datetime.now().time())
        
        informal = st.checkbox("Art. 239 KSH (Informal Convening)")
        
        location = st.radio("Location", ["Physical", "Remote"])
        location_str = "remote" if location == "Remote" else "physical"
        
        st.divider()
        st.subheader("📋 Agenda Items")
        agenda_text = st.text_area("Enter agenda items (one per line)", height=150)
        
        if st.form_submit_button("📅 Create Meeting"):
            is_valid, message = validate_meeting_date_with_informal(date, informal)
            if not is_valid:
                st.error(message)
            elif not title:
                st.error("Meeting title is required")
            elif not agenda_text.strip():
                st.error("At least one agenda item is required")
            else:
                scheduled_at = datetime.combine(date, time)
                agenda_items = [item.strip() for item in agenda_text.split('\n') if item.strip()]
                
                success, message = create_meeting(
                    company_id=company_id,
                    title=title,
                    scheduled_at=scheduled_at,
                    location=location_str,
                    agenda=agenda_items
                )
                
                if success:
                    meetings = get_company_meetings(company_id)
                    if meetings:
                        latest_meeting = meetings[-1]
                        approval_id = create_approval(
                            company_id=company_id,
                            meeting_id=latest_meeting['id'],
                            required_signatures=1
                        )
                        if approval_id:
                            st.success("✅ Meeting created!")
                            st.balloons()
                            st.rerun()

with tab2:
    st.subheader("Your Meetings")
    meetings = get_company_meetings(company_id)
    
    if not meetings:
        st.info("No meetings yet for this company.")
    else:
        for meeting in meetings:
            with st.expander(
                f"📅 {meeting['title']} — {meeting['scheduled_at'][:10]} | {meeting['status'].upper()}"
            ):
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.write(f"**Status:** {meeting['status']}")
                with col2:
                    st.write(f"**Location:** {meeting['location']}")
                with col3:
                    st.write(f"**Created:** {meeting['created_at'][:10]}")
