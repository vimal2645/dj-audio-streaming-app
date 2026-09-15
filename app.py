import streamlit as st
import soundfile as sf
import io
import threading

from bgm_core.jobs import run_remix_job

render_lock = threading.Lock()


def render_remix(audio_file, track_2_file, **options):
    audio_bytes = audio_file.getvalue()
    track_2_bytes = track_2_file.getvalue() if track_2_file is not None else None
    with render_lock:
        return run_remix_job(audio_bytes, track_2_bytes, options)


# ================== PAGE CONFIG ==================
st.set_page_config(page_title="DJ Audio Studio", page_icon="🎧", layout="centered")

custom_css = """
<style>
    /* Hide the main hamburger menu (3 dots) */
    #MainMenu {visibility: hidden;}
    
    /* Hide the top right 'Deploy' & 'Manage App' header */
    header {visibility: hidden !important;}
    
    /* Hide the bottom 'Made with Streamlit' or 'Hosted with Streamlit' viewer badge */
    footer {visibility: hidden !important;}
    .st-emotion-cache-18ni7ap {visibility: hidden !important;} /* Badge target */
    div[data-testid="stToolbar"] {visibility: hidden !important;}
    
    /* Remove top padding so the app sits flush */
    .block-container {padding-top: 1rem !important;}
    
    /* Button styling */
    button[data-baseweb="tab"] {
        font-size: 1.1rem !important;
        font-weight: 600 !important;
    }
    button[kind="primary"] {
        border-radius: 8px !important;
        transition: all 0.3s ease !important;
        box-shadow: 0 0 10px rgba(0, 255, 255, 0.3) !important;
    }
    button[kind="primary"]:hover {
        box-shadow: 0 0 20px rgba(0, 255, 255, 0.7) !important;
        transform: translateY(-2px);
    }
</style>
"""
st.markdown(custom_css, unsafe_allow_html=True)


