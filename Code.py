# pip install streamlit requests fpdf pandas
import streamlit as st
import requests, json, os, re, time
import hashlib
from datetime import datetime, timedelta
from io import BytesIO
from fpdf import FPDF
import unicodedata
import pandas as pd

# Configure the page settings
st.set_page_config(
    page_title="Business Problem Level Classifier",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Improved CSS with enhanced styles for a creative UI
# Enhanced Creative CSS with Advanced Animations and Effects
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700;800&family=Inter:wght@300;400;500;600;700&display=swap');
    
    /* Main Background with Animated Gradient */
    .main {
        font-family: 'Poppins', sans-serif;
        background: linear-gradient(-45deg, #ee7752, #e73c7e, #23a6d5, #23d5ab);
        background-size: 400% 400%;
        animation: gradient 15s ease infinite;
        background-attachment: fixed;
        min-height: 100vh;
    }
    
    @keyframes gradient {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }
    
    .stApp {
        background: transparent;
    }
    
    /* Page Title with Glass Morphism */
    .page-title {
        background: linear-gradient(135deg, rgba(102, 126, 234, 0.8), rgba(118, 75, 162, 0.8));
        backdrop-filter: blur(10px);
        -webkit-backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.2);
        padding: 2.5rem;
        border-radius: 25px;
        color: white;
        text-align: center;
        margin-bottom: 2rem;
        box-shadow: 0 20px 40px rgba(0,0,0,0.3);
        position: relative;
        overflow: hidden;
    }
    
    .page-title::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background: linear-gradient(45deg, transparent, rgba(255,255,255,0.1), transparent);
        transform: translateX(-100%);
        animation: shimmer 3s infinite;
    }
    
    @keyframes shimmer {
        100% { transform: translateX(100%); }
    }
    
    .page-title h1 {
        font-size: 3rem;
        font-weight: 800;
        margin: 0;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
        background: linear-gradient(45deg, #fff, #f0f0f0, #fff);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-size: 200% 100%;
        animation: textShine 3s ease-in-out infinite;
    }
    
    @keyframes textShine {
        0%, 100% { background-position: -200% 0; }
        50% { background-position: 200% 0; }
    }
    
    /* Dimension Boxes with Gradient Animations */
    .dimension-box {
        background: linear-gradient(135deg, #667eea, #764ba2, #667eea);
        background-size: 200% 200%;
        animation: gradientShift 4s ease infinite;
        color: white;
        padding: 2rem;
        border-radius: 20px;
        text-align: center;
        cursor: pointer;
        transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
        box-shadow: 0 15px 35px rgba(102, 126, 234, 0.4);
        min-height: 140px;
        margin-bottom: 1.5rem;
        position: relative;
        overflow: hidden;
        border: 1px solid rgba(255,255,255,0.3);
    }
    
    @keyframes gradientShift {
        0%, 100% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
    }
    
    .dimension-box::before {
        content: '';
        position: absolute;
        top: 0;
        left: -100%;
        width: 100%;
        height: 100%;
        background: linear-gradient(90deg, transparent, rgba(255,255,255,0.2), transparent);
        transition: left 0.5s;
    }
    
    .dimension-box:hover::before {
        left: 100%;
    }
    
    .dimension-box:hover {
        transform: translateY(-10px) scale(1.05);
        box-shadow: 0 25px 50px rgba(102, 126, 234, 0.6);
    }
    
    .dimension-score {
        font-size: 3rem;
        font-weight: 900;
        margin: 0.5rem 0;
        text-shadow: 2px 2px 8px rgba(0,0,0,0.3);
        background: linear-gradient(45deg, #fff, #e0e0ff, #fff);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-size: 200% 100%;
        animation: textShine 3s ease-in-out infinite;
    }
    
    .dimension-label {
        font-size: 1.3rem;
        font-weight: 600;
        opacity: 0.95;
        text-transform: uppercase;
        letter-spacing: 1px;
        text-shadow: 1px 1px 3px rgba(0,0,0,0.3);
    }
    
    /* Hardness Badges with Pulse Animations */
    .hardness-badge-hard {
        background: linear-gradient(135deg, #ff6b6b, #ff5252, #ff0000);
        background-size: 200% 200%;
        animation: gradientPulse 2s ease infinite, pulse-hard 2s infinite;
        color: white;
        padding: 2rem;
        border-radius: 25px;
        font-size: 2rem;
        font-weight: 800;
        text-align: center;
        box-shadow: 0 20px 40px rgba(255, 107, 107, 0.5);
        min-height: 180px;
        display: flex;
        align-items: center;
        justify-content: center;
        position: relative;
        overflow: hidden;
        border: 2px solid rgba(255,255,255,0.3);
    }
    
    @keyframes gradientPulse {
        0%, 100% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
    }
    
    @keyframes pulse-hard {
        0%, 100% { transform: scale(1); box-shadow: 0 20px 40px rgba(255, 107, 107, 0.5); }
        50% { transform: scale(1.02); box-shadow: 0 25px 50px rgba(255, 107, 107, 0.7); }
    }
            
    .hardness-badge-moderate-to-hard {
        background: linear-gradient(135deg, #ff9800, #ffb74d, #ffa726);
        background-size: 200% 200%;
        animation: gradientPulse 3s ease infinite, pulse-moderate 3s infinite;
        color: white;
        padding: 2rem;
        border-radius: 25px;
        font-size: 2rem;
        font-weight: 800;
        text-align: center;
        box-shadow: 0 20px 40px rgba(255, 152, 0, 0.5);
        min-height: 180px;
        display: flex;
        align-items: center;
        justify-content: center;
        position: relative;
        overflow: hidden;
        border: 2px solid rgba(255,255,255,0.3);
    }
    
    @keyframes pulse-moderate {
        0%, 100% { transform: scale(1); }
        50% { transform: scale(1.01); }
    }
    
    .hardness-badge-moderate {
        background: linear-gradient(135deg, #ffa726, #ffb74d, #ffcc80);
        background-size: 200% 200%;
        animation: gradientPulse 4s ease infinite;
        color: white;
        padding: 2rem;
        border-radius: 25px;
        font-size: 2rem;
        font-weight: 800;
        text-align: center;
        box-shadow: 0 20px 40px rgba(255, 167, 38, 0.5);
        min-height: 180px;
        display: flex;
        align-items: center;
        justify-content: center;
        position: relative;
        overflow: hidden;
        border: 2px solid rgba(255,255,255,0.3);
    }
    
    .hardness-badge-easy {
        background: linear-gradient(135deg, #66bb6a, #4caf50, #81c784);
        background-size: 200% 200%;
        animation: gradientPulse 5s ease infinite, pulse-easy 4s infinite;
        color: white;
        padding: 2rem;
        border-radius: 25px;
        font-size: 2rem;
        font-weight: 800;
        text-align: center;
        box-shadow: 0 20px 40px rgba(102, 187, 106, 0.5);
        min-height: 180px;
        display: flex;
        align-items: center;
        justify-content: center;
        position: relative;
        overflow: hidden;
        border: 2px solid rgba(255,255,255,0.3);
    }
    
    @keyframes pulse-easy {
        0%, 100% { transform: scale(1); }
        50% { transform: scale(1.005); }
    }
    
    /* Score Badge with Shimmer Effect */
    .score-badge {
        background: linear-gradient(135deg, #667eea, #764ba2, #667eea);
        background-size: 200% 200%;
        animation: gradientShift 3s ease infinite;
        color: white;
        padding: 2rem;
        border-radius: 25px;
        text-align: center;
        box-shadow: 0 20px 40px rgba(102, 126, 234, 0.5);
        min-height: 180px;
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        position: relative;
        overflow: hidden;
        border: 1px solid rgba(255,255,255,0.3);
    }
    
    /* Buttons with Gradient Hover Effects */
    .stButton > button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        background-size: 200% 100%;
        color: white;
        border: none;
        border-radius: 15px;
        font-weight: 700;
        font-family: 'Poppins', sans-serif;
        padding: 1rem 2rem;
        transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
        box-shadow: 0 12px 25px rgba(102, 126, 234, 0.4);
        position: relative;
        overflow: hidden;
        font-size: 1.1rem;
        letter-spacing: 0.5px;
    }
    
    .stButton > button::before {
        content: '';
        position: absolute;
        top: 0;
        left: -100%;
        width: 100%;
        height: 100%;
        background: linear-gradient(90deg, transparent, rgba(255,255,255,0.3), transparent);
        transition: left 0.5s;
    }
    
    .stButton > button:hover::before {
        left: 100%;
    }
    
    .stButton > button:hover {
        background: linear-gradient(135deg, #764ba2 0%, #667eea 100%);
        transform: translateY(-5px) scale(1.05);
        box-shadow: 0 20px 40px rgba(102, 126, 234, 0.6);
    }
    
    /* Q&A Boxes with Gradient Borders */
    .qa-box {
        background: linear-gradient(135deg, rgba(255, 255, 255, 0.95), rgba(248, 250, 252, 0.95));
        padding: 2rem;
        border-radius: 20px;
        margin-bottom: 2rem;
        box-shadow: 0 15px 35px rgba(0,0,0,0.1);
        border-left: 6px solid;
        border-image: linear-gradient(135deg, #667eea, #764ba2) 1;
        transition: all 0.3s ease;
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255,255,255,0.2);
        position: relative;
        overflow: hidden;
    }
    
    .qa-box::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 4px;
        background: linear-gradient(90deg, #667eea, #764ba2);
    }
    
    .qa-box:hover {
        transform: translateX(10px);
        box-shadow: 0 20px 40px rgba(0,0,0,0.15);
    }
    
    .qa-question {
        font-weight: 700;
        color: #667eea;
        margin-bottom: 1rem;
        font-size: 1.2rem;
        display: flex;
        align-items: center;
        gap: 10px;
        background: linear-gradient(135deg, #667eea, #764ba2);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    
    .qa-question::before {
        content: '❓';
        font-size: 1.5rem;
        background: linear-gradient(135deg, #667eea, #764ba2);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    
    .qa-answer {
        color: #4a5568;
        line-height: 1.8;
        font-size: 1.05rem;
        padding-left: 1.5rem;
        border-left: 3px solid;
        border-image: linear-gradient(to bottom, #667eea, #764ba2) 1;
    }
    
    /* Section Titles with Gradient Underlines */
    .section-title {
        color: #667eea;
        font-size: 1.8rem;
        font-weight: 700;
        margin-top: 2rem;
        margin-bottom: 1.5rem;
        padding-bottom: 1rem;
        position: relative;
        display: inline-block;
        background: linear-gradient(135deg, #667eea, #764ba2);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    
    .section-title::after {
        content: '';
        position: absolute;
        bottom: 0;
        left: 0;
        width: 100%;
        height: 4px;
        background: linear-gradient(90deg, #667eea, #764ba2);
        border-radius: 2px;
    }
    
    /* Problem Display with Glass Morphism */
    .problem-display {
        background: linear-gradient(135deg, rgba(255, 255, 255, 0.95), rgba(248, 250, 252, 0.95));
        backdrop-filter: blur(10px);
        -webkit-backdrop-filter: blur(10px);
        padding: 2rem;
        border-radius: 20px;
        margin-bottom: 2.5rem;
        box-shadow: 0 15px 35px rgba(0,0,0,0.1);
        border-left: 6px solid;
        border-image: linear-gradient(135deg, #667eea, #764ba2) 1;
        position: relative;
        border: 1px solid rgba(255,255,255,0.2);
    }
    
    .problem-display::before {
        content: '💡';
        position: absolute;
        top: -15px;
        left: -15px;
        background: linear-gradient(135deg, #667eea, #764ba2);
        color: white;
        width: 50px;
        height: 50px;
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 1.5rem;
        box-shadow: 0 5px 15px rgba(102, 126, 234, 0.5);
        z-index: 2;
    }
    
    .problem-display h4 {
        color: #667eea;
        margin-bottom: 1rem;
        font-weight: 700;
        font-size: 1.4rem;
        background: linear-gradient(135deg, #667eea, #764ba2);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    
    /* Content Text with Subtle Gradient Background */
    .content-text {
        background: linear-gradient(135deg, rgba(255, 255, 255, 0.95), rgba(248, 250, 252, 0.95));
        backdrop-filter: blur(10px);
        -webkit-backdrop-filter: blur(10px);
        padding: 2rem;
        border-radius: 20px;
        line-height: 1.9;
        color: #4a5568;
        box-shadow: 0 10px 30px rgba(0,0,0,0.1);
        margin-bottom: 1.5rem;
        border: 1px solid rgba(255,255,255,0.2);
        position: relative;
        overflow: hidden;
    }
    
    .content-text::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        width: 4px;
        height: 100%;
        background: linear-gradient(to bottom, #667eea, #764ba2);
    }
    
    /* Select Box Styling */
    .stSelectbox > div > div {
        background: linear-gradient(135deg, rgba(255, 255, 255, 0.95), rgba(248, 250, 252, 0.95));
        backdrop-filter: blur(10px);
        border-radius: 12px;
        border: 2px solid #e2e8f0;
        transition: all 0.3s ease;
        box-shadow: 0 5px 15px rgba(0,0,0,0.1);
    }
    
    .stSelectbox > div > div:hover {
        border-color: #667eea;
        box-shadow: 0 8px 25px rgba(102, 126, 234, 0.3);
        transform: translateY(-2px);
    }
    
    /* Text Area Styling */
    .stTextArea > div > div > textarea {
        border-radius: 15px;
        border: 2px solid #e2e8f0;
        background: linear-gradient(135deg, rgba(255, 255, 255, 0.95), rgba(248, 250, 252, 0.95));
        backdrop-filter: blur(10px);
        transition: all 0.3s ease;
        font-family: 'Inter', sans-serif;
        box-shadow: 0 5px 15px rgba(0,0,0,0.1);
    }
    
    .stTextArea > div > div > textarea:focus {
        border-color: #667eea;
        box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.2), 0 8px 25px rgba(102, 126, 234, 0.3);
        transform: translateY(-2px);
    }
    
    /* Expander Styling */
    .streamlit-expanderHeader {
        background: linear-gradient(135deg, #667eea, #764ba2);
        color: white;
        border-radius: 12px;
        font-weight: 600;
        border: none;
        box-shadow: 0 5px 15px rgba(102, 126, 234, 0.4);
        transition: all 0.3s ease;
    }
    
    .streamlit-expanderHeader:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 25px rgba(102, 126, 234, 0.6);
    }
    
    /* Success Message Styling */
    .stSuccess {
        background: linear-gradient(135deg, #48bb78, #38a169);
        color: white;
        border-radius: 15px;
        border: none;
        box-shadow: 0 10px 25px rgba(72, 187, 120, 0.4);
    }
    
    /* Progress Bar Styling */
    .stProgress > div > div {
        background: linear-gradient(90deg, #667eea, #764ba2, #f093fb);
        border-radius: 10px;
        box-shadow: 0 3px 10px rgba(102, 126, 234, 0.3);
    }
    
    /* Custom Scrollbar */
    ::-webkit-scrollbar {
        width: 8px;
    }
    
    ::-webkit-scrollbar-track {
        background: rgba(255,255,255,0.1);
        border-radius: 10px;
    }
    
    ::-webkit-scrollbar-thumb {
        background: linear-gradient(135deg, #667eea, #764ba2);
        border-radius: 10px;
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: linear-gradient(135deg, #764ba2, #667eea);
    }
</style>
""", unsafe_allow_html=True)# The rest of the program configuration, data handling, and application logic would continue from here.
# For brevity, I'm focusing on the style and UI updates as requested.


# -----------------------------
# Config - Data & Auth
# -----------------------------
TENANT_ID = "talos"
AUTH_TOKEN = None
HEADERS_BASE = {"Content-Type": "application/json"}

ACCOUNTS = [
    "Select Account",
    "Abbive", "BMS", "BLR Airport", "Chevron", "Coles", "DELL", "Microsoft", 
    "Mu Labs", "Nike", "Skill Development", "Southwest Airlines", "THD", "Tmobile", "Walmart"
]

INDUSTRIES = [
    "Select Industry",
    "Airlines", "Automotive", "Consumer Goods", "E-commerce", "Education", "Energy", 
    "Finance", "Healthcare", "Hospitality", "Logistics", "Other", "Pharma", "Retail", "Technology"
]

# API Configuration
API_CONFIGS = [
    {
        "name": "vocabulary",
        "url": "https://eoc.mu-sigma.com/talos-engine/agency/reasoning_api?society_id=1757657318406&agency_id=1758548233201&level=1",
        "multiround_convo": 3,
        "description": "Vocabulary Extraction"
    },
    {
        "name": "current_system",
        "url": "https://eoc.mu-sigma.com/talos-engine/agency/reasoning_api?society_id=1757657318406&agency_id=1758549095254&level=1",
        "multiround_convo": 2,
        "description": "Current System Analysis"
    },
    {
        "name": "Q1",
        "url": "https://eoc.mu-sigma.com/talos-engine/agency/reasoning_api?society_id=1757657318406&agency_id=1758555344231&level=1",
        "multiround_convo": 2,
        "question": "What is the frequency and pace of change in the key inputs driving the business?"
    },
    {
        "name": "Q2",
        "url": "https://eoc.mu-sigma.com/talos-engine/agency/reasoning_api?society_id=1757657318406&agency_id=1758549615986&level=1",
        "multiround_convo": 2,
        "question": "To what extent are these changes cyclical and predictable versus sporadic and unpredictable?"
    },
    {
        "name": "Q3",
        "url": "https://eoc.mu-sigma.com/talos-engine/agency/reasoning_api?society_id=1757657318406&agency_id=1758614550482&level=1",
        "multiround_convo": 2,
        "question": "How resilient is the current system in absorbing these changes without requiring significant rework or disruption?"
    },
    {
        "name": "Q4",
        "url": "https://eoc.mu-sigma.com/talos-engine/agency/reasoning_api?society_id=1757657318406&agency_id=1758614809984&level=1",
        "multiround_convo": 2,
        "question": "To what extent do stakeholders share a common understanding of the key terms and concepts?"
    },
    {
        "name": "Q5",
        "url": "https://eoc.mu-sigma.com/talos-engine/agency/reasoning_api?society_id=1757657318406&agency_id=1758615038050&level=1",
        "multiround_convo": 2,
        "question": "Are there any conflicting definitions or interpretations that could create confusion?"
    },
    {
        "name": "Q6",
        "url": "https://eoc.mu-sigma.com/talos-engine/agency/reasoning_api?society_id=1757657318406&agency_id=1758615386880&level=1",
        "multiround_convo": 2,
        "question": "Are objectives, priorities, and constraints clearly communicated and well-defined?"
    },
    {
        "name": "Q7",
        "url": "https://eoc.mu-sigma.com/talos-engine/agency/reasoning_api?society_id=1757657318406&agency_id=1758615778653&level=1",
        "multiround_convo": 2,
        "question": "To what extent are key inputs interdependent?"
    },
    {
        "name": "Q8",
        "url": "https://eoc.mu-sigma.com/talos-engine/agency/reasoning_api?society_id=1757657318406&agency_id=1758616081630&level=1",
        "multiround_convo": 2,
        "question": "How well are the governing rules, functions, and relationships between inputs understood?"
    },
    {
        "name": "Q9",
        "url": "https://eoc.mu-sigma.com/talos-engine/agency/reasoning_api?society_id=1757657318406&agency_id=1758616793510&level=1",
        "multiround_convo": 2,
        "question": "Are there any hidden or latent dependencies that could impact outcomes?"
    },
    {
        "name": "Q10",
        "url": "https://eoc.mu-sigma.com/talos-engine/agency/reasoning_api?society_id=1757657318406&agency_id=1758617140479&level=1",
        "multiround_convo": 2,
        "question": "Are there hidden or latent dependencies that could affect outcomes?"
    },
    {
        "name": "Q11",
        "url": "https://eoc.mu-sigma.com/talos-engine/agency/reasoning_api?society_id=1757657318406&agency_id=1758618137301&level=1",
        "multiround_convo": 2,
        "question": "Are feedback loops insufficient or missing, limiting our ability to adapt?"
    },
    {
        "name": "Q12",
        "url": "https://eoc.mu-sigma.com/talos-engine/agency/reasoning_api?society_id=1757657318406&agency_id=1758619317968&level=1",
        "multiround_convo": 2,
        "question": "Do we lack established benchmarks or 'gold standards' to validate results?"
    },
    {
        "name": "hardness_summary",
        "url": "https://eoc.mu-sigma.com/talos-engine/agency/reasoning_api?society_id=1757657318406&agency_id=1758619658634&level=1",
        "multiround_convo": 2,
        "description": "Hardness Level & Dimension Scores"
    }
]

# Dimension mapping
DIMENSION_QUESTIONS = {
    "Volatility": ["Q1", "Q2", "Q3"],
    "Ambiguity": ["Q4", "Q5", "Q6"],
    "Interconnectedness": ["Q7", "Q8", "Q9"],
    "Uncertainty": ["Q10", "Q11", "Q12"]
}

# -----------------------------
# Utility Functions
# -----------------------------
def json_to_text(data):
    if data is None: 
        return ""
    if isinstance(data, str): 
        return data
    if isinstance(data, dict):
        for key in ("result", "output", "content", "text"):
            if key in data and data[key]: 
                return json_to_text(data[key])
        if "data" in data: 
            return json_to_text(data["data"])
        return "\n".join(f"{k}: {json_to_text(v)}" for k, v in data.items() if v)
    if isinstance(data, list): 
        return "\n".join(json_to_text(x) for x in data if x)
    return str(data)

def call_api(api_cfg, problem_text, outputs, tenant_id=TENANT_ID, auth_token=AUTH_TOKEN, tries=3):
    # Build prompt based on API
    if api_cfg["name"] == "vocabulary":
        prompt = f"{problem_text}\n\nExtract the vocabulary from this problem statement."
    elif api_cfg["name"] == "current_system":
        prompt = f"Problem statement - {problem_text}\n\nContext from vocabulary:\n{outputs.get('vocabulary','')}\n\nDescribe the current system, inputs, outputs, and pain points."
    elif api_cfg["name"] in [f"Q{i}" for i in range(1, 13)]:
        prompt = f"Problem statement - {problem_text}\n\nContext from Current System:\n{outputs.get('current_system','')}\n\n{api_cfg.get('question', '')} Provide detailed analysis, score 0–5, and justification."
    elif api_cfg["name"] == "hardness_summary":
        # Build comprehensive context for hardness summary
        context_parts = []
        if outputs.get('vocabulary'):
            context_parts.append(f"Vocabulary:\n{outputs['vocabulary']}")
        if outputs.get('current_system'):
            context_parts.append(f"Current System Analysis:\n{outputs['current_system']}")
        
        # Add all Q&A responses
        for i in range(1, 13):
            q_key = f"Q{i}"
            if outputs.get(q_key):
                context_parts.append(f"{q_key}:\n{outputs[q_key]}")
        
        context = "\n\n".join(context_parts)
        prompt = f"""Problem statement: {problem_text}

Based on the following comprehensive analysis, provide:
1. Overall Hardness Level (Hard/Moderate/Easy)
2. Overall Difficulty Score (0-5)
3. Individual dimension scores for Volatility, Ambiguity, Interconnectedness, and Uncertainty (0-5 scale)
4. Detailed summary and key takeaways

Analysis Context:
{context}

Please structure your response clearly with the scores and classification."""
    else:
        prompt = problem_text
    
    headers_list = []
    base = HEADERS_BASE.copy()
    if tenant_id:
        headers_list = [
            dict(base, **{"Tenant-ID": tenant_id}), 
            dict(base, **{"X-Tenant-ID": tenant_id})
        ]
    else:
        headers_list = [base]
    
    if auth_token:
        headers_list = [dict(h, **{"Authorization": f"Bearer {auth_token}"}) for h in headers_list]

    last_err = None
    for attempt in range(1, tries + 1):
        for headers in headers_list:
            try:
                resp = requests.post(
                    api_cfg["url"], 
                    headers=headers, 
                    json={"prompt": prompt}, 
                    timeout=60
                )
                if resp.status_code == 200:
                    res = json_to_text(resp.json())
                    for r in range(1, api_cfg.get("multiround_convo", 1)):
                        resp2 = requests.post(
                            api_cfg["url"], 
                            headers=headers, 
                            json={"prompt": res}, 
                            timeout=60
                        )
                        if resp2.status_code == 200: 
                            res = json_to_text(resp2.json())
                    return res
                else:
                    last_err = f"{resp.status_code}-{resp.text}"
            except Exception as e:
                last_err = str(e)
        time.sleep(1 + attempt * 0.5)
    
    return f"API failed after {tries} attempts. Last error: {last_err}"

def classify_hardness(overall_score):
    """Classify hardness level based on overall score with new thresholds"""
    if overall_score >= 4.0:
        return "Hard"
    elif overall_score >= 3.6:
        return "Moderate to Hard"
    elif overall_score >= 3.5:
        return "Moderate"
    else:
        return "Easy"

def extract_score_from_text(text, dimension):
    """Extract dimension score from hardness_summary API output"""
    if not text:
        return 0.0
    
    # Multiple patterns to catch different formats
    patterns = [
        # Pattern 1: **Volatility Score**: 4.2/5
        rf"\*\*{dimension}\s+Score\*\*:\s*(\d+(?:\.\d+)?)\s*\/\s*5",
        # Pattern 2: Volatility: 4.2/5
        rf"{dimension}:\s*(\d+(?:\.\d+)?)\s*\/\s*5",
        # Pattern 3: **Volatility**: 4.2
        rf"\*\*{dimension}\*\*:\s*(\d+(?:\.\d+)?)",
        # Pattern 4: Volatility - 4.2
        rf"{dimension}\s*[-\—]\s*(\d+(?:\.\d+)?)",
        # Pattern 5: Look for scores in tables or lists
        rf"{dimension}.*?(\d+(?:\.\d+)?)\s*(?=\/|$)",
    ]
    
    for pattern in patterns:
        match = re.search(pattern, text, re.IGNORECASE | re.MULTILINE)
        if match:
            try:
                score = float(match.group(1))
                if 0 <= score <= 5:
                    return score
            except:
                continue
    
    # Fallback: Look for any number between 0-5 near the dimension name
    fallback_pattern = rf"{dimension}.*?(\d+(?:\.\d+)?)"
    matches = re.findall(fallback_pattern, text, re.IGNORECASE | re.MULTILINE)
    for match in matches:
        try:
            num_match = re.search(r"(\d+(?:\.\d+)?)", match)
            if num_match:
                score = float(num_match.group(1))
                if 0 <= score <= 5:
                    return score
        except:
            continue
    
    return 0.0

def extract_overall_score(text):
    """Calculate Overall Difficulty Score as average of all four dimension scores"""
    dimensions = ["Volatility", "Ambiguity", "Interconnectedness", "Uncertainty"]
    scores = []
    
    for dim in dimensions:
        score = extract_score_from_text(text, dim)
        if score > 0:
            scores.append(score)
    
    # Calculate average of all four dimensions
    if len(scores) == 4:  # We have all four dimension scores
        return sum(scores) / len(scores)
    elif len(scores) >= 2:  # Fallback if we don't have all four
        return sum(scores) / len(scores)
    
    return 0.0

def extract_hardness_level(text, overall_score):
    """Extract hardness level based on calculated overall score"""
    return classify_hardness(overall_score)

def extract_current_system_full(text):
    """Extract the full current system description from current_system API"""
    if not text:
        return "No current system information available"
    
    # Remove any "Analysis of the Problem Statement" sections
    text = re.sub(r'\*\*Analysis\s+of\s+the\s+Problem\s+Statement\*\*.*?(?=###|\*\*[A-Z]|\Z)', '', text, flags=re.DOTALL | re.IGNORECASE)
    
    # Look for ### Current System section
    pattern1 = r'###\s*Current\s*System[:\s]*(.*?)(?=###\s*Input|###\s*Output|###\s*Pain|\Z)'
    match = re.search(pattern1, text, re.DOTALL | re.IGNORECASE)
    if match:
        content = match.group(1).strip()
        # Clean up
        content = re.sub(r'\n{3,}', '\n\n', content)
        if content and len(content) > 50:
            return content
    
    # Alternative: Look for text before ### Inputs
    pattern2 = r'^(.*?)(?=###\s*Input)'
    match = re.search(pattern2, text, re.DOTALL | re.IGNORECASE)
    if match:
        content = match.group(1).strip()
        # Remove title lines
        content = re.sub(r'^Current\s*System[:\s]*[-]*\s*', '', content, flags=re.IGNORECASE)
        content = re.sub(r'\n{3,}', '\n\n', content)
        if content and len(content) > 50:
            return content
    
    return "No current system information found"

def extract_input(text):
    """Extract Input section from current_system API"""
    if not text:
        return "No input information available"
    
    # Look for ### Inputs or ### Input section
    patterns = [
        r'###\s*Input[s]?[:\s]*(.*?)(?=###\s*Output|###\s*Pain|\Z)',
        r'\*\*Input[s]?\*\*[:\s]*(.*?)(?=###\s*Output|###\s*Pain|\*\*Output|\*\*Pain|\Z)',
    ]
    
    for pattern in patterns:
        match = re.search(pattern, text, re.DOTALL | re.IGNORECASE)
        if match:
            content = match.group(1).strip()
            # Clean up
            content = re.sub(r'^\s*:?\s*[-]*\s*', '', content)
            content = re.sub(r'\n{3,}', '\n\n', content)
            if content and len(content) > 20:
                return content
    
    return "No input information found"

def extract_output(text):
    """Extract Output section from current_system API"""
    if not text:
        return "No output information available"
    
    # Look for ### Outputs or ### Output section
    patterns = [
        r'###\s*Output[s]?[:\s]*(.*?)(?=###\s*Pain|###\s*Input|\Z)',
        r'\*\*Output[s]?\*\*[:\s]*(.*?)(?=###\s*Pain|###\s*Input|\*\*Pain|\*\*Input|\Z)',
    ]
    
    for pattern in patterns:
        match = re.search(pattern, text, re.DOTALL | re.IGNORECASE)
        if match:
            content = match.group(1).strip()
            # Clean up
            content = re.sub(r'^\s*:?\s*[-]*\s*', '', content)
            content = re.sub(r'\n{3,}', '\n\n', content)
            if content and len(content) > 20:
                return content
    
    return "No output information found"

def extract_pain_points(text):
    """Extract Pain Points section from current_system API"""
    if not text:
        return "No pain points information available"
    
    # Look for ### Pain Points or similar sections
    patterns = [
        r'###\s*Pain\s*Point[s]?[:\s]*(.*?)(?=###\s*[A-Z]|\Z)',
        r'\*\*Pain\s*Point[s]?\*\*[:\s]*(.*?)(?=###\s*[A-Z]|\*\*[A-Z]|\Z)',
        r'###\s*Challenge[s]?[:\s]*(.*?)(?=###\s*[A-Z]|\Z)',
        r'###\s*Shortcoming[s]?[:\s]*(.*?)(?=###\s*[A-Z]|\Z)',
    ]
    
    for pattern in patterns:
        match = re.search(pattern, text, re.DOTALL | re.IGNORECASE)
        if match:
            content = match.group(1).strip()
            # Clean up
            content = re.sub(r'^\s*:?\s*[-]*\s*', '', content)
            content = re.sub(r'\n{3,}', '\n\n', content)
            if content and len(content) > 20:
                return content
    
    return "No pain points information found"

def extract_summary_and_takeaways(text):
    """Extract and format Summary as crisp bullet points supporting the classification"""
    if not text:
        return ""
    
    # Remove "Analysis of the Problem Statement" sections
    text = re.sub(r'\*\*Analysis\s+of\s+the\s+Problem\s+Statement\*\*.*?(?=\*\*Summary|\*\*Hardness|\Z)', '', text, flags=re.DOTALL | re.IGNORECASE)
    
    # Look for Summary section
    patterns = [
        r'\*\*Summary\s*&?\s*Key\s*Takeaway[s]?\*\*[:\s]*(.*?)(?=\Z)',
        r'\*\*Key\s*Takeaway[s]?\*\*[:\s]*(.*?)(?=\Z)',
        r'\*\*Summary\*\*[:\s]*(.*?)(?=\Z)',
    ]
    
    summary_text = ""
    for pattern in patterns:
        match = re.search(pattern, text, re.DOTALL | re.IGNORECASE)
        if match:
            content = match.group(1).strip()
            if content and len(content) > 20:
                summary_text = content
                break
    
    # If no summary found, try "In conclusion"
    if not summary_text:
        pattern2 = r'(?:In\s+conclusion|Summary)[:\s]*(.*?)(?=\Z)'
        match = re.search(pattern2, text, re.DOTALL | re.IGNORECASE)
        if match:
            summary_text = match.group(1).strip()
    
    # If still no summary, get last substantial section
    if not summary_text:
        sections = [s.strip() for s in text.split('**') if s.strip() and len(s.strip()) > 50]
        if sections:
            for section in reversed(sections):
                if not re.search(r'\d+\.\d+\s*/\s*\d+', section) and not re.search(r'Score.*?=', section):
                    summary_text = section
                    break
    
    if not summary_text:
        return ""
    
    # Convert to crisp bullet points
    # Extract numbered points or convert paragraphs to bullets
    bullet_points = []
    
    # Try to find numbered points (1., 2., etc.)
    numbered_pattern = r'\d+\.\s*\*\*([^*]+)\*\*[:\s]*([^\n]+(?:\n(?!\d+\.)[^\n]+)*)'
    matches = re.findall(numbered_pattern, summary_text, re.MULTILINE)
    
    if matches:
        for title, content in matches:
            title = title.strip()
            content = content.strip()
            # Clean up content - remove extra whitespace
            content = re.sub(r'\s+', ' ', content)
            bullet_points.append(f"**{title}:** {content}")
    else:
        # Split by sentences or paragraphs
        sentences = re.split(r'[.!?]\s+', summary_text)
        for sentence in sentences:
            sentence = sentence.strip()
            if len(sentence) > 30 and not re.search(r'\d+\.\d+\s*/\s*\d+', sentence):
                # Clean up
                sentence = re.sub(r'\s+', ' ', sentence)
                if not sentence.endswith('.'):
                    sentence += '.'
                bullet_points.append(sentence)
    
    # Limit to 4-5 key points
    bullet_points = bullet_points[:5]
    
    # Format as markdown bullets
    if bullet_points:
        return '\n\n'.join(f"• {point}" for point in bullet_points)
    
    return summary_text

# -----------------------------
# Session State Initialization
# -----------------------------
def init_session_state():
    defaults = {
        "current_page": "page1",
        "problem_text": "",
        "industry": "Select Industry",
        "account": "Select Account",
        "outputs": {},
        "analysis_complete": False,
        "dimension_scores": {
            "Volatility": 0.0,
            "Ambiguity": 0.0, 
            "Interconnectedness": 0.0,
            "Uncertainty": 0.0
        },
        "hardness_level": None,
        "overall_score": 0.0,
        "summary": "",
        "current_system_full": "",
        "input_text": "",
        "output_text": "",
        "pain_points_text": "",
        "hardness_summary_text": ""  # Add this to store the hardness summary
    }
    
    for key, default_value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = default_value

init_session_state()

# -----------------------------
# PAGE 1: Business Problem Input & Analysis
# -----------------------------
if st.session_state.current_page == "page1":
    st.markdown('<div class="page-title"><h1>Business Problem Level Classifier</h1></div>', unsafe_allow_html=True)
    
    # Industry & Account Selection
    col1, col2 = st.columns(2)
    
    with col1:
        st.session_state.industry = st.selectbox(
            "Select Industry",
            INDUSTRIES,
            index=INDUSTRIES.index(st.session_state.industry) if st.session_state.industry in INDUSTRIES else 0
        )
    
    with col2:
        st.session_state.account = st.selectbox(
            "Select Account",
            ACCOUNTS,
            index=ACCOUNTS.index(st.session_state.account) if st.session_state.account in ACCOUNTS else 0
        )
    
    # Business Problem Description
    st.markdown("### Business Problem Description")
    st.session_state.problem_text = st.text_area(
        "Describe your business problem in detail:",
        value=st.session_state.problem_text,
        height=200,
        placeholder="Enter a detailed description of your business challenge..."
    )
    
    # Analysis Button and Vocabulary Button
    col1, col2 = st.columns([3, 1])
    
    with col1:
        analyze_btn = st.button(
            "Analyze Problem",
            type="primary",
            use_container_width=True,
            disabled=not (st.session_state.problem_text.strip() and 
                         st.session_state.industry != "Select Industry" and 
                         st.session_state.account != "Select Account")
        )
    
    with col2:
        if st.session_state.analysis_complete:
            with st.expander("📚 Vocabulary"):
                st.write(st.session_state.outputs.get('vocabulary', 'No vocabulary data available'))
    
    if analyze_btn:
        with st.spinner("Analyzing your business problem..."):
            progress_bar = st.progress(0)
            st.session_state.outputs = {}
            
            # Process all APIs including hardness_summary
            total_apis = len(API_CONFIGS)
            for i, api_config in enumerate(API_CONFIGS):
                progress = (i / total_apis)
                progress_bar.progress(progress)
                
                result = call_api(api_config, st.session_state.problem_text, st.session_state.outputs)
                st.session_state.outputs[api_config['name']] = result
                
                time.sleep(0.5)
            
            progress_bar.progress(1.0)
            
            # Extract data from hardness_summary API
            hardness_summary = st.session_state.outputs.get('hardness_summary', '')
            st.session_state.hardness_summary_text = hardness_summary  # Store the full text
            # Extract dimension scores first
            dimension_scores_list = []
            for dimension in ["Volatility", "Ambiguity", "Interconnectedness", "Uncertainty"]:
                score = extract_score_from_text(hardness_summary, dimension)
                st.session_state.dimension_scores[dimension] = score
                dimension_scores_list.append(score)
            # Calculate overall score as average of all four dimension scores
            st.session_state.overall_score = sum(dimension_scores_list) / len(dimension_scores_list)
            # Classify hardness based on the calculated overall score using new thresholds
            st.session_state.hardness_level = extract_hardness_level(hardness_summary, st.session_state.overall_score)
            
            # Extract summary
            st.session_state.summary = extract_summary_and_takeaways(hardness_summary)
            
            # Extract current system components from current_system API
            current_system_text = st.session_state.outputs.get('current_system', '')
            st.session_state.current_system_full = extract_current_system_full(current_system_text)
            st.session_state.input_text = extract_input(current_system_text)
            st.session_state.output_text = extract_output(current_system_text)
            st.session_state.pain_points_text = extract_pain_points(current_system_text)
            
            st.session_state.analysis_complete = True
            st.success("Analysis complete!")
            st.rerun()
    
    # Display Results if analysis is complete
    if st.session_state.analysis_complete:
        st.markdown("---")
        
        # Hardness Level Section
        col1, col2 = st.columns(2)
        
        with col1:
            hardness = st.session_state.hardness_level
            if hardness == "Hard":
                badge_class = "hardness-badge-hard"
            elif hardness == "Moderate to Hard":
                badge_class = "hardness-badge-moderate-to-hard"
            elif hardness == "Moderate":
                badge_class = "hardness-badge-moderate"
            else:
                badge_class = "hardness-badge-easy"
            
            st.markdown(f'<div class="{badge_class}">{hardness}</div>', unsafe_allow_html=True)
        
        with col2:
            overall = st.session_state.overall_score
            st.markdown(f'''
            <div class="score-badge">
                <div style="font-size: 1.2rem; font-weight: 600; opacity: 0.95; margin-bottom: 0.5rem;">Overall Difficulty Score</div>
                <div style="font-size: 2.5rem; font-weight: 800;">{overall:.2f}/5</div>
            </div>
            ''', unsafe_allow_html=True)
        
        # Dimension Scores - Four boxes only
        st.markdown("---")
        col1, col2 = st.columns(2)
        dimensions = ["Volatility", "Ambiguity", "Interconnectedness", "Uncertainty"]
        
        for i, dimension in enumerate(dimensions):
            with col1 if i < 2 else col2:
                score = st.session_state.dimension_scores.get(dimension, 0.0)
                st.markdown(f"""
                <div class="dimension-box">
                    <div class="dimension-label">{dimension}</div>
                    <div class="dimension-score">{score:.2f}/5</div>
                </div>
                """, unsafe_allow_html=True)
        
        # Summary & Key Takeaways - Clear background box
        st.markdown("---")
        st.markdown("### Summary & Key Takeaways")
        
        if st.session_state.summary:
            st.markdown(f'<div class="content-text">{st.session_state.summary}</div>', unsafe_allow_html=True)
        else:
            # Fallback: Show the full hardness summary if no summary extracted
            st.markdown(f'<div class="content-text">{st.session_state.hardness_summary_text}</div>', unsafe_allow_html=True)
        
        # Navigation Buttons
        st.markdown("---")
        col1, col2, col3 = st.columns([2, 1, 1])
        with col2:
            if st.button("View Details →", use_container_width=True):
                st.session_state.current_page = "page2"
                st.rerun()
        with col3:
            if st.button("View Hardness Summary →", use_container_width=True):
                st.session_state.current_page = "hardness_summary"
                st.rerun()

# -----------------------------
# PAGE 2: Current System & Pain Points
# -----------------------------
elif st.session_state.current_page == "page2":
    st.markdown('<div class="page-title"><h1>Current System & Pain Points</h1></div>', unsafe_allow_html=True)
    
    # Display Business Problem
    st.markdown('<div class="problem-display">', unsafe_allow_html=True)
    st.markdown("<h4>Business Problem</h4>", unsafe_allow_html=True)
    st.write(st.session_state.problem_text)
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Back button
    if st.button("← Back to Analysis", use_container_width=False):
        st.session_state.current_page = "page1"
        st.rerun()
    
    # Current System Section - No box
    st.markdown('<p class="section-title">Current System</p>', unsafe_allow_html=True)
    st.markdown(f'<div class="content-text">{st.session_state.current_system_full}</div>', unsafe_allow_html=True)
    
    # Input and Output - No boxes
    st.markdown('<p class="section-title">Input and Output</p>', unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### Input")
        st.markdown(f'<div class="content-text">{st.session_state.input_text}</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown("#### Output")
        st.markdown(f'<div class="content-text">{st.session_state.output_text}</div>', unsafe_allow_html=True)
    
    # Pain Points Section - No box
    st.markdown('<p class="section-title">Pain Points</p>', unsafe_allow_html=True)
    st.markdown(f'<div class="content-text">{st.session_state.pain_points_text}</div>', unsafe_allow_html=True)
    
    # Dimension Scores - Click to view details
    st.markdown('<p class="section-title">Dimension Scores - Click to view details</p>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    dimensions = ["Volatility", "Ambiguity", "Interconnectedness", "Uncertainty"]
    
    for i, dimension in enumerate(dimensions):
        with col1 if i < 2 else col2:
            score = st.session_state.dimension_scores.get(dimension, 0.0)
            
            st.markdown(f"""
            <div class="dimension-box">
                <div class="dimension-label">{dimension}</div>
                <div class="dimension-score">{score:.2f}/5</div>
            </div>
            """, unsafe_allow_html=True)
            
            if st.button(f"View {dimension} Details", key=f"dim_{dimension}", use_container_width=True):
                st.session_state.current_page = f"dimension_{dimension.lower()}"
                st.rerun()
    
    # Navigation to Hardness Summary
    st.markdown("---")
    if st.button("View Hardness Summary →", use_container_width=True):
        st.session_state.current_page = "hardness_summary"
        st.rerun()

# -----------------------------
# NEW PAGE: Hardness Summary
# -----------------------------
elif st.session_state.current_page == "hardness_summary":
    st.markdown('<div class="page-title"><h1>Hardness Summary Analysis</h1></div>', unsafe_allow_html=True)
    
    # Display Business Problem
    st.markdown('<div class="problem-display">', unsafe_allow_html=True)
    st.markdown("<h4>Business Problem</h4>", unsafe_allow_html=True)
    st.write(st.session_state.problem_text)
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Back button
    col1, col2 = st.columns([3, 1])
    with col1:
        if st.button("← Back to System Overview", use_container_width=False):
            st.session_state.current_page = "page2"
            st.rerun()
    
    # Display Hardness Summary
    st.markdown('<p class="section-title">Hardness Summary Analysis</p>', unsafe_allow_html=True)
    
    if st.session_state.hardness_summary_text:
        st.markdown(f'<div class="content-text">{st.session_state.hardness_summary_text}</div>', unsafe_allow_html=True)
    else:
        st.markdown('<div class="content-text">No hardness summary available. Please run the analysis first.</div>', unsafe_allow_html=True)
    
    # Display Scores Summary
    st.markdown('<p class="section-title">Extracted Scores</p>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown(f'''
        <div class="score-badge">
            <div style="font-size: 1.2rem; font-weight: 600; opacity: 0.95; margin-bottom: 0.5rem;">Overall Difficulty Score</div>
            <div style="font-size: 2.5rem; font-weight: 800;">{st.session_state.overall_score:.2f}/5</div>
        </div>
        ''', unsafe_allow_html=True)
        
        hardness = st.session_state.hardness_level
        if hardness == "Hard":
            badge_class = "hardness-badge-hard"
        elif hardness == "Moderate":
            badge_class = "hardness-badge-moderate"
        else:
            badge_class = "hardness-badge-easy"
        
        st.markdown(f'<div class="{badge_class}" style="margin-top: 1rem;">{hardness}</div>', unsafe_allow_html=True)
    
    with col2:
        # Display dimension scores
        dimensions = ["Volatility", "Ambiguity", "Interconnectedness", "Uncertainty"]
        for dimension in dimensions:
            score = st.session_state.dimension_scores.get(dimension, 0.0)
            st.markdown(f"""
            <div class="dimension-box" style="min-height: 80px; padding: 1rem;">
                <div class="dimension-label">{dimension}</div>
                <div class="dimension-score" style="font-size: 1.8rem;">{score:.2f}/5</div>
            </div>
            """, unsafe_allow_html=True)

# -----------------------------
# PAGES 3-6: Dimension Details
# -----------------------------
elif st.session_state.current_page.startswith("dimension_"):
    dimension_name = st.session_state.current_page.replace("dimension_", "").title()
    
    st.markdown(f'<div class="page-title"><h1>{dimension_name} Analysis</h1></div>', unsafe_allow_html=True)
    
    # Display Business Problem
    st.markdown('<div class="problem-display">', unsafe_allow_html=True)
    st.markdown("<h4>Business Problem</h4>", unsafe_allow_html=True)
    st.write(st.session_state.problem_text)
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Back button
    if st.button("← Back to System Overview", use_container_width=False):
        st.session_state.current_page = "page2"
        st.rerun()
    
    # Display dimension score
    score = st.session_state.dimension_scores.get(dimension_name, 0.0)
    st.markdown(f"""
    <div class="score-badge" style="margin-bottom: 2rem;">
        <div style="font-size: 1.5rem; font-weight: 600; margin-bottom: 0.5rem;">{dimension_name}</div>
        <div style="font-size: 3rem; font-weight: 800;">{score:.2f}/5</div>
    </div>
    """, unsafe_allow_html=True)
    
    # Display Q&A for this dimension
    st.markdown("### Detailed Analysis")
    questions = DIMENSION_QUESTIONS.get(dimension_name, [])
    
    for q_name in questions:
        q_config = next((cfg for cfg in API_CONFIGS if cfg["name"] == q_name), None)
        if q_config:
            question_text = q_config.get("question", f"Question {q_name}")
            answer_text = st.session_state.outputs.get(q_name, "No analysis available")
            
            st.markdown('<div class="qa-box">', unsafe_allow_html=True)
            st.markdown(f'<div class="qa-question">Q: {question_text}</div>', unsafe_allow_html=True)
            st.markdown(f'<div class="qa-answer">{answer_text}</div>', unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)
    
    # Navigation to Hardness Summary
    st.markdown("---")
    if st.button("View Hardness Summary →", use_container_width=True):
        st.session_state.current_page = "hardness_summary"
        st.rerun()