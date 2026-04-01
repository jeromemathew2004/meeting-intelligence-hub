import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import streamlit as st
import requests
import pandas as pd
import json
from datetime import datetime


API_URL = "http://127.0.0.1:8000"

# ══════════════════════════════════════════════════════════════════════════════
# PAGE CONFIGURATION
# ══════════════════════════════════════════════════════════════════════════════
st.set_page_config(
    page_title="Meeting Intelligence Hub",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ══════════════════════════════════════════════════════════════════════════════
# CUSTOM CSS FOR PROFESSIONAL STYLING
# ══════════════════════════════════════════════════════════════════════════════
st.markdown("""
<style>
    /* Main theme colors */
    :root {
        --primary-color: #6366f1;
        --secondary-color: #8b5cf6;
        --success-color: #10b981;
        --warning-color: #f59e0b;
        --danger-color: #ef4444;
    }
    
    /* Hide default Streamlit elements */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    
    /* Header styling */
    .main-header {
        background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 100%);
        padding: 2rem;
        border-radius: 1rem;
        margin-bottom: 2rem;
        box-shadow: 0 10px 30px rgba(99, 102, 241, 0.3);
    }
    
    .main-header h1 {
        color: white !important;
        font-size: 2.5rem !important;
        font-weight: 700 !important;
        margin: 0 !important;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.1);
    }
    
    .main-header p {
        color: rgba(255, 255, 255, 0.9) !important;
        font-size: 1.1rem !important;
        margin-top: 0.5rem !important;
    }
    
    /* Metric cards */
    .metric-card {
        background: white;
        padding: 1.5rem;
        border-radius: 0.75rem;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.07);
        border-left: 4px solid #6366f1;
        transition: transform 0.2s, box-shadow 0.2s;
    }
    
    .metric-card:hover {
        transform: translateY(-4px);
        box-shadow: 0 12px 24px rgba(99, 102, 241, 0.15);
    }
    
    /* Sidebar styling */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #f8fafc 0%, #f1f5f9 100%);
    }
    
    [data-testid="stSidebar"] .stSuccess {
        background-color: #d1fae5;
        border-left: 3px solid #10b981;
        border-radius: 0.5rem;
        padding: 0.75rem;
        margin: 0.5rem 0;
    }
    
    /* Tab styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 1rem;
        background-color: #f8fafc;
        padding: 0.5rem;
        border-radius: 0.75rem;
    }
    
    .stTabs [data-baseweb="tab"] {
        height: 3.5rem;
        background-color: white;
        border-radius: 0.5rem;
        padding: 0 1.5rem;
        font-weight: 600;
        border: 2px solid transparent;
        transition: all 0.2s;
    }
    
    .stTabs [data-baseweb="tab"]:hover {
        background-color: #eef2ff;
        border-color: #c7d2fe;
    }
    
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 100%) !important;
        color: white !important;
        border-color: #6366f1 !important;
    }
    
    /* Upload zone */
    [data-testid="stFileUploader"] {
        background: linear-gradient(135deg, #eef2ff 0%, #faf5ff 100%);
        border: 2px dashed #a5b4fc;
        border-radius: 1rem;
        padding: 2rem;
        transition: all 0.3s;
    }
    
    [data-testid="stFileUploader"]:hover {
        border-color: #6366f1;
        background: linear-gradient(135deg, #e0e7ff 0%, #f3e8ff 100%);
    }
    
    /* Dataframe styling */
    [data-testid="stDataFrame"] {
        border-radius: 0.75rem;
        overflow: hidden;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.07);
    }
    
    /* Button styling */
    .stDownloadButton > button {
        background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 100%);
        color: white;
        border: none;
        border-radius: 0.5rem;
        padding: 0.75rem 1.5rem;
        font-weight: 600;
        transition: all 0.2s;
        box-shadow: 0 4px 6px rgba(99, 102, 241, 0.3);
    }
    
    .stDownloadButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 12px rgba(99, 102, 241, 0.4);
    }
    
    /* Expander styling */
    .streamlit-expanderHeader {
        background-color: #f8fafc;
        border-radius: 0.5rem;
        border-left: 3px solid #6366f1;
        font-weight: 600;
    }
    
    .streamlit-expanderHeader:hover {
        background-color: #eef2ff;
    }
    
    /* Info/Success/Warning boxes */
    .stAlert {
        border-radius: 0.75rem;
        border: none;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
    }
    
    /* Chat messages */
    .stChatMessage {
        background-color: white;
        border-radius: 1rem;
        padding: 1rem;
        margin: 0.5rem 0;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
    }
    
    /* Divider */
    hr {
        margin: 2rem 0;
        border: none;
        height: 2px;
        background: linear-gradient(90deg, transparent, #e5e7eb, transparent);
    }
    
    /* Confidence badges */
    .confidence-badge {
        display: inline-block;
        padding: 0.25rem 0.75rem;
        border-radius: 1rem;
        font-size: 0.875rem;
        font-weight: 600;
    }
    
    .confidence-high {
        background-color: #d1fae5;
        color: #065f46;
    }
    
    .confidence-medium {
        background-color: #fed7aa;
        color: #92400e;
    }
    
    .confidence-low {
        background-color: #fee2e2;
        color: #991b1b;
    }
</style>
""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
# SESSION STATE INITIALIZATION
# ══════════════════════════════════════════════════════════════════════════════
if "transcripts" not in st.session_state:
    st.session_state.transcripts = []
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# ══════════════════════════════════════════════════════════════════════════════
# HEADER
# ══════════════════════════════════════════════════════════════════════════════
st.markdown("""
<div class="main-header">
    <h1>🧠 Meeting Intelligence Hub</h1>
    <p>Transform raw meeting transcripts into actionable intelligence with AI-powered insights</p>
</div>
""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
# SIDEBAR - STATISTICS & TRANSCRIPT LIST
# ══════════════════════════════════════════════════════════════════════════════
with st.sidebar:
    st.markdown("### 📊 Dashboard")
    
    # Statistics
    total_transcripts = len(st.session_state.transcripts)
    total_decisions = sum(len(t.get("insights", {}).get("decisions", [])) for t in st.session_state.transcripts)
    total_actions = sum(len(t.get("insights", {}).get("actions", [])) for t in st.session_state.transcripts)
    
    col1, col2 = st.columns(2)
    with col1:
        st.metric("📁 Transcripts", total_transcripts)
        st.metric("✅ Decisions", total_decisions)
    with col2:
        st.metric("🎯 Actions", total_actions)
        total_words = sum(t.get("metadata", {}).get("word_count", 0) for t in st.session_state.transcripts)
        st.metric("📝 Words", f"{total_words:,}")
    
    st.divider()
    
    # Transcript list
    st.markdown("### 📁 Uploaded Transcripts")
    if st.session_state.transcripts:
        for i, t in enumerate(st.session_state.transcripts, 1):
            st.success(f"**{i}.** {t['filename']}")
    else:
        st.info("💡 No transcripts uploaded yet.\n\nGet started by uploading your first transcript!")

# ══════════════════════════════════════════════════════════════════════════════
# MAIN TABS
# ══════════════════════════════════════════════════════════════════════════════
tab1, tab2, tab3 = st.tabs(["📤 Upload Transcripts", "📋 Insights & Analytics", "💬 AI Assistant"])

# ══════════════════════════════════════════════════════════════════════════════
# TAB 1 — UPLOAD
# ══════════════════════════════════════════════════════════════════════════════
with tab1:
    st.markdown("### 📤 Upload Meeting Transcripts")
    st.markdown("Upload your meeting transcripts and let AI extract key insights, decisions, and action items automatically.")
    
    col1, col2 = st.columns([2, 1])
    with col1:
        st.markdown("**Supported Formats:** `.txt`, `.vtt`")
    with col2:
        st.markdown(f"**Status:** {len(st.session_state.transcripts)} file(s) processed")
    
    st.markdown("---")
    
    # File uploader
    uploaded_files = st.file_uploader(
        "📎 Drag and drop files here or click to browse",
        type=["txt", "vtt"],
        accept_multiple_files=True,
        help="Upload meeting transcript files in .txt or .vtt format"
    )
    
    if uploaded_files:
        for uploaded_file in uploaded_files:
            # Check if already processed
            already_uploaded = any(
                t["filename"] == uploaded_file.name
                for t in st.session_state.transcripts
            )
            
            if not already_uploaded:
                with st.spinner(f"🔄 Processing **{uploaded_file.name}**..."):
                    try:
                        response = requests.post(
                            f"{API_URL}/process",
                            files={"file": (uploaded_file.name, uploaded_file.getvalue())},
                            timeout=30
                        )
                        
                        if response.status_code == 200:
                            data = response.json()
                            data["filename"] = uploaded_file.name
                            data["upload_time"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                            st.session_state.transcripts.append(data)
                            st.success(f"✅ **{uploaded_file.name}** processed successfully!")
                        else:
                            st.error(f"❌ Failed to process **{uploaded_file.name}**: {response.text}")
                    except requests.exceptions.RequestException as e:
                        st.error(f"❌ Connection error: {str(e)}\n\nMake sure the API server is running at {API_URL}")
    
    # Show upload summaries
    if st.session_state.transcripts:
        st.markdown("---")
        st.markdown("### 📊 Processed Transcripts")
        
        for t in st.session_state.transcripts:
            with st.expander(f"📄 **{t['filename']}** - Uploaded: {t.get('upload_time', 'N/A')}", expanded=False):
                col1, col2, col3, col4 = st.columns(4)
                
                metadata = t.get("metadata", {})
                insights = t.get("insights", {})
                
                col1.metric("📝 Words", metadata.get("word_count", 0))
                col2.metric("📏 Lines", metadata.get("line_count", 0))
                col3.metric("✅ Decisions", len(insights.get("decisions", [])))
                col4.metric("🎯 Actions", len(insights.get("actions", [])))
                
                # Preview
                if "clean_text" in metadata:
                    st.markdown("**Preview:**")
                    preview_text = metadata["clean_text"][:500] + ("..." if len(metadata["clean_text"]) > 500 else "")
                    st.text_area("", preview_text, height=100, disabled=True, key=f"preview_{t['filename']}")

# ══════════════════════════════════════════════════════════════════════════════
# TAB 2 — DECISIONS & ACTIONS
# ══════════════════════════════════════════════════════════════════════════════
with tab2:
    st.markdown("### 📋 Insights & Analytics")
    
    if not st.session_state.transcripts:
        st.info("📤 **Get Started!** Upload a transcript in the Upload tab to see extracted insights, decisions, and action items.")
    else:
        from services.exporter import export_pdf
        
        # Collect all decisions and actions across all transcripts
        all_decisions = []
        all_actions = []
        
        for t in st.session_state.transcripts:
            insights = t.get("insights", {})
            for d in insights.get("decisions", []):
                d_copy = d.copy()
                d_copy["source"] = t["filename"]
                all_decisions.append(d_copy)
            for a in insights.get("actions", []):
                a_copy = a.copy()
                a_copy["source"] = t["filename"]
                all_actions.append(a_copy)
        
        # Overview metrics
        col1, col2, col3 = st.columns(3)
        with col1:
            st.markdown("""
            <div class="metric-card">
                <h3 style="color: #6366f1; margin: 0;">✅ Decisions Made</h3>
                <h1 style="margin: 0.5rem 0;">{}</h1>
                <p style="color: #64748b; margin: 0;">Extracted from {} transcript(s)</p>
            </div>
            """.format(len(all_decisions), len(st.session_state.transcripts)), unsafe_allow_html=True)
        
        with col2:
            st.markdown("""
            <div class="metric-card">
                <h3 style="color: #8b5cf6; margin: 0;">🎯 Action Items</h3>
                <h1 style="margin: 0.5rem 0;">{}</h1>
                <p style="color: #64748b; margin: 0;">Tasks assigned to team members</p>
            </div>
            """.format(len(all_actions), len(st.session_state.transcripts)), unsafe_allow_html=True)
        
        with col3:
            avg_confidence = 0
            if all_decisions or all_actions:
                all_items = all_decisions + all_actions
                avg_confidence = sum(item.get("confidence", 0) for item in all_items) / len(all_items)
            
            st.markdown("""
            <div class="metric-card">
                <h3 style="color: #10b981; margin: 0;">📊 Avg Confidence</h3>
                <h1 style="margin: 0.5rem 0;">{:.0%}</h1>
                <p style="color: #64748b; margin: 0;">AI extraction accuracy</p>
            </div>
            """.format(avg_confidence), unsafe_allow_html=True)
        
        st.markdown("---")
        
        # ── DECISIONS SECTION
        st.markdown("### ✅ Decisions Made")
        if all_decisions:
            # Display as cards
            for i, decision in enumerate(all_decisions, 1):
                confidence = decision.get("confidence", 0)
                confidence_class = "confidence-high" if confidence > 0.8 else "confidence-medium" if confidence > 0.6 else "confidence-low"
                
                st.markdown(f"""
                <div style="background: linear-gradient(135deg, #f0fdf4 0%, #dcfce7 100%); 
                            padding: 1.5rem; 
                            border-radius: 0.75rem; 
                            margin-bottom: 1rem;
                            border-left: 4px solid #10b981;
                            box-shadow: 0 2px 4px rgba(0,0,0,0.05);">
                    <div style="display: flex; justify-content: space-between; align-items: start; margin-bottom: 0.5rem;">
                        <div>
                            <span style="background: #10b981; color: white; padding: 0.25rem 0.75rem; border-radius: 1rem; font-size: 0.75rem; font-weight: 600;">
                                DECISION #{i}
                            </span>
                            <span style="margin-left: 0.5rem; color: #64748b; font-size: 0.875rem;">
                                📄 {decision.get("source", "Unknown")}
                            </span>
                        </div>
                        <span class="confidence-badge {confidence_class}">
                            {confidence:.0%} confidence
                        </span>
                    </div>
                    <p style="font-size: 0.875rem; color: #475569; margin: 0.5rem 0 0 0;">
                        <strong>👤 {decision.get("speaker", "Unknown")}</strong>
                    </p>
                    <p style="font-size: 1rem; color: #1e293b; margin: 0.75rem 0 0 0;">
                        {decision.get("text", "No text available")}
                    </p>
                </div>
                """, unsafe_allow_html=True)
            
            # Export options
            df_decisions = pd.DataFrame(all_decisions)[
                ["source", "speaker", "text", "confidence"]
            ]
            df_decisions.columns = ["Source", "Speaker", "Decision", "Confidence"]
            df_decisions["Confidence"] = df_decisions["Confidence"].apply(
                lambda x: f"{x:.0%}"
            )
            
            st.markdown("---")
            st.markdown("**📥 Export Decisions**")
            col1, col2 = st.columns(2)
            with col1:
                csv = df_decisions.to_csv(index=False)
                st.download_button(
                    label="⬇️ Download as CSV",
                    data=csv,
                    file_name="decisions.csv",
                    mime="text/csv"
                )
            with col2:
                st.dataframe(df_decisions, use_container_width=True, hide_index=True)
        else:
            st.info("ℹ️ No decisions found in uploaded transcripts.")
        
        st.divider()
        
        # ── ACTIONS SECTION
        st.markdown("### 🎯 Action Items")
        if all_actions:
            # Display as cards
            for i, action in enumerate(all_actions, 1):
                confidence = action.get("confidence", 0)
                confidence_class = "confidence-high" if confidence > 0.8 else "confidence-medium" if confidence > 0.6 else "confidence-low"
                
                st.markdown(f"""
                <div style="background: linear-gradient(135deg, #eef2ff 0%, #e0e7ff 100%); 
                            padding: 1.5rem; 
                            border-radius: 0.75rem; 
                            margin-bottom: 1rem;
                            border-left: 4px solid #6366f1;
                            box-shadow: 0 2px 4px rgba(0,0,0,0.05);">
                    <div style="display: flex; justify-content: space-between; align-items: start; margin-bottom: 0.5rem;">
                        <div>
                            <span style="background: #6366f1; color: white; padding: 0.25rem 0.75rem; border-radius: 1rem; font-size: 0.75rem; font-weight: 600;">
                                ACTION #{i}
                            </span>
                            <span style="margin-left: 0.5rem; color: #64748b; font-size: 0.875rem;">
                                📄 {action.get("source", "Unknown")}
                            </span>
                        </div>
                        <span class="confidence-badge {confidence_class}">
                            {confidence:.0%} confidence
                        </span>
                    </div>
                    <p style="font-size: 0.875rem; color: #475569; margin: 0.5rem 0 0 0;">
                        <strong>👤 Assigned to: {action.get("speaker", "Unknown")}</strong>
                    </p>
                    <p style="font-size: 1rem; color: #1e293b; margin: 0.75rem 0 0 0;">
                        {action.get("text", "No text available")}
                    </p>
                </div>
                """, unsafe_allow_html=True)
            
            # Export options
            df_actions = pd.DataFrame(all_actions)[
                ["source", "speaker", "text", "confidence"]
            ]
            df_actions.columns = ["Source", "Assignee", "Task", "Confidence"]
            df_actions["Confidence"] = df_actions["Confidence"].apply(
                lambda x: f"{x:.0%}"
            )
            
            st.markdown("---")
            st.markdown("**📥 Export Action Items**")
            col1, col2 = st.columns(2)
            with col1:
                csv_actions = df_actions.to_csv(index=False)
                st.download_button(
                    label="⬇️ Download as CSV",
                    data=csv_actions,
                    file_name="action_items.csv",
                    mime="text/csv"
                )
            with col2:
                st.dataframe(df_actions, use_container_width=True, hide_index=True)
        else:
            st.info("ℹ️ No action items found in uploaded transcripts.")
        
        st.divider()
        
        # ── PDF EXPORT
        if all_decisions or all_actions:
            st.markdown("### 📄 Full Report Export")
            st.markdown("Download a comprehensive PDF report with all decisions and action items.")
            pdf_bytes = export_pdf(all_decisions, all_actions)
            st.download_button(
                label="⬇️ Download Full Report as PDF",
                data=pdf_bytes,
                file_name=f"meeting_insights_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf",
                mime="application/pdf"
            )

# ══════════════════════════════════════════════════════════════════════════════
# TAB 3 — CHATBOT
# ══════════════════════════════════════════════════════════════════════════════
with tab3:
    st.markdown("### 💬 AI Assistant")
    st.markdown("Ask questions about your meeting transcripts and get instant AI-powered answers.")
    
    if not st.session_state.transcripts:
        st.info("📤 **Upload Required!** Please upload at least one transcript to start chatting with the AI assistant.")
        
        # Show example questions
        st.markdown("---")
        st.markdown("**Example Questions You Can Ask:**")
        example_questions = [
            "What were the main decisions made in the meetings?",
            "Who has action items assigned to them?",
            "Summarize the key discussion points",
            "What topics were discussed most frequently?",
            "What are the deadlines mentioned?"
        ]
        for q in example_questions:
            st.markdown(f"- 💡 *{q}*")
    else:
        # Display chat history
        for message in st.session_state.chat_history:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])
        
        # Chat input
        if prompt := st.chat_input("💭 Ask anything about your meetings..."):
            # Add user message
            st.session_state.chat_history.append({
                "role": "user",
                "content": prompt
            })
            with st.chat_message("user"):
                st.markdown(prompt)
            
            # Get answer from API
            with st.chat_message("assistant"):
                with st.spinner("🔍 Searching transcripts and generating response..."):
                    # Combine all transcript text
                    all_text = "\n\n".join([
                        f"=== {t['filename']} ===\n{t.get('metadata', {}).get('clean_text', '')}"
                        for t in st.session_state.transcripts
                    ])
                    
                    try:
                        response = requests.post(
                            f"{API_URL}/query",
                            json={"question": prompt, "transcript_text": all_text},
                            timeout=30
                        )
                        
                        if response.status_code == 200:
                            answer = response.json().get("answer", "No answer found.")
                        else:
                            answer = f"⚠️ Sorry, I encountered an error: {response.text}\n\nPlease try rephrasing your question."
                    except requests.exceptions.RequestException as e:
                        answer = f"❌ Connection error: {str(e)}\n\nMake sure the API server is running at {API_URL}"
                
                st.markdown(answer)
                st.session_state.chat_history.append({
                    "role": "assistant",
                    "content": answer
                })
        
        # Show helpful tips if no chat history
        if len(st.session_state.chat_history) == 0:
            st.markdown("---")
            st.markdown("**💡 Quick Tips:**")
            col1, col2 = st.columns(2)
            with col1:
                st.markdown("""
                - Ask specific questions for better answers
                - Reference speaker names or topics
                - Request summaries or analysis
                """)
            with col2:
                st.markdown("""
                - Ask about decisions or action items
                - Inquire about timelines or deadlines
                - Request comparisons across meetings
                """)

# ══════════════════════════════════════════════════════════════════════════════
# FOOTER
# ══════════════════════════════════════════════════════════════════════════════
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #64748b; padding: 1rem;">
    <p>🧠 <strong>Meeting Intelligence Hub</strong> | Powered by AI | Made with ❤️ using Streamlit</p>
</div>
""", unsafe_allow_html=True)