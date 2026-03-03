"""
app.py — SHL Assessment Recommendation Frontend
Connects to: https://alokxsingh-shl-rag-api.hf.space
"""

import streamlit as st
import requests
import json
import time

API_URL = "https://alokxsingh-shl-rag-api.hf.space"

st.set_page_config(
    page_title="SHL Assessment Recommender",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Serif+Display:ital@0;1&family=DM+Sans:wght@300;400;500;600&family=JetBrains+Mono:wght@400;500&display=swap');
:root{--bg:#0d0f14;--surface:#13161e;--border:#1e2330;--accent:#4f8ef7;--accent2:#f7714f;--text:#e8eaf0;--muted:#6b7280;--success:#34d399;--warning:#fbbf24;--danger:#f87171;--radius:10px;}
html,body,[class*="css"]{font-family:'DM Sans',sans-serif;background-color:var(--bg)!important;color:var(--text)!important;}
.stApp{background-color:var(--bg)!important;}
#MainMenu,footer,header{visibility:hidden;}
.block-container{padding:2rem 3rem 3rem 3rem!important;max-width:1300px!important;}
.hero{display:flex;align-items:center;gap:1.2rem;padding:2.4rem 0 1.6rem 0;border-bottom:1px solid var(--border);margin-bottom:2rem;}
.hero-icon{font-size:2.8rem;background:linear-gradient(135deg,var(--accent),var(--accent2));-webkit-background-clip:text;-webkit-text-fill-color:transparent;line-height:1;}
.hero-title{font-family:'DM Serif Display',serif;font-size:2.2rem;font-weight:400;letter-spacing:-0.5px;color:var(--text)!important;margin:0;line-height:1.1;}
.hero-sub{font-size:0.92rem;color:var(--muted);margin-top:0.3rem;font-weight:300;}
.stTextArea textarea{background-color:var(--surface)!important;border:1px solid var(--border)!important;border-radius:var(--radius)!important;color:var(--text)!important;font-family:'DM Sans',sans-serif!important;font-size:0.97rem!important;padding:1rem!important;}
.stTextArea textarea:focus{border-color:var(--accent)!important;box-shadow:0 0 0 3px rgba(79,142,247,0.12)!important;}
.stTextArea label{color:var(--muted)!important;font-size:0.82rem!important;}
.stButton>button{background:linear-gradient(135deg,var(--accent),#3b74e0)!important;color:#fff!important;border:none!important;border-radius:var(--radius)!important;font-family:'DM Sans',sans-serif!important;font-weight:600!important;font-size:0.95rem!important;padding:0.7rem 1.6rem!important;transition:opacity 0.2s,transform 0.1s!important;}
.stButton>button:hover{opacity:0.88!important;transform:translateY(-1px)!important;}
.stSelectbox>div>div{background-color:var(--surface)!important;border:1px solid var(--border)!important;border-radius:var(--radius)!important;color:var(--text)!important;}
[data-testid="stSidebar"]{background-color:var(--surface)!important;border-right:1px solid var(--border)!important;}
.assessment-card{background:var(--surface);border:1px solid var(--border);border-radius:var(--radius);padding:1.4rem 1.6rem;margin-bottom:1rem;position:relative;transition:border-color 0.2s,box-shadow 0.2s;}
.assessment-card:hover{border-color:rgba(79,142,247,0.4);box-shadow:0 4px 24px rgba(79,142,247,0.07);}
.assessment-rank{font-family:'JetBrains Mono',monospace;font-size:0.75rem;color:var(--muted);background:var(--border);padding:0.18rem 0.55rem;border-radius:4px;display:inline-block;margin-bottom:0.6rem;}
.assessment-name{font-family:'DM Serif Display',serif;font-size:1.18rem;font-weight:400;color:var(--text);margin-bottom:0.6rem;line-height:1.3;}
.assessment-desc{font-size:0.88rem;color:var(--muted);line-height:1.65;margin-bottom:1rem;}
.badge{display:inline-block;font-size:0.72rem;font-weight:600;padding:0.2rem 0.6rem;border-radius:4px;margin-right:0.35rem;margin-bottom:0.35rem;letter-spacing:0.02em;text-transform:uppercase;}
.badge-type{background:rgba(79,142,247,0.12);color:var(--accent);border:1px solid rgba(79,142,247,0.25);}
.badge-remote{background:rgba(52,211,153,0.12);color:var(--success);border:1px solid rgba(52,211,153,0.25);}
.badge-adaptive{background:rgba(251,191,36,0.12);color:var(--warning);border:1px solid rgba(251,191,36,0.25);}
.badge-duration{background:rgba(107,114,128,0.15);color:var(--muted);border:1px solid var(--border);font-family:'JetBrains Mono',monospace;}
.card-link{display:inline-flex;align-items:center;gap:0.35rem;font-size:0.82rem;font-weight:600;color:var(--accent)!important;text-decoration:none!important;transition:opacity 0.2s;}
.card-link:hover{opacity:0.75;}
.metrics-row{display:flex;gap:1rem;margin-bottom:2rem;flex-wrap:wrap;}
.metric-box{background:var(--surface);border:1px solid var(--border);border-radius:var(--radius);padding:1rem 1.4rem;min-width:130px;flex:1;}
.metric-label{font-size:0.72rem;color:var(--muted);text-transform:uppercase;letter-spacing:0.06em;font-weight:600;margin-bottom:0.4rem;}
.metric-value{font-family:'DM Serif Display',serif;font-size:1.6rem;color:var(--accent);line-height:1;}
.metric-sub{font-size:0.75rem;color:var(--muted);margin-top:0.25rem;}
.type-grid{display:flex;flex-wrap:wrap;gap:0.6rem;margin-bottom:2rem;}
.type-chip{background:var(--surface);border:1px solid var(--border);border-radius:6px;padding:0.5rem 0.9rem;font-size:0.82rem;display:flex;align-items:center;gap:0.5rem;}
.type-chip-code{font-family:'JetBrains Mono',monospace;font-weight:500;color:var(--accent);font-size:0.78rem;}
.type-chip-name{color:var(--muted);}
.type-chip-count{background:rgba(79,142,247,0.15);color:var(--accent);border-radius:3px;padding:0.05rem 0.35rem;font-size:0.72rem;font-weight:700;}
.alert-box{border-radius:var(--radius);padding:1rem 1.2rem;margin-bottom:1.2rem;font-size:0.9rem;line-height:1.6;}
.alert-warning{background:rgba(251,191,36,0.08);border:1px solid rgba(251,191,36,0.25);color:var(--warning);}
.alert-error{background:rgba(248,113,113,0.08);border:1px solid rgba(248,113,113,0.25);color:var(--danger);}
.alert-success{background:rgba(52,211,153,0.08);border:1px solid rgba(52,211,153,0.25);color:var(--success);}
.section-label{font-size:0.75rem;font-weight:600;text-transform:uppercase;letter-spacing:0.08em;color:var(--muted);margin-bottom:0.8rem;}
.score-pill{font-family:'JetBrains Mono',monospace;font-size:0.72rem;background:rgba(79,142,247,0.1);border:1px solid rgba(79,142,247,0.2);color:var(--accent);padding:0.15rem 0.5rem;border-radius:4px;float:right;}
.feature-item{display:flex;align-items:center;gap:0.6rem;padding:0.5rem 0;font-size:0.85rem;color:var(--muted);border-bottom:1px solid var(--border);}
hr{border-color:var(--border)!important;margin:1.5rem 0!important;}
</style>
""", unsafe_allow_html=True)

TYPE_MAP = {
    "A": "Ability & Aptitude",
    "B": "Biodata & SJT",
    "C": "Competencies",
    "D": "Development & 360",
    "E": "Assessment Exercises",
    "K": "Knowledge & Skills",
    "P": "Personality & Behavior",
    "S": "Simulations",
}

EXAMPLES = [
    "I am hiring Java developers who collaborate with business teams.",
    "Mid-level professionals proficient in Python, SQL and JavaScript.",
    "Data analyst role — assess analytical thinking and cognitive ability.",
    "Customer service manager with strong interpersonal and leadership skills.",
    "Assess writing proficiency and communication skills for a content writer.",
    "Entry-level sales executive with high resilience and persuasion skills.",
]

# ── Sidebar ──
with st.sidebar:
    st.markdown("""
    <div style='padding:0.5rem 0 1.2rem 0;'>
        <div style='font-family:DM Serif Display,serif;font-size:1.15rem;color:#e8eaf0;'>SHL RAG System</div>
        <div style='font-size:0.78rem;color:#6b7280;margin-top:0.2rem;'>v2.0 · Powered by LangGraph</div>
    </div>""", unsafe_allow_html=True)

    st.markdown('<div class="section-label">Pipeline Features</div>', unsafe_allow_html=True)
    for icon, label in [
        ("🔍","Hybrid Search (FAISS + BM25)"),
        ("⚖️","Reciprocal Rank Fusion"),
        ("🎯","Cross-Encoder Reranking"),
        ("🔄","Corrective RAG (CRAG)"),
        ("🧩","Lost-in-Middle Reorder"),
        ("🚫","Abstention Guard"),
        ("🤖","LLaMA-3.3-70b via Groq"),
    ]:
        st.markdown(f'<div class="feature-item"><span>{icon}</span><span>{label}</span></div>', unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown('<div class="section-label">API Health</div>', unsafe_allow_html=True)
    if st.button("🩺 Check API Status", use_container_width=True):
        with st.spinner("Pinging..."):
            try:
                r = requests.get(f"{API_URL}/health", timeout=15)
                if r.status_code == 200:
                    st.markdown('<div class="alert-box alert-success">✅ API is healthy</div>', unsafe_allow_html=True)
                else:
                    st.markdown(f'<div class="alert-box alert-error">❌ Status {r.status_code}</div>', unsafe_allow_html=True)
            except Exception as e:
                st.markdown(f'<div class="alert-box alert-error">❌ Unreachable — {e}</div>', unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown('<div class="section-label">Assessment Types</div>', unsafe_allow_html=True)
    for code, name in TYPE_MAP.items():
        st.markdown(f"""<div style='display:flex;align-items:center;gap:0.5rem;padding:0.3rem 0;font-size:0.8rem;color:#6b7280;'>
            <span style='font-family:JetBrains Mono,monospace;color:#4f8ef7;font-size:0.75rem;'>{code}</span>
            <span>{name}</span></div>""", unsafe_allow_html=True)

# ── Hero ──
st.markdown("""
<div class="hero">
    <div class="hero-icon">🎯</div>
    <div>
        <div class="hero-title">SHL Assessment Recommender</div>
        <div class="hero-sub">Enter a job description or query · Get the most relevant SHL assessments · Powered by RAG</div>
    </div>
</div>""", unsafe_allow_html=True)

# ── Input ──
col_input, col_example = st.columns([3, 1])
with col_example:
    st.markdown('<div class="section-label">Quick examples</div>', unsafe_allow_html=True)
    selected = st.selectbox("", ["— pick one —"] + EXAMPLES, label_visibility="collapsed")
with col_input:
    st.markdown('<div class="section-label">Query / Job Description</div>', unsafe_allow_html=True)
    query = st.text_area(
        "",
        value="" if selected == "— pick one —" else selected,
        height=140,
        placeholder="e.g.  Hiring a senior Java developer who works closely with business stakeholders…",
        label_visibility="collapsed",
    )

btn_col, _, info_col = st.columns([2, 3, 2])
with btn_col:
    submit = st.button("🔍  Get Recommendations", type="primary", use_container_width=True)
with info_col:
    st.markdown('<div style="font-size:0.78rem;color:#6b7280;text-align:right;padding-top:0.5rem;">First request may take ~30s if API is sleeping</div>', unsafe_allow_html=True)

st.markdown("<hr>", unsafe_allow_html=True)

# ── Results ──
if submit:
    if not query.strip():
        st.markdown('<div class="alert-box alert-warning">⚠️ Please enter a query before submitting.</div>', unsafe_allow_html=True)
        st.stop()

    with st.spinner("Running pipeline — Hybrid Search → Reranking → CRAG → LLM…"):
        t0 = time.time()
        try:
            resp = requests.post(f"{API_URL}/recommend", json={"query": query.strip()}, timeout=120)
            resp.raise_for_status()
            data = resp.json()
            elapsed = round(time.time() - t0, 1)
            assessments = data.get("recommended_assessments", [])
            error_msg = None
        except requests.HTTPError as e:
            data, assessments, error_msg = {}, [], f"API error {e.response.status_code}: {e.response.text[:300]}"
            elapsed = round(time.time() - t0, 1)
        except Exception as e:
            data, assessments, error_msg = {}, [], str(e)
            elapsed = round(time.time() - t0, 1)

    if error_msg:
        st.markdown(f'<div class="alert-box alert-error"> {error_msg}</div>', unsafe_allow_html=True)
        st.stop()

    if data.get("abstained"):
        st.markdown(f"""<div class="alert-box alert-warning">
             <strong>No suitable assessments found</strong><br>
            <span style='font-size:0.85rem;'>{data.get("abstention_reason","")}</span>
        </div>""", unsafe_allow_html=True)
        st.markdown(f'<div style="font-size:0.78rem;color:#6b7280;">Best score: <code>{data.get("retrieval_top_score","N/A")}</code> · {elapsed}s</div>', unsafe_allow_html=True)
        st.stop()

    if not assessments:
        st.markdown('<div class="alert-box alert-warning">No assessments returned.</div>', unsafe_allow_html=True)
        st.stop()

    from collections import Counter
    all_types = []
    for a in assessments:
        all_types.extend(a.get("test_type", []))
    type_counts = Counter(all_types)
    remote_count = sum(1 for a in assessments if a.get("remote_support","No") == "Yes")
    adaptive_count = sum(1 for a in assessments if a.get("adaptive_support","No") == "Yes")
    durations = [a["duration"] for a in assessments if a.get("duration")]
    avg_duration = round(sum(durations)/len(durations)) if durations else None
    top_score = data.get("retrieval_top_score","—")

    st.markdown(f"""
    <div class="metrics-row">
        <div class="metric-box"><div class="metric-label">Assessments Found</div><div class="metric-value">{len(assessments)}</div><div class="metric-sub">of 377 in catalog</div></div>
        <div class="metric-box"><div class="metric-label">Remote Available</div><div class="metric-value" style="color:#34d399;">{remote_count}</div><div class="metric-sub">support remote testing</div></div>
        <div class="metric-box"><div class="metric-label">Adaptive / IRT</div><div class="metric-value" style="color:#fbbf24;">{adaptive_count}</div><div class="metric-sub">use adaptive scoring</div></div>
        <div class="metric-box"><div class="metric-label">Avg Duration</div><div class="metric-value" style="color:#a78bfa;">{f"{avg_duration} min" if avg_duration else "—"}</div><div class="metric-sub">across all tests</div></div>
        <div class="metric-box"><div class="metric-label">Top Relevance Score</div><div class="metric-value" style="font-size:1.25rem;font-family:JetBrains Mono,monospace;">{top_score}</div><div class="metric-sub">pipeline: {elapsed}s</div></div>
    </div>""", unsafe_allow_html=True)

    if type_counts:
        st.markdown('<div class="section-label">Test Type Breakdown</div>', unsafe_allow_html=True)
        chips = '<div class="type-grid">'
        for code, cnt in sorted(type_counts.items(), key=lambda x: -x[1]):
            chips += f'<div class="type-chip"><span class="type-chip-code">{code}</span><span class="type-chip-name">{TYPE_MAP.get(code,code)}</span><span class="type-chip-count">{cnt}</span></div>'
        chips += "</div>"
        st.markdown(chips, unsafe_allow_html=True)

    st.markdown('<div class="section-label">Recommended Assessments</div>', unsafe_allow_html=True)
    for i, a in enumerate(assessments):
        name     = a.get("name","Unknown")
        desc     = a.get("description","")
        url      = a.get("url","")
        remote   = a.get("remote_support","No")
        adaptive = a.get("adaptive_support","No")
        duration = a.get("duration")
        types    = a.get("test_type",[])
        score_v  = a.get("_rerank_score","")

        badges = "".join(f'<span class="badge badge-type">{TYPE_MAP.get(t,t)}</span>' for t in types)
        if remote == "Yes":  badges += '<span class="badge badge-remote">Remote</span>'
        if adaptive == "Yes": badges += '<span class="badge badge-adaptive">Adaptive</span>'
        if duration:          badges += f'<span class="badge badge-duration">⏱ {duration} min</span>'

        score_html = f'<span class="score-pill">score {score_v}</span>' if score_v else ""
        link_html  = f'<a href="{url}" target="_blank" class="card-link">View on SHL Catalog →</a>' if url else ""

        st.markdown(f"""
        <div class="assessment-card">
            {score_html}
            <div class="assessment-rank">#{i+1:02d}</div>
            <div class="assessment-name">{name}</div>
            <div style='margin-bottom:0.85rem;'>{badges}</div>
            <div class="assessment-desc">{desc[:320]}{"…" if len(desc)>320 else ""}</div>
            {link_html}
        </div>""", unsafe_allow_html=True)

    with st.expander("Raw JSON Response", expanded=False):
        st.code(json.dumps(data, indent=2), language="json")
