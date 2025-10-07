import streamlit as st
import requests, json, os, re, time
import hashlib
from datetime import datetime, timedelta
from io import BytesIO
import unicodedata
import pandas as pd

# ---------------------------
# Page config
# ---------------------------
st.set_page_config(
    page_title="Problem Complexity Analyzer",
    page_icon="🔍",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ---------------------------
# Theme Toggle in Session State
# ---------------------------
if 'dark_mode' not in st.session_state:
    st.session_state.dark_mode = True

# ---------------------------
# Enhanced Creative Styles with Light/Dark Mode Toggle
# ---------------------------
if st.session_state.dark_mode:
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@300;400;500;600;700&family=Inter:wght@300;400;500;600;700&family=Orbitron:wght@400;500;700;900&family=Poppins:wght@300;400;500;600;700;800;900&display=swap');

    * {
        font-family: 'Poppins', sans-serif;
    }

    .main {
        background: linear-gradient(135deg, #0f0f23 0%, #1a1a2e 50%, #16213e 100%);
        color: #ffffff;
    }

    .stApp { 
        background: linear-gradient(135deg, #0f0f23 0%, #1a1a2e 50%, #16213e 100%);
        background-attachment: fixed;
    }

    /* Text Colors with Better Contrast - FIXED FOR DARK MODE */
    .primary-text { color: #ffffff !important; }
    .secondary-text { color: #e0e0e0 !important; }
    .muted-text { color: #b8b8b8 !important; }
    .accent-text { color: #ffd700 !important; }

    /* White headings for all sections */
    .white-heading {
        color: #ffffff !important;
        font-weight: 700;
        margin-bottom: 1rem;
    }

    .section-header-white {
        color: #ffffff !important;
        font-size: 1.8rem;
        font-weight: 700;
        margin-bottom: 1.5rem;
        border-bottom: 2px solid rgba(255, 193, 7, 0.3);
        padding-bottom: 0.5rem;
    }

    /* Animated Background Elements */
    .background-elements {
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        z-index: -1;
        overflow: hidden;
    }

    .floating-shape {
        position: absolute;
        background: rgba(255, 193, 7, 0.1);
        border-radius: 50%;
        animation: float 20s infinite linear;
    }

    .shape-1 { width: 200px; height: 200px; top: 10%; left: 5%; animation-delay: 0s; }
    .shape-2 { width: 150px; height: 150px; top: 60%; left: 80%; animation-delay: -5s; }
    .shape-3 { width: 100px; height: 100px; top: 80%; left: 20%; animation-delay: -10s; }
    .shape-4 { width: 120px; height: 120px; top: 20%; left: 70%; animation-delay: -15s; }

    @keyframes float {
        0%, 100% { transform: translateY(0px) rotate(0deg); }
        33% { transform: translateY(-30px) rotate(120deg); }
        66% { transform: translateY(30px) rotate(240deg); }
    }

    /* Header with Glass Morphism */
    .app-header {
        background: rgba(255, 255, 255, 0.08);
        backdrop-filter: blur(20px);
        border: 1px solid rgba(255, 255, 255, 0.1);
        padding: 2rem;
        border-radius: 24px;
        margin-bottom: 2rem;
        text-align: center;
        position: relative;
        overflow: hidden;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
    }

    .app-header::before {
        content: '';
        position: absolute;
        top: 0;
        left: -100%;
        width: 100%;
        height: 100%;
        background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.1), transparent);
        transition: 0.5s;
    }

    .app-header:hover::before {
        left: 100%;
    }

    .app-title { 
        font-size: 3.5rem; 
        font-weight: 900;
        font-family: 'Orbitron', sans-serif;
        background: linear-gradient(45deg, #ffd700, #ff8c00, #ff6b6b, #4ecdc4);
        background-size: 300% 300%;
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        animation: gradientShift 3s ease infinite;
        text-shadow: 0 0 30px rgba(255, 215, 0, 0.3);
        margin-bottom: 0.5rem;
    }

    .app-sub { 
        font-size: 1.3rem;
        color: #e0e0e0 !important;
        opacity: 0.95;
        font-weight: 400;
        letter-spacing: 1px;
        text-shadow: 0 1px 2px rgba(0,0,0,0.5);
        line-height: 1.4;
        white-space: normal !important;
        word-wrap: break-word !important;
    }

    @keyframes gradientShift {
        0%, 100% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
    }

    /* Three info boxes with hover effects */
    .info-box { 
        background: rgba(255,255,255,0.05); 
        border-radius: 20px; 
        padding: 2rem;
        border: 1px solid rgba(255,255,255,0.1);
        transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
        position: relative;
        overflow: hidden;
        height: 100%;
    }

    .info-box::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background: linear-gradient(135deg, rgba(255,215,0,0.1), rgba(255,140,0,0.05));
        opacity: 0;
        transition: opacity 0.4s ease;
    }

    .info-box:hover {
        transform: translateY(-10px) scale(1.02);
        box-shadow: 0 20px 40px rgba(0,0,0,0.4);
        border-color: rgba(255,193,7,0.3);
    }

    .info-box:hover::before {
        opacity: 1;
    }

    .info-emoji { 
        font-size: 2.5rem; 
        margin-bottom: 1rem;
        display: block;
        text-align: center;
    }

    .info-box strong {
        color: #ffffff !important;
        font-size: 1.2rem;
        display: block;
        margin-bottom: 0.5rem;
    }

    /* Analysis card with neon glow */
    .analysis-card { 
        background: rgba(255,255,255,0.03); 
        padding: 2.5rem;
        border-radius: 24px; 
        border: 1px solid rgba(255,255,255,0.1);
        box-shadow: 0 8px 32px rgba(0,0,0,0.2);
        position: relative;
        overflow: hidden;
    }

    .analysis-card::after {
        content: '';
        position: absolute;
        top: -2px;
        left: -2px;
        right: -2px;
        bottom: -2px;
        background: linear-gradient(45deg, #ffd700, #ff8c00, transparent);
        border-radius: 25px;
        z-index: -1;
        opacity: 0;
        transition: opacity 0.4s ease;
    }

    .analysis-card:hover::after {
        opacity: 0.3;
    }

    /* Colored classification boxes with animations */
    .box-easy { 
        background: linear-gradient(135deg,#d4edda,#c3e6cb);
        color:#034214 !important;
        padding: 1.5rem;
        border-radius: 16px; 
        border: none;
        box-shadow: 0 8px 25px rgba(34, 197, 94, 0.3);
        animation: pulse-glow 2s infinite;
    }

    .box-moderate { 
        background: linear-gradient(135deg,#fff3cd,#ffe8a1);
        color:#665200 !important;
        padding: 1.5rem;
        border-radius: 16px; 
        border: none;
        box-shadow: 0 8px 25px rgba(245, 158, 11, 0.3);
        animation: pulse-glow 2s infinite;
    }

    .box-hard { 
        background: linear-gradient(135deg,#f8d7da,#f1b0b7);
        color:#66101a !important;
        padding: 1.5rem;
        border-radius: 16px; 
        border: none;
        box-shadow: 0 8px 25px rgba(239, 68, 68, 0.3);
        animation: pulse-glow 2s infinite;
    }

    @keyframes pulse-glow {
        0%, 100% { box-shadow: 0 8px 25px rgba(255, 215, 0, 0.3); }
        50% { box-shadow: 0 12px 35px rgba(255, 215, 0, 0.5); }
    }

    /* Dimension boxes with 3D effect - UPDATED COLORS */
    .dimension-box {
        border-radius: 20px;
        padding: 2rem;
        border: 1px solid rgba(255,255,255,0.1);
        transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
        height: 100%;
        position: relative;
        overflow: hidden;
        backdrop-filter: blur(10px);
    }

    .dimension-box::before {
        content: '';
        position: absolute;
        top: 0;
        left: -100%;
        width: 100%;
        height: 100%;
        background: linear-gradient(90deg, transparent, rgba(255,255,255,0.1), transparent);
        transition: 0.6s;
    }

    .dimension-box:hover::before {
        left: 100%;
    }

    .dimension-box:hover {
        transform: translateY(-15px) scale(1.03);
        box-shadow: 0 25px 50px rgba(0,0,0,0.5);
        border-color: rgba(255,193,7,0.4);
    }

    /* Volatility Box - Red Theme */
    .volatility-box {
        background: linear-gradient(135deg, rgba(239, 68, 68, 0.15), rgba(185, 28, 28, 0.1));
        border-left: 6px solid #ef4444;
    }

    /* Ambiguity Box - Purple Theme */
    .ambiguity-box {
        background: linear-gradient(135deg, rgba(147, 51, 234, 0.15), rgba(126, 34, 206, 0.1));
        border-left: 6px solid #9333ea;
    }

    /* Interconnectedness Box - Blue Theme */
    .interconnectedness-box {
        background: linear-gradient(135deg, rgba(59, 130, 246, 0.15), rgba(37, 99, 235, 0.1));
        border-left: 6px solid #3b82f6;
    }

    /* Uncertainty Box - Orange Theme */
    .uncertainty-box {
        background: linear-gradient(135deg, rgba(249, 115, 22, 0.15), rgba(234, 88, 12, 0.1));
        border-left: 6px solid #f97316;
    }

    .dimension-title {
        font-size: 1.4rem;
        font-weight: 700;
        margin-bottom: 1rem;
        text-align: center;
        background: linear-gradient(45deg, #ffffff, #e0e0e0);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-family: 'Orbitron', sans-serif;
        text-shadow: 0 0 10px rgba(255,255,255,0.3);
    }

    .dimension-score {
        font-size: 2.5rem;
        font-weight: 900;
        text-align: center;
        margin: 1.5rem 0;
        background: linear-gradient(45deg, #ffffff, #e0e0e0);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-shadow: 0 0 20px rgba(255,255,255,0.3);
    }

    /* Enhanced buttons */
    .stButton > button {
        border-radius: 12px !important;
        padding: 12px 24px !important;
        font-weight: 600 !important;
        border: none !important;
        transition: all 0.3s cubic-bezier(0.175, 0.885, 0.32, 1.275) !important;
        position: relative;
        overflow: hidden;
    }

    .stButton > button::before {
        content: '';
        position: absolute;
        top: 0;
        left: -100%;
        width: 100%;
        height: 100%;
        background: linear-gradient(90deg, transparent, rgba(255,255,255,0.2), transparent);
        transition: 0.5s;
    }

    .stButton > button:hover::before {
        left: 100%;
    }

    .stButton > button:hover {
        transform: translateY(-3px) scale(1.05);
        box-shadow: 0 10px 25px rgba(0,0,0,0.3);
    }

    /* Primary button */
    .stButton > button[kind="primary"] {
        background: linear-gradient(135deg, #ffd700, #ff8c00) !important;
        color: #000000 !important;
        font-weight: 700 !important;
    }

    .stButton > button[kind="primary"]:hover {
        box-shadow: 0 15px 30px rgba(255, 193, 7, 0.4) !important;
    }

    /* Secondary button */
    .stButton > button[kind="secondary"] {
        background: linear-gradient(135deg, #6c757d, #495057) !important;
        color: white !important;
    }

    /* Current System Display */
    .system-display {
        background: linear-gradient(135deg, rgba(255,255,255,0.03), rgba(255,255,255,0.01));
        border-radius: 20px;
        padding: 2rem;
        border: 1px solid rgba(255,255,255,0.1);
        margin: 2rem 0;
        backdrop-filter: blur(10px);
        box-shadow: 0 8px 32px rgba(0,0,0,0.2);
    }

    .system-section {
        margin-bottom: 2rem;
        padding: 1.5rem;
        background: rgba(255,255,255,0.02);
        border-radius: 16px;
        border-left: 4px solid #ffc107;
        transition: all 0.3s ease;
    }

    .system-section:hover {
        background: rgba(255,255,255,0.05);
        transform: translateX(10px);
    }

    .system-section h4 {
        color: #ffffff !important;
        margin-bottom: 1rem;
        border-bottom: 2px solid rgba(255,255,255,0.1);
        padding-bottom: 0.5rem;
        font-family: 'Orbitron', sans-serif;
        font-weight: 600;
    }

    .system-section p, .system-section div {
        color: #e0e0e0 !important;
        line-height: 1.6;
    }

    /* Question Display - UPDATED FOR WHITE TEXT */
    .question-card {
        background: linear-gradient(135deg, rgba(255,255,255,0.03), rgba(255,255,255,0.01));
        border-radius: 16px;
        padding: 1.5rem;
        margin: 1rem 0;
        border-left: 6px solid #ffc107;
        box-shadow: 0 4px 20px rgba(0,0,0,0.1);
        transition: all 0.3s ease;
        backdrop-filter: blur(5px);
    }

    .question-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 8px 30px rgba(255, 193, 7, 0.2);
    }

    .question-card strong {
        color: #ffffff !important;
        font-size: 1.1rem;
        display: block;
        margin-bottom: 1rem;
    }

    .question-card p, .question-card div {
        color: #e0e0e0 !important;
        line-height: 1.6;
    }

    /* Progress bar styling */
    .stProgress > div > div > div {
        background: linear-gradient(90deg, #ffd700, #ff8c00) !important;
        border-radius: 10px !important;
    }

    /* Select box styling */
    .stSelectbox > div > div {
        background: #000000 !important;
        border: 1px solid rgba(255,255,255,0.3) !important;
        border-radius: 12px !important;
        color: white !important;
    }

    .stSelectbox > div > div:hover {
        border-color: #ffc107 !important;
        background: #111111 !important;
    }

    .stSelectbox label {
        color: #ffffff !important;
        font-weight: 600;
    }

    /* Text area styling - UPDATED WITH BLACK BACKGROUND */
    .stTextArea > div > div > textarea {
        background: #000000 !important;
        border: 1px solid rgba(255,255,255,0.3) !important;
        border-radius: 16px !important;
        color: #ffffff !important;
        padding: 1rem !important;
        font-size: 1rem !important;
        transition: all 0.3s ease !important;
    }

    .stTextArea > div > div > textarea:focus {
        border-color: #ffc107 !important;
        box-shadow: 0 0 0 2px rgba(255, 193, 7, 0.2) !important;
        background: #111111 !important;
    }

    .stTextArea > div > div > textarea::placeholder {
        color: #b0b0b0 !important;
        opacity: 0.8;
    }

    .stTextArea label {
        color: #ffffff !important;
        font-weight: 600;
    }

    /* Expander styling */
    .streamlit-expanderHeader {
        background: rgba(255,255,255,0.03) !important;
        border-radius: 12px !important;
        border: 1px solid rgba(255,255,255,0.1) !important;
        font-weight: 600 !important;
        color: #ffffff !important;
    }

    .streamlit-expanderContent {
        background: rgba(255,255,255,0.02) !important;
        border-radius: 0 0 12px 12px !important;
    }

    .streamlit-expanderContent p, .streamlit-expanderContent div {
        color: #e0e0e0 !important;
        line-height: 1.6;
    }

    /* Small helpers */
    .small-muted { 
        color: #b8b8b8 !important;
        font-size: 0.9rem; 
        line-height: 1.4;
    }

    .medium-text {
        color: #e0e0e0 !important;
        font-size: 1rem;
        line-height: 1.5;
    }

    .large-text {
        color: #ffffff !important;
        font-size: 1.1rem;
        line-height: 1.6;
    }

    /* Floating action button */
    .floating-btn {
        position: fixed;
        bottom: 30px;
        right: 30px;
        z-index: 1000;
        background: linear-gradient(135deg, #ffd700, #ff8c00);
        border: none;
        border-radius: 50%;
        width: 60px;
        height: 60px;
        color: black !important;
        font-size: 1.5rem;
        cursor: pointer;
        box-shadow: 0 8px 25px rgba(255, 193, 7, 0.4);
        transition: all 0.3s ease;
        display: flex;
        align-items: center;
        justify-content: center;
    }

    .floating-btn:hover {
        transform: scale(1.1) rotate(90deg);
        box-shadow: 0 12px 35px rgba(255, 193, 7, 0.6);
    }

    /* Particle background */
    .particles {
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        z-index: -2;
        overflow: hidden;
    }

    .particle {
        position: absolute;
        background: rgba(255, 215, 0, 0.3);
        border-radius: 50%;
        animation: float-particle 15s infinite linear;
    }

    @keyframes float-particle {
        0% { transform: translateY(100vh) rotate(0deg); opacity: 0; }
        10% { opacity: 1; }
        90% { opacity: 1; }
        100% { transform: translateY(-100px) rotate(360deg); opacity: 0; }
    }

    /* Custom scrollbar */
    ::-webkit-scrollbar {
        width: 8px;
    }

    ::-webkit-scrollbar-track {
        background: rgba(255,255,255,0.05);
        border-radius: 10px;
    }

    ::-webkit-scrollbar-thumb {
        background: linear-gradient(135deg, #ffd700, #ff8c00);
        border-radius: 10px;
    }

    ::-webkit-scrollbar-thumb:hover {
        background: linear-gradient(135deg, #ff8c00, #ff6b6b);
    }

    /* Typewriter effect */
    .typewriter {
        overflow: hidden;
        border-right: 3px solid #ffc107;
        white-space: nowrap;
        margin: 0 auto;
        animation: typing 3.5s steps(40, end), blink-caret 0.75s step-end infinite;
    }

    @keyframes typing {
        from { width: 0 }
        to { width: 100% }
    }

    @keyframes blink-caret {
        from, to { border-color: transparent }
        50% { border-color: #ffc107 }
    }

    /* Glow text */
    .glow-text {
        text-shadow: 0 0 10px currentColor, 0 0 20px currentColor, 0 0 30px currentColor;
    }

    /* Warning and Info messages */
    .stAlert {
        border-radius: 12px !important;
    }

    .stWarning {
        background: rgba(255, 193, 7, 0.1) !important;
        border: 1px solid rgba(255, 193, 7, 0.3) !important;
        color: #ffd700 !important;
    }

    .stInfo {
        background: rgba(33, 150, 243, 0.1) !important;
        border: 1px solid rgba(33, 150, 243, 0.3) !important;
        color: #4fc3f7 !important;
    }

    /* Card content styling */
    .card-content {
        color: #e0e0e0 !important;
        line-height: 1.6;
        font-size: 1rem;
    }

    .highlight-text {
        color: #ffd700 !important;
        font-weight: 600;
    }

    /* Section headers */
    .section-header {
        color: #ffffff !important;
        font-size: 1.8rem;
        font-weight: 700;
        margin-bottom: 1.5rem;
        border-bottom: 2px solid rgba(255, 193, 7, 0.3);
        padding-bottom: 0.5rem;
    }

    .sub-section-header {
        color: #ffd700 !important;
        font-size: 1.3rem;
        font-weight: 600;
        margin: 1.5rem 0 1rem 0;
    }

    /* Summary section styling */
    .summary-section {
        background: linear-gradient(135deg, rgba(255,255,255,0.03), rgba(255,255,255,0.01));
        border-radius: 20px;
        padding: 2rem;
        border: 1px solid rgba(255,255,255,0.1);
        margin: 2rem 0;
        backdrop-filter: blur(10px);
    }

    .summary-item {
        background: rgba(255,255,255,0.02);
        border-radius: 12px;
        padding: 1.5rem;
        margin: 1rem 0;
        border-left: 4px solid #ffc107;
    }

    .takeaway-item {
        background: rgba(255,255,255,0.02);
        border-radius: 12px;
        padding: 1.5rem;
        margin: 1rem 0;
        border-left: 4px solid #4ecdc4;
    }

    /* Input field styling for better visibility */
    .input-dark {
        background: #000000 !important;
        color: #ffffff !important;
        border: 1px solid rgba(255,255,255,0.3) !important;
    }

    .input-dark:focus {
        background: #111111 !important;
        border-color: #ffc107 !important;
    }

    /* White text for all questions */
    .question-text-white {
        color: #ffffff !important;
        font-weight: 600;
        font-size: 1.1rem;
        line-height: 1.5;
    }

    /* Theme Toggle Container */
    .theme-toggle-container {
        position: fixed;
        top: 20px;
        right: 20px;
        z-index: 1000;
        background: rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(10px);
        border-radius: 12px;
        padding: 10px;
        border: 1px solid rgba(255, 255, 255, 0.2);
    }
                

    /* Radio button styling for dark mode - WHITE TEXT */
    .stRadio > div {
        flex-direction: row !important;
        gap: 10px !important;
    }

    .stRadio > div > label {
        margin-bottom: 0 !important;
        padding: 8px 12px !important;
        border-radius: 8px !important;
        border: 1px solid rgba(255, 255, 255, 0.3) !important;
        background: rgba(255, 255, 255, 0.1) !important;
        transition: all 0.3s ease !important;
        color: #ffffff !important; /* WHITE TEXT for dark mode */
        white-space: nowrap !important;
    }

    .stRadio > div > label:hover {
        border-color: #ffd700 !important;
        background: rgba(255, 215, 0, 0.1) !important;
    }

    .stRadio > div > label[data-testid="stRadio"] {
        background: linear-gradient(135deg, #ffd700, #ff8c00) !important;
        color: #000000 !important;
        border-color: #ffd700 !important;
        font-weight: 600 !important;
    }

    /* Hide empty content */
    .empty-content {
        display: none !important;
    }

    /* Back button styling - FIXED FOR SINGLE LINE */
    .back-button {
        background: linear-gradient(135deg, #6c757d, #495057) !important;
        color: white !important;
        border-radius: 12px !important;
        padding: 10px 20px !important;
        font-weight: 600 !important;
        border: none !important;
        transition: all 0.3s ease !important;
        white-space: nowrap !important;
        min-width: 150px !important;
        overflow: hidden !important;
        text-overflow: ellipsis !important;
    }

    .back-button:hover {
        transform: translateY(-2px);
        box-shadow: 0 5px 15px rgba(0,0,0,0.3);
    }

    /* Dimension detail navigation */
    .dimension-nav {
        display: flex;
        justify-content: space-between;
        margin: 2rem 0;
        gap: 1rem;
    }

    /* Enhanced colorful boxes for dimensions */
    .dimension-detail-box {
        border-radius: 20px;
        padding: 2.5rem;
        margin: 1rem 0;
        border: 1px solid rgba(255,255,255,0.2);
        transition: all 0.4s ease;
        position: relative;
        overflow: hidden;
    }

    .dimension-detail-box::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background: linear-gradient(135deg, rgba(255,255,255,0.1), transparent);
        opacity: 0;
        transition: opacity 0.4s ease;
    }

    .dimension-detail-box:hover::before {
        opacity: 1;
    }

    .volatility-detail {
        background: linear-gradient(135deg, rgba(239, 68, 68, 0.25), rgba(185, 28, 28, 0.15));
        border-left: 8px solid #ef4444;
        box-shadow: 0 10px 30px rgba(239, 68, 68, 0.2);
    }

    .ambiguity-detail {
        background: linear-gradient(135deg, rgba(147, 51, 234, 0.25), rgba(126, 34, 206, 0.15));
        border-left: 8px solid #9333ea;
        box-shadow: 0 10px 30px rgba(147, 51, 234, 0.2);
    }

    .interconnectedness-detail {
        background: linear-gradient(135deg, rgba(59, 130, 246, 0.25), rgba(37, 99, 235, 0.15));
        border-left: 8px solid #3b82f6;
        box-shadow: 0 10px 30px rgba(59, 130, 246, 0.2);
    }

    .uncertainty-detail {
        background: linear-gradient(135deg, rgba(249, 115, 22, 0.25), rgba(234, 88, 12, 0.15));
        border-left: 8px solid #f97316;
        box-shadow: 0 10px 30px rgba(249, 115, 22, 0.2);
    }

    /* Dark mode specific score styling */
    .dark-score {
        font-size: 4rem;
        font-weight: 900;
        text-align: center;
        margin: 1.5rem 0;
        background: linear-gradient(45deg, #ffffff, #e0e0e0);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-shadow: 0 0 20px rgba(255,255,255,0.3);
    }

    /* FIX FOR DARK MODE TEXT COLORS */
    .stMarkdown, .stText, .stCaption {
        color: #ffffff !important;
    }
    
    .stSelectbox > div > div > div {
        color: #ffffff !important;
    }
    
    .stTextInput > div > div > input {
        color: #ffffff !important;
    }
    
    .stNumberInput > div > div > input {
        color: #ffffff !important;
    }
    
    .stTextArea > div > div > textarea {
        color: #ffffff !important;
    }
    
    div[data-testid="stExpander"] div {
        color: #ffffff !important;
    }
    </style>
    """, unsafe_allow_html=True)
else:
    # LIGHT MODE STYLES
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@300;400;500;600;700&family=Inter:wght@300;400;500;600;700&family=Orbitron:wght@400;500;700;900&family=Poppins:wght@300;400;500;600;700;800;900&display=swap');

    * {
        font-family: 'Poppins', sans-serif;
    }

    .main {
        background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 50%, #dee2e6 100%);
        color: #333333;
    }

    .stApp { 
        background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 50%, #dee2e6 100%);
        background-attachment: fixed;
    }

    /* Text Colors for Light Mode */
    .primary-text { color: #333333 !important; }
    .secondary-text { color: #555555 !important; }
    .muted-text { color: #777777 !important; }
    .accent-text { color: #ff6b00 !important; }

    /* Headings for Light Mode */
    .white-heading {
        color: #333333 !important;
        font-weight: 700;
        margin-bottom: 1rem;
    }

    .section-header-white {
        color: #333333 !important;
        font-size: 1.8rem;
        font-weight: 700;
        margin-bottom: 1.5rem;
        border-bottom: 2px solid rgba(255, 107, 0, 0.3);
        padding-bottom: 0.5rem;
    }

    /* Header with Light Glass Morphism */
    .app-header {
        background: rgba(255, 255, 255, 0.8);
        backdrop-filter: blur(20px);
        border: 1px solid rgba(0, 0, 0, 0.1);
        padding: 2rem;
        border-radius: 24px;
        margin-bottom: 2rem;
        text-align: center;
        position: relative;
        overflow: hidden;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
    }

    .app-title { 
        font-size: 3.5rem; 
        font-weight: 900;
        font-family: 'Orbitron', sans-serif;
        background: linear-gradient(45deg, #ff6b00, #ff8c00, #ff5252, #4ecdc4);
        background-size: 300% 300%;
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        animation: gradientShift 3s ease infinite;
        margin-bottom: 0.5rem;
    }

    .app-sub { 
        font-size: 1.3rem;
        color: #555555 !important;
        opacity: 0.95;
        font-weight: 400;
        letter-spacing: 1px;
        line-height: 1.4;
        white-space: normal !important;
        word-wrap: break-word !important;
    }

    @keyframes gradientShift {
        0%, 100% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
    }

    /* Info boxes for Light Mode */
    .info-box { 
        background: rgba(255, 255, 255, 0.7); 
        border-radius: 20px; 
        padding: 2rem;
        border: 1px solid rgba(0, 0, 0, 0.1);
        transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
        position: relative;
        overflow: hidden;
        height: 100%;
    }

    .info-box:hover {
        transform: translateY(-10px) scale(1.02);
        box-shadow: 0 20px 40px rgba(0,0,0,0.15);
        border-color: rgba(255, 107, 0, 0.3);
    }

    .info-emoji { 
        font-size: 2.5rem; 
        margin-bottom: 1rem;
        display: block;
        text-align: center;
    }

    .info-box strong {
        color: #333333 !important;
        font-size: 1.2rem;
        display: block;
        margin-bottom: 0.5rem;
    }

    /* Analysis card for Light Mode */
    .analysis-card { 
        background: rgba(255, 255, 255, 0.8); 
        padding: 2.5rem;
        border-radius: 24px; 
        border: 1px solid rgba(0, 0, 0, 0.1);
        box-shadow: 0 8px 32px rgba(0,0,0,0.1);
        position: relative;
        overflow: hidden;
    }

    /* Dimension boxes for Light Mode */
    .dimension-box {
        border-radius: 20px;
        padding: 2rem;
        border: 1px solid rgba(0, 0, 0, 0.1);
        transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
        height: 100%;
        position: relative;
        overflow: hidden;
        backdrop-filter: blur(10px);
        background: rgba(255, 255, 255, 0.7);
    }

    .dimension-box:hover {
        transform: translateY(-15px) scale(1.03);
        box-shadow: 0 25px 50px rgba(0,0,0,0.15);
    }

    /* Volatility Box - Red Theme */
    .volatility-box {
        background: linear-gradient(135deg, rgba(239, 68, 68, 0.1), rgba(255, 255, 255, 0.7));
        border-left: 6px solid #ef4444;
    }

    /* Ambiguity Box - Purple Theme */
    .ambiguity-box {
        background: linear-gradient(135deg, rgba(147, 51, 234, 0.1), rgba(255, 255, 255, 0.7));
        border-left: 6px solid #9333ea;
    }

    /* Interconnectedness Box - Blue Theme */
    .interconnectedness-box {
        background: linear-gradient(135deg, rgba(59, 130, 246, 0.1), rgba(255, 255, 255, 0.7));
        border-left: 6px solid #3b82f6;
    }

    /* Uncertainty Box - Orange Theme */
    .uncertainty-box {
        background: linear-gradient(135deg, rgba(249, 115, 22, 0.1), rgba(255, 255, 255, 0.7));
        border-left: 6px solid #f97316;
    }

    .dimension-title {
        font-size: 1.4rem;
        font-weight: 700;
        margin-bottom: 1rem;
        text-align: center;
        color: #333333 !important;
        font-family: 'Orbitron', sans-serif;
    }

    .dimension-score {
        font-size: 2.5rem;
        font-weight: 900;
        text-align: center;
        margin: 1.5rem 0;
        color: #333333 !important;
    }

    /* Buttons for Light Mode */
    .stButton > button {
        border-radius: 12px !important;
        padding: 12px 24px !important;
        font-weight: 600 !important;
        border: none !important;
        transition: all 0.3s cubic-bezier(0.175, 0.885, 0.32, 1.275) !important;
    }

    .stButton > button:hover {
        transform: translateY(-3px) scale(1.05);
        box-shadow: 0 10px 25px rgba(0,0,0,0.2);
    }

    .stButton > button[kind="primary"] {
        background: linear-gradient(135deg, #ff6b00, #ff8c00) !important;
        color: #ffffff !important;
        font-weight: 700 !important;
    }

    /* System Display for Light Mode */
    .system-display {
        background: rgba(255, 255, 255, 0.7);
        border-radius: 20px;
        padding: 2rem;
        border: 1px solid rgba(0, 0, 0, 0.1);
        margin: 2rem 0;
        backdrop-filter: blur(10px);
        box-shadow: 0 8px 32px rgba(0,0,0,0.1);
    }

    .system-section {
        margin-bottom: 2rem;
        padding: 1.5rem;
        background: rgba(255, 255, 255, 0.5);
        border-radius: 16px;
        border-left: 4px solid #ff6b00;
        transition: all 0.3s ease;
    }

    .system-section h4 {
        color: #333333 !important;
        margin-bottom: 1rem;
        border-bottom: 2px solid rgba(0, 0, 0, 0.1);
        padding-bottom: 0.5rem;
        font-family: 'Orbitron', sans-serif;
        font-weight: 600;
    }

    .system-section p, .system-section div {
        color: #555555 !important;
        line-height: 1.6;
    }

    /* Form elements for Light Mode */
    .stSelectbox > div > div {
        background: #ffffff !important;
        border: 1px solid #ced4da !important;
        border-radius: 12px !important;
        color: #333333 !important;
    }

    .stSelectbox label {
        color: #333333 !important;
        font-weight: 600;
    }

    .stTextArea > div > div > textarea {
        background: #ffffff !important;
        border: 1px solid #ced4da !important;
        border-radius: 16px !important;
        color: #333333 !important;
        padding: 1rem !important;
        font-size: 1rem !important;
    }

    .stTextArea label {
        color: #333333 !important;
        font-weight: 600;
    }

    /* Theme Toggle Container for Light Mode */
    .theme-toggle-container {
        position: fixed;
        top: 20px;
        right: 20px;
        z-index: 1000;
        background: rgba(255, 255, 255, 0.9);
        backdrop-filter: blur(10px);
        border-radius: 12px;
        padding: 10px;
        border: 1px solid rgba(0, 0, 0, 0.1);
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
    }

    /* Radio button styling for light mode */
    .stRadio > div {
        flex-direction: row !important;
        gap: 10px !important;
    }

    .stRadio > div > label {
        margin-bottom: 0 !important;
        padding: 8px 12px !important;
        border-radius: 8px !important;
        border: 1px solid #ddd !important;
        background: white !important;
        transition: all 0.3s ease !important;
        color: #333333 !important;
        white-space: nowrap !important;
    }

    .stRadio > div > label:hover {
        border-color: #ff6b00 !important;
        background: #f8f9fa !important;
    }

    .stRadio > div > label[data-testid="stRadio"] {
        background: linear-gradient(135deg, #ff6b00, #ff8c00) !important;
        color: white !important;
        border-color: #ff6b00 !important;
        font-weight: 600 !important;
    }

    /* Card content for Light Mode */
    .card-content {
        color: #555555 !important;
        line-height: 1.6;
        font-size: 1rem;
    }

    .question-text-white {
        color: #333333 !important;
        font-weight: 600;
        font-size: 1.1rem;
        line-height: 1.5;
    }

    /* Summary section for Light Mode */
    .summary-section {
        background: rgba(255, 255, 255, 0.7);
        border-radius: 20px;
        padding: 2rem;
        border: 1px solid rgba(0, 0, 0, 0.1);
        margin: 2rem 0;
        backdrop-filter: blur(10px);
    }

    /* Hide empty content */
    .empty-content {
        display: none !important;
    }

    /* Back button styling for Light Mode - FIXED FOR SINGLE LINE */
    .back-button {
        background: linear-gradient(135deg, #6c757d, #495057) !important;
        color: white !important;
        border-radius: 12px !important;
        padding: 10px 20px !important;
        font-weight: 600 !important;
        border: none !important;
        transition: all 0.3s ease !important;
        white-space: nowrap !important;
        min-width: 150px !important;
        overflow: hidden !important;
        text-overflow: ellipsis !important;
    }

    .back-button:hover {
        transform: translateY(-2px);
        box-shadow: 0 5px 15px rgba(0,0,0,0.2);
    }

    /* Dimension detail navigation */
    .dimension-nav {
        display: flex;
        justify-content: space-between;
        margin: 2rem 0;
        gap: 1rem;
    }

    /* Enhanced colorful boxes for dimensions - Light Mode */
    .dimension-detail-box {
        border-radius: 20px;
        padding: 2.5rem;
        margin: 1rem 0;
        border: 1px solid rgba(0,0,0,0.1);
        transition: all 0.4s ease;
        position: relative;
        overflow: hidden;
        background: rgba(255, 255, 255, 0.8);
    }

    .volatility-detail {
        background: linear-gradient(135deg, rgba(239, 68, 68, 0.15), rgba(255, 255, 255, 0.7));
        border-left: 8px solid #ef4444;
        box-shadow: 0 10px 30px rgba(239, 68, 68, 0.1);
    }

    .ambiguity-detail {
        background: linear-gradient(135deg, rgba(147, 51, 234, 0.15), rgba(255, 255, 255, 0.7));
        border-left: 8px solid #9333ea;
        box-shadow: 0 10px 30px rgba(147, 51, 234, 0.1);
    }

    .interconnectedness-detail {
        background: linear-gradient(135deg, rgba(59, 130, 246, 0.15), rgba(255, 255, 255, 0.7));
        border-left: 8px solid #3b82f6;
        box-shadow: 0 10px 30px rgba(59, 130, 246, 0.1);
    }

    .uncertainty-detail {
        background: linear-gradient(135deg, rgba(249, 115, 22, 0.15), rgba(255, 255, 255, 0.7));
        border-left: 8px solid #f97316;
        box-shadow: 0 10px 30px rgba(249, 115, 22, 0.1);
    }

    /* Light mode specific score styling - BOLD AND BLACK */
    .light-score {
        font-size: 4rem;
        font-weight: 900;
        text-align: center;
        margin: 1.5rem 0;
        color: #000000 !important;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.1);
    }
    </style>
    """, unsafe_allow_html=True)

# Add theme toggle container
st.markdown("""
<div class="theme-toggle-container">
""", unsafe_allow_html=True)

# Theme toggle radio buttons
theme = st.radio(
    "Theme",
    ["Dark Mode", "Light Mode"],
    index=0 if st.session_state.dark_mode else 1,
    key="theme_toggle",
    horizontal=True,
    label_visibility="collapsed"
)

st.markdown("</div>", unsafe_allow_html=True)

# Update theme based on radio selection
if theme == "Dark Mode" and not st.session_state.dark_mode:
    st.session_state.dark_mode = True
    st.rerun()
elif theme == "Light Mode" and st.session_state.dark_mode:
    st.session_state.dark_mode = False
    st.rerun()

# JavaScript for floating button
st.markdown("""
<script>
// Create floating particles (only for dark mode)
function createParticles() {
    const container = document.getElementById('particles-container');
    if (!container) return;
    
    // Clear existing particles
    container.innerHTML = '';
    
    // Only create particles for dark mode
    const isDarkMode = document.querySelector('.stApp').style.background.includes('0f0f23') || 
                       document.querySelector('.stApp').style.background.includes('1a1a2e');
    
    if (isDarkMode) {
        for (let i = 0; i < 20; i++) {
            const particle = document.createElement('div');
            particle.className = 'particle';
            
            const size = Math.random() * 10 + 5;
            const left = Math.random() * 100;
            const delay = Math.random() * 15;
            const duration = Math.random() * 10 + 10;
            
            particle.style.width = `${size}px`;
            particle.style.height = `${size}px`;
            particle.style.left = `${left}vw`;
            particle.style.animationDelay = `${delay}s`;
            particle.style.animationDuration = `${duration}s`;
            
            container.appendChild(particle);
        }
    }
}

// Initialize particles when page loads
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', createParticles);
} else {
    createParticles();
}

// Recreate particles when theme changes
const observer = new MutationObserver(function(mutations) {
    mutations.forEach(function(mutation) {
        if (mutation.type === 'attributes' && mutation.attributeName === 'style') {
            setTimeout(createParticles, 100);
        }
    });
});

// Observe the main app container for style changes
const appContainer = document.querySelector('.stApp');
if (appContainer) {
    observer.observe(appContainer, { attributes: true, attributeFilter: ['style'] });
}

// Floating button functionality
function scrollToTop() {
    window.scrollTo({top: 0, behavior: 'smooth'});
}
</script>

<!-- Background Elements (only for dark mode) -->
<div class="background-elements">
    <div class="floating-shape shape-1"></div>
    <div class="floating-shape shape-2"></div>
    <div class="floating-shape shape-3"></div>
    <div class="floating-shape shape-4"></div>
</div>

<!-- Particle Background -->
<div class="particles" id="particles-container"></div>

<!-- Floating Action Button -->
<button class="floating-btn" onclick="scrollToTop()">↑</button>
""", unsafe_allow_html=True)

# -----------------------------
# EXPANDED ACCOUNTS with Industry Mapping (Final Corrected Version)
# -----------------------------
ACCOUNT_INDUSTRY_MAP = {
    "Select Account": "Select Industry",
 
    # --- Priority Accounts (shown first) ---
    "Abbvie": "Pharma",
    "BMS": "Pharma",
    "BLR Airport": "Other",
    "Chevron": "Energy",
    "Coles": "Retail",
    "DELL": "Technology",
    "Microsoft": "Technology",
    "Mu Labs": "Technology",
    "Nike": "Consumer Goods",
    "Skill Development": "Education",
    "Southwest Airlines": "Airlines",
    "Sabic": "Energy",
    "Johnson & Johnson": "Pharma",
    "THD": "Retail",
    "Tmobile": "Telecom",
    "Walmart": "Retail",
 
    # --- Rest of the Accounts ---
    # Pharmaceutical
    "Pfizer": "Pharma",
    "Novartis": "Pharma",
    "Merck": "Pharma",
    "Roche": "Pharma",
 
    # Technology
    "IBM": "Technology",
    "Oracle": "Technology",
    "SAP": "Technology",
    "Salesforce": "Technology",
    "Adobe": "Technology",
 
    # Retail
    "Target": "Retail",
    "Costco": "Retail",
    "Kroger": "Retail",
    "Tesco": "Retail",
    "Carrefour": "Retail",
 
    # Airlines
    "Delta Airlines": "Airlines",
    "United Airlines": "Airlines",
    "American Airlines": "Airlines",
    "Emirates": "Airlines",
    "Lufthansa": "Airlines",
 
    # Consumer Goods
    "Adidas": "Consumer Goods",
    "Unilever": "Consumer Goods",
    "Procter & Gamble": "Consumer Goods",
    "Coca-Cola": "Consumer Goods",
    "PepsiCo": "Consumer Goods",
 
    # Energy
    "ExxonMobil": "Energy",
    "Shell": "Energy",
    "BP": "Energy",
    "TotalEnergies": "Energy",
 
    # Finance
    "JPMorgan Chase": "Finance",
    "Bank of America": "Finance",
    "Wells Fargo": "Finance",
    "Goldman Sachs": "Finance",
    "Morgan Stanley": "Finance",
    "Citigroup": "Finance",
 
    # Healthcare
    "UnitedHealth": "Healthcare",
    "CVS Health": "Healthcare",
    "Anthem": "Healthcare",
    "Humana": "Healthcare",
    "Kaiser Permanente": "Healthcare",
 
    # Logistics
    "FedEx": "Logistics",
    "UPS": "Logistics",
    "DHL": "Logistics",
    "Maersk": "Logistics",
    "Amazon Logistics": "Logistics",
 
    # E-commerce
    "Amazon": "E-commerce",
    "Alibaba": "E-commerce",
    "eBay": "E-commerce",
    "Shopify": "E-commerce",
    "Flipkart": "E-commerce",
 
    # Automotive
    "Tesla": "Automotive",
    "Ford": "Automotive",
    "General Motors": "Automotive",
    "Toyota": "Automotive",
    "Volkswagen": "Automotive",
 
    # Hospitality
    "Marriott": "Hospitality",
    "Hilton": "Hospitality",
    "Hyatt": "Hospitality",
    "Airbnb": "Hospitality",
 
    # Education
    "Coursera": "Education",
    "Udemy": "Education",
    "Khan Academy": "Education",
    "Mars": "Confectionery",
}
 
# --- Priority Account Order ---
PRIORITY_ACCOUNTS = [
    "Abbvie", "BMS", "BLR Airport", "Chevron", "Coles", "DELL",
    "Microsoft","Mars", "Mu Labs", "Nike", "Skill Development",
    "Southwest Airlines", "Sabic", "Johnson & Johnson",
    "THD", "Tmobile", "Walmart"
]
 
# --- Add Remaining Accounts (Alphabetically), keeping 'Others' at the end ---
OTHER_ACCOUNTS = [
    acc for acc in ACCOUNT_INDUSTRY_MAP.keys()
    if acc not in PRIORITY_ACCOUNTS and acc != "Select Account"
]
OTHER_ACCOUNTS.sort()
OTHER_ACCOUNTS.append("Others")  # ✅ Keep Others at last
 
# --- Final Ordered Account List ---
ACCOUNTS = ["Select Account"] + PRIORITY_ACCOUNTS + OTHER_ACCOUNTS
 
# --- Add 'Others' Industry mapping ---
ACCOUNT_INDUSTRY_MAP["Others"] = "Other"
 
# --- Unique Industries ---
INDUSTRIES = sorted(list(set(ACCOUNT_INDUSTRY_MAP.values())))

# Create industry to accounts mapping
INDUSTRY_ACCOUNT_MAP = {}
for account, industry in ACCOUNT_INDUSTRY_MAP.items():
    if industry not in INDUSTRY_ACCOUNT_MAP:
        INDUSTRY_ACCOUNT_MAP[industry] = []
    INDUSTRY_ACCOUNT_MAP[industry].append(account)

# Sort accounts within each industry
for industry in INDUSTRY_ACCOUNT_MAP:
    INDUSTRY_ACCOUNT_MAP[industry].sort()

# ---------------------------
# API Configuration
# ---------------------------
TENANT_ID = "talos"
AUTH_TOKEN = None
HEADERS_BASE = {"Content-Type": "application/json"}

API_CONFIGS = [
    {
        "name": "vocabulary",
        "url": "https://eoc.mu-sigma.com/talos-engine/agency/reasoning_api?society_id=1757657318406&agency_id=1758548233201&level=1",
        "multiround_convo": 3,
        "description": "Vocabulary Extraction",
        "prompt": lambda problem_text, outputs: f"Extract key vocabulary and terminology from this business problem: {problem_text}"
    },
    {
        "name": "current_system",
        "url": "https://eoc.mu-sigma.com/talos-engine/agency/reasoning_api?society_id=1757657318406&agency_id=1758549095254&level=1",
        "multiround_convo": 2,
        "description": "Current System Analysis",
        "prompt": lambda problem_text, outputs: f"Analyze the current system, inputs, outputs, and pain points for this business problem. Provide clear sections for Current System, Inputs, Outputs, and Pain Points: {problem_text}"
    },
    # Q1..Q12
    {
        "name": "Q1",
        "url": "https://eoc.mu-sigma.com/talos-engine/agency/reasoning_api?society_id=1757657318406&agency_id=1758555344231&level=1",
        "multiround_convo": 2,
        "question": "What is the frequency and pace of change in the key inputs driving the business?",
        "prompt": lambda problem_text, outputs: f"Assess volatility - {problem_text}"
    },
    {
        "name": "Q2",
        "url": "https://eoc.mu-sigma.com/talos-engine/agency/reasoning_api?society_id=1757657318406&agency_id=1758549615986&level=1",
        "multiround_convo": 2,
        "question": "To what extent are these changes cyclical and predictable versus sporadic and unpredictable?",
        "prompt": lambda problem_text, outputs: f"Assess volatility - {problem_text}"
    },
    {
        "name": "Q3",
        "url": "https://eoc.mu-sigma.com/talos-engine/agency/reasoning_api?society_id=1757657318406&agency_id=1758614550482&level=1",
        "multiround_convo": 2,
        "question": "How resilient is the current system in absorbing these changes without requiring significant rework or disruption?",
        "prompt": lambda problem_text, outputs: f"Assess volatility - {problem_text}"
    },
    {
        "name": "Q4",
        "url": "https://eoc.mu-sigma.com/talos-engine/agency/reasoning_api?society_id=1757657318406&agency_id=1758614809984&level=1",
        "multiround_convo": 2,
        "question": "To what extent do stakeholders share a common understanding of the key terms and concepts?",
        "prompt": lambda problem_text, outputs: f"Assess ambiguity - {problem_text}"
    },
    {
        "name": "Q5",
        "url": "https://eoc.mu-sigma.com/talos-engine/agency/reasoning_api?society_id=1757657318406&agency_id=1758615038050&level=1",
        "multiround_convo": 2,
        "question": "Are there any conflicting definitions or interpretations that could create confusion?",
        "prompt": lambda problem_text, outputs: f"Assess ambiguity - {problem_text}"
    },
    {
        "name": "Q6",
        "url": "https://eoc.mu-sigma.com/talos-engine/agency/reasoning_api?society_id=1757657318406&agency_id=1758615386880&level=1",
        "multiround_convo": 2,
        "question": "Are objectives, priorities, and constraints clearly communicated and well-defined?",
        "prompt": lambda problem_text, outputs: f"Assess ambiguity - {problem_text}"
    },
    {
        "name": "Q7",
        "url": "https://eoc.mu-sigma.com/talos-engine/agency/reasoning_api?society_id=1757657318406&agency_id=1758615778653&level=1",
        "multiround_convo": 2,
        "question": "To what extent are key inputs interdependent?",
        "prompt": lambda problem_text, outputs: f"Assess interconnectedness - {problem_text}"
    },
    {
        "name": "Q8",
        "url": "https://eoc.mu-sigma.com/talos-engine/agency/reasoning_api?society_id=1757657318406&agency_id=1758616081630&level=1",
        "multiround_convo": 2,
        "question": "How well are the governing rules, functions, and relationships between inputs understood?",
        "prompt": lambda problem_text, outputs: f"Assess interconnectedness - {problem_text}"
    },
    {
        "name": "Q9",
        "url": "https://eoc.mu-sigma.com/talos-engine/agency/reasoning_api?society_id=1757657318406&agency_id=1758616793510&level=1",
        "multiround_convo": 2,
        "question": "Are there any hidden or latent dependencies that could impact outcomes?",
        "prompt": lambda problem_text, outputs: f"Assess interconnectedness - {problem_text}"
    },
    {
        "name": "Q10",
        "url": "https://eoc.mu-sigma.com/talos-engine/agency/reasoning_api?society_id=1757657318406&agency_id=1758617140479&level=1",
        "multiround_convo": 2,
        "question": "Are there hidden or latent dependencies that could affect outcomes?",
        "prompt": lambda problem_text, outputs: f"Assess uncertainty - {problem_text}"
    },
    {
        "name": "Q11",
        "url": "https://eoc.mu-sigma.com/talos-engine/agency/reasoning_api?society_id=1757657318406&agency_id=1758618137301&level=1",
        "multiround_convo": 2,
        "question": "Are feedback loops insufficient or missing, limiting our ability to adapt?",
        "prompt": lambda problem_text, outputs: f"Assess uncertainty - {problem_text}"
    },
    {
        "name": "Q12",
        "url": "https://eoc.mu-sigma.com/talos-engine/agency/reasoning_api?society_id=1757657318406&agency_id=1758619317968&level=1",
        "multiround_convo": 2,
        "question": "Do we lack established benchmarks or 'gold standards' to validate results?",
        "prompt": lambda problem_text, outputs: f"Assess uncertainty - {problem_text}"
    },
    {
        "name": "hardness_summary",
        "url": "https://eoc.mu-sigma.com/talos-engine/agency/reasoning_api?society_id=1757657318406&agency_id=1758619658634&level=1",
        "multiround_convo": 2,
        "description": "Hardness Level & Dimension Scores",
        "prompt": lambda problem_text, outputs: f"Provide overall hardness summary and dimension scores for: {problem_text}"
    }
]

DIMENSION_QUESTIONS = {
    "Volatility": ["Q1", "Q2", "Q3"],
    "Ambiguity": ["Q4", "Q5", "Q6"],
    "Interconnectedness": ["Q7", "Q8", "Q9"],
    "Uncertainty": ["Q10", "Q11", "Q12"]
}

# ---------------------------
# Utility functions
# ---------------------------
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
    """Calls the API with retry logic"""
    prompt = api_cfg["prompt"](problem_text, outputs)
    
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
                payload = {
                    "agency_goal": prompt,
                    "multiround_convo": api_cfg.get("multiround_convo", 1),
                    "user_id": "talos-rest-endpoint"
                }
                
                resp = requests.post(api_cfg["url"], headers=headers, json=payload, timeout=60)
                
                if resp.status_code == 200:
                    res = json_to_text(resp.json())
                    for r in range(1, api_cfg.get("multiround_convo", 1)):
                        next_payload = {
                            "agency_goal": res,
                            "multiround_convo": 1,
                            "user_id": "talos-rest-endpoint"
                        }
                        resp2 = requests.post(api_cfg["url"], headers=headers, json=next_payload, timeout=60)
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
    if overall_score >= 4.0:
        return "Hard", "box-hard"
    elif overall_score >= 3.0:
        return "Moderate", "box-moderate"
    else:
        return "Easy", "box-easy"

def extract_score_from_text(text, dimension):
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
    return 3.0

def extract_overall_score(text):
    dimensions = ["Volatility", "Ambiguity", "Interconnectedness", "Uncertainty"]
    scores = []
    for dim in dimensions:
        score = extract_score_from_text(text, dim)
        if score > 0:
            scores.append(score)
    if len(scores) >= 2:
        return sum(scores) / len(scores)
    return 3.0

def sanitize_text(text):
    """Remove markdown artifacts and clean up text"""
    if not text:
        return ""
    
    # Fix the "s" character issue - only remove standalone 's' that are clearly artifacts
    # Remove 's' only if it's alone on a line or at the very beginning followed by space
    text = re.sub(r'^\s*s\s*\n', '', text.strip())
    text = re.sub(r'\n\s*s\s*\n', '\n', text)
    
    # Don't remove 's' at the beginning of content if it's part of actual text
    # Only remove if it's clearly a formatting artifact
    
    text = re.sub(r'Q\d+\s*Answer\s*Explanation\s*:', '', text, flags=re.IGNORECASE)
    text = re.sub(r'\*\*(.*?)\*\*', r'\1', text)
    text = re.sub(r'\*(.*?)\*', r'\1', text)
    text = re.sub(r'`(.*?)`', r'\1', text)
    text = re.sub(r'#+\s*', '', text)
    text = re.sub(r'!\[.*?\]\(.*?\)', '', text)
    text = re.sub(r'\[(.*?)\]\(.*?\)', r'\1', text)
    text = re.sub(r'\n{3,}', '\n\n', text)
    text = re.sub(r' {2,}', ' ', text)
    text = re.sub(r'^\s*[-*]\s+', '• ', text, flags=re.MULTILINE)
    text = re.sub(r'<\/?[^>]+>', '', text)
    text = re.sub(r'&amp;', '&', text)
    text = re.sub(r'& Key Takeaway:', 'Key Takeaway:', text)
    
    # Remove any remaining standalone single characters that are clearly artifacts
    # But be more careful - only remove if they're on their own line
    text = re.sub(r'\n\s*[a-z]\s*\n', '\n', text, flags=re.IGNORECASE)
    
    return text.strip()

def extract_current_system_components(text):
    """Extract current system, inputs, outputs, and pain points from the current_system API response"""
    if not text:
        return {
            "current_system": "No current system information available",
            "inputs": "No input information available",
            "outputs": "No output information available",
            "pain_points": "No pain points identified"
        }
    
    # Initialize sections
    sections = {
        "current_system": "",
        "inputs": "",
        "outputs": "",
        "pain_points": ""
    }
    
    # Enhanced pattern matching with proper boundaries for emoji headers
    patterns = [
        # Pattern with emoji headers (from your API output)
        (r"🏢\s*CURRENT SYSTEM[:\s\-]*(.*?)(?=📥\s*INPUTS|📤\s*OUTPUTS|⚠️\s*PAIN POINTS|$)", "current_system"),
        (r"📥\s*INPUTS[:\s\-]*(.*?)(?=📤\s*OUTPUTS|⚠️\s*PAIN POINTS|$)", "inputs"),
        (r"📤\s*OUTPUTS[:\s\-]*(.*?)(?=⚠️\s*PAIN POINTS|$)", "outputs"),
        (r"⚠️\s*PAIN POINTS[:\s\-]*(.*?)$", "pain_points"),
        
        # Pattern 1: Numbered sections
        (r"1\.\s*Current\s+System[:\s]*(.*?)(?=2\.\s*Input|📥|📤|⚠️|$)", "current_system"),
        (r"2\.\s*Input[:\s]*(.*?)(?=3\.\s*Output|📤|⚠️|$)", "inputs"),
        (r"3\.\s*Output[:\s]*(.*?)(?=4\.\s*Pain\s+Points|⚠️|$)", "outputs"),
        (r"4\.\s*Pain\s+Points[:\s]*(.*?)$", "pain_points"),
       
        # Pattern 2: Bold sections
        (r"\*\*Current System\*\*[:\s]*(.*?)(?=\*\*Input|\*\*Output|\*\*Pain Points|📥|📤|⚠️|$)", "current_system"),
        (r"\*\*Input\*\*[:\s]*(.*?)(?=\*\*Output|\*\*Pain Points|📤|⚠️|$)", "inputs"),
        (r"\*\*Output\*\*[:\s]*(.*?)(?=\*\*Pain Points|⚠️|$)", "outputs"),
        (r"\*\*Pain Points\*\*[:\s]*(.*?)$", "pain_points"),
       
        # Pattern 3: Simple section headers
        (r"Current System[:\s]*(.*?)(?=Input|Output|Pain Points|📥|📤|⚠️|$)", "current_system"),
        (r"Input[:\s]*(.*?)(?=Output|Pain Points|📤|⚠️|$)", "inputs"),
        (r"Output[:\s]*(.*?)(?=Pain Points|⚠️|$)", "outputs"),
        (r"Pain Points[:\s]*(.*?)$", "pain_points")
    ]
    
    for pattern, section in patterns:
        match = re.search(pattern, text, re.IGNORECASE | re.DOTALL)
        if match:
            content = match.group(1).strip()
            # Clean the content - but be careful not to remove actual text
            # Only remove obvious artifacts, not words starting with 's'
            if content and len(content) > 10 and not sections[section]:
                # Apply gentle cleaning - don't remove words starting with 's'
                cleaned_content = sanitize_text(content)
                sections[section] = cleaned_content
    
    # If no structured sections found, try to extract using the structure from your example
    if not any(sections.values()):
        # Try to split by the emoji sections
        emoji_sections = re.split(r'(🏢\s*CURRENT SYSTEM|📥\s*INPUTS|📤\s*OUTPUTS|⚠️\s*PAIN POINTS)', text)
        if len(emoji_sections) > 1:
            current_section = None
            for i, section in enumerate(emoji_sections):
                if section.strip() == "🏢 CURRENT SYSTEM":
                    current_section = "current_system"
                elif section.strip() == "📥 INPUTS":
                    current_section = "inputs"
                elif section.strip() == "📤 OUTPUTS":
                    current_section = "outputs" 
                elif section.strip() == "⚠️ PAIN POINTS":
                    current_section = "pain_points"
                elif current_section and i + 1 < len(emoji_sections):
                    content = section.strip()
                    if content and len(content) > 10:
                        sections[current_section] = sanitize_text(content)
    
    # Final fallback: if still no content, use the entire text as current system
    if not any(sections.values()):
        sections["current_system"] = sanitize_text(text)
    
    # Final validation - if any section starts with just a single letter, check if it's actual content
    for section_name, content in sections.items():
        if content and len(content) > 0:
            # If content starts with a single letter followed by space, check if it's a real word
            single_letter_match = re.match(r'^\s*([a-z])\s+', content, re.IGNORECASE)
            if single_letter_match:
                letter = single_letter_match.group(1).lower()
                # Common words that start with these letters - don't remove them
                common_words = {
                    't': ['The','the','this', 'that', 'these', 'those', 'they'],
                    's': ['system', 'some', 'such', 'same', 'see'],
                    'a': ['a', 'an', 'all', 'any', 'are'],
                    'i': ['i', 'in', 'is', 'it', 'if'],
                    'c': ['current', 'can', 'could', 'company'],
                    'p': ['pain', 'points', 'problem', 'process']
                }
                
                # Check if this might be the start of a real word
                words_after = content[single_letter_match.end():].split()
                if words_after and len(words_after[0]) > 2:
                    # It's likely a real word, don't remove the first letter
                    pass
                else:
                    # It might be an artifact, remove just this single letter
                    sections[section_name] = content[single_letter_match.end():].strip()
    
    return sections

def extract_summary(text):
    """Enhanced summary extraction from hardness summary"""
    if not text:
        return "No summary available"
    
    summary_patterns = [
        r'\*\*Summary[:\s\-]*(.*?)(?=\*\*[A-Z]|\Z)',
        r'Summary[:\s\-]*(.*?)(?=###|Key Takeaway|Recommendation|\Z)',
        r'Overall[:\s\-]*(.*?)(?=###|Dimension|\Z)',
        r'Executive Summary[:\s\-]*(.*?)(?=###|Key|Dimension|\Z)',
    ]
    
    for pattern in summary_patterns:
        match = re.search(pattern, text, re.DOTALL | re.IGNORECASE)
        if match:
            summary = match.group(1).strip()
            if summary and len(summary) > 20:
                # Clean the summary - remove truncation artifacts
                summary = re.sub(r'\.\.\.$|…$|\(cut off\)|\(truncated\)', '', summary)
                return summary.strip()
    
    # Fallback: return first meaningful paragraph without arbitrary cutting
    paragraphs = text.split('\n\n')
    for para in paragraphs:
        clean_para = para.strip()
        if len(clean_para) > 50 and not clean_para.startswith('**'):
            # Remove any truncation patterns but return full content
            clean_para = re.sub(r'\.\.\.$|…$|\(cut off\)|\(truncated\)', '', clean_para)
            return clean_para
    
    # Return the full text without arbitrary cutting, just clean truncation patterns
    full_text = re.sub(r'\.\.\.$|…$|\(cut off\)|\(truncated\)', '', text)
    return full_text.strip()

def extract_key_takeaways(text):
    """Enhanced key takeaways extraction from hardness summary"""
    if not text:
        return ["No key takeaways available"]
    
    # Look for structured takeaways
    patterns = [
        r'(?:Key\s+Takeaways?|Recommendations?|Key\s+Points?|Implications?)[:\s\-]*(.*?)(?=###|\*\*[A-Z]|\Z)',
        r'(?:\d+\.\s*(.*?)(?=\n\d+\.|\n\*\*|\Z))',
        r'(?:[\-\*•]\s*(.*?)(?=\n[\-\*•]|\n\*\*|\Z))',
    ]
    
    takeaways = []
    for pattern in patterns:
        matches = re.findall(pattern, text, re.DOTALL | re.IGNORECASE)
        if matches:
            for match in matches:
                if isinstance(match, tuple):
                    match = match[0]
                if match and len(match.strip()) > 20:
                    takeaways.append(match.strip())
    
    # If no structured takeaways, extract meaningful sentences
    if not takeaways:
        sentences = re.split(r'[.!?]+', text)
        for sentence in sentences:
            clean_sentence = sentence.strip()
            if (len(clean_sentence) > 30 and 
                any(keyword in clean_sentence.lower() for keyword in 
                    ['recommend', 'suggest', 'should', 'must', 'need to', 'important', 'critical', 'consider', 'focus on'])):
                takeaways.append(clean_sentence)
    
    return takeaways[:5] if takeaways else ["Review the dimension scores above for specific guidance on addressing complexity."]

# ---------------------------
# Session state init
# ---------------------------
def init_session_state():
    defaults = {
        "current_page": "landing",
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
        "complexity_level": "Easy",
        "complexity_class": "box-easy",
        "overall_score": 0.0,
        "summary": "",
        "current_system_full": "",
        "input_text": "",
        "output_text": "",
        "pain_points_text": "",
        "hardness_summary_text": "",
        "selected_dimension": None,
        "show_vocabulary": False,
        "key_takeaways": [],
        "dark_mode": True,
        "current_dimension_index": 0,
        "previous_page": "landing"
    }
    for k, v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v

init_session_state()

def reset_analysis_state():
    keys = ["outputs", "analysis_complete", "dimension_scores", "complexity_level",
            "complexity_class", "overall_score", "summary", "current_system_full",
            "input_text", "output_text", "pain_points_text", "hardness_summary_text", "key_takeaways", "current_dimension_index"]
    for k in keys:
        if k in st.session_state:
            if k == "outputs": st.session_state[k] = {}
            elif k == "dimension_scores":
                st.session_state[k] = {"Volatility":0.0,"Ambiguity":0.0,"Interconnectedness":0.0,"Uncertainty":0.0}
            elif k == "key_takeaways":
                st.session_state[k] = []
            elif k == "current_dimension_index":
                st.session_state[k] = 0
            else:
                st.session_state[k] = "" if isinstance(st.session_state[k], str) else 0.0
    st.session_state.analysis_complete = False

def full_reset():
    """Complete reset of all inputs"""
    st.session_state.problem_text = ""
    st.session_state.industry = "Select Industry"
    st.session_state.account = "Select Account"
    reset_analysis_state()
    st.session_state.show_vocabulary = False

# ---------------------------
# Enhanced Landing Page with Account-Industry Mapping
# ---------------------------
def landing_page():
    st.markdown("""
    <div class="app-header">
        <div class="app-title">Problem Complexity Analyzer</div>
        <div class="app-sub">Discover how hard a business problem is across four dimensions — with actionable recommendations.</div>
    </div>
    """, unsafe_allow_html=True)

    # Single navigation button to Results Dashboard
    if st.button("📊 Results Dashboard", key="nav_dashboard", use_container_width=True):
        if st.session_state.analysis_complete:
            st.session_state.previous_page = "landing"
            st.session_state.current_page = "analyze_results"
            st.rerun()
        else:
            st.warning("Please complete an analysis first")

    st.markdown("<br/>", unsafe_allow_html=True)

    # Creative info boxes with better contrast
    c1, c2, c3 = st.columns([1,1,1])
    with c1:
        st.markdown("""
        <div class="info-box">
            <span class="info-emoji">🚀</span>
            <strong>Smart Analysis</strong>
            <div class="medium-text">AI-powered assessment across 4 complexity dimensions with real-time insights</div>
        </div>
        """, unsafe_allow_html=True)
    with c2:
        st.markdown("""
        <div class="info-box">
            <span class="info-emoji">🎯</span>
            <strong>Precision Metrics</strong>
            <div class="medium-text">Detailed scoring for volatility, ambiguity, interconnectedness, and uncertainty</div>
        </div>
        """, unsafe_allow_html=True)
    with c3:
        st.markdown("""
        <div class="info-box">
            <span class="info-emoji">💡</span>
            <strong>Actionable Insights</strong>
            <div class="medium-text">Clear recommendations and strategic guidance for complex problems</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<br/>", unsafe_allow_html=True)

    # Enhanced Input card
    st.markdown('<div class="analysis-card">', unsafe_allow_html=True)
    
    st.markdown("""
    <div style="text-align: center; margin-bottom: 2rem;">
        <h3 style="background: linear-gradient(45deg, #ffd700, #ff8c00); -webkit-background-clip: text; -webkit-text-fill-color: transparent; font-weight: 700;">
            🎯 Describe Your Challenge
        </h3>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    with col1:
        # Account selection
        account = st.selectbox("💼 Business Account", ACCOUNTS, index=ACCOUNTS.index(st.session_state.account))
        if account != st.session_state.account:
            st.session_state.account = account
            # Auto-set industry based on account
            if account != "Select Account":
                st.session_state.industry = ACCOUNT_INDUSTRY_MAP.get(account, "Select Industry")
    
    with col2:
        # Industry selection (auto-populated based on account, but can be changed)
        industry = st.selectbox("🏭 Industry Domain", INDUSTRIES, index=INDUSTRIES.index(st.session_state.industry))
        st.session_state.industry = industry

    st.session_state.problem_text = st.text_area(
        "📝 Describe Your Business Challenge",
        value=st.session_state.problem_text,
        height=180,
        placeholder="💡 Provide a detailed description of the business problem, including context, challenges, and desired outcomes...\n\nExample: Our e-commerce platform is experiencing declining customer retention rates despite increasing marketing spend. We need to understand the root causes and develop a strategy to improve customer loyalty and lifetime value."
    )

    # Enhanced Action buttons
    colA, colB, colC = st.columns([1,1,1])
    with colA:
        analyze_btn = st.button("🚀 Start Analysis", type="primary", use_container_width=True,
            disabled=not (st.session_state.problem_text.strip() and 
                          st.session_state.industry != "Select Industry" and 
                          st.session_state.account != "Select Account"))
        if analyze_btn:
            reset_analysis_state()
            st.session_state.previous_page = "landing"
            st.session_state.current_page = "analyze_results"
            with st.spinner("🚀 Conducting comprehensive analysis..."):
                progress_bar = st.progress(0.0)
                st.session_state.outputs = {}
                total_apis = len(API_CONFIGS)
                for i, api_config in enumerate(API_CONFIGS):
                    progress = (i / total_apis)
                    progress_bar.progress(progress)
                    result = call_api(api_config, st.session_state.problem_text, st.session_state.outputs)
                    st.session_state.outputs[api_config['name']] = result
                    time.sleep(0.3)
                progress_bar.progress(1.0)
                
                # Process results - CORRECTED SECTION
                hardness_summary = st.session_state.outputs.get('hardness_summary', '')
                st.session_state.hardness_summary_text = hardness_summary
                
                for dimension in ["Volatility", "Ambiguity", "Interconnectedness", "Uncertainty"]:
                    score = extract_score_from_text(hardness_summary, dimension)
                    st.session_state.dimension_scores[dimension] = score
                
                scores = list(st.session_state.dimension_scores.values())
                st.session_state.overall_score = sum(scores)/len(scores) if scores else 0.0
                level, cls = classify_complexity(st.session_state.overall_score)
                st.session_state.complexity_level = level
                st.session_state.complexity_class = cls
                st.session_state.summary = extract_summary(hardness_summary)
                st.session_state.key_takeaways = extract_key_takeaways(hardness_summary)
                
                # CORRECTED: Handle the dictionary return properly
                current_system_text = st.session_state.outputs.get('current_system', '')
                sections = extract_current_system_components(current_system_text)
                st.session_state.current_system_full = sections["current_system"]
                st.session_state.input_text = sections["inputs"]
                st.session_state.output_text = sections["outputs"]
                st.session_state.pain_points_text = sections["pain_points"]
                
                st.session_state.analysis_complete = True
            st.rerun()

    with colB:
        if st.button("📚 Show Vocabulary", use_container_width=True):
            st.session_state.show_vocabulary = not st.session_state.show_vocabulary

    with colC:
        if st.button("🔄 Reset All", type="secondary", use_container_width=True, key="reset_btn"):
            full_reset()
            st.rerun()

    # Display vocabulary if toggled
    if st.session_state.show_vocabulary:
        with st.expander("📚 Extracted Vocabulary", expanded=True):
            vocab_text = st.session_state.outputs.get('vocabulary', 'No vocabulary available yet. Run analysis first.')
            if vocab_text and vocab_text.strip() and vocab_text != "No vocabulary available yet. Run analysis first.":
                st.markdown(f"""
                <div class="card-content">
                    {vocab_text}
                </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown('<div class="empty-content"></div>', unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)

# ---------------------------
# Enhanced Analyze Results Page with Summary Section
# ---------------------------
def analyze_results_page():
    st.markdown("""
    <div class="app-header">
        <div class="app-title">Analysis Results</div>
        <div class="app-sub">Comprehensive insights across all complexity dimensions</div>
    </div>
    """, unsafe_allow_html=True)

    # Back button - FIXED: properly working with single line text
    col1, col2 = st.columns([1, 5])
    with col1:
        if st.button("← Back to Analysis", key="back_to_home", use_container_width=True, 
                    help="Return to the main analysis page"):
            st.session_state.current_page = "landing"
            st.rerun()

    # Overall classification with enhanced design - MOVED TO TOP
    cls = st.session_state.complexity_class
    level = st.session_state.complexity_level
    overall_score = st.session_state.overall_score
    
    if level == "Hard":
        box_html = f'''
        <div class="box-hard pulse">
            <div style="text-align: center;">
                <h3 style="margin: 0; font-size: 1.8rem;">🚨 {level} PROBLEM</h3>
                <p style="margin: 0.5rem 0 0 0; font-size: 1.2rem;">Overall Complexity Score: {overall_score:.1f}/5.0</p>
                <p style="margin: 0.5rem 0 0 0; font-size: 1rem;">Requires significant strategic planning and resources</p>
            </div>
        </div>
        '''
    elif level == "Moderate":
        box_html = f'''
        <div class="box-moderate pulse">
            <div style="text-align: center;">
                <h3 style="margin: 0; font-size: 1.8rem;">⚠️ {level} PROBLEM</h3>
                <p style="margin: 0.5rem 0 0 0; font-size: 1.2rem;">Overall Complexity Score: {overall_score:.1f}/5.0</p>
                <p style="margin: 0.5rem 0 0 0; font-size: 1rem;">Manageable with proper planning and execution</p>
            </div>
        </div>
        '''
    else:
        box_html = f'''
        <div class="box-easy pulse">
            <div style="text-align: center;">
                <h3 style="margin: 0; font-size: 1.8rem;">✅ {level} PROBLEM</h3>
                <p style="margin: 0.5rem 0 0 0; font-size: 1.2rem;">Overall Complexity Score: {overall_score:.1f}/5.0</p>
                <p style="margin: 0.5rem 0 0 0; font-size: 1rem;">Straightforward to address with standard approaches</p>
            </div>
        </div>
        '''

    st.markdown(box_html, unsafe_allow_html=True)

    st.markdown("<br/>", unsafe_allow_html=True)

    # Dimension boxes in 2x2 layout with different colors
    st.markdown("<br/>", unsafe_allow_html=True)
    
    # First row: Volatility and Ambiguity
    col1, col2 = st.columns(2)
    
    with col1:
        # Volatility Box - Red Theme
        volatility_score = st.session_state.dimension_scores.get("Volatility", 0.0)
        st.markdown(f'''
        <div class="dimension-box volatility-box">
            <div class="dimension-title">⚡ VOLATILITY</div>
            <div class="dimension-score">{volatility_score:.1f}/5.0</div>
            <div class="medium-text">Measures the frequency and unpredictability of changes in your business environment</div>
        </div>
        ''', unsafe_allow_html=True)
        
        if st.button("🔍 View Q1-Q3 Details", key="volatility_btn", use_container_width=True):
            st.session_state.previous_page = "analyze_results"
            st.session_state.selected_dimension = "Volatility"
            st.session_state.current_page = "dimension_detail"
            st.rerun()

    with col2:
        # Ambiguity Box - Purple Theme
        ambiguity_score = st.session_state.dimension_scores.get("Ambiguity", 0.0)
        st.markdown(f'''
        <div class="dimension-box ambiguity-box">
            <div class="dimension-title">🎯 AMBIGUITY</div>
            <div class="dimension-score">{ambiguity_score:.1f}/5.0</div>
            <div class="medium-text">Assesses clarity of definitions and shared understanding among stakeholders</div>
        </div>
        ''', unsafe_allow_html=True)
        
        if st.button("🔍 View Q4-Q6 Details", key="ambiguity_btn", use_container_width=True):
            st.session_state.previous_page = "analyze_results"
            st.session_state.selected_dimension = "Ambiguity"
            st.session_state.current_page = "dimension_detail"
            st.rerun()

    st.markdown("<br/>", unsafe_allow_html=True)
    
    # Second row: Interconnectedness and Uncertainty
    col3, col4 = st.columns(2)
    
    with col3:
        # Interconnectedness Box - Blue Theme
        interconnectedness_score = st.session_state.dimension_scores.get("Interconnectedness", 0.0)
        st.markdown(f'''
        <div class="dimension-box interconnectedness-box">
            <div class="dimension-title">🕸️ INTERCONNECTEDNESS</div>
            <div class="dimension-score">{interconnectedness_score:.1f}/5.0</div>
            <div class="medium-text">Evaluates dependencies and relationships between different system components</div>
        </div>
        ''', unsafe_allow_html=True)
        
        if st.button("🔍 View Q7-Q9 Details", key="interconnectedness_btn", use_container_width=True):
            st.session_state.previous_page = "analyze_results"
            st.session_state.selected_dimension = "Interconnectedness"
            st.session_state.current_page = "dimension_detail"
            st.rerun()

    with col4:
        # Uncertainty Box - Orange Theme
        uncertainty_score = st.session_state.dimension_scores.get("Uncertainty", 0.0)
        st.markdown(f'''
        <div class="dimension-box uncertainty-box">
            <div class="dimension-title">❓ UNCERTAINTY</div>
            <div class="dimension-score">{uncertainty_score:.1f}/5.0</div>
            <div class="medium-text">Measures knowledge gaps and predictability of business outcomes</div>
        </div>
        ''', unsafe_allow_html=True)
        
        if st.button("🔍 View Q10-Q12 Details", key="uncertainty_btn", use_container_width=True):
            st.session_state.previous_page = "analyze_results"
            st.session_state.selected_dimension = "Uncertainty"
            st.session_state.current_page = "dimension_detail"
            st.rerun()

    st.markdown("<br/>", unsafe_allow_html=True)

    # Button to view current system analysis
    if st.button("📋 View Current System Analysis", use_container_width=True, key="system_analysis_btn"):
        st.session_state.previous_page = "analyze_results"
        st.session_state.current_page = "system_analysis"
        st.rerun()

    # Enhanced Summary and Key Takeaways Section with API Integration
    st.markdown("---")
    st.markdown('<h3 class="section-header-white">📊 OVERALL SUMMARY & KEY TAKEAWAYS</h3>', unsafe_allow_html=True)

    st.markdown('<div class="summary-section">', unsafe_allow_html=True)

    # Get the hardness summary from API output
    hardness_summary = st.session_state.outputs.get('hardness_summary', '')
    if hardness_summary:
        # Extract structured summary from the hardness summary
        summary_text = extract_summary(hardness_summary)
        key_takeaways = extract_key_takeaways(hardness_summary)
        
        # Executive Summary
        if summary_text and summary_text != "No summary section found" and summary_text.strip():
            st.markdown('<div class="summary-item">', unsafe_allow_html=True)
            st.markdown('<h4 class="white-heading">📋 Executive Summary</h4>', unsafe_allow_html=True)
            st.markdown(f'<div class="card-content">{summary_text}</div>', unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)
        else:
            # Fallback: use the first part of hardness summary as executive summary
            fallback_summary = hardness_summary[:500] + "..." if len(hardness_summary) > 500 else hardness_summary
            if fallback_summary.strip():
                st.markdown('<div class="summary-item">', unsafe_allow_html=True)
                st.markdown('<h4 class="white-heading">📋 Executive Summary</h4>', unsafe_allow_html=True)
                st.markdown(f'<div class="card-content">{fallback_summary}</div>', unsafe_allow_html=True)
                st.markdown('</div>', unsafe_allow_html=True)

        # Key Takeaways
        if key_takeaways and any(takeaway.strip() for takeaway in key_takeaways):
            st.markdown('<div class="takeaway-item">', unsafe_allow_html=True)
            st.markdown('<h4 class="white-heading">💡 Key Insights</h4>', unsafe_allow_html=True)
            for i, takeaway in enumerate(key_takeaways, 1):
                if takeaway.strip():
                    st.markdown(f'<div class="card-content"><strong>{i}.</strong> {takeaway}</div>', unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown("<br/>", unsafe_allow_html=True)
    
    # Quick actions
    if st.button("🔄 Run New Analysis", use_container_width=True):
        reset_analysis_state()
        st.session_state.previous_page = "analyze_results"
        st.session_state.current_page = "landing"
        st.rerun()

# ---------------------------
# System Analysis Page
# ---------------------------
def system_analysis_page():
    st.markdown(f"""
    <div class="app-header">
        <div class="app-title">Current System Analysis</div>
        <div class="app-sub">Detailed breakdown of current system, inputs, outputs, and pain points</div>
    </div>
    """, unsafe_allow_html=True)

    # Back button - FIXED: properly working with single line text
    col1, col2 = st.columns([1, 5])
    with col1:
        if st.button("← Back to Analysis", key="back_to_results", use_container_width=True,
                    help="Return to the analysis results"):
            st.session_state.current_page = "analyze_results"
            st.rerun()

    # Enhanced Current System Analysis Section with White Heading
    st.markdown("---")
    st.markdown('<h3 class="section-header-white">🔄 CURRENT SYSTEM ANALYSIS</h3>', unsafe_allow_html=True)

    st.markdown('<div class="system-display">', unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        st.markdown('<div class="system-section"><h4 class="white-heading">🏢 CURRENT SYSTEM</h4></div>', unsafe_allow_html=True)
        current_system_content = st.session_state.current_system_full or "No current system description available."
        if current_system_content.strip() and current_system_content != "No current system description available.":
            st.markdown(f'<div class="card-content">{current_system_content}</div>', unsafe_allow_html=True)
        else:
            st.markdown('<div class="empty-content"></div>', unsafe_allow_html=True)
        
        st.markdown('<div class="system-section"><h4 class="white-heading">📥 INPUTS</h4></div>', unsafe_allow_html=True)
        input_content = st.session_state.input_text or "No input information available."
        if input_content.strip() and input_content != "No input information available.":
            st.markdown(f'<div class="card-content">{input_content}</div>', unsafe_allow_html=True)
        else:
            st.markdown('<div class="empty-content"></div>', unsafe_allow_html=True)

    with col2:
        st.markdown('<div class="system-section"><h4 class="white-heading">📤 OUTPUTS</h4></div>', unsafe_allow_html=True)
        output_content = st.session_state.output_text or "No output information available."
        if output_content.strip() and output_content != "No output information available.":
            st.markdown(f'<div class="card-content">{output_content}</div>', unsafe_allow_html=True)
        else:
            st.markdown('<div class="empty-content"></div>', unsafe_allow_html=True)
        
        st.markdown('<div class="system-section"><h4 class="white-heading">⚠️ PAIN POINTS</h4></div>', unsafe_allow_html=True)
        pain_points_content = st.session_state.pain_points_text or "No pain points identified."
        if pain_points_content.strip() and pain_points_content != "No pain points identified.":
            st.markdown(f'<div class="card-content">{pain_points_content}</div>', unsafe_allow_html=True)
        else:
            st.markdown('<div class="empty-content"></div>', unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)

# ---------------------------
# Enhanced Dimension Detail Page with White Question Text and Navigation
# ---------------------------
def dimension_detail_page():
    dimension = st.session_state.selected_dimension
    st.markdown(f"""
    <div class="app-header">
        <div class="app-title">{dimension} Analysis</div>
        <div class="app-sub">Detailed breakdown and insights for {dimension}</div>
    </div>
    """, unsafe_allow_html=True)

    # Back button - FIXED: properly working with single line text
    col1, col2 = st.columns([1, 5])
    with col1:
        if st.button("← Back to Analysis", key="back_to_dimensions", use_container_width=True,
                    help="Return to the analysis results"):
            st.session_state.current_page = "analyze_results"
            st.rerun()

    # Display score with enhanced design - using proper class for light/dark mode
    score = st.session_state.dimension_scores.get(dimension, 0.0)
    score_class = "dark-score" if st.session_state.dark_mode else "light-score"
    
    st.markdown(f"""
    <div style="text-align: center; margin: 2rem 0;">
        <h2 style="background: linear-gradient(45deg, #ffd700, #ff8c00); -webkit-background-clip: text; -webkit-text-fill-color: transparent;">
            📊 {dimension} SCORE
        </h2>
        <div class="{score_class}">
            {score:.1f}<span style="font-size: 2rem;">/5.0</span>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")

    # Display questions and answers for this dimension with WHITE TEXT
    question_keys = DIMENSION_QUESTIONS.get(dimension, [])
    
    for q_key in question_keys:
        q_config = next((cfg for cfg in API_CONFIGS if cfg["name"] == q_key), None)
        if q_config and "question" in q_config:
            answer = st.session_state.outputs.get(q_key, "No answer available.")
            
            # Apply different colored boxes based on dimension
            dimension_class = f"{dimension.lower()}-detail"
            
            st.markdown(f'<div class="dimension-detail-box {dimension_class}">', unsafe_allow_html=True)
            # Question in proper color for theme
            st.markdown(f'<div class="question-text-white">{q_config["question"]}</div>', unsafe_allow_html=True)
            st.markdown("---")
            if answer and answer.strip() and answer != "No answer available.":
                st.markdown(f"""
                <div class="card-content" style="background: rgba(255,255,255,0.02); padding: 1.5rem; border-radius: 12px; margin: 1rem 0;">
                    {answer}
                </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown('<div class="empty-content"></div>', unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)

    # Navigation to next dimension
    dimensions = list(DIMENSION_QUESTIONS.keys())
    current_index = dimensions.index(dimension)
    
    # Navigation buttons
    nav_col1, nav_col2, nav_col3 = st.columns([1, 2, 1])
    
    with nav_col1:
        if current_index > 0:
            prev_dimension = dimensions[current_index - 1]
            if st.button(f"⬅️ Previous: {prev_dimension}", use_container_width=True, key=f"prev_{dimension}"):
                st.session_state.previous_page = "dimension_detail"
                st.session_state.selected_dimension = prev_dimension
                st.rerun()
    
    with nav_col3:
        if current_index < len(dimensions) - 1:
            next_dimension = dimensions[current_index + 1]
            if st.button(f"Next: {next_dimension} ➡️", use_container_width=True, key=f"next_{dimension}"):
                st.session_state.previous_page = "dimension_detail"
                st.session_state.selected_dimension = next_dimension
                st.rerun()

# ---------------------------
# Router
# ---------------------------
page = st.session_state.current_page

if page == "landing":
    landing_page()
elif page == "analyze_results":
    if not st.session_state.analysis_complete:
        st.warning("No analysis performed yet. Please provide inputs on the Home page and click Analyze.")
        if st.button("← Back to Home"):
            st.session_state.current_page = "landing"
            st.rerun()
        st.stop()
    analyze_results_page()
elif page == "dimension_detail":
    dimension_detail_page()
elif page == "system_analysis":
    system_analysis_page()
else:
    st.session_state.current_page = "landing"
    landing_page()
