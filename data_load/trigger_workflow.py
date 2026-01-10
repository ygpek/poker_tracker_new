import requests
import streamlit as st


def trigger_workflow(workflow_file: str):
    url = (
        f"https://api.github.com/repos/"
        f"{st.secrets['GITHUB_OWNER']}/"
        f"{st.secrets['GITHUB_REPO']}/"
        f"actions/workflows/{workflow_file}/dispatches"
    )

    headers = {
        "Authorization": f"Bearer {st.secrets['GITHUB_TOKEN']}",
        "Accept": "application/vnd.github+json",
    }

    payload = {"ref": "main"}

    response = requests.post(url, headers=headers, json=payload)

    return response.status_code == 204