# ================== CUSTOM CSS (COOL + CLEAR) ==================
CUSTOM_CSS = """
<style>
:root {
    --bg-dark: #020617;
    --bg-mid: #02081f;
    --accent-blue: #38bdf8;
    --accent-purple: #a855f7;
    --accent-green: #22c55e;
    --text-main: #e5e7eb;
    --text-muted: #9ca3af;
}

/* Background: smooth dark gradient with subtle noise-like feel */
[data-testid="stAppViewContainer"] {
    background: radial-gradient(circle at 0% 0%, #020617 0%, #02081f 40%, #020617 100%);
    color: var(--text-main);
}

/* Sidebar */
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #020617, #020617);
    border-right: 1px solid #1f2937;
    color: var(--text-main);
}

/* Hide default Streamlit header/footer */
header[data-testid="stHeader"] {background: transparent;}
footer {visibility: hidden;}

/* Main card (glassmorphism, but dark and readable) */
.main-card {
    position: relative;
    background: linear-gradient(135deg, rgba(15,23,42,0.92), rgba(15,23,42,0.96));
    border-radius: 22px;
    padding: 1.7rem 2.1rem;
    border: 1px solid rgba(148, 163, 184, 0.3);
    box-shadow:
        0 24px 55px rgba(15, 23, 42, 0.9),
        0 0 0 1px rgba(15, 23, 42, 0.9);
    backdrop-filter: blur(16px);
    -webkit-backdrop-filter: blur(16px);
    animation: cardFadeIn 0.4s ease-out;
}

/* Decorative glow behind card */
.main-card::before {
    content: "";
    position: absolute;
    inset: -1px;
    border-radius: inherit;
    background: radial-gradient(circle at top left, rgba(56,189,248,0.35), transparent 55%),
                radial-gradient(circle at bottom right, rgba(168,85,247,0.28), transparent 60%);
    opacity: 0.7;
    z-index: -1;
}

/* Title */
.app-title {
    font-size: 2.2rem;
    font-weight: 800;
    letter-spacing: 0.08em;
    text-transform: uppercase;
    color: var(--text-main);
}
.app-subtitle {
    font-size: 0.96rem;
    color: var(--text-muted);
}

/* Section title */
.section-title {
    font-size: 1.0rem;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.16em;
    color: var(--text-muted);
    margin-top: 0.4rem;
    margin-bottom: 0.35rem;
}

/* Labels and general text: high contrast */
label, .stText, .stMarkdown, .stNumberInput label, .stSlider label {
    color: var(--text-main) !important;
}

/* Buttons */
div.stButton > button:first-child {
    background: linear-gradient(135deg, var(--accent-blue), var(--accent-purple));
    color: #020617;
    border-radius: 999px;
    padding: 0.55rem 1.7rem;
    font-weight: 700;
    border: none;
    box-shadow: 0 16px 36px rgba(56, 189, 248, 0.45);
    transition: all 0.16s ease-out;
}
div.stButton > button:first-child:hover {
    transform: translateY(-1px) scale(1.01);
    box-shadow: 0 20px 44px rgba(129, 140, 248, 0.7);
}

/* Sliders accent */
.stSlider > div > div > div {
    background: linear-gradient(90deg, var(--accent-blue), var(--accent-green)) !important;
}

/* Checkboxes text */
.stCheckbox > label {
    color: var(--text-main) !important;
}

/* Audio player tweaks (WebKit) */
audio::-webkit-media-controls-panel,
audio::-webkit-media-controls-enclosure {
    background-color: #020617;
}
audio::-webkit-media-controls-current-time-display,
audio::-webkit-media-controls-time-remaining-display {
    color: #e5e7eb;
}
audio::-webkit-media-controls-timeline {
    background-color: #111827;
    border-radius: 999px;
    margin-left: 10px;
    margin-right: 10px;
}
audio {
    width: 100%;
}

/* Small glowing pill */
.tag-pill {
    display: inline-flex;
    align-items: center;
    gap: 0.4rem;
    padding: 0.22rem 0.7rem;
    border-radius: 999px;
    background: rgba(15, 23, 42, 0.95);
    border: 1px solid rgba(56, 189, 248, 0.65);
    color: #bae6fd;
    font-size: 0.72rem;
    text-transform: uppercase;
    letter-spacing: 0.14em;
}

/* Testing Phase Pill & Pulse */
.testing-pill {
    background: rgba(245, 158, 11, 0.15) !important;
    border: 1px solid rgba(245, 158, 11, 0.7) !important;
    color: #fbbf24 !important;
    font-weight: 700 !important;
}
.pulse-dot {
    width: 7px;
    height: 7px;
    border-radius: 50%;
    background: #fbbf24;
    box-shadow: 0 0 8px #fbbf24;
    animation: pulseAnim 1.6s infinite ease-in-out;
    display: inline-block;
}
@keyframes pulseAnim {
    0%, 100% { opacity: 1; transform: scale(1); }
    50% { opacity: 0.35; transform: scale(0.8); }
}

/* Status Banner */
.status-banner {
    margin-top: 0.8rem;
    padding: 0.6rem 0.95rem;
    border-radius: 12px;
    background: rgba(245, 158, 11, 0.08);
    border: 1px dashed rgba(245, 158, 11, 0.45);
    color: #fef3c7;
    font-size: 0.83rem;
    display: flex;
    align-items: center;
    gap: 0.65rem;
}

/* Footer Styling (by VPIXCEL) */
.custom-footer {
    margin-top: 3rem;
    margin-bottom: 1.5rem;
    padding: 1.25rem 1.6rem;
    border-radius: 20px;
    background: linear-gradient(135deg, rgba(15, 23, 42, 0.92), rgba(30, 41, 59, 0.75));
    border: 1px solid rgba(148, 163, 184, 0.25);
    box-shadow: 0 16px 36px rgba(2, 6, 23, 0.7);
    backdrop-filter: blur(14px);
    -webkit-backdrop-filter: blur(14px);
}
.footer-content {
    display: flex;
    justify-content: space-between;
    align-items: center;
    flex-wrap: wrap;
    gap: 1.2rem;
}
.footer-left {
    display: flex;
    align-items: center;
    gap: 0.7rem;
    flex-wrap: wrap;
}
.footer-brand {
    font-weight: 800;
    color: #f8fafc;
    font-size: 1.05rem;
    letter-spacing: 0.04em;
}
.footer-by {
    color: #94a3b8;
    font-size: 0.9rem;
}
.footer-by strong {
    color: #38bdf8;
    font-weight: 700;
    letter-spacing: 0.03em;
}
.footer-tag {
    font-size: 0.72rem;
    padding: 0.2rem 0.6rem;
    border-radius: 999px;
    background: rgba(245, 158, 11, 0.15);
    border: 1px solid rgba(245, 158, 11, 0.5);
    color: #fbbf24;
    font-weight: 700;
}
.footer-links {
    display: flex;
    align-items: center;
    gap: 0.8rem;
    flex-wrap: wrap;
}
.footer-link {
    display: inline-flex;
    align-items: center;
    gap: 0.5rem;
    padding: 0.4rem 0.9rem;
    border-radius: 999px;
    font-size: 0.84rem;
    font-weight: 600;
    text-decoration: none !important;
    transition: all 0.2s ease-in-out;
}
.insta-link {
    background: linear-gradient(135deg, rgba(225, 48, 108, 0.15), rgba(253, 29, 29, 0.15));
    border: 1px solid rgba(225, 48, 108, 0.45);
    color: #f472b6 !important;
}
.insta-link:hover {
    background: linear-gradient(135deg, rgba(225, 48, 108, 0.35), rgba(253, 29, 29, 0.35));
    border-color: rgba(225, 48, 108, 0.9);
    box-shadow: 0 0 16px rgba(225, 48, 108, 0.45);
    transform: translateY(-2px);
    color: #ffffff !important;
}
.mail-link {
    background: rgba(56, 189, 248, 0.12);
    border: 1px solid rgba(56, 189, 248, 0.4);
    color: #38bdf8 !important;
}
.mail-link:hover {
    background: rgba(56, 189, 248, 0.28);
    border-color: rgba(56, 189, 248, 0.85);
    box-shadow: 0 0 16px rgba(56, 189, 248, 0.45);
    transform: translateY(-2px);
    color: #ffffff !important;
}

/* Fade-in animation */
@keyframes cardFadeIn {
    from { opacity: 0; transform: translateY(6px);}
    to   { opacity: 1; transform: translateY(0);}
}
</style>
"""
st.markdown(CUSTOM_CSS, unsafe_allow_html=True)


