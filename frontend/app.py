import streamlit as st
import requests
import pandas as pd
import json

API_URL = "http://127.0.0.1:8000"

st.set_page_config(
    page_title="Meeting Intelligence Hub",
    page_icon="🧠",
    layout="wide"
)

st.title("🧠 Meeting Intelligence Hub")
st.markdown("Transform raw meeting transcripts into actionable intelligence.")

# ── SESSION STATE ─────────────────────────────────────────────────────────────
if "transcripts" not in st.session_state:
    st.session_state.transcripts = []
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# ── SIDEBAR ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.header("📁 Uploaded Transcripts")
    if st.session_state.transcripts:
        for t in st.session_state.transcripts:
            st.success(f"✅ {t['filename']}")
    else:
        st.info("No transcripts uploaded yet.")

# ── TABS ──────────────────────────────────────────────────────────────────────
tab1, tab2, tab3 = st.tabs(["📤 Upload", "📋 Decisions & Actions", "💬 Chatbot"])

# ══════════════════════════════════════════════════════════════════════════════
# TAB 1 — UPLOAD
# ══════════════════════════════════════════════════════════════════════════════
with tab1:
    st.header("Upload Meeting Transcripts")
    st.markdown("Supported formats: `.txt` and `.vtt`")

    uploaded_files = st.file_uploader(
        "Drag and drop or browse files",
        type=["txt", "vtt"],
        accept_multiple_files=True
    )

    if uploaded_files:
        for uploaded_file in uploaded_files:
            # Check if already processed
            already_uploaded = any(
                t["filename"] == uploaded_file.name
                for t in st.session_state.transcripts
            )

            if not already_uploaded:
                with st.spinner(f"Processing {uploaded_file.name}..."):
                    response = requests.post(
                        f"{API_URL}/process",
                        files={"file": (uploaded_file.name, uploaded_file.getvalue())}
                    )

                if response.status_code == 200:
                    data = response.json()
                    data["filename"] = uploaded_file.name
                    st.session_state.transcripts.append(data)
                    st.success(f"✅ {uploaded_file.name} processed successfully!")
                else:
                    st.error(f"❌ Failed to process {uploaded_file.name}: {response.text}")

    # Show upload summaries
    if st.session_state.transcripts:
        st.subheader("📊 Upload Summary")
        for t in st.session_state.transcripts:
            with st.expander(f"📄 {t['filename']}"):
                col1, col2, col3 = st.columns(3)
                col1.metric("Words", t["metadata"]["word_count"])
                col2.metric("Lines", t["metadata"]["line_count"])
                col3.metric("Characters", t["metadata"]["char_count"])

# ══════════════════════════════════════════════════════════════════════════════
# TAB 2 — DECISIONS & ACTIONS
# ══════════════════════════════════════════════════════════════════════════════
with tab2:
    st.header("Decisions & Action Items")

    if not st.session_state.transcripts:
        st.info("Upload a transcript first to see extracted insights.")
    else:
        # Collect all decisions and actions across all transcripts
        all_decisions = []
        all_actions = []

        for t in st.session_state.transcripts:
            for d in t["insights"]["decisions"]:
                d["source"] = t["filename"]
                all_decisions.append(d)
            for a in t["insights"]["actions"]:
                a["source"] = t["filename"]
                all_actions.append(a)

        # ── DECISIONS TABLE
        st.subheader("✅ Decisions Made")
        if all_decisions:
            df_decisions = pd.DataFrame(all_decisions)[
                ["source", "speaker", "text", "confidence"]
            ]
            df_decisions.columns = ["Source", "Speaker", "Decision", "Confidence"]
            df_decisions["Confidence"] = df_decisions["Confidence"].apply(
                lambda x: f"{x:.0%}"
            )
            st.dataframe(df_decisions, use_container_width=True)

            # CSV Export
            csv = df_decisions.to_csv(index=False)
            st.download_button(
                label="⬇️ Export Decisions as CSV",
                data=csv,
                file_name="decisions.csv",
                mime="text/csv"
            )
        else:
            st.info("No decisions found in uploaded transcripts.")

        st.divider()

        # ── ACTIONS TABLE
        st.subheader("🎯 Action Items")
        if all_actions:
            df_actions = pd.DataFrame(all_actions)[
                ["source", "speaker", "text", "confidence"]
            ]
            df_actions.columns = ["Source", "Assignee", "Task", "Confidence"]
            df_actions["Confidence"] = df_actions["Confidence"].apply(
                lambda x: f"{x:.0%}"
            )
            st.dataframe(df_actions, use_container_width=True)

            # CSV Export
            csv_actions = df_actions.to_csv(index=False)
            st.download_button(
                label="⬇️ Export Action Items as CSV",
                data=csv_actions,
                file_name="action_items.csv",
                mime="text/csv"
            )
        else:
            st.info("No action items found in uploaded transcripts.")

# ══════════════════════════════════════════════════════════════════════════════
# TAB 3 — CHATBOT
# ══════════════════════════════════════════════════════════════════════════════
with tab3:
    st.header("💬 Ask Questions About Your Meetings")

    if not st.session_state.transcripts:
        st.info("Upload a transcript first to start asking questions.")
    else:
        # Display chat history
        for message in st.session_state.chat_history:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

        # Chat input
        if prompt := st.chat_input("Ask anything about your meetings..."):
            # Add user message
            st.session_state.chat_history.append({
                "role": "user",
                "content": prompt
            })
            with st.chat_message("user"):
                st.markdown(prompt)

            # Get answer from API
            with st.chat_message("assistant"):
                with st.spinner("Searching transcripts..."):
                    # Combine all transcript text
                    all_text = "\n\n".join([
                        f"=== {t['filename']} ===\n{t['metadata'].get('clean_text', '')}"
                        for t in st.session_state.transcripts
                    ])

                    response = requests.post(
                        f"{API_URL}/query",
                        json={"question": prompt, "transcript_text": all_text}
                    )

                if response.status_code == 200:
                    answer = response.json().get("answer", "No answer found.")
                else:
                    answer = "Sorry, I could not process your question. Please try again."

                st.markdown(answer)
                st.session_state.chat_history.append({
                    "role": "assistant",
                    "content": answer
                })