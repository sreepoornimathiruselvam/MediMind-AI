"""
MediMind AI – Smart Health Intelligence Platform
Home page: UI foundation only. Nothing on this page analyzes real reports yet.

How this file is organized:
  1. Page settings
  2. Page content  -> edit these lists to change text and cards
  3. Styles        -> the MediMind look (colors, fonts, layout)
  4. Section builders -> small functions, one per section
  5. The page itself, top to bottom
"""

import textwrap

import streamlit as st

# ---------------------------------------------------------------
# 1. Page settings (must be the first Streamlit command)
# ---------------------------------------------------------------
st.set_page_config(
    page_title="MediMind AI",
    page_icon="🩺",
    layout="wide",
)

# ---------------------------------------------------------------
# 2. Page content
# ---------------------------------------------------------------
DISCLAIMER = (
    "MediMind AI is for educational and informational purposes only. "
    "It does not provide medical advice, diagnosis, or treatment."
)

STEPS = [
    ("Upload your report", "A PDF or a clear photo of your lab report."),
    ("Read it in plain words", "Each value explained simply, next to your report's own range."),
    ("Talk to your doctor", "Take a short list of questions to your next appointment."),
]

# (title, description, sketch name)
FEATURES = [
    ("AI report summary", "A short, plain-language overview of your whole report.", "summary"),
    ("Important values", "The results that deserve your attention, shown first.", "values"),
    ("Reference range comparison", "See where each value sits against your report's range.", "range"),
    ("Ask your report", "Ask questions about your results and get simple answers.", "ask"),
    ("Health trends", "Follow how a value changes across reports over time.", "trends"),
]

PRINCIPLES = [
    ("Explains, never diagnoses",
     "MediMind AI won't name conditions or suggest treatment. "
     "Every explanation points you back to your doctor."),
    ("Uses your report's own ranges",
     "Values are compared with the reference range printed on your report, "
     "not a generic chart from the internet."),
    ("Private by design",
     "Your report will be used only to create your explanation. "
     "It will never be sold or shared."),
]

# Small drawings (SVG) used on the page. Colors come from the CSS classes.
LOGO = ('<svg viewBox="0 0 32 32" aria-hidden="true"><path d="M5 17h5l2.5-6 4 11 3-8 1.5 3H27" '
        'fill="none" stroke="#fff" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round"/></svg>')
UPLOAD_ICON = ('<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M12 15V4M7.5 8.5 12 4l4.5 4.5'
               'M4 15v3a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2v-3"/></svg>')
INFO_ICON = '<svg viewBox="0 0 24 24" aria-hidden="true"><circle cx="12" cy="12" r="9"/><path d="M12 11v5M12 7.5v.5"/></svg>'

SKETCHES = {
    "summary": '<rect x="14" y="14" width="104" height="7" rx="3.5" class="s-ink"/>'
               '<rect x="14" y="29" width="132" height="7" rx="3.5" class="s-soft"/>'
               '<rect x="14" y="44" width="80" height="7" rx="3.5" class="s-soft"/>',
    "values": '<rect x="14" y="13" width="72" height="8" rx="4" class="s-soft"/>'
              '<rect x="110" y="10" width="36" height="14" rx="7" class="s-amber"/>'
              '<rect x="14" y="41" width="56" height="8" rx="4" class="s-soft"/>'
              '<rect x="110" y="38" width="36" height="14" rx="7" class="s-mint"/>',
    "range": '<rect x="14" y="29" width="132" height="6" rx="3" class="s-soft"/>'
             '<rect x="48" y="29" width="58" height="6" rx="3" class="s-ink"/>'
             '<circle cx="124" cy="32" r="7" class="s-amber"/>',
    "ask": '<rect x="14" y="9" width="90" height="20" rx="10" class="s-soft"/>'
           '<rect x="56" y="35" width="90" height="20" rx="10" class="s-ink"/>',
    "trends": '<polyline points="14,48 44,40 72,44 100,26 126,30 146,16" class="s-line"/>'
              '<circle cx="146" cy="16" r="4.5" class="s-ink"/>',
}

# ---------------------------------------------------------------
# 3. Styles
# ---------------------------------------------------------------
CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Atkinson+Hyperlegible+Next:wght@400;600;700&family=Atkinson+Hyperlegible+Mono:wght@400;500&display=swap');

:root {
  --paper: #F2F6F7;        /* page background: cool mist */
  --surface: #FFFFFF;      /* cards */
  --ink: #14303A;          /* main text */
  --slate: #56707A;        /* secondary text */
  --line: #D9E4E6;         /* borders */
  --lagoon: #1F6F78;       /* brand color */
  --lagoon-deep: #175961;
  --seafoam: #DDEFEC;      /* soft brand tint */
  --amber: #93590F;        /* "worth a look" text: calm, not alarming */
  --amber-mark: #D8963A;
  --amber-tint: #FBF1E3;
  --font: 'Atkinson Hyperlegible Next', system-ui, sans-serif;
  --mono: 'Atkinson Hyperlegible Mono', ui-monospace, monospace;
}

/* ---- Streamlit page shell ---- */
html, body, .stApp { font-family: var(--font); }
.stApp { background: var(--paper); color: var(--ink); }
[data-testid="stHeader"] { background: transparent; }
[data-testid="stMarkdownContainer"] { font-family: var(--font); }   /* use our font in st.markdown blocks */
[data-testid="stHeaderActionElements"] { display: none; }          /* hide Streamlit's heading link icons */
[data-testid="stMainBlockContainer"], .block-container {
  max-width: 1120px; padding: 1.25rem 1.5rem 3rem;
}

/* ---- Navigation ---- */
.mm-nav { display: flex; justify-content: space-between; align-items: center; padding: .5rem 0 1.25rem; }
.mm-brand { display: flex; align-items: center; gap: .75rem; }
.mm-logo { width: 42px; height: 42px; border-radius: 13px; background: var(--lagoon); display: grid; place-items: center; }
.mm-logo svg { width: 28px; height: 28px; }
.mm-wordmark { font-weight: 700; font-size: 1.15rem; line-height: 1.1; color: var(--ink); }
.mm-wordmark small { display: block; font-weight: 400; font-size: .82rem; color: var(--slate); }
.mm-pill { display: inline-flex; align-items: center; gap: .4rem; padding: .3rem .75rem; border-radius: 999px;
  background: var(--seafoam); color: var(--lagoon-deep); font-size: .82rem; font-weight: 600; white-space: nowrap; }
.mm-pill-quiet { background: var(--surface); border: 1px solid var(--line); color: var(--slate); }

/* ---- Hero (a Streamlit container with key="hero") ---- */
.st-key-hero { background: var(--surface); border: 1px solid var(--line); border-radius: 28px;
  padding: clamp(1.5rem, 4vw, 3.25rem); }
h1.mm-title { font-family: var(--font); font-size: clamp(2.2rem, 4.6vw, 3.4rem); font-weight: 700;
  line-height: 1.08; letter-spacing: -0.02em; color: var(--ink); margin: 0; padding: 0; max-width: 15ch; }
p.mm-lead { font-size: 1.15rem; line-height: 1.6; color: var(--slate); margin: 1.25rem 0 .5rem; max-width: 34em; }
p.mm-note { font-size: .9rem; color: var(--slate); margin: 0; }

/* ---- Main button (Streamlit button with key="cta") ---- */
.st-key-cta button { background: var(--lagoon); color: #fff; border: 0; border-radius: 999px;
  padding: .85rem 1.75rem; font-family: var(--font); font-weight: 600;
  box-shadow: 0 10px 24px -12px rgba(23, 89, 97, .7); transition: background-color .2s ease, transform .2s ease; }