# ================== HEADER ==================
st.markdown(
    """
<div class="main-card">
  <div class="app-title">WHZ LoopRoom</div>
  <div class="app-subtitle">
    Three‑section remix tool to turn any track into smooth background music with fine control.
  </div>
  <div style="margin-top:0.75rem; display:flex; gap:0.5rem; flex-wrap:wrap; align-items:center;">
    <span class="tag-pill">🎧 Remix existing song</span>
    <span class="tag-pill testing-pill"><span class="pulse-dot"></span> In Testing Phase</span>
  </div>
  <div class="status-banner">
    <span>🧪</span>
    <span><strong>Testing Phase Active:</strong> Cloud-optimized with <strong>30-Sec Reel Cutter</strong> for fast rendering and stability on Render Free Tier.</span>
  </div>
</div>
""",
    unsafe_allow_html=True,
)
st.write("")


# ================== SESSION STATE INIT ==================
default_states = {
    "speed": 1.0,
    "pitch": 0,
    "wow_flutter": 0.0,
    "transition_style": "Smooth Crossfade",
    "crossfade_sec": 3.5,
    "fade": True,
    "reverse_flag": False,
    "use_fast_reverb": False,
    "enable_sections": True,
    "crackle": 0.0,
    "sub_woofer": 0.0,
    "bitcrush_amount": 0.0,
    "audio_8d_amount": 0.0,
    "t1": 10.0,
    "t2": 20.0,
    "bass1": 20, "high1": 20, "reverb1": 20, "lofi1": 0,
    "bass2": 60, "high2": 40, "reverb2": 30, "lofi2": 10,
    "bass3": 35, "high3": 20, "reverb3": 40, "lofi3": 40,
    "track_2_volume": 0.5,
    "track_2_start_delay": 0,
    "track_2_mode": "Overlay (Mashup)",
    "track_2_in_point": 0.0,
    "return_to_track_1": False,
    "track_2_out_point": 60.0,
    "track_1_resume_point": 120.0,
    "reel_start": 0.0,
    "preview_start": 0.0
}
for key, val in default_states.items():
    if key not in st.session_state:
        st.session_state[key] = val

