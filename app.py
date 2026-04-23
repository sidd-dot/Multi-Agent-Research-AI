import streamlit as st
import time
from agents import build_reader_agent, build_search_agent, writer_chain, critic_chain

st.set_page_config(
    page_title="ResearchMind · AI Research Agent",
    page_icon="🔬",
    layout="wide",
    initial_sidebar_state="collapsed",
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;600;700;800&family=DM+Mono:wght@300;400;500&family=DM+Sans:ital,wght@0,300;0,400;0,500;1,300&display=swap');

html, body, [class*="css"] {
    font-family: 'DM Sans', sans-serif;
    color: #e8e4dc;
}
.stApp {
    background: #0a0a0f;
    background-image:
        radial-gradient(ellipse 80% 50% at 20% -10%, rgba(108,99,255,0.10) 0%, transparent 60%),
        radial-gradient(ellipse 60% 40% at 80% 110%, rgba(108,99,255,0.06) 0%, transparent 55%);
}
#MainMenu, footer, header { visibility: hidden; }
.block-container { padding: 2rem 3rem 4rem; max-width: 1200px; }

.hero { text-align:center; padding:3.5rem 0 2rem; }
.hero-eyebrow {
    font-family:'DM Mono',monospace; font-size:.7rem; font-weight:500;
    letter-spacing:.25em; text-transform:uppercase; color:#6C63FF;
    margin-bottom:1rem; opacity:.9;
}
.hero h1 {
    font-family:'Syne',sans-serif; font-size:clamp(2.8rem,6vw,5rem);
    font-weight:800; line-height:1.0; letter-spacing:-.03em;
    margin:0 0 1rem;
}
    .hero h1 .white {
    color: #ffffff;
}
    .hero h1 .blue {
    color: #6C63FF;
}

.hero-sub {
    font-size:1.05rem; font-weight:300; color:#a09890;
    max-width:520px; margin:0 auto; line-height:1.65;
}
.divider {
    height:1px;
    background:linear-gradient(90deg,transparent,rgba(108,99,255,.4),transparent);
    margin:2rem 0;
}

.input-card {
    background:rgba(255,255,255,.03); border:1px solid rgba(108,99,255,.2);
    border-radius:16px; padding:2rem 2.5rem; margin-bottom:1.5rem;
    backdrop-filter:blur(8px);
}
.stTextInput > div > div > input {
    background:rgba(255,255,255,.05) !important;
    border:1px solid rgba(108,99,255,.3) !important;
    border-radius:10px !important; color:#f0ebe0 !important;
    font-family:'DM Sans',sans-serif !important; font-size:1rem !important;
    padding:.75rem 1rem !important; transition:border-color .2s,box-shadow .2s !important;
}
.stTextInput > div > div > input:focus {
    border-color:#6C63FF !important;
    box-shadow:0 0 0 3px rgba(108,99,255,.15) !important;
}
.stTextInput > div > div > input::placeholder { color:#555 !important; }
.stTextInput > label {
    font-family:'DM Mono',monospace !important; font-size:.72rem !important;
    letter-spacing:.15em !important; text-transform:uppercase !important;
    color:#6C63FF !important; font-weight:500 !important;
}

/* Run button — blue/violet */
.stButton > button {
    background: #6C63FF !important;
    color:#ffffff !important; font-family:'Syne',sans-serif !important;
    font-weight:700 !important; font-size:.95rem !important;
    letter-spacing:.04em !important; border:none !important;
    border-radius:10px !important; padding:.75rem 2.2rem !important;
    transition:transform .15s,box-shadow .15s,opacity .15s !important;
    box-shadow:0 4px 20px rgba(108,99,255,.35) !important; width:100%;
}
.stButton > button:hover {
    background: #574ee0 !important;
    transform:translateY(-2px) !important;
    box-shadow:0 8px 28px rgba(108,99,255,.5) !important;
}
.stButton > button:active {
    background: #4840cc !important;
    transform:translateY(0) !important;
}

/* Clear button — ghost style */
div[data-testid="stButton"]:nth-of-type(2) button {
    background: transparent !important;
    border: 1px solid rgba(108,99,255,.35) !important;
    color: #a09890 !important;
    box-shadow: none !important;
    font-size: .8rem !important;
    padding: .5rem 1.2rem !important;
}
div[data-testid="stButton"]:nth-of-type(2) button:hover {
    background: rgba(108,99,255,.08) !important;
    border-color: #6C63FF !important;
    color: #6C63FF !important;
    transform: none !important;
    box-shadow: none !important;
}

div[data-testid="stDownloadButton"] button {
    background:rgba(108,99,255,.08) !important;
    border:1px solid rgba(108,99,255,.3) !important;
    color:#6C63FF !important; font-family:'DM Mono',monospace !important;
    font-size:.7rem !important; letter-spacing:.1em !important;
    border-radius:8px !important; padding:.45rem 1.1rem !important;
    width:auto !important; transition:all .2s !important;
    text-transform:uppercase;
}
div[data-testid="stDownloadButton"] button:hover {
    background:rgba(108,99,255,.15) !important;
    box-shadow:0 0 12px rgba(108,99,255,.25) !important;
}

.step-card {
    background:rgba(255,255,255,.03); border:1px solid rgba(255,255,255,.07);
    border-radius:14px; padding:1.2rem 1.5rem; margin-bottom:.9rem;
    position:relative; overflow:hidden; transition:all .3s;
}
.step-card.active { border-color:rgba(108,99,255,.5); background:rgba(108,99,255,.06); }
.step-card.done   { border-color:rgba(80,200,120,.3);  background:rgba(80,200,120,.03); }
.step-card::before {
    content:''; position:absolute; left:0; top:0; bottom:0; width:3px;
    border-radius:14px 0 0 14px; background:rgba(255,255,255,.05); transition:background .3s;
}
.step-card.active::before { background:#6C63FF; }
.step-card.done::before   { background:#50c878; }
.step-header { display:flex; align-items:center; gap:.8rem; margin-bottom:.2rem; }
.step-num {
    font-family:'DM Mono',monospace; font-size:.68rem;
    font-weight:500; letter-spacing:.15em; color:#6C63FF; opacity:.8;
}
.step-title { font-family:'Syne',sans-serif; font-size:.95rem; font-weight:700; color:#f0ebe0; }
.step-status { margin-left:auto; font-family:'DM Mono',monospace; font-size:.68rem; letter-spacing:.1em; }
.status-waiting { color:#444; }
.status-running { color:#6C63FF; }
.status-done    { color:#50c878; }
.step-desc { font-size:.78rem; color:#5e5650; margin-top:.15rem; padding-left:1.6rem; }

.section-heading {
    font-family:'Syne',sans-serif; font-size:1.4rem; font-weight:700;
    color:#f0ebe0; margin:1.5rem 0 1rem;
}

.result-panel {
    background:rgba(255,255,255,.025); border:1px solid rgba(255,255,255,.07);
    border-radius:14px; padding:1.6rem 1.8rem; margin-bottom:.75rem;
}
.result-panel-title {
    font-family:'DM Mono',monospace; font-size:.68rem; font-weight:500;
    letter-spacing:.2em; text-transform:uppercase; color:#6C63FF;
    margin-bottom:.9rem; padding-bottom:.6rem;
    border-bottom:1px solid rgba(108,99,255,.2);
}
.result-content {
    font-size:.88rem; line-height:1.9; color:#b0a89e;
    white-space:pre-wrap; font-family:'DM Sans',sans-serif; font-weight:300;
}

.report-panel {
    background:rgba(255,255,255,.025); border:1px solid rgba(108,99,255,.25);
    border-radius:16px; padding:2rem 2.5rem; margin-bottom:1rem;
}
.feedback-panel {
    background:rgba(255,255,255,.025); border:1px solid rgba(80,200,120,.2);
    border-radius:16px; padding:2rem 2.5rem; margin-bottom:1rem;
}
.panel-label {
    font-family:'DM Mono',monospace; font-size:.68rem; letter-spacing:.2em;
    text-transform:uppercase; margin-bottom:1rem; padding-bottom:.6rem; font-weight:500;
}
.panel-label.violet { color:#6C63FF; border-bottom:1px solid rgba(108,99,255,.2); }
.panel-label.green  { color:#50c878; border-bottom:1px solid rgba(80,200,120,.15); }

div[data-testid="stExpander"] {
    background:rgba(255,255,255,.025) !important;
    border:1px solid rgba(255,255,255,.07) !important;
    border-radius:14px !important; margin-bottom:.75rem;
}
div[data-testid="stExpander"] > details > summary {
    font-family:'DM Mono',monospace !important; font-size:.72rem !important;
    color:#a09890 !important; letter-spacing:.1em !important; padding:.9rem 1.1rem;
}
div[data-testid="stExpanderDetails"] { background:transparent !important; }
.stSpinner > div { color:#6C63FF !important; }
div[data-testid="stAlert"] {
    background:rgba(108,99,255,.06) !important;
    border:1px solid rgba(108,99,255,.25) !important;
    border-radius:10px !important; color:#6C63FF !important;
}
.notice {
    font-family:'DM Mono',monospace; font-size:.65rem; color:#383430;
    text-align:center; margin-top:3rem; letter-spacing:.12em;
}
</style>
""", unsafe_allow_html=True)


# ── Content parser ────────────────────────────────────────────────────────────
def to_str(val):
    if isinstance(val, str):
        return val
    if isinstance(val, list):
        parts = []
        for item in val:
            if isinstance(item, dict):
                if item.get("type") == "text":
                    parts.append(item.get("text", ""))
            else:
                parts.append(str(item))
        return "\n".join(p for p in parts if p.strip())
    return str(val)


# ── Step card renderer ────────────────────────────────────────────────────────
def step_card(num, title, state, desc=""):
    status_map = {
        "waiting": ("WAITING",   "status-waiting"),
        "running": ("● RUNNING", "status-running"),
        "done":    ("✓ DONE",    "status-done"),
    }
    label, cls = status_map.get(state, ("", ""))
    card_cls = {"running": "active", "done": "done"}.get(state, "")
    st.markdown(f"""
    <div class="step-card {card_cls}">
        <div class="step-header">
            <span class="step-num">{num}</span>
            <span class="step-title">{title}</span>
            <span class="step-status {cls}">{label}</span>
        </div>
        {"<div class='step-desc'>" + desc + "</div>" if desc else ""}
    </div>
    """, unsafe_allow_html=True)


# ── Session state ─────────────────────────────────────────────────────────────
for k, v in [("results", {}), ("running", False), ("done", False),
              ("active_step", -1), ("clear_topic", False)]:
    if k not in st.session_state:
        st.session_state[k] = v


# ── Handle clear ──────────────────────────────────────────────────────────────
# We use a flag + rerun trick because st.text_input can't be cleared directly
if st.session_state.get("clear_topic"):
    st.session_state["topic_input"] = ""
    st.session_state["clear_topic"] = False
    st.session_state["results"]     = {}
    st.session_state["running"]     = False
    st.session_state["done"]        = False
    st.session_state["active_step"] = -1


# ── Hero ──────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="hero">
    <div class="hero-eyebrow">Multi-Agent AI System</div>
    <h1><span class="white">Research</span><span class="blue">Mind</span></h1>
    <p class="hero-sub">Four specialized AI agents collaborate — searching, scraping, writing,
    and critiquing — to deliver a polished research report on any topic.</p>
</div>
<div class="divider"></div>
""", unsafe_allow_html=True)


# ── Layout ────────────────────────────────────────────────────────────────────
col_input, col_spacer, col_pipeline = st.columns([5, 0.4, 4])

with col_input:
    st.markdown('<div class="input-card">', unsafe_allow_html=True)

    # Fix 1: on_change fires when user presses Enter in the text input
    def on_enter():
        val = st.session_state.get("topic_input", "").strip()
        if val and not st.session_state.running:
            st.session_state.results     = {}
            st.session_state.running     = True
            st.session_state.done        = False
            st.session_state.active_step = 0

    topic = st.text_input(
        "Research Topic",
        placeholder="e.g. Quantum computing breakthroughs in 2025",
        key="topic_input",
        on_change=on_enter,   # ← Enter key now triggers the pipeline
    )

    btn_col1, btn_col2 = st.columns([3, 1])
    with btn_col1:
        run_btn = st.button("⚡  Run Research Pipeline", use_container_width=True)
    with btn_col2:
        # Fix 2: Clear button
        clear_btn = st.button("✕  Clear", use_container_width=True)

    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown("""
    <div style="display:flex;align-items:center;gap:.6rem;flex-wrap:wrap;margin-top:.25rem;">
        <span style="font-family:'DM Mono',monospace;font-size:.65rem;color:#555;letter-spacing:.1em;">TRY →</span>
        <span style="background:rgba(255,255,255,.04);border:1px solid rgba(255,255,255,.08);border-radius:6px;padding:.25rem .7rem;font-size:.75rem;color:#a09890;">LLM agents 2025</span>
        <span style="background:rgba(255,255,255,.04);border:1px solid rgba(255,255,255,.08);border-radius:6px;padding:.25rem .7rem;font-size:.75rem;color:#a09890;">CRISPR gene editing</span>
        <span style="background:rgba(255,255,255,.04);border:1px solid rgba(255,255,255,.08);border-radius:6px;padding:.25rem .7rem;font-size:.75rem;color:#a09890;">Fusion energy progress</span>
    </div>
    """, unsafe_allow_html=True)


# ── Fix 3: Pipeline shows live step-by-step using active_step ─────────────────
with col_pipeline:
    st.markdown('<div class="section-heading">Pipeline</div>', unsafe_allow_html=True)

    r    = st.session_state.results
    STEPS = ["search", "reader", "writer", "critic"]

    def get_state(i, step):
        if step in r:
            return "done"
        if st.session_state.running and st.session_state.active_step == i:
            return "running"
        return "waiting"

    step_card("01", "Search Agent", get_state(0, "search"), "Gathers recent web information")
    step_card("02", "Reader Agent", get_state(1, "reader"), "Scrapes & extracts deep content")
    step_card("03", "Writer Chain", get_state(2, "writer"), "Drafts the full research report")
    step_card("04", "Critic Chain", get_state(3, "critic"), "Reviews & scores the report")


# ── Handle clear button ───────────────────────────────────────────────────────
if clear_btn:
    st.session_state["clear_topic"] = True
    st.rerun()

# ── Handle run button ─────────────────────────────────────────────────────────
if run_btn:
    val = st.session_state.get("topic_input", "").strip()
    if not val:
        st.warning("Please enter a research topic first.")
    else:
        st.session_state.results     = {}
        st.session_state.running     = True
        st.session_state.done        = False
        st.session_state.active_step = 0
        st.rerun()


# ── Execute pipeline (step-by-step with rerun between steps) ──────────────────
if st.session_state.running and not st.session_state.done:
    topic_val = st.session_state.topic_input
    results   = dict(st.session_state.results)
    step      = st.session_state.active_step

    # Step 0 — Search
    if step == 0 and "search" not in results:
        with st.spinner("🔍  Search Agent is working…"):
            search_agent = build_search_agent()
            sr = search_agent.invoke({
                "messages": [("user", f"Find recent, reliable and detailed information about: {topic_val}")]
            })
            results["search"] = to_str(sr["messages"][-1].content)
        st.session_state.results     = dict(results)
        st.session_state.active_step = 1
        st.rerun()

    # Step 1 — Reader
    elif step == 1 and "reader" not in results:
        with st.spinner("📄  Reader Agent is scraping top resources…"):
            reader_agent = build_reader_agent()
            rr = reader_agent.invoke({
                "messages": [("user",
                    f"Based on the following search results about '{topic_val}', "
                    f"pick the most relevant URL and scrape it for deeper content.\n\n"
                    f"Search Results:\n{results['search'][:800]}"
                )]
            })
            results["reader"] = to_str(rr["messages"][-1].content)
        st.session_state.results     = dict(results)
        st.session_state.active_step = 2
        st.rerun()

    # Step 2 — Writer
    elif step == 2 and "writer" not in results:
        with st.spinner("✍️  Writer is drafting the report…"):
            research_combined = (
                f"SEARCH RESULTS:\n{results['search']}\n\n"
                f"DETAILED SCRAPED CONTENT:\n{results['reader']}"
            )
            results["writer"] = to_str(writer_chain.invoke({
                "topic": topic_val,
                "research": research_combined,
            }))
        st.session_state.results     = dict(results)
        st.session_state.active_step = 3
        st.rerun()

    # Step 3 — Critic
    elif step == 3 and "critic" not in results:
        with st.spinner("🧐  Critic is reviewing the report…"):
            results["critic"] = to_str(critic_chain.invoke({
                "report": results["writer"]
            }))
        st.session_state.results     = dict(results)
        st.session_state.active_step = 4
        st.session_state.running     = False
        st.session_state.done        = True
        st.rerun()


# ── Results ───────────────────────────────────────────────────────────────────
r = st.session_state.results

if r:
    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
    st.markdown('<div class="section-heading">Results</div>', unsafe_allow_html=True)

    if "search" in r:
        with st.expander("🔍  Search Results", expanded=False):
            st.markdown(
                f'<div class="result-panel">'
                f'<div class="result-panel-title">Search Agent Output</div>'
                f'<div class="result-content">{r["search"]}</div>'
                f'</div>',
                unsafe_allow_html=True,
            )
            st.download_button(
                label="⬇  Download",
                data=r["search"],
                file_name=f"search_results_{int(time.time())}.txt",
                mime="text/plain",
                key="dl_search",
            )

    if "reader" in r:
        with st.expander("📄  Scraped Content", expanded=False):
            st.markdown(
                f'<div class="result-panel">'
                f'<div class="result-panel-title">Reader Agent Output</div>'
                f'<div class="result-content">{r["reader"]}</div>'
                f'</div>',
                unsafe_allow_html=True,
            )
            st.download_button(
                label="⬇  Download",
                data=r["reader"],
                file_name=f"scraped_content_{int(time.time())}.txt",
                mime="text/plain",
                key="dl_reader",
            )

    if "writer" in r:
        st.markdown('<div class="report-panel"><div class="panel-label violet">📝 Final Research Report</div>', unsafe_allow_html=True)
        st.markdown(r["writer"])
        st.markdown('</div>', unsafe_allow_html=True)
        col_a, col_b = st.columns([1, 4])
        with col_a:
            st.download_button(
                label="⬇  Download Report (.md)",
                data=r["writer"],
                file_name=f"research_report_{int(time.time())}.md",
                mime="text/markdown",
                key="dl_report",
            )

    if "critic" in r:
        st.markdown('<div class="feedback-panel"><div class="panel-label green">🧐 Critic Feedback</div>', unsafe_allow_html=True)
        st.markdown(r["critic"])
        st.markdown('</div>', unsafe_allow_html=True)
        col_c, col_d = st.columns([1, 4])
        with col_c:
            st.download_button(
                label="⬇  Download Feedback (.txt)",
                data=r["critic"],
                file_name=f"critic_feedback_{int(time.time())}.txt",
                mime="text/plain",
                key="dl_critic",
            )

    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
    full_export = "\n\n".join([
        f"TOPIC: {st.session_state.topic_input}",
        f"=== SEARCH RESULTS ===\n{r.get('search', '')}",
        f"=== SCRAPED CONTENT ===\n{r.get('reader', '')}",
        f"=== FINAL REPORT ===\n{r.get('writer', '')}",
        f"=== CRITIC FEEDBACK ===\n{r.get('critic', '')}",
    ])
    st.download_button(
        label="⬇  Download Full Research Package (.txt)",
        data=full_export,
        file_name=f"research_package_{int(time.time())}.txt",
        mime="text/plain",
        key="dl_full",
        use_container_width=True,
    )


# ── Footer ────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="notice">
    ResearchMind · Powered by LangChain multi-agent pipeline · Built with Streamlit
</div>
""", unsafe_allow_html=True)