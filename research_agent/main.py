import streamlit as st
import os
from dotenv import load_dotenv
from tavily import TavilyClient
from groq import Groq
import datetime

# --- CORE CONFIG ---
load_dotenv()
st.set_page_config(page_title="SYNTH.AI // INTELLIGENCE", page_icon="⚡", layout="wide")

# --- UI DESIGN (UPGRADED) ---
st.markdown("""
<style>

@import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@300;500;700&family=Inter:wght@400;600;700&display=swap');

.stApp {
    background: #020617;
    color: #e2e8f0;
    font-family: 'Inter', sans-serif;
}

/* TITLE */
.main-title {
    font-family: 'Space Grotesk', sans-serif;
    font-weight: 700;
    background: linear-gradient(135deg, #22d3ee, #2563eb);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    font-size: 3.6rem !important;
}

/* INPUT */
.stTextInput input {
    background: #0f172a !important;
    border: 1px solid #1e293b !important;
    border-radius: 14px !important;
    padding: 14px 20px !important;
    color: #e2e8f0 !important;
    transition: 0.3s;
}

.stTextInput input:focus {
    border-color: #22d3ee !important;
    box-shadow: 0 0 15px rgba(34, 211, 238, 0.3) !important;
}

/* BUTTON */
.stButton>button {
    background: linear-gradient(135deg, #22d3ee, #2563eb) !important;
    color: #020617 !important;
    font-weight: 700 !important;
    border-radius: 14px !important;
    padding: 18px !important;
    border: none !important;
    transition: 0.3s;
}

.stButton>button:hover {
    box-shadow: 0 10px 30px rgba(34, 211, 238, 0.4);
    transform: translateY(-2px);
}

/* CARD */
.res-card {
    background: #0f172a;
    border-radius: 20px;
    padding: 35px;
    border: 1px solid #1e293b;
}

/* SOURCE */
.source-card {
    background: #020617;
    padding: 15px;
    border-radius: 12px;
    border: 1px solid #1e293b;
    transition: 0.3s;
}

.source-card:hover {
    border-color: #22d3ee;
    transform: translateX(5px);
}

/* TEXT */
.muted {
    color: #64748b;
}

/* LOADER */
.loader {
    text-align: center;
    color: #22d3ee;
    animation: pulse 1.5s infinite;
}

/* ANIMATION */
@keyframes pulse {
    0% {opacity: 0.4;}
    50% {opacity: 1;}
    100% {opacity: 0.4;}
}

#MainMenu, footer {visibility: hidden;}

</style>
""", unsafe_allow_html=True)

# --- ENGINE ---
tavily = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))
ai_client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def run_synthesis(query, depth, count):
    search_data = tavily.search(query=query, search_depth=depth, max_results=count)

    context = "\n".join([
        f"SOURCE {i+1}: {r['content']}\nURL: {r['url']}"
        for i, r in enumerate(search_data['results'])
    ])

    prompt = f"""
    Act as a Lead Intelligence Analyst.

    TOPIC: {query}
    DATA: {context}

    OUTPUT:
    ## EXECUTIVE SUMMARY
    ## KEY INSIGHTS
    ## FUTURE OUTLOOK

    Keep it sharp, structured, and professional.
    """

    response = ai_client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.2
    )

    return response.choices[0].message.content, search_data['results']

# --- HEADER ---
st.markdown('<h1 class="main-title">SYNTH.AI // INTELLIGENCE</h1>', unsafe_allow_html=True)
st.markdown("<p style='color:#94a3b8;'>Strategic Intelligence Engine</p>", unsafe_allow_html=True)

# --- SIDEBAR ---
with st.sidebar:
    st.markdown("### SYSTEM CORE")
    depth = st.radio("Search Depth", ["basic", "advanced"], index=1)
    count = st.slider("Source Nodes", 3, 15, 6)

    st.divider()
    st.markdown("Status: OPERATIONAL")
    st.markdown("Model: LLaMA-3.3-70B")
    st.markdown("Date: " + datetime.datetime.now().strftime("%Y-%m-%d"))

# --- INPUT ---
query = st.text_input("", placeholder="Ask something complex...")

# --- ACTION ---
if st.button("⚡ Run Intelligence"):

    if query:

        # LOADING EXPERIENCE
        with st.spinner(""):
            st.markdown('<div class="loader">Synthesizing intelligence...</div>', unsafe_allow_html=True)
            report, sources = run_synthesis(query, depth, count)

        col1, col2 = st.columns([2, 1])

        # REPORT
        with col1:
            st.markdown(f'<div class="res-card">{report}</div>', unsafe_allow_html=True)

        # SOURCES
        with col2:
            st.markdown("### Sources")
            for s in sources:
                st.markdown(f"""
                <div class="source-card">
                    <a href="{s['url']}" target="_blank" style="color:#4facfe;">
                        {s['url'][:40]}...
                    </a>
                    <p style="font-size:0.8rem; color:#94a3b8;">
                        {s['content'][:120]}...
                    </p>
                </div>
                """, unsafe_allow_html=True)

    else:
        st.warning("Enter a query first.")