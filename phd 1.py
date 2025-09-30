import streamlit as st
import requests, json, os, re, time
import hashlib
from datetime import datetime, timedelta
from io import BytesIO
import unicodedata
import pandas as pd

# Configure the page settings
st.set_page_config(
    page_title="Problem Complexity Analyzer",
    page_icon="🔍",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Dark Theme CSS with Black Text
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@300;400;500;600;700&family=Inter:wght@300;400;500;600;700&display=swap');

.main {
    background: linear-gradient(135deg, #0f0f23 0%, #1a1a2e 50%, #16213e 100%);
    font-family: 'Inter', sans-serif;
    color: #000000;  /* Black text */
}

.stApp {
    background: transparent;
}

/* Header Styles */
.app-header {
    background: rgba(255, 255, 255, 0.05);
    backdrop-filter: blur(20px);
    border: 1px solid rgba(255, 193, 7, 0.2);
    padding: 2rem;
    border-radius: 20px;
    margin-bottom: 2rem;
    text-align: center;
    position: relative;
    overflow: hidden;
}

.app-header::before {
    content: '';
    position: absolute;
    top: 0;
    left: -100%;
    width: 100%;
    height: 100%;
    background: linear-gradient(90deg, transparent, rgba(255, 193, 7, 0.1), transparent);
    transition: left 0.5s;
}

.app-header:hover::before {
    left: 100%;
}

.app-title {
    font-size: 3rem;
    font-weight: 700;
    background: linear-gradient(45deg, #ffd700, #ffa500, #ff8c00);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-size: 200% 100%;
    animation: shimmer 3s ease-in-out infinite;
    margin-bottom: 0.5rem;
}

@keyframes shimmer {
    0%, 100% { background-position: -200% 0; }
    50% { background-position: 200% 0; }
}

.app-subtitle {
    color: #000000; /* Black text */
    font-size: 1.2rem;
    font-weight: 300;
}

/* Card Components */
.analysis-card {
    background: rgba(255, 255, 255, 0.05);
    backdrop-filter: blur(20px);
    border: 1px solid rgba(255, 193, 7, 0.1);
    border-radius: 16px;
    padding: 2rem;
    margin-bottom: 1.5rem;
    transition: all 0.3s ease;
    position: relative;
    overflow: hidden;
    color: #000000; /* Black text */
}

.analysis-card::before {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    height: 3px;
    background: linear-gradient(90deg, #ffd700, #ffa500, #ff8c00);
}

.analysis-card:hover {
    transform: translateY(-5px);
    border-color: rgba(255, 193, 7, 0.3);
    box-shadow: 0 20px 40px rgba(255, 193, 7, 0.1);
}

/* Complexity Badges */
.complexity-badge {
    padding: 1.5rem;
    border-radius: 16px;
    text-align: center;
    font-weight: 700;
    font-size: 1.5rem;
    margin-bottom: 1rem;
    position: relative;
    overflow: hidden;
    color: #000000; /* Black text */
}

.complexity-high {
    background: linear-gradient(135deg, #dc3545, #c82333, #dc3545);
    background-size: 200% 200%;
    animation: gradientShift 2s ease infinite;
    color: #ffffff; /* Keep white for contrast */
}

.complexity-medium {
    background: linear-gradient(135deg, #ffc107, #ff8c00, #ffc107);
    background-size: 200% 200%;
    animation: gradientShift 3s ease infinite;
    color: #000000; /* Black text */
}

.complexity-low {
    background: linear-gradient(135deg, #28a745, #20c997, #28a745);
    background-size: 200% 200%;
    animation: gradientShift 4s ease infinite;
    color: #ffffff;
}

@keyframes gradientShift {
    0%, 100% { background-position: 0% 50%; }
    50% { background-position: 100% 50%; }
}

/* Dimension Meters */
.dimension-meter {
    background: rgba(255, 255, 255, 0.05);
    border-radius: 12px;
    padding: 1.5rem;
    margin-bottom: 1rem;
    border: 1px solid rgba(255, 255, 255, 0.1);
    transition: all 0.3s ease;
    color: #000000; /* Black text */
}

.dimension-meter:hover {
    border-color: rgba(255, 193, 7, 0.3);
    transform: translateX(5px);
}

.meter-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 1rem;
}

.meter-label, .meter-value {
    color: #000000; /* Black text */
}

.meter-bar {
    height: 8px;
    background: rgba(255, 255, 255, 0.1);
    border-radius: 4px;
    overflow: hidden;
    margin-bottom: 0.5rem;
}

.meter-fill {
    height: 100%;
    border-radius: 4px;
    transition: width 1s ease-in-out;
}

.fill-high { background: linear-gradient(90deg, #dc3545, #c82333); }
.fill-medium { background: linear-gradient(90deg, #ffc107, #ff8c00); }
.fill-low { background: linear-gradient(90deg, #28a745, #20c997); }

/* Buttons */
.stButton > button {
    background: linear-gradient(135deg, #ffc107 0%, #ff8c00 100%);
    color: #000000;  /* Black text */
    border: none;
    border-radius: 12px;
    font-weight: 600;
    padding: 1rem 2rem;
    transition: all 0.3s ease;
    font-family: 'Inter', sans-serif;
}

.stButton > button:hover {
    transform: translateY(-2px);
    box-shadow: 0 10px 25px rgba(255, 193, 7, 0.4);
    background: linear-gradient(135deg, #ff8c00 0%, #ffc107 100%);
}

/* Input Fields */
.stTextArea > div > div > textarea,
.stSelectbox > div > div {
    background: rgba(255, 255, 255, 0.05) !important;
    border: 1px solid rgba(255, 255, 255, 0.1) !important;
    border-radius: 12px !important;
    color: #000000 !important;  /* Black text */
    font-family: 'Inter', sans-serif !important;
}

/* Section Headers */
.section-header {
    color: #000000; /* Black text */
    font-size: 1.5rem;
    font-weight: 600;
    margin: 2rem 0 1rem 0;
    padding-bottom: 0.5rem;
    border-bottom: 2px solid rgba(255, 193, 7, 0.3);
}

/* Content Boxes */
.content-box, .highlight-box {
    background: rgba(255, 255, 255, 0.03);
    border: 1px solid rgba(255, 193, 7, 0.1);
    border-radius: 12px;
    padding: 1.5rem;
    margin: 1rem 0;
    color: #000000; /* Black text */
    line-height: 1.6;
}


</style>
""", unsafe_allow_html=True)

# ---------- Rest of your original code (API configs, functions, Streamlit logic) ----------
# Keep the rest of your code unchanged from the version you provided
# (the code will function as before with black text now)


# Configuration
TENANT_ID = "talos"
AUTH_TOKEN = None
HEADERS_BASE = {"Content-Type": "application/json"}

ACCOUNTS = [
    "Select Account", "Abbive", "BMS", "BLR Airport", "Chevron", "Coles", 
    "DELL", "Microsoft", "Mu Labs", "Nike", "Skill Development", 
    "Southwest Airlines", "THD", "Tmobile", "Walmart"
]

INDUSTRIES = [
    "Select Industry", "Airlines", "Automotive", "Consumer Goods", "E-commerce", 
    "Education", "Energy", "Finance", "Healthcare", "Hospitality", 
    "Logistics", "Other", "Pharma", "Retail", "Technology"
]

# Full API Configuration
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

# Utility Functions
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
1. Overall Complexity Level (High/Medium/Low)
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

def classify_complexity(overall_score):
    """Classify complexity level based on overall score"""
    if overall_score >= 4.0:
        return "High", "complexity-high"
    elif overall_score >= 3.0:
        return "Medium", "complexity-medium"
    else:
        return "Low", "complexity-low"

def extract_score_from_text(text, dimension):
    """Extract dimension score from hardness_summary API output"""
    if not text:
        return 0.0
    
    patterns = [
        rf"\*\*{dimension}\s+Score\*\*:\s*(\d+(?:\.\d+)?)\s*\/\s*5",
        rf"{dimension}:\s*(\d+(?:\.\d+)?)\s*\/\s*5",
        rf"\*\*{dimension}\*\*:\s*(\d+(?:\.\d+)?)",
        rf"{dimension}\s*[-\—]\s*(\d+(?:\.\d+)?)",
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
    
    return 3.0  # Default score

def extract_overall_score(text):
    """Calculate Overall Difficulty Score as average of all four dimension scores"""
    dimensions = ["Volatility", "Ambiguity", "Interconnectedness", "Uncertainty"]
    scores = []
    for dim in dimensions:
        score = extract_score_from_text(text, dim)
        if score > 0:
            scores.append(score)
    
    if len(scores) >= 2:
        return sum(scores) / len(scores)
    return 3.0

def extract_current_system_components(text):
    """Extract current system components"""
    if not text:
        return "No current system information available", "No input information available", "No output information available", "No pain points available"
    
    # Extract current system
    system_pattern = r'(?:###\s*Current\s*System|Current\s*System)[:\s]*(.*?)(?=###\s*Input|\*\*Input|\Z)'
    system_match = re.search(system_pattern, text, re.DOTALL | re.IGNORECASE)
    current_system = system_match.group(1).strip() if system_match else "No current system description found"
    
    # Extract input
    input_pattern = r'(?:###\s*Input|Input)[:\s]*(.*?)(?=###\s*Output|\*\*Output|\Z)'
    input_match = re.search(input_pattern, text, re.DOTALL | re.IGNORECASE)
    input_text = input_match.group(1).strip() if input_match else "No input information found"
    
    # Extract output
    output_pattern = r'(?:###\s*Output|Output)[:\s]*(.*?)(?=###\s*Pain|\*\*Pain|\Z)'
    output_match = re.search(output_pattern, text, re.DOTALL | re.IGNORECASE)
    output_text = output_match.group(1).strip() if output_match else "No output information found"
    
    # Extract pain points
    pain_pattern = r'(?:###\s*Pain|Pain)[:\s]*(.*?)(?=###|\*\*[A-Z]|\Z)'
    pain_match = re.search(pain_pattern, text, re.DOTALL | re.IGNORECASE)
    pain_points = pain_match.group(1).strip() if pain_match else "No pain points found"
    
    return current_system, input_text, output_text, pain_points

def extract_summary(text):
    """Extract summary section"""
    if not text:
        return "No summary available"
    
    summary_patterns = [
        r'\*\*Summary[:\s]*(.*?)(?=\*\*|\Z)',
        r'Summary[:\s]*(.*?)(?=###|\Z)',
        r'Key\s+Takeaway[s]?[:\s]*(.*?)(?=###|\Z)'
    ]
    
    for pattern in summary_patterns:
        match = re.search(pattern, text, re.DOTALL | re.IGNORECASE)
        if match:
            return match.group(1).strip()
    
    return "No summary section found"

# Session State Management
def init_session_state():
    defaults = {
        "current_page": "analyzer",
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
        "complexity_level": "Low",
        "complexity_class": "complexity-low",
        "overall_score": 0.0,
        "summary": "",
        "current_system_full": "",
        "input_text": "",
        "output_text": "",
        "pain_points_text": "",
        "hardness_summary_text": ""
    }
    
    for key, default_value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = default_value

init_session_state()

# Main Application
if st.session_state.current_page == "analyzer":
    # Header
    st.markdown("""
    <div class="app-header">
        <div class="app-title">Problem Complexity Analyzer</div>
        <div class="app-subtitle">Comprehensive analysis of business problem complexity across multiple dimensions</div>
    </div>
    """, unsafe_allow_html=True)
    
    # Input Section
    with st.container():
        st.markdown('<div class="analysis-card">', unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        with col1:
            st.session_state.industry = st.selectbox(
                "Industry Domain",
                INDUSTRIES,
                index=INDUSTRIES.index(st.session_state.industry)
            )
        with col2:
            st.session_state.account = st.selectbox(
                "Business Account",
                ACCOUNTS,
                index=ACCOUNTS.index(st.session_state.account)
            )
        
        st.session_state.problem_text = st.text_area(
            "Describe Your Business Challenge",
            value=st.session_state.problem_text,
            height=150,
            placeholder="Provide a detailed description of the business problem, including context, challenges, and desired outcomes..."
        )
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Analysis Button
    analyze_col, _ = st.columns([1, 3])
    with analyze_col:
        analyze_btn = st.button(
            "🚀 Analyze Complexity",
            type="primary",
            use_container_width=True,
            disabled=not (st.session_state.problem_text.strip() and 
                         st.session_state.industry != "Select Industry" and 
                         st.session_state.account != "Select Account")
        )
    
    if analyze_btn:
        with st.spinner("Conducting comprehensive analysis..."):
            progress_bar = st.progress(0)
            st.session_state.outputs = {}
            
            # Process all APIs
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
            st.session_state.hardness_summary_text = hardness_summary
            
            # Extract dimension scores
            dimension_scores_list = []
            for dimension in ["Volatility", "Ambiguity", "Interconnectedness", "Uncertainty"]:
                score = extract_score_from_text(hardness_summary, dimension)
                st.session_state.dimension_scores[dimension] = score
                dimension_scores_list.append(score)
            
            # Calculate overall score
            st.session_state.overall_score = sum(dimension_scores_list) / len(dimension_scores_list)
            
            # Classify complexity
            complexity_level, complexity_class = classify_complexity(st.session_state.overall_score)
            st.session_state.complexity_level = complexity_level
            st.session_state.complexity_class = complexity_class
            
            # Extract summary
            st.session_state.summary = extract_summary(hardness_summary)
            
            # Extract current system components
            current_system_text = st.session_state.outputs.get('current_system', '')
            (st.session_state.current_system_full, 
             st.session_state.input_text, 
             st.session_state.output_text, 
             st.session_state.pain_points_text) = extract_current_system_components(current_system_text)
            
            st.session_state.analysis_complete = True
            st.success("Comprehensive analysis complete!")
    
    # Display Results
    if st.session_state.analysis_complete:
        st.markdown("---")
        
        # Complexity Overview
        col1, col2 = st.columns([2, 1])
        
        with col1:
            st.markdown(f"""
            <div class="{st.session_state.complexity_class} complexity-badge">
                {st.session_state.complexity_level} Complexity
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown(f"""
            <div class="analysis-card" style="text-align: center;">
                <div style="font-size: 0.9rem; color: #adb5bd; margin-bottom: 0.5rem;">Overall Score</div>
                <div style="font-size: 2.5rem; font-weight: 700; color: #ffd700;">{st.session_state.overall_score:.1f}/5.0</div>
            </div>
            """, unsafe_allow_html=True)
        
        # Dimension Meters
        st.markdown("### Complexity Dimensions")
        
        for dimension, score in st.session_state.dimension_scores.items():
            fill_class = "fill-high" if score >= 4.0 else "fill-medium" if score >= 3.0 else "fill-low"
            
            st.markdown(f"""
            <div class="dimension-meter">
                <div class="meter-header">
                    <div class="meter-label">{dimension}</div>
                    <div class="meter-value">{score:.1f}/5.0</div>
                </div>
                <div class="meter-bar">
                    <div class="meter-fill {fill_class}" style="width: {score * 20}%;"></div>
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        # Detailed Analysis Sections
        st.markdown("---")
        
        # Vocabulary Section
        with st.expander("📚 Vocabulary Analysis", expanded=False):
            vocab_text = st.session_state.outputs.get('vocabulary', 'No vocabulary analysis available.')
            st.markdown(f'<div class="content-box">{vocab_text}</div>', unsafe_allow_html=True)
        
        # Current System Section
        with st.expander("🔄 Current System Analysis", expanded=False):
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("#### Current System")
                st.markdown(f'<div class="content-box">{st.session_state.current_system_full}</div>', unsafe_allow_html=True)
                
                st.markdown("#### Inputs")
                st.markdown(f'<div class="content-box">{st.session_state.input_text}</div>', unsafe_allow_html=True)
            
            with col2:
                st.markdown("#### Outputs")
                st.markdown(f'<div class="content-box">{st.session_state.output_text}</div>', unsafe_allow_html=True)
                
                st.markdown("#### Pain Points")
                st.markdown(f'<div class="content-box">{st.session_state.pain_points_text}</div>', unsafe_allow_html=True)
        
        # Summary Section
        with st.expander("📊 Executive Summary", expanded=True):
            st.markdown(f'<div class="highlight-box">{st.session_state.summary}</div>', unsafe_allow_html=True)
        
        # Detailed Q&A Analysis
        with st.expander("🔍 Detailed Dimension Analysis", expanded=False):
            for dimension, questions in DIMENSION_QUESTIONS.items():
                st.markdown(f"#### {dimension} Analysis")
                for q_name in questions:
                    q_config = next((cfg for cfg in API_CONFIGS if cfg["name"] == q_name), None)
                    if q_config and q_name in st.session_state.outputs:
                        st.markdown(f"**{q_config.get('question', 'Question')}**")
                        st.markdown(f'<div class="content-box">{st.session_state.outputs[q_name]}</div>', unsafe_allow_html=True)
        
        # Action Buttons
        col1, col2 = st.columns(2)
        with col1:
            if st.button("🔄 Analyze New Problem", use_container_width=True):
                for key in ["problem_text", "outputs", "analysis_complete", "dimension_scores", 
                           "overall_score", "summary", "current_system_full", "input_text", 
                           "output_text", "pain_points_text", "hardness_summary_text"]:
                    if key in st.session_state:
                        del st.session_state[key]
                st.rerun()
        
        with col2:
            if st.button("💡 View Recommendations", use_container_width=True):
                st.session_state.current_page = "recommendations"
                st.rerun()

# Recommendations Page
elif st.session_state.current_page == "recommendations":
    st.markdown("""
    <div class="app-header">
        <div class="app-title">Complexity Recommendations</div>
        <div class="app-subtitle">Tailored suggestions based on your comprehensive problem analysis</div>
    </div>
    """, unsafe_allow_html=True)
    
    if st.button("← Back to Analyzer", use_container_width=False):
        st.session_state.current_page = "analyzer"
        st.rerun()
    
    # Generate recommendations based on complexity
    complexity = st.session_state.complexity_level
    scores = st.session_state.dimension_scores
    
    recommendations = {
        "High": [
            "Break down into smaller, manageable sub-problems with clear ownership",
            "Implement phased approach with clear milestones and review points",
            "Engage cross-functional expertise early in the process",
            "Establish robust risk mitigation and contingency strategies",
            "Allocate additional resources and buffer time for uncertainties",
            "Implement rigorous change control and version management",
            "Establish frequent stakeholder communication cycles"
        ],
        "Medium": [
            "Define clear success metrics and key performance indicators",
            "Establish regular progress review and adjustment cycles",
            "Document all assumptions, constraints, and dependencies clearly",
            "Implement iterative development with frequent validation",
            "Maintain continuous stakeholder alignment and feedback",
            "Use agile methodologies with short sprint cycles",
            "Establish clear escalation paths for issues"
        ],
        "Low": [
            "Proceed with standard project management best practices",
            "Focus on efficient execution and timely delivery",
            "Maintain clear and open communication channels",
            "Document lessons learned for process improvement",
            "Celebrate quick wins and milestone achievements",
            "Establish basic monitoring and reporting mechanisms",
            "Focus on quality assurance and user acceptance"
        ]
    }
    
    st.markdown(f'<div class="analysis-card">', unsafe_allow_html=True)
    st.markdown(f"### 🎯 Strategic Recommendations for {complexity} Complexity Problems")
    
    for i, recommendation in enumerate(recommendations.get(complexity, []), 1):
        st.markdown(f"**{i}.** {recommendation}")
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Dimension-specific recommendations
    high_dimensions = [dim for dim, score in scores.items() if score >= 4.0]
    if high_dimensions:
        st.markdown('<div class="analysis-card">', unsafe_allow_html=True)
        st.markdown("### 🚨 High Priority Focus Areas")
        
        dimension_advice = {
            "Volatility": [
                "Implement flexible architectures that can adapt to changes",
                "Use adaptive planning with regular reassessment cycles",
                "Establish early warning systems for market changes",
                "Build modular systems with loose coupling"
            ],
            "Ambiguity": [
                "Conduct stakeholder workshops to align on definitions",
                "Create clear requirement documentation with examples",
                "Establish a glossary of terms and concepts",
                "Use prototyping to clarify ambiguous requirements"
            ],
            "Interconnectedness": [
                "Create comprehensive dependency mapping",
                "Establish clear interfaces and integration points",
                "Implement robust error handling and fallback mechanisms",
                "Use microservices architecture for complex systems"
            ],
            "Uncertainty": [
                "Develop multiple scenario plans and contingencies",
                "Implement phased rollouts with feedback loops",
                "Use pilot programs to test assumptions",
                "Establish metrics for uncertainty reduction"
            ]
        }
        
        for dim in high_dimensions:
            if dim in dimension_advice:
                st.markdown(f"#### {dim}")
                for advice in dimension_advice[dim]:
                    st.markdown(f"• {advice}")
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Success Metrics
    st.markdown('<div class="analysis-card">', unsafe_allow_html=True)
    st.markdown("### 📈 Success Metrics & Monitoring")
    
    success_metrics = {
        "High": [
            "Risk mitigation effectiveness (reduced high-risk items)",
            "Stakeholder satisfaction with communication",
            "Milestone achievement rate",
            "Change request handling efficiency",
            "Team velocity and predictability"
        ],
        "Medium": [
            "Project timeline adherence",
            "Budget compliance",
            "Quality metrics (defect rates, etc.)",
            "Stakeholder feedback scores",
            "Requirement stability index"
        ],
        "Low": [
            "On-time delivery",
            "Within-budget performance",
            "User acceptance rates",
            "Post-implementation satisfaction",
            "Process efficiency metrics"
        ]
    }
    
    st.markdown("**Key metrics to track:**")
    for metric in success_metrics.get(complexity, []):
        st.markdown(f"• {metric}")
    
    st.markdown('</div>', unsafe_allow_html=True)