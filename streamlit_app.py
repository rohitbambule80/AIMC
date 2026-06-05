import streamlit as st
import requests

st.set_page_config(
    page_title="AIMC",
    layout="wide"
)

st.title("✈️ Aerospace Intelligent Maintenance Copilot")

st.markdown("---")

question = st.text_area(
    "Ask Aerospace Question"
)

if st.button("Ask AIMC"):

    with st.spinner("Analyzing aerospace manuals..."):

        response = requests.post(
            "http://127.0.0.1:8000/chat",
            json={
                "question": question
            }
        )

        data = response.json()

        st.subheader("Answer")

        st.write(data["answer"])

        st.subheader("Citations")

        for citation in data["citations"]:

            st.info(
                f"""
Source: {citation['source']}

ATA: {citation['ata']}

Manual: {citation['manual_type']}
"""
            )
