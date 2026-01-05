import streamlit as st
import gspread
import json
import os
from google.oauth2.service_account import Credentials


@st.cache_resource
def get_gspread_client():
    service_account_info = json.loads(os.environ["GCP_SERVICE_ACCOUNT"])

    scopes = [
        "https://www.googleapis.com/auth/spreadsheets",
        "https://www.googleapis.com/auth/drive",
    ]

    creds = Credentials.from_service_account_info(service_account_info, scopes=scopes)

    return gspread.authorize(creds)