def set_preset_lofi():
    st.session_state.enable_sections = False
    st.session_state.crackle = 0.6
    st.session_state.wow_flutter = 0.7
    st.session_state.bitcrush_amount = 0.2
    st.session_state.sub_woofer = 0.4
    st.toast("Lofi Vibe applied! Check the FX tab.", icon="✨")

def set_preset_dj_switch():
    st.session_state.track_2_mode = "Switch (DJ Cut to Track 2)"
    st.session_state.track_2_start_delay = 30
    st.session_state.return_to_track_1 = True
    st.toast("Auto DJ Mix applied! Check the Mashup tab.", icon="🎧")

# ================== REMIX EXISTING ==================
st.markdown('<div class="main-card">', unsafe_allow_html=True)
st.markdown(
    '<div class="section-title">Remix controls</div>',
    unsafe_allow_html=True,
)

tab1, tab2, tab3 = st.tabs(["✨ Presets", "🎵 Main Track & FX", "🎧 DJ Mashup"])

with tab1:
    with st.expander("📖 How to Use This App", expanded=False):
        st.markdown("""
1. **Upload**: Go to the 🎵 Main Track tab and upload your base song.
2. **Vibe Check**: Click a ✨ Magic Preset below, or manually tweak the Tape, Vinyl, and 8D sliders.
3. **Mashup (Optional)**: Go to 🎧 DJ Mashup to layer a second song, sync the BPM, and trigger a beat drop.
4. **30s Reel Export**: Set your start point and hit **✂️ Generate 30-Sec Reel** to render an Instagram / TikTok ready 30s cut with all effects applied!
        """)

    st.markdown("### Magic Presets")
    st.info("💡 **Tip:** Magic presets instantly configure the sliders hidden in the other tabs. You'll still need to upload a song in **Tab 2** to hear the results!")
    col_p1, col_p2 = st.columns(2)
    with col_p1:
        st.button("Instant Lofi Vibe", on_click=set_preset_lofi, use_container_width=True)
        st.markdown("*Turns off 3-Tier mode, adds heavy vinyl crackle, tape wobble, slight bitcrush, and sub-woofer bass.*")
    with col_p2:
        st.button("Auto DJ Mix", on_click=set_preset_dj_switch, use_container_width=True)
        st.markdown("*Sets Track 2 to Switch mode, cuts Main Track at 30s, and enables Return to Main Track.*")

with tab2:
    audio_file = st.file_uploader("Upload a song (mp3/wav)", type=["mp3", "wav"])
    
    st.markdown("### Global Options")
    col_g1, col_g2 = st.columns(2)
    with col_g1:
        speed = st.slider("Speed (0.3 = very slow, 2.0 = fast)", 0.3, 2.0, key="speed", step=0.05)
        pitch = st.slider("Pitch shift (semitones)", -12, 12, key="pitch", step=1)
        transition_style = st.selectbox("Transition Style", ["Smooth Crossfade", "Hard Beat Drop"], key="transition_style")
        crossfade_sec = st.slider("Transition Crossfade (seconds)", 0.1, 6.0, key="crossfade_sec", step=0.1)
    with col_g2:
        fade = st.checkbox("Fade in / fade out", key="fade")
        reverse_flag = st.checkbox("Reverse whole track", key="reverse_flag")
        use_fast_reverb = st.checkbox("Use Fast Reverb (Recommended for long tracks)", key="use_fast_reverb")

    with st.expander("Retro Effects (Vinyl, Tape, 8D)"):
        wow_flutter = st.slider("Tape Wobble (Wow & Flutter)", 0.0, 1.0, key="wow_flutter", step=0.05)
        crackle = st.slider("Vinyl Crackle Level", 0.0, 1.0, key="crackle", step=0.05)
        sub_woofer = st.slider("Sub-Woofer Bass", 0.0, 1.0, key="sub_woofer")
        bitcrush_amount = st.slider("Bitcrusher (Retro Crunch)", 0.0, 1.0, key="bitcrush_amount")
        audio_8d_amount = st.slider("8D Audio Panning", 0.0, 1.0, key="audio_8d_amount")

    with st.expander("3-Tier Engine (Intro/Drop/Outro)"):
        enable_sections = st.checkbox("Enable 3-Section Remixing", key="enable_sections")
        
        st.markdown("**Section Times (seconds)**")
        t1 = st.number_input("End of Section 1 (t1)", min_value=0.0, key="t1", step=1.0)
        t2 = st.number_input("End of Section 2 (t2)", min_value=0.0, key="t2", step=1.0)

        st.markdown("**Section 1 (Intro)**")
        c1_1, c1_2, c1_3, c1_4 = st.columns(4)
        with c1_1: bass1 = st.slider("Bass 1", 0, 100, key="bass1") / 100.0
        with c1_2: high1 = st.slider("Highs 1", 0, 100, key="high1") / 100.0
        with c1_3: reverb1 = st.slider("Reverb 1", 0, 100, key="reverb1") / 100.0
        with c1_4: lofi1 = st.slider("Lo-fi 1", 0, 100, key="lofi1") / 100.0

        st.markdown("**Section 2 (Drop)**")
        c2_1, c2_2, c2_3, c2_4 = st.columns(4)
        with c2_1: bass2 = st.slider("Bass 2", 0, 100, key="bass2") / 100.0
        with c2_2: high2 = st.slider("Highs 2", 0, 100, key="high2") / 100.0
        with c2_3: reverb2 = st.slider("Reverb 2", 0, 100, key="reverb2") / 100.0
        with c2_4: lofi2 = st.slider("Lo-fi 2", 0, 100, key="lofi2") / 100.0

        st.markdown("**Section 3 (Outro)**")
        c3_1, c3_2, c3_3, c3_4 = st.columns(4)
        with c3_1: bass3 = st.slider("Bass 3", 0, 100, key="bass3") / 100.0
        with c3_2: high3 = st.slider("Highs 3", 0, 100, key="high3") / 100.0
        with c3_3: reverb3 = st.slider("Reverb 3", 0, 100, key="reverb3") / 100.0
        with c3_4: lofi3 = st.slider("Lo-fi 3", 0, 100, key="lofi3") / 100.0

with tab3:
    st.markdown("### Mashup / Layer Track 2")
    track_2_file = st.file_uploader("Upload Track 2 (mp3/wav) for mashup", type=["mp3", "wav"], key="track_2")
    
    col_m1, col_m2 = st.columns(2)
    with col_m1:
        track_2_volume = st.slider("Track 2 Volume", 0.0, 1.0, key="track_2_volume")
    with col_m2:
        track_2_start_delay = st.slider("Track 2 Start Delay (Seconds)", 0, 60, key="track_2_start_delay")
        
    track_2_mode = st.radio("Track 2 Mode", ["Overlay (Mashup)", "Switch (DJ Cut to Track 2)"], key="track_2_mode")
    track_2_in_point = st.slider("Track 2 In-Point (Skip first X seconds)", 0.0, 180.0, key="track_2_in_point")

    return_to_track_1 = st.checkbox("Return to Main Track (A -> B -> A)", key="return_to_track_1")
    
    # Extract conditionally shown variables
    if return_to_track_1:
        track_2_out_point = st.slider("Track 2 Out-Point (Cut Track 2 at X seconds)", 0.0, 300.0, key="track_2_out_point")
        track_1_resume_point = st.slider("Track 1 Resume Timestamp (Start Track 1 again at X seconds)", 0.0, 300.0, key="track_1_resume_point")
    else:
        track_2_out_point = None
        track_1_resume_point = st.session_state.get("track_1_resume_point", 120.0)