.st-key-cta button p { font-size: 1.05rem; font-weight: 600; font-family: var(--font); }
.st-key-cta button:hover, .st-key-cta button:focus:not(:active) { background: var(--lagoon-deep); color: #fff; }
.st-key-cta button:hover { transform: translateY(-1px); }
.st-key-cta button:focus-visible { outline: 3px solid #8CC9C2; outline-offset: 3px; }

/* ---- Hero example: a lab report line, then the same line in plain words ---- */
.mm-report { background: var(--paper); border: 1px solid var(--line); border-radius: 22px; padding: 1.25rem; }
.mm-report-head { display: flex; justify-content: space-between; align-items: center; gap: .5rem;
  font-size: .88rem; color: var(--slate); margin-bottom: .75rem; }
.mm-raw { font-family: var(--mono); font-size: .86rem; display: grid; grid-template-columns: 1fr auto auto auto;
  gap: .75rem; padding: .8rem .9rem; background: var(--surface); border: 1px solid var(--line); border-radius: 10px; }
.mm-flag { color: var(--amber); font-weight: 500; }
.mm-plain { margin-top: .75rem; background: var(--surface); border: 1px solid var(--line); border-radius: 14px;
  padding: 1.1rem 1.15rem 1.2rem; animation: mm-reveal .8s ease-out .6s both; }
.mm-plain-label { font-size: .88rem; font-weight: 600; color: var(--lagoon); margin-bottom: .35rem; }
.mm-plain p { margin: 0; font-size: 1rem; line-height: 1.55; color: var(--ink); }
.mm-plain .mm-ask { margin-top: .4rem; font-size: .92rem; color: var(--slate); }
.mm-range { position: relative; height: 8px; background: #E7EEEF; border-radius: 99px; margin: 1.25rem 0 .45rem; }
.mm-range-band { position: absolute; left: 25%; width: 40%; top: 0; bottom: 0; background: #A9D3CE; border-radius: 99px; }
.mm-range-dot { position: absolute; left: 77.5%; top: 50%; width: 18px; height: 18px; margin: -9px 0 0 -9px;
  background: var(--amber-mark); border: 3px solid #fff; border-radius: 50%;
  box-shadow: 0 0 0 1px rgba(147, 89, 15, .35); animation: mm-slide 1s cubic-bezier(.2, .8, .2, 1) 1.1s both; }
.mm-range-scale { position: relative; height: 1.2rem; font-size: .8rem; color: var(--slate); margin-bottom: .75rem; }
.mm-range-scale span { position: absolute; transform: translateX(-50%); }
.mm-range-scale .you { color: var(--amber); font-weight: 600; }
@keyframes mm-reveal { from { opacity: 0; transform: translateY(8px); } to { opacity: 1; transform: none; } }
@keyframes mm-slide { from { left: 45%; opacity: 0; } to { left: 77.5%; opacity: 1; } }

/* ---- Sections ---- */
.mm-section { padding-top: clamp(2.5rem, 6vw, 4rem); }
h2.mm-h2 { font-family: var(--font); font-size: 1.75rem; font-weight: 700; letter-spacing: -0.01em;
  color: var(--ink); margin: 0; padding: 0; }
p.mm-sub { font-size: 1.02rem; line-height: 1.6; color: var(--slate); margin: .5rem 0 1.5rem; max-width: 40em; }

/* Upload placeholder + steps */
.mm-upload-grid { display: grid; grid-template-columns: 1.25fr 1fr; gap: 2rem; align-items: center; }
.mm-drop { border: 1.5px dashed #9CC5C3; background: #F8FBFB; border-radius: 22px; padding: 2.75rem 1.5rem;
  text-align: center; cursor: not-allowed; }
.mm-drop-icon { width: 58px; height: 58px; margin: 0 auto 1rem; border-radius: 50%; background: var(--seafoam);
  display: grid; place-items: center; }
.mm-drop-icon svg { width: 26px; height: 26px; fill: none; stroke: var(--lagoon); stroke-width: 2;
  stroke-linecap: round; stroke-linejoin: round; }
.mm-drop-title { font-size: 1.15rem; font-weight: 600; color: var(--ink); }
.mm-drop-text { color: var(--slate); margin: .3rem 0 1rem; }
h3.mm-steps-title { font-family: var(--font); font-size: 1rem; font-weight: 600; color: var(--ink); margin: 0 0 1rem; }
.mm-steps { list-style: none; margin: 0; padding: 0; display: grid; gap: 1.1rem; }
.mm-steps li { display: grid; grid-template-columns: 34px 1fr; gap: .9rem; align-items: start; margin: 0; }
.mm-step-num { width: 34px; height: 34px; border-radius: 50%; border: 1.5px solid var(--lagoon); color: var(--lagoon);
  display: grid; place-items: center; font-weight: 700; }
.mm-steps strong { color: var(--ink); }
.mm-steps p { margin: .15rem 0 0; color: var(--slate); font-size: .95rem; line-height: 1.5; }

/* Planned feature cards */
.mm-features { display: grid; grid-template-columns: repeat(auto-fit, minmax(190px, 1fr)); gap: 1rem; }
.mm-feature { background: var(--surface); border: 1px solid var(--line); border-radius: 18px; padding: 1rem 1rem 1.15rem;
  display: flex; flex-direction: column; }
.mm-sketch { background: var(--paper); border-radius: 12px; margin-bottom: .9rem; }
.mm-sketch svg { display: block; width: 100%; height: 64px; }
.s-ink { fill: var(--lagoon); } .s-soft { fill: #CFDFE1; } .s-mint { fill: #A9D3CE; } .s-amber { fill: var(--amber-mark); }
.s-line { fill: none; stroke: var(--lagoon); stroke-width: 3; stroke-linecap: round; stroke-linejoin: round; }
.mm-feature h3 { font-family: var(--font); font-size: 1.02rem; font-weight: 700; color: var(--ink); margin: 0; padding: 0; }
.mm-feature p { font-size: .93rem; line-height: 1.5; color: var(--slate); margin: .35rem 0 .9rem; flex-grow: 1; }
.mm-feature .mm-pill { align-self: flex-start; }

/* Trust principles */
.mm-principles { display: grid; grid-template-columns: repeat(auto-fit, minmax(240px, 1fr)); gap: 1.5rem 2rem; }
.mm-principle { border-top: 2px solid var(--lagoon); padding-top: 1rem; }
.mm-principle h3 { font-family: var(--font); font-size: 1.1rem; font-weight: 700; color: var(--ink); margin: 0; padding: 0; }
.mm-principle p { color: var(--slate); line-height: 1.6; margin: .4rem 0 0; }

/* Disclaimer */
.mm-disclaimer { display: flex; gap: 1rem; align-items: flex-start; background: var(--amber-tint);
  border: 1px solid #EBD3AE; border-radius: 18px; padding: 1.25rem 1.5rem; margin-top: clamp(2.5rem, 6vw, 4rem); }
.mm-disclaimer svg { flex: none; width: 24px; height: 24px; fill: none; stroke: var(--amber); stroke-width: 2;
  stroke-linecap: round; }
.mm-disclaimer strong { color: var(--ink); }
.mm-disclaimer p { margin: .25rem 0 0; color: var(--ink); line-height: 1.6; }

/* Footer */
.mm-footer { display: flex; justify-content: space-between; flex-wrap: wrap; gap: .5rem; margin-top: 2.5rem;
  padding-top: 1.5rem; border-top: 1px solid var(--line); font-size: .88rem; color: var(--slate); }

/* ---- Small screens and reduced motion ---- */
@media (max-width: 760px) {
  .mm-upload-grid { grid-template-columns: 1fr; }
  .mm-nav .mm-pill { display: none; }
  .mm-raw { grid-template-columns: 1fr auto auto; }
  .mm-raw span:first-child { grid-column: 1 / -1; }   /* test name on its own row */
}
.mm-raw span + span { white-space: nowrap; }
@media (prefers-reduced-motion: reduce) {
  .mm-plain, .mm-range-dot { animation: none; }
  .st-key-cta button { transition: none; }
}
</style>
"""


# ---------------------------------------------------------------
# 4. Section builders
# ---------------------------------------------------------------
def show_html(markup):
    """Put a block of our own HTML on the page.

    st.markdown with unsafe_allow_html=True keeps the SVG drawings.
    (st.html removes SVG, so we only use it for the stylesheet.)
    textwrap.dedent removes the code indentation so Markdown doesn't
    mistake the HTML for a code block.
    """
    st.markdown(textwrap.dedent(markup), unsafe_allow_html=True)


def nav():
    show_html(f"""
    <nav class="mm-nav">
      <div class="mm-brand">
        <span class="mm-logo">{LOGO}</span>
        <span class="mm-wordmark">MediMind AI<small>Smart Health Intelligence Platform</small></span>
      </div>
      <span class="mm-pill">Early preview</span>
    </nav>
    """)


def hero_text():
    show_html("""
    <h1 class="mm-title">Understand your medical reports in simple language.</h1>
    <p class="mm-lead">MediMind AI is an AI assistant, now in development, that reads your lab report
    and explains each value in calm, everyday words. You'll know what your results mean
    and what to ask your doctor.</p>
    """)


def hero_example():
    show_html("""
    <div class="mm-report">
      <div class="mm-report-head">
        <span>A line from a lab report</span>
        <span class="mm-pill mm-pill-quiet">Illustrative example</span>
      </div>
      <div class="mm-raw">
        <span>HbA1c (Glycated Hb)</span><span>6.1 %</span><span>4.0–5.6</span><span class="mm-flag">H</span>
      </div>
      <div class="mm-plain">
        <div class="mm-plain-label">In plain words</div>
        <p>HbA1c reflects your average blood sugar over the past 2–3 months.
        Your result is a little above the range printed on this report.</p>
        <div class="mm-range"><div class="mm-range-band"></div><div class="mm-range-dot"></div></div>
        <div class="mm-range-scale">
          <span style="left:25%">4.0</span><span style="left:65%">5.6</span>
          <span class="you" style="left:77.5%">6.1</span>
        </div>
        <p class="mm-ask">A good question for your doctor: "What does this result mean for me?"</p>
      </div>
    </div>
    """)


def upload_section():
    steps = "".join(
        f'<li><span class="mm-step-num">{n}</span><div><strong>{title}</strong><p>{text}</p></div></li>'
        for n, (title, text) in enumerate(STEPS, start=1)
    )
    show_html(f"""
    <section class="mm-section">
      <h2 class="mm-h2">Upload your medical report</h2>
      <p class="mm-sub">This is where your report will go. Uploading isn't switched on yet.
      It's the next part being built.</p>
      <div class="mm-upload-grid">
        <div class="mm-drop" aria-disabled="true">
          <div class="mm-drop-icon">{UPLOAD_ICON}</div>
          <div class="mm-drop-title">Drop your report here</div>
          <div class="mm-drop-text">PDF, JPG or PNG files</div>
          <span class="mm-pill mm-pill-quiet">Not available yet</span>
        </div>
        <div>
          <h3 class="mm-steps-title">How it will work</h3>
          <ol class="mm-steps">{steps}</ol>
        </div>
      </div>
    </section>
    """)


def features_section():
    cards = "".join(
        f'<article class="mm-feature">'
        f'<div class="mm-sketch"><svg viewBox="0 0 160 64" aria-hidden="true">{SKETCHES[sketch]}</svg></div>'
        f'<h3>{title}</h3><p>{text}</p><span class="mm-pill">Planned</span></article>'
        for title, text, sketch in FEATURES
    )
    show_html(f"""
    <section class="mm-section">
      <h2 class="mm-h2">What MediMind AI will help you do</h2>
      <p class="mm-sub">These features are planned and in development. None of them work with real reports yet.</p>
      <div class="mm-features">{cards}</div>
    </section>
    """)


def trust_section():
    items = "".join(
        f'<div class="mm-principle"><h3>{title}</h3><p>{text}</p></div>'
        for title, text in PRINCIPLES
    )
    show_html(f"""
    <section class="mm-section">
      <h2 class="mm-h2">Why you can trust MediMind AI</h2>
      <p class="mm-sub">Three rules every feature is built around.</p>
      <div class="mm-principles">{items}</div>
    </section>
    """)


def disclaimer_and_footer():
    show_html(f"""
    <aside class="mm-disclaimer" role="note">
      {INFO_ICON}
      <div>
        <strong>Medical disclaimer</strong>
        <p>{DISCLAIMER} Always talk to a qualified healthcare professional about your results.
        In an emergency, contact your local emergency number right away.</p>
      </div>
    </aside>
    <footer class="mm-footer">
      <span>MediMind AI, an educational portfolio project</span>
      <span>Built with Python and Streamlit</span>
    </footer>
    """)


# ---------------------------------------------------------------
# 5. The page
# ---------------------------------------------------------------
st.html(CSS)
nav()

with st.container(key="hero"):
    left, right = st.columns([1.1, 1], gap="large", vertical_alignment="center")
    with left:
        hero_text()
        if st.button("Start analyzing a report", type="primary", key="cta"):
            st.toast("Report upload isn't available yet. It's the next feature being built.",
                     icon=":material/construction:")
        show_html('<p class="mm-note">No account needed. For education only, not a diagnosis.</p>')
    with right:
        hero_example()

upload_section()
features_section()
trust_section()
disclaimer_and_footer()