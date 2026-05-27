# KSH Meeting Hub — Streamlit MVP

A legal-tech platform for managing shareholder meetings in Polish companies (sp. z o.o., S.A.) with maker-checker workflow compliant with the Polish Commercial Code (KSH).

## Features

- 📋 Create and manage shareholder meetings
- ✅ Multi-signature approval workflow (maker-checker)
- 🔐 Secure authentication via Supabase
- 🔍 Compliance with Art. 238-239 KSH

## Tech Stack

- **Frontend:** Streamlit
- **Backend:** Supabase (PostgreSQL)
- **Auth:** Supabase Auth

## Setup

### 1. Install dependencies

```bash
cd streamlit_app
pip install -r requirements.txt
```

### 2. Configure secrets

Create `.streamlit/secrets.toml` (or set in Streamlit Cloud):

```toml
supabase_url = "https://your-project.supabase.co"
supabase_key = "eyJhbGc..."
smtp_server = "smtp.gmail.com"
smtp_port = 587
sender_email = "your-email@gmail.com"
sender_password = "your-app-password"
```

### 3. Run locally

```bash
streamlit run app.py
```

## Deployment

Push to GitHub, then deploy to Streamlit Cloud:
1. Go to https://streamlit.io/cloud
2. Select your repo
3. Set secrets in Settings → Secrets
4. Deploy!

## License

MIT
