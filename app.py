import os
import streamlit as st
from dotenv import load_dotenv

load_dotenv()

st.set_page_config(
    page_title="viAct | Industry Page Generator",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ─────────────────────────────── CSS ─────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Jost:wght@300;400;500;600;700;800&display=swap');

/* ── Global reset ── */
html, body, .stApp { font-family: 'Jost', sans-serif !important; background: #0a0a0a !important; }
.stMainBlockContainer, .main .block-container {
    max-width: 980px !important;
    padding: 0 2rem 6rem 2rem !important;
}
#MainMenu, footer, header { visibility: hidden !important; }

/* ── Typography ── */
h1, h2, h3, h4 { font-family: 'Jost', sans-serif !important; color: #fff !important; }

/* ── Text inputs ── */
.stTextInput label, .stTextArea label, .stFileUploader label {
    font-family: 'Jost', sans-serif !important;
    font-size: 0.68rem !important; font-weight: 700 !important;
    letter-spacing: 1.8px !important; text-transform: uppercase !important;
    color: #4a4a4a !important;
}
.stTextInput input {
    background: #111 !important; border: 1.5px solid #1e1e1e !important;
    border-radius: 8px !important; color: #eee !important;
    font-family: 'Jost', sans-serif !important; font-size: 0.95rem !important;
    padding: 0.65rem 0.9rem !important;
}
.stTextInput input:focus {
    border-color: #ff6a3d !important;
    box-shadow: 0 0 0 3px rgba(255,106,61,0.1) !important;
    outline: none !important;
}
.stTextInput input::placeholder { color: #2e2e2e !important; }

/* ── Text areas ── */
.stTextArea textarea {
    background: #111 !important; border: 1.5px solid #1e1e1e !important;
    border-radius: 8px !important; color: #bbb !important;
    font-family: 'Jost', sans-serif !important; font-size: 0.85rem !important;
    padding: 0.65rem 0.9rem !important; line-height: 1.65 !important;
}
.stTextArea textarea:focus {
    border-color: #ff6a3d !important;
    box-shadow: 0 0 0 3px rgba(255,106,61,0.1) !important;
}
.stTextArea textarea::placeholder { color: #2a2a2a !important; }

/* ── File uploader ── */
[data-testid="stFileUploaderDropzone"] {
    background: #111 !important; border: 1.5px dashed #1e1e1e !important;
    border-radius: 8px !important;
    padding: 0.75rem 1.1rem !important;
    box-sizing: border-box !important;
}
[data-testid="stFileUploaderDropzone"] > div {
    display: flex !important;
    flex-direction: row !important;
    align-items: center !important;
    justify-content: space-between !important;
    gap: 1rem !important;
    flex-wrap: nowrap !important;
}
[data-testid="stFileUploaderDropzone"]:hover { border-color: #ff6a3d !important; }
[data-testid="stFileUploaderDropzone"] span,
[data-testid="stFileUploaderDropzone"] small,
[data-testid="stFileUploaderDropzone"] p { color: #333 !important; font-family: 'Jost', sans-serif !important; }

/* ── PRIMARY BUTTONS — orange filled ── */
button[kind="primary"],
button[data-testid="baseButton-primary"] {
    font-family: 'Jost', sans-serif !important; font-weight: 700 !important;
    font-size: 0.72rem !important; letter-spacing: 1.5px !important;
    text-transform: uppercase !important; border-radius: 6px !important;
    background: #ff6a3d !important; color: #fff !important;
    border: 2px solid #ff6a3d !important;
    transition: all 0.18s ease !important; cursor: pointer !important;
}
button[kind="primary"]:hover,
button[data-testid="baseButton-primary"]:hover {
    background: #e55a2e !important; border-color: #e55a2e !important;
    box-shadow: 0 4px 20px rgba(255,106,61,0.28) !important;
}

/* ── SECONDARY BUTTONS — ghost pill (chips, refine) ── */
button[kind="secondary"],
button[data-testid="baseButton-secondary"] {
    font-family: 'Jost', sans-serif !important; font-weight: 600 !important;
    font-size: 0.68rem !important; letter-spacing: 1px !important;
    text-transform: uppercase !important; border-radius: 20px !important;
    background: transparent !important; color: #ff6a3d !important;
    border: 1.5px solid rgba(255,106,61,0.3) !important;
    transition: all 0.18s ease !important;
}
button[kind="secondary"]:hover,
button[data-testid="baseButton-secondary"]:hover {
    background: rgba(255,106,61,0.07) !important;
    border-color: #ff6a3d !important;
}

/* ── FILE UPLOADER BROWSE BUTTON — override pill + uppercase from secondary ── */
[data-testid="stFileUploaderDropzone"] button,
[data-testid="stFileUploader"] section button {
    border-radius: 6px !important; border: 1px solid #222 !important;
    color: #555 !important; background: #1a1a1a !important;
    font-size: 0.72rem !important; letter-spacing: 0.5px !important;
    padding: 0.35rem 0.9rem !important;
    text-transform: none !important;
    flex-shrink: 0 !important;
    white-space: nowrap !important;
}
[data-testid="stFileUploaderDropzone"] button:hover,
[data-testid="stFileUploader"] section button:hover {
    border-color: #ff6a3d !important; color: #ff6a3d !important;
    background: #1a1a1a !important; box-shadow: none !important;
}

/* ── DOWNLOAD BUTTON — subtle ghost override ── */
[data-testid="stDownloadButton"] button {
    border-radius: 5px !important; border-color: #1c1c1c !important;
    color: #444 !important; font-size: 0.65rem !important; padding: 0.3rem 0.8rem !important;
}
[data-testid="stDownloadButton"] button:hover {
    border-color: #ff6a3d !important; color: #ff6a3d !important;
    background: transparent !important;
}

/* ── AGENT BUTTON VARIANTS via :has() — differentiates 3 generate buttons ── */
/* Agent 02: orange outline */
.stElementContainer:has(.agent-btn-02) + .stElementContainer button[kind="primary"],
.stElementContainer:has(.agent-btn-02) + .stElementContainer button[data-testid="baseButton-primary"] {
    background: transparent !important; color: #ff6a3d !important;
    border: 2px solid #ff6a3d !important; box-shadow: none !important;
}
.stElementContainer:has(.agent-btn-02) + .stElementContainer button[kind="primary"]:hover,
.stElementContainer:has(.agent-btn-02) + .stElementContainer button[data-testid="baseButton-primary"]:hover {
    background: rgba(255,106,61,0.07) !important; box-shadow: none !important;
}
/* Agent 03: dark ghost */
.stElementContainer:has(.agent-btn-03) + .stElementContainer button[kind="primary"],
.stElementContainer:has(.agent-btn-03) + .stElementContainer button[data-testid="baseButton-primary"] {
    background: #141414 !important; color: #777 !important;
    border: 2px solid #1e1e1e !important; box-shadow: none !important;
}
.stElementContainer:has(.agent-btn-03) + .stElementContainer button[kind="primary"]:hover,
.stElementContainer:has(.agent-btn-03) + .stElementContainer button[data-testid="baseButton-primary"]:hover {
    border-color: #ff6a3d !important; color: #ff6a3d !important;
    background: rgba(255,106,61,0.04) !important; box-shadow: none !important;
}

/* ── EXPANDERS ── */
details[data-testid="stExpander"] {
    border: 1px solid #1a1a1a !important; border-radius: 8px !important;
    background: #0e0e0e !important; overflow: hidden !important;
}
details[data-testid="stExpander"] summary {
    font-family: 'Jost', sans-serif !important; color: #555 !important;
    font-size: 0.78rem !important; font-weight: 600 !important;
    letter-spacing: 0.3px !important; padding: 0.7rem 1rem !important;
    list-style: none !important;
}
details[data-testid="stExpander"] summary:hover { color: #ff6a3d !important; }
details[data-testid="stExpander"] summary::-webkit-details-marker { display: none; }
details[data-testid="stExpander"] > div { background: #0a0a0a !important; padding: 1rem !important; }
/* fallback for older Streamlit selectors */
.streamlit-expanderHeader {
    background: #0e0e0e !important; color: #555 !important;
    font-family: 'Jost', sans-serif !important; font-size: 0.78rem !important;
    font-weight: 600 !important; border-radius: 8px !important;
}

/* ── TABS ── */
.stTabs [data-baseweb="tab-list"] {
    background: #0e0e0e !important; border-bottom: 1px solid #1a1a1a !important;
}
.stTabs [data-baseweb="tab"] {
    background: transparent !important; color: #444 !important;
    font-family: 'Jost', sans-serif !important; font-weight: 600 !important;
    font-size: 0.75rem !important; letter-spacing: 0.3px !important;
    padding: 0.65rem 1.2rem !important; border: none !important;
}
.stTabs [aria-selected="true"] {
    color: #ff6a3d !important; border-bottom: 2px solid #ff6a3d !important;
}
.stTabs [data-baseweb="tab-panel"] {
    background: #0a0a0a !important; border: 1px solid #1a1a1a !important;
    border-top: none !important; border-radius: 0 0 8px 8px !important;
    padding: 1.2rem !important;
}

/* ── CODE BLOCKS ── */
pre, .stCode { background: #080808 !important; border: 1px solid #1a1a1a !important; border-radius: 8px !important; }
code { font-size: 0.8rem !important; }

/* ── ALERTS ── */
.stAlert { border-radius: 8px !important; font-family: 'Jost', sans-serif !important; }
.stSuccess { border-left-color: #ff6a3d !important; }

/* ── SPINNER ── */
.stSpinner > div > div { border-top-color: #ff6a3d !important; }

/* ── SCROLLBAR ── */
::-webkit-scrollbar { width: 3px; height: 3px; }
::-webkit-scrollbar-track { background: #0a0a0a; }
::-webkit-scrollbar-thumb { background: #1e1e1e; border-radius: 4px; }
::-webkit-scrollbar-thumb:hover { background: #ff6a3d; }
</style>
""", unsafe_allow_html=True)


# ─────────────────────────── CONSTANTS ───────────────────────────────────────
AGENT_META = {
    "sections": {
        "num": "01", "btn_num": "01",
        "agent_name": "Content Agent",
        "title": "SEO Webpage — Dynamic Sections",
        "desc": "Hero (with YouTube video link), impact metrics ×3, AI CCTV use cases ×6, "
                "viGent EHS agent, testimonials ×4, and CTA — all H-tagged and word-count verified.",
        "tags": ["Hero + YouTube", "Metrics ×3", "Use Cases ×6", "viGent", "Reviews ×4", "CTA"],
        "btn_label": "Generate Content",
        "custom_placeholder": (
            "Tell the Content Agent exactly what you want — it will follow your instructions above everything else.\n\n"
            "Examples:\n"
            "• Focus on underground mining. Emphasise methane gas and slope failure detection.\n"
            "• Metrics must reference Asia-Pacific deployments (500,000+ workers covered).\n"
            "• Reviewer 1: Mine Safety Officer, Queensland. Reviewer 2: HSE Director, Indonesia.\n"
            "• Hero sub-headline must mention 'zero SIF' and 'predictive intelligence'.\n"
            "• Use cases: gas leak detection, haul truck proximity, blast zone compliance."
        ),
    },
    "seo": {
        "num": "02", "btn_num": "02",
        "agent_name": "On-Page SEO Agent",
        "title": "On-Page SEO — Meta & Alt Tags",
        "desc": "Meta title (≤60 chars), meta description (150–160 chars), 5–6 long-tail keywords, "
                "3 schema types, YouTube video SEO title & description, and alt texts for all 11 images.",
        "tags": ["Meta Title", "Meta Desc", "Keywords ×6", "Schema ×3", "Alt Texts ×11"],
        "btn_label": "Generate SEO",
        "custom_placeholder": (
            "Tell the SEO Agent your priorities — it will optimise precisely for them.\n\n"
            "Examples:\n"
            "• Primary keyword: 'AI safety monitoring for underground mining'. Target: Australia, India.\n"
            "• Include hreflang notes for en-AU and en-IN.\n"
            "• Video description should work for YouTube Shorts (60-second watch time).\n"
            "• Keywords must include 'SIF prevention AI' and 'predictive safety analytics mining'.\n"
            "• Meta description must open with: 'Stop reactive safety. viAct AI...'"
        ),
    },
    "images": {
        "num": "03", "btn_num": "03",
        "agent_name": "Image Prompt Agent",
        "title": "Nano Banana — AI Image Prompts",
        "desc": "11 production-ready prompts with exact pixel dimensions: 6 CCTV use case overlays, "
                "1 viGent dark-mode dashboard, 4 professional reviewer headshots. (Hero = YouTube video, no image.)",
        "tags": ["Use Cases ×6", "viGent 422×377", "Headshots ×4", "No Hero Image"],
        "btn_label": "Generate Prompts",
        "custom_placeholder": (
            "Tell the Image Prompt Agent exactly what you want — it will craft photorealistic, brand-aligned prompts.\n\n"
            "Examples:\n"
            "• All field images: underground mine tunnels with rock face walls, conveyor belts visible.\n"
            "• Workers: orange PPE. Bounding boxes: yellow for people, red for active hazard alerts.\n"
            "• Reviewer 1 = South Asian male, mid-40s. Reviewer 2 = White female, early 30s.\n"
            "• viGent dashboard: show methane gas level alert prominently with red pulsing indicator.\n"
            "• Lighting: dawn overcast, open-cut mine with haul trucks in background."
        ),
    },
}


# ─────────────────────────── HELPERS ─────────────────────────────────────────

def get_api_key() -> str:
    key = os.getenv("GROQ_API_KEY", "")
    if not key:
        try:
            key = st.secrets["GROQ_API_KEY"]
        except Exception:
            pass
    return key


def read_uploaded_file(uploaded) -> tuple[str, str]:
    name = uploaded.name.lower()
    try:
        if name.endswith((".txt", ".md")):
            text = uploaded.read().decode("utf-8", errors="ignore")
            return text, f"Extracted {len(text):,} chars from text file"
        if name.endswith(".pdf"):
            from pypdf import PdfReader
            r = PdfReader(uploaded)
            text = "\n".join(p.extract_text() or "" for p in r.pages)
            return text, f"Extracted {len(text):,} chars from {len(r.pages)} PDF pages"
        if name.endswith(".docx"):
            from docx import Document
            doc = Document(uploaded)
            text = "\n".join(p.text for p in doc.paragraphs)
            return text, f"Extracted {len(text):,} chars from Word document"
    except Exception as e:
        return "", f"Parse error: {e}"
    return "", "Unsupported file type"


def validate(industry: str) -> bool:
    if not industry.strip():
        st.warning("Enter an industry name first.")
        return False
    if not get_api_key():
        st.error("GROQ_API_KEY not found. Add it to your .env file.")
        return False
    return True


def divider():
    st.markdown("<div style='border-top:1px solid #161616;margin:2rem 0 1.8rem 0;'></div>",
                unsafe_allow_html=True)


def eyebrow(step: str, label: str):
    st.markdown(
        f'<p style="font-family:Jost,sans-serif;font-size:0.6rem;font-weight:700;'
        f'letter-spacing:3.5px;text-transform:uppercase;color:#ff6a3d;margin:0 0 0.15rem 0;">'
        f'{step} — {label}</p>',
        unsafe_allow_html=True,
    )


def section_heading(title: str, subtitle: str = ""):
    st.markdown(
        f'<h2 style="font-family:Jost,sans-serif;font-size:1.75rem;font-weight:800;'
        f'color:#fff;line-height:1.15;margin:0 0 {"0.35rem" if subtitle else "1.4rem"} 0;">'
        f'{title}</h2>',
        unsafe_allow_html=True,
    )
    if subtitle:
        st.markdown(
            f'<p style="font-family:Jost,sans-serif;font-size:0.88rem;color:#404040;'
            f'line-height:1.7;margin:0 0 1.4rem 0;max-width:580px;">{subtitle}</p>',
            unsafe_allow_html=True,
        )


def agent_card(meta: dict):
    tags_html = " ".join(
        f'<span style="display:inline-block;font-size:0.58rem;font-weight:600;'
        f'letter-spacing:0.8px;color:#ff6a3d;background:rgba(255,106,61,0.07);'
        f'border:1px solid rgba(255,106,61,0.18);padding:2px 7px;border-radius:20px;'
        f'margin:2px 2px 0 0;">{t}</span>'
        for t in meta["tags"]
    )
    st.markdown(
        f'<div style="background:#0e0e0e;border:1px solid #1a1a1a;'
        f'border-left:3px solid #ff6a3d;border-radius:10px;'
        f'padding:1rem 1.2rem 0.85rem 1.2rem;height:100%;box-sizing:border-box;">'
        f'<div style="font-size:0.56rem;font-weight:700;letter-spacing:4px;'
        f'text-transform:uppercase;color:#ff6a3d;margin-bottom:0.2rem;">{meta["num"]}</div>'
        f'<div style="font-size:0.96rem;font-weight:700;color:#f0f0f0;margin-bottom:0.12rem;'
        f'line-height:1.3;">{meta["title"]}</div>'
        f'<div style="font-size:0.8rem;color:#484848;line-height:1.55;margin-bottom:0.65rem;">'
        f'{meta["desc"]}</div>'
        f'<div style="line-height:1.8;">{tags_html}</div>'
        f'</div>',
        unsafe_allow_html=True,
    )


def result_block(key: str, label: str, content: str, custom_inst: str, gen_fn, industry: str, context: str):
    st.markdown(
        f'<div style="display:flex;align-items:center;gap:8px;margin-bottom:0.5rem;">'
        f'<div style="width:4px;height:4px;border-radius:50%;background:#ff6a3d;flex-shrink:0;"></div>'
        f'<span style="font-size:0.6rem;font-weight:700;letter-spacing:2.5px;'
        f'text-transform:uppercase;color:#ff6a3d;font-family:Jost,sans-serif;">{label}</span></div>',
        unsafe_allow_html=True,
    )
    tab1, tab2 = st.tabs(["Rendered Preview", "Raw Markdown — Copy"])
    with tab1:
        st.markdown(content)
    with tab2:
        st.code(content, language="markdown")

    # Download button
    fname = f"viact_{key}_{industry.lower().replace(' ','_').replace('&','and')}.md"
    st.download_button(
        "⬇ Download .md", data=content, file_name=fname,
        mime="text/markdown", key=f"dl_{key}",
    )

    # Refine expander
    with st.expander("Refine / Improve this output"):
        st.markdown(
            '<p style="font-size:0.78rem;color:#3a3a3a;font-family:Jost,sans-serif;margin:0 0 0.6rem 0;">'
            'Describe exactly what to change. The agent will apply your feedback and regenerate only this section.</p>',
            unsafe_allow_html=True,
        )
        feedback = st.text_area(
            "feedback",
            placeholder=(
                "e.g. Make the hero description more urgent. "
                "Metric 2 needs a dollar figure. "
                "Reviewer 3 should be from Saudi Arabia."
            ),
            height=90, key=f"feedback_{key}", label_visibility="collapsed",
        )
        if st.button("Regenerate with Improvements", key=f"refine_{key}", type="secondary"):
            if feedback.strip():
                combined = (custom_inst or "") + f"\n\nIMPROVEMENT FEEDBACK:\n{feedback}"
                with st.spinner("Applying improvements…"):
                    try:
                        st.session_state[f"{key}_out"] = gen_fn(
                            industry, get_api_key(), context, combined
                        )
                        st.rerun()
                    except Exception as e:
                        st.error(f"Regeneration failed: {e}")
            else:
                st.warning("Describe what to improve first.")

    st.markdown("<div style='height:16px;'></div>", unsafe_allow_html=True)


# ─────────────────────────── SESSION STATE ───────────────────────────────────
_state_defaults = {
    "sections_out": None, "seo_out": None, "images_out": None,
    "sections_custom": "", "seo_custom": "", "images_custom": "",
    "last_industry": "",
}
for k, v in _state_defaults.items():
    if k not in st.session_state:
        st.session_state[k] = v


# ══════════════════════════════════════════════════════════════════════════════
#  HEADER
# ══════════════════════════════════════════════════════════════════════════════
st.markdown("""
<div style="display:flex;align-items:center;justify-content:space-between;
            padding:1.6rem 0 1.4rem 0;border-bottom:1px solid #141414;margin-bottom:2.2rem;">
  <div style="display:flex;align-items:center;gap:10px;">
    <div style="width:4px;height:26px;background:#ff6a3d;border-radius:2px;flex-shrink:0;"></div>
    <span style="font-family:'Jost',sans-serif;font-size:1.3rem;font-weight:800;
                 color:#fff;letter-spacing:-0.3px;line-height:1;">
      vi<span style="color:#ff6a3d">Act</span>.ai
    </span>
  </div>
  <span style="font-family:'Jost',sans-serif;font-size:0.58rem;font-weight:700;
               letter-spacing:2.5px;text-transform:uppercase;color:#2e2e2e;">
    3-Agent Industry Page Generator
  </span>
</div>
""", unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
#  STEP 01 — CONFIGURE
# ══════════════════════════════════════════════════════════════════════════════
eyebrow("STEP 01", "CONFIGURE")
section_heading(
    "Define Your Industry",
    "Type your industry name below. Add a YouTube video URL for the hero section, "
    "a reference URL, or upload a document to ground the agents in your specific context.",
)

# ── Main inputs ───────────────────────────────────────────────────────────────
col_a, col_b = st.columns(2, gap="medium")
with col_a:
    industry = st.text_input(
        "Industry Name",
        placeholder="e.g. Mining, Oil & Gas, Logistics, Construction",
        key="industry_text",
    )
with col_b:
    ref_url = st.text_input(
        "Reference URL (optional)",
        placeholder="https://viact.ai/industry/... or competitor URL",
        key="ref_url_input",
    )

# ── YouTube video URL (hero section) ─────────────────────────────────────────
yt_url = st.text_input(
    "Hero YouTube Video URL",
    placeholder="https://www.youtube.com/watch?v=... — embedded in the hero section instead of a static image",
    key="yt_url_input",
)

# ── File upload ───────────────────────────────────────────────────────────────
uploaded_file = st.file_uploader(
    "Upload Reference Document (optional)",
    type=["txt", "md", "pdf", "docx"],
    help="Supported: .txt  .md  .pdf  .docx — agents read up to 4,000 chars",
    key="file_upload",
)

# ── Build context string ──────────────────────────────────────────────────────
context_parts = []
if yt_url.strip():
    context_parts.append(f"Hero YouTube Video URL: {yt_url.strip()}")
if ref_url.strip():
    context_parts.append(f"Reference URL: {ref_url.strip()}")
if uploaded_file:
    file_text, stat_msg = read_uploaded_file(uploaded_file)
    if file_text.strip():
        context_parts.append(f"Uploaded document:\n{file_text[:4000]}")
        st.markdown(
            f'<div style="background:rgba(255,106,61,0.04);border:1px solid rgba(255,106,61,0.15);'
            f'border-left:3px solid #ff6a3d;border-radius:6px;padding:0.55rem 0.9rem;'
            f'margin-top:0.4rem;font-size:0.72rem;color:#ff6a3d;font-family:Jost,sans-serif;">'
            f'{stat_msg}{"  ·  first 4,000 chars used" if len(file_text) > 4000 else ""}</div>',
            unsafe_allow_html=True,
        )
    else:
        st.warning(stat_msg or "Could not extract text — try a .txt or .md file.")
context = "\n\n".join(context_parts)

# Auto-clear results on industry change
if industry.strip() and industry.strip() != st.session_state.last_industry:
    st.session_state.sections_out = None
    st.session_state.seo_out = None
    st.session_state.images_out = None
    st.session_state.last_industry = industry.strip()


# ══════════════════════════════════════════════════════════════════════════════
#  STEP 02 — GENERATE
# ══════════════════════════════════════════════════════════════════════════════
divider()
eyebrow("STEP 02", "GENERATE")
section_heading(
    "Choose Your Agent",
    "Each agent is a specialist. Open the custom instructions panel to guide them precisely — "
    "your instructions take highest priority over the default rules.",
)

# ── Improvements & tips panel ─────────────────────────────────────────────────
with st.expander("Agent Tips & Improvement Areas"):
    c1, c2, c3 = st.columns(3, gap="medium")
    tip_style = (
        'background:#0e0e0e;border:1px solid #1a1a1a;border-radius:8px;'
        'padding:0.9rem 1rem;height:100%;'
    )
    with c1:
        st.markdown(
            f'<div style="{tip_style}">'
            f'<p style="font-size:0.6rem;font-weight:700;letter-spacing:2px;'
            f'text-transform:uppercase;color:#ff6a3d;margin:0 0 0.5rem 0;">Agent 01 — Content</p>'
            f'<p style="font-size:0.78rem;color:#484848;line-height:1.7;margin:0;">'
            f'<b style="color:#777;">Hero:</b> max 10 words + YouTube URL<br>'
            f'<b style="color:#777;">Sub-headline:</b> max 20 words, bold<br>'
            f'<b style="color:#777;">Description:</b> 35–45 words<br>'
            f'<b style="color:#777;">Metrics:</b> exactly 3, real numbers<br>'
            f'<b style="color:#777;">Use Cases:</b> 6 blocks, 20–30 words each<br>'
            f'<b style="color:#777;">Reviews:</b> 4 blocks, 35–50 words<br>'
            f'<b style="color:#777;">CTA:</b> 20–30 words<br><br>'
            f'<b style="color:#ff6a3d;">Tip:</b> Upload a competitor page for targeted output.'
            f'</p></div>',
            unsafe_allow_html=True,
        )
    with c2:
        st.markdown(
            f'<div style="{tip_style}">'
            f'<p style="font-size:0.6rem;font-weight:700;letter-spacing:2px;'
            f'text-transform:uppercase;color:#ff6a3d;margin:0 0 0.5rem 0;">Agent 02 — SEO</p>'
            f'<p style="font-size:0.78rem;color:#484848;line-height:1.7;margin:0;">'
            f'<b style="color:#777;">Meta Title:</b> ≤60 chars exactly<br>'
            f'<b style="color:#777;">Meta Desc:</b> 150–160 chars exactly<br>'
            f'<b style="color:#777;">Keywords:</b> 5–6 long-tail (3+ words)<br>'
            f'<b style="color:#777;">Schema:</b> LB + SoftwareApp + FAQ<br>'
            f'<b style="color:#777;">Alt Texts:</b> 11 images, ≤125 chars each<br>'
            f'<b style="color:#777;">Must mention:</b> CCTV, IoT, Edge, Wearables<br><br>'
            f'<b style="color:#ff6a3d;">Tip:</b> Specify target country for local SEO.'
            f'</p></div>',
            unsafe_allow_html=True,
        )
    with c3:
        st.markdown(
            f'<div style="{tip_style}">'
            f'<p style="font-size:0.6rem;font-weight:700;letter-spacing:2px;'
            f'text-transform:uppercase;color:#ff6a3d;margin:0 0 0.5rem 0;">Agent 03 — Images</p>'
            f'<p style="font-size:0.78rem;color:#484848;line-height:1.7;margin:0;">'
            f'<b style="color:#777;">Hero:</b> YouTube video — no image needed<br>'
            f'<b style="color:#777;">Use Cases:</b> 6 prompts, exact dimensions<br>'
            f'<b style="color:#777;">viGent:</b> 422×377 px, dark dashboard only<br>'
            f'<b style="color:#777;">Headshots:</b> 4 × 56×56 px professional<br>'
            f'<b style="color:#777;">Bounding boxes:</b> green (safe) / red (hazard)<br><br>'
            f'<b style="color:#ff6a3d;">Tip:</b> Specify PPE colour, lighting, worker ethnicity.'
            f'</p></div>',
            unsafe_allow_html=True,
        )

from tools.generate_content import generate_sections, generate_seo_metadata, generate_image_prompts


def agent_row(key: str, meta: dict, gen_fn):
    card_col, btn_col = st.columns([5, 2], gap="medium")
    with card_col:
        agent_card(meta)
    with btn_col:
        st.markdown("<div style='height:16px;'></div>", unsafe_allow_html=True)
        # Marker div for CSS :has() agent button targeting
        st.markdown(f'<div class="agent-btn-{meta["btn_num"]}"></div>', unsafe_allow_html=True)
        clicked = st.button(meta["btn_label"], key=f"btn_{key}", type="primary",
                            use_container_width=True)

    with st.expander(f"+ Custom Instructions — {meta['agent_name']}"):
        st.markdown(
            f'<p style="font-size:0.74rem;color:#ff6a3d;font-weight:600;'
            f'font-family:Jost,sans-serif;margin:0 0 0.5rem 0;">'
            f'The {meta["agent_name"]} follows your instructions with highest priority. '
            f'Be as specific as you want.</p>',
            unsafe_allow_html=True,
        )
        custom = st.text_area(
            "custom", value=st.session_state.get(f"{key}_custom", ""),
            placeholder=meta["custom_placeholder"],
            height=120, key=f"custom_ta_{key}", label_visibility="collapsed",
        )
        st.session_state[f"{key}_custom"] = custom

    st.markdown("<div style='height:8px;'></div>", unsafe_allow_html=True)

    if clicked and validate(industry):
        with st.spinner(f"{meta['agent_name']} generating for **{industry}**…"):
            try:
                st.session_state[f"{key}_out"] = gen_fn(
                    industry, get_api_key(), context,
                    st.session_state.get(f"{key}_custom", ""),
                )
                st.success(f"Agent {meta['num']} done.")
            except Exception as e:
                st.error(f"Generation failed: {e}")


# ── Render 3 agents ───────────────────────────────────────────────────────────
agent_row("sections", AGENT_META["sections"], generate_sections)
agent_row("seo",      AGENT_META["seo"],      generate_seo_metadata)
agent_row("images",   AGENT_META["images"],   generate_image_prompts)


# ══════════════════════════════════════════════════════════════════════════════
#  STEP 03 — OUTPUT
# ══════════════════════════════════════════════════════════════════════════════
has_results = any(st.session_state.get(f"{k}_out") for k in ("sections", "seo", "images"))

if has_results:
    divider()
    eyebrow("STEP 03", "OUTPUT")
    section_heading("Generated Results")

    if st.session_state.get("sections_out"):
        result_block(
            "sections", "01 — Webpage Dynamic Sections",
            st.session_state.sections_out,
            st.session_state.get("sections_custom", ""),
            generate_sections, industry, context,
        )
    if st.session_state.get("seo_out"):
        result_block(
            "seo", "02 — On-Page SEO Metadata",
            st.session_state.seo_out,
            st.session_state.get("seo_custom", ""),
            generate_seo_metadata, industry, context,
        )
    if st.session_state.get("images_out"):
        result_block(
            "images", "03 — Nano Banana Image Prompts",
            st.session_state.images_out,
            st.session_state.get("images_custom", ""),
            generate_image_prompts, industry, context,
        )