st.markdown("</div>", unsafe_allow_html=True)
st.write("")

export_container = st.container()
with export_container:
    st.markdown("### 🎬 30-Sec Reel Cutter & Export")
    st.caption("⚡ **Cloud-Optimized (Free Tier):** Generates a high-quality 30-second reel clip for Instagram, TikTok, and Shorts without cloud memory limit crashes.")

    col_exp1, col_exp2 = st.columns([3, 1])
    with col_exp1:
        reel_start = st.number_input(
            "Reel Start Time (seconds)",
            min_value=0.0,
            value=float(st.session_state.get("reel_start", 0.0)),
            key="reel_start_input",
            step=1.0,
            help="Choose the start timestamp for your 30-second reel cut",
        )
        st.session_state["reel_start"] = reel_start
        st.session_state["preview_start"] = reel_start
    with col_exp2:
        st.metric(label="Reel Duration", value="30.0 s", delta="Cloud Safe")

    col_btn1, col_btn2 = st.columns(2)
    with col_btn1:
        preview_click = st.button("▶ Quick 15s Preview", use_container_width=True)
    with col_btn2:
        reel_click = st.button("✂️ Generate 30-Sec Reel", use_container_width=True, type="primary")


# ================== PREVIEW LOGIC ==================
if audio_file is not None and preview_click:
    with st.spinner("Rendering 15s preview..."):
        y_prev, sr_prev = render_remix(
            audio_file,
            track_2_file,
            speed=speed,
            pitch_steps=pitch,
            fade_flag=fade,
            reverse_flag=reverse_flag,
            t1=t1,
            t2=t2,
            bass1=bass1,
            high1=high1,
            reverb1=reverb1,
            lofi1=lofi1,
            bass2=bass2,
            high2=high2,
            reverb2=reverb2,
            lofi2=lofi2,
            bass3=bass3,
            high3=high3,
            reverb3=reverb3,
            lofi3=lofi3,
            start_time=st.session_state["reel_start"],
            duration=15.0,
            wow_flutter_amount=wow_flutter,
            crackle_amount=crackle,
            use_fast_reverb=use_fast_reverb,
            enable_sections=enable_sections,
            transition_style=transition_style,
            sub_woofer_amount=sub_woofer,
            bitcrush_amount=bitcrush_amount,
            audio_8d_amount=audio_8d_amount,
            track_2_volume=track_2_volume,
            track_2_start_delay=track_2_start_delay,
            track_2_mode=track_2_mode,
            track_2_in_point=track_2_in_point,
            crossfade_sec=crossfade_sec,
            return_to_track_1=return_to_track_1,
            track_2_out_point=track_2_out_point,
            track_1_resume_point=track_1_resume_point,
        )

    buf_prev = io.BytesIO()
    sf.write(buf_prev, y_prev, sr_prev, format="wav")
    buf_prev.seek(0)
    # Persist in session_state so it survives reruns
    st.session_state["preview_buf"] = buf_prev.getvalue()

# Always render preview player if a buffer exists
if "preview_buf" in st.session_state:
    with export_container:
        st.markdown("**▶ 15s Preview Player**")
        st.audio(st.session_state["preview_buf"], format="audio/wav")


