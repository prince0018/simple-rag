import os, requests, streamlit as st

API_URL = os.getenv("RAG_API_URL", "http://localhost:8000/query")

st.title("🧠 Simple RAG Front-End")

question = st.text_input("Ask anything:", placeholder="Who is Alexander the Great?")
submit = st.button("🔍 Query")

if submit and question:
    with st.spinner("Calling RAG API…"):
        resp = requests.post(API_URL, json={"question": question}, timeout=60)
        if resp.ok:
            data = resp.json()
            st.success(data["answer"])
            with st.expander("Sources"):
                for src in data.get("sources", []):
                    st.markdown(f"• `{src}`")
        else:
            st.error(f"❌ {resp.status_code}: {resp.text}")
