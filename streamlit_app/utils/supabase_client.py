import streamlit as st
from utils.auth import get_supabase_client, get_user_id
from datetime import datetime, timedelta

# ============= COMPANIES =============

def get_user_companies(user_id: str):
    """Get all companies where user is an admin"""
    try:
        supabase = get_supabase_client()
        response = supabase.table("companies").select(
            "*, company_admins!inner(id)"
        ).eq("company_admins.user_id", user_id).execute()
        return response.data if response.data else []
    except Exception as e:
        st.error(f"Error fetching companies: {e}")
        return []

def create_company(krs: str, name: str, legal_form: str, nip: str = None, regon: str = None):
    """Create new company"""
    try:
        supabase = get_supabase_client()
        user_id = get_user_id()
        
        company_data = {
            "krs_number": krs,
            "name": name,
            "legal_form": legal_form,
            "nip": nip,
            "regon": regon,
            "status": "pending_activation",
            "representation_type": "single",
            "required_signatures": 1,
        }
        
        response = supabase.table("companies").insert(company_data).execute()
        company = response.data[0] if response.data else None
        
        if company:
            admin_data = {
                "company_id": company["id"],
                "user_id": user_id,
                "role": "board_member",
                "can_sign": True,
                "status": "active"
            }
            supabase.table("company_admins").insert(admin_data).execute()
            return True, f"Company '{name}' created."
        return False, "Failed to create company"
    except Exception as e:
        return False, f"Error: {e}"

def activate_company(company_id: int):
    """Activate company"""
    try:
        supabase = get_supabase_client()
        response = supabase.table("companies").update(
            {"status": "active"}
        ).eq("id", company_id).execute()
        return True, "Company activated"
    except Exception as e:
        return False, f"Error: {e}"

# ============= MEETINGS =============

def create_meeting(company_id: int, title: str, scheduled_at: datetime, 
                   location: str, agenda: list):
    """Create new meeting"""
    try:
        supabase = get_supabase_client()
        
        company = supabase.table("companies").select("name").eq("id", company_id).execute()
        company_name = company.data[0]["name"] if company.data else "Unknown"
        
        meeting_data = {
            "company_id": company_id,
            "title": title,
            "scheduled_at": scheduled_at.isoformat(),
            "location": location,
            "is_remote": location == "remote",
            "status": "draft",
            "approval_status": "pending",
            "company_name": company_name,
            "description": "\n".join(agenda) if isinstance(agenda, list) else agenda,
        }
        
        response = supabase.table("meetings").insert(meeting_data).execute()
        meeting = response.data[0] if response.data else None
        
        if meeting:
            return True, f"Meeting '{title}' created as draft"
        return False, "Failed to create meeting"
    except Exception as e:
        return False, f"Error: {e}"

def get_company_meetings(company_id: int):
    """Get all meetings for a company"""
    try:
        supabase = get_supabase_client()
        response = supabase.table("meetings").select("*").eq("company_id", company_id).execute()
        return response.data if response.data else []
    except Exception as e:
        st.error(f"Error fetching meetings: {e}")
        return []

def get_meeting(meeting_id: int):
    """Get single meeting details"""
    try:
        supabase = get_supabase_client()
        response = supabase.table("meetings").select("*").eq("id", meeting_id).execute()
        return response.data[0] if response.data else None
    except Exception as e:
        st.error(f"Error fetching meeting: {e}")
        return None

def update_meeting_status(meeting_id: int, status: str):
    """Update meeting status"""
    try:
        supabase = get_supabase_client()
        response = supabase.table("meetings").update(
            {"status": status, "updated_at": datetime.now().isoformat()}
        ).eq("id", meeting_id).execute()
        return True, f"Meeting status updated to {status}"
    except Exception as e:
        return False, f"Error: {e}"

# ============= APPROVALS =============

def create_approval(company_id: int, meeting_id: int, required_signatures: int = 1):
    """Create approval workflow for meeting"""
    try:
        supabase = get_supabase_client()
        
        approval_data = {
            "company_id": company_id,
            "resource_type": "meeting_call",
            "resource_id": meeting_id,
            "required_signatures": required_signatures,
            "current_signatures": 0,
            "status": "pending",
            "expires_at": (datetime.now() + timedelta(days=7)).isoformat(),
        }
        
        response = supabase.table("approvals").insert(approval_data).execute()
        return response.data[0]["id"] if response.data else None
    except Exception as e:
        st.error(f"Error creating approval: {e}")
        return None

def get_pending_approvals(user_id: str):
    """Get all pending approvals for user"""
    try:
        supabase = get_supabase_client()
        response = supabase.table("approvals").select("*").eq("status", "pending").execute()
        return response.data if response.data else []
    except Exception as e:
        st.error(f"Error fetching approvals: {e}")
        return []

def accept_approval(approval_id: int, user_id: str):
    """Accept approval"""
    try:
        supabase = get_supabase_client()
        
        sig_data = {
            "approval_id": approval_id,
            "user_id": user_id,
            "signature_method": "internal_token",
        }
        supabase.table("approval_signatures").insert(sig_data).execute()
        
        approval = supabase.table("approvals").select("*").eq("id", approval_id).execute()
        if approval.data:
            app = approval.data[0]
            new_count = app["current_signatures"] + 1
            
            if new_count >= app["required_signatures"]:
                supabase.table("approvals").update({
                    "status": "approved",
                    "current_signatures": new_count,
                    "completed_at": datetime.now().isoformat()
                }).eq("id", approval_id).execute()
                return True, "Approval accepted and APPROVED!"
            else:
                supabase.table("approvals").update({
                    "current_signatures": new_count
                }).eq("id", approval_id).execute()
                return True, f"Signature added ({new_count}/{app['required_signatures']})"
        return False, "Approval not found"
    except Exception as e:
        return False, f"Error: {e}"

def reject_approval(approval_id: int, user_id: str, reason: str = ""):
    """Reject approval"""
    try:
        supabase = get_supabase_client()
        supabase.table("approvals").update({
            "status": "rejected",
            "completed_at": datetime.now().isoformat()
        }).eq("id", approval_id).execute()
        return True, f"Objection recorded: {reason}"
    except Exception as e:
        return False, f"Error: {e}"