# ================== 30-SEC REEL REMIX LOGIC ==================
if audio_file is not None and reel_click:
    with st.spinner("Processing 30-second reel remix..."):
        y_reel, sr_reel = render_remix(
            audio_file,
            track_2_file,
            speed=speed,
            pitch_steps=pitch,
            fade_flag=fade,
            reverse_flag=reverse_flag,
            t1=t1,
            t2=t2,
            bass1=bass1,
            high1=high1,
            reverb1=reverb1,
            lofi1=lofi1,
            bass2=bass2,
            high2=high2,
            reverb2=reverb2,
            lofi2=lofi2,
            bass3=bass3,
            high3=high3,
            reverb3=reverb3,
            lofi3=lofi3,
            start_time=st.session_state["reel_start"],
            duration=30.0,
            wow_flutter_amount=wow_flutter,
            crackle_amount=crackle,
            use_fast_reverb=use_fast_reverb,
            enable_sections=enable_sections,
            transition_style=transition_style,
            sub_woofer_amount=sub_woofer,
            bitcrush_amount=bitcrush_amount,
            audio_8d_amount=audio_8d_amount,
            track_2_volume=track_2_volume,
            track_2_start_delay=track_2_start_delay,
            track_2_mode=track_2_mode,
            track_2_in_point=track_2_in_point,
            crossfade_sec=crossfade_sec,
            return_to_track_1=return_to_track_1,
            track_2_out_point=track_2_out_point,
            track_1_resume_point=track_1_resume_point,
        )

    buf_reel = io.BytesIO()
    sf.write(buf_reel, y_reel, sr_reel, format="wav")
    buf_reel.seek(0)
    # Persist in session_state so it survives reruns
    st.session_state["reel_buf"] = buf_reel.getvalue()

# Always render 30s reel player + download if a buffer exists
if "reel_buf" in st.session_state:
    with export_container:
        st.success("✅ 30-Second Reel Remix Ready!")
        st.audio(st.session_state["reel_buf"], format="audio/wav")
        st.download_button(
            "📥 Download 30-Sec Reel (WAV)",
            st.session_state["reel_buf"],
            file_name="remix_30s_reel.wav",
            mime="audio/wav",
        )


# ================== FOOTER (by VPIXCEL) ==================
footer_html = """
<div class="custom-footer">
  <div class="footer-content">
    <div class="footer-left">
      <span class="footer-brand">🎧 WHZ LoopRoom</span>
      <span class="footer-by">by <strong>VPIXCEL</strong></span>
      <span class="footer-tag">🧪 In Testing Phase</span>
    </div>
    <div class="footer-links">
      <a href="https://instagram.com/VPIXCEL" target="_blank" rel="noopener noreferrer" class="footer-link insta-link">
        <svg class="footer-icon" viewBox="0 0 24 24" width="16" height="16" stroke="currentColor" stroke-width="2" fill="none" stroke-linecap="round" stroke-linejoin="round">
          <rect x="2" y="2" width="20" height="20" rx="5" ry="5"></rect>
          <path d="M16 11.37A4 4 0 1 1 12.63 8 4 4 0 0 1 16 11.37z"></path>
          <line x1="17.5" y1="6.5" x2="17.51" y2="6.5"></line>
        </svg>
        <span>@VPIXCEL</span>
      </a>
      <a href="mailto:vpixel.builds@gmail.com" class="footer-link mail-link">
        <svg class="footer-icon" viewBox="0 0 24 24" width="16" height="16" stroke="currentColor" stroke-width="2" fill="none" stroke-linecap="round" stroke-linejoin="round">
          <path d="M4 4h16c1.1 0 2 .9 2 2v12c0 1.1-.9 2-2 2H4c-1.1 0-2-.9-2-2V6c0-1.1.9-2 2-2z"></path>
          <polyline points="22,6 12,13 2,6"></polyline>
        </svg>
        <span>vpixel.builds@gmail.com</span>
      </a>
    </div>
  </div>
</div>
"""
st.markdown(footer_html, unsafe_allow_html=True)
