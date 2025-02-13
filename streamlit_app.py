import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
import random

# Page config
st.set_page_config(
    page_title="Beacon Health",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS with modern, dreamy colors
st.markdown("""
    <style>
    /* Modern color palette */
    :root {
        --primary-color: #6C63FF;      /* Dreamy purple */
        --secondary-color: #4FACFE;    /* Soft blue */
        --accent-color: #00F2FE;       /* Bright cyan */
        --success-color: #4CAF50;      /* Green */
        --warning-color: #FF9800;      /* Orange */
        --error-color: #f44336;        /* Red */
        --background-light: #F8F9FE;   /* Light gray-blue */
        --text-primary: #2C3E50;       /* Dark blue-gray */
    }

    .stApp {
        background: linear-gradient(135deg, #F8F9FE 0%, #E8EAF6 100%);
    }

    .main {
        padding: 1rem 2rem;
    }

    /* Modern card styling */
    .card {
        background: white;
        padding: 1.5rem;
        border-radius: 15px;
        box-shadow: 0 4px 20px rgba(108, 99, 255, 0.1);
        margin-bottom: 1.5rem;
        border: 1px solid rgba(108, 99, 255, 0.1);
        transition: transform 0.2s ease, box-shadow 0.2s ease;
    }

    .card:hover {
        transform: translateY(-5px);
        box-shadow: 0 8px 25px rgba(108, 99, 255, 0.15);
    }

    /* Gradient buttons */
    .stButton > button {
        background: linear-gradient(45deg, var(--primary-color), var(--secondary-color)) !important;
        color: white !important;
        border: none !important;
        padding: 0.5rem 1rem !important;
        border-radius: 25px !important;
        font-weight: 500 !important;
        transition: all 0.3s ease !important;
        width: 100% !important;
    }

    .stButton > button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 4px 15px rgba(79, 172, 254, 0.4) !important;
    }

    /* Metric container with gradients */
    .metric-container {
        background: white;
        padding: 1.5rem;
        border-radius: 15px;
        box-shadow: 0 4px 20px rgba(108, 99, 255, 0.1);
        border: 1px solid rgba(108, 99, 255, 0.1);
        text-align: center;
        transition: transform 0.2s ease;
    }

    .metric-container:hover {
        transform: translateY(-5px);
    }

    /* Big numbers with gradients */
    .big-number {
        font-size: 2.5rem;
        font-weight: bold;
        background: linear-gradient(45deg, var(--primary-color), var(--secondary-color));
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0.5rem;
    }

    .metric-label {
        font-size: 1rem;
        color: var(--text-primary);
        font-weight: 500;
    }

    /* Status badges */
    .status-badge {
        padding: 6px 12px;
        border-radius: 20px;
        font-weight: 500;
        display: inline-block;
        margin: 4px;
    }

    .status-active {
        background: linear-gradient(45deg, #4CAF50, #81C784);
        color: white;
    }

    .status-pending {
        background: linear-gradient(45deg, #FF9800, #FFB74D);
        color: white;
    }

    /* Navigation tabs */
    .stTabs [data-baseweb="tab-list"] {
        gap: 24px;
        background: white;
        padding: 1rem;
        border-radius: 15px;
        box-shadow: 0 4px 20px rgba(108, 99, 255, 0.1);
        margin-bottom: 2rem;
    }

    .stTabs [data-baseweb="tab"] {
        height: 50px;
        padding: 0px 24px;
        background: white;
        border-radius: 25px;
        border: 1px solid rgba(108, 99, 255, 0.1);
        transition: all 0.3s ease;
    }

    .stTabs [data-baseweb="tab-list"] button[aria-selected="true"] {
        background: linear-gradient(45deg, var(--primary-color), var(--secondary-color));
        color: white;
        border: none;
    }

    /* Feature badges */
    .feature-badge {
        background: linear-gradient(45deg, #E3F2FD, #BBDEFB);
        padding: 8px 12px;
        border-radius: 10px;
        color: #1976D2;
        margin: 4px;
        display: inline-block;
        font-weight: 500;
    }

    /* Timeline styles */
    .timeline-card {
        border-left: 4px solid var(--primary-color);
        padding-left: 1rem;
        margin-bottom: 1rem;
    }

    /* Message styles */
    .message-card {
        background: white;
        padding: 1rem;
        border-radius: 10px;
        margin-bottom: 1rem;
        border-left: 4px solid var(--primary-color);
    }

    /* Progress bar enhancements */
    .stProgress > div > div > div > div {
        background: linear-gradient(45deg, var(--primary-color), var(--secondary-color));
        border-radius: 10px;
    }
    </style>
""", unsafe_allow_html=True)

# Initialize session state with demo data
if 'initialized' not in st.session_state:
    # Apps data
    st.session_state.apps = pd.DataFrame([
        {
            'id': 1,
            'name': 'MindfulPath',
            'category': 'Mental Health',
            'description': '🧠 AI-powered CBT therapy platform with personalized interventions',
            'features': ['Daily Mood Tracking', 'AI Therapy Sessions', 'Crisis Support', 'Progress Analytics'],
            'clinical_score': 4.8,
            'ux_score': 4.7,
            'security_score': 4.9,
            'integration_score': 4.6,
            'fda_status': 'FDA Cleared',
            'testimonial': "Life-changing app! Helped me manage anxiety effectively.",
            'active_users': 15000,
            'success_rate': '87%'
        },
        {
            'id': 2,
            'name': 'DiabetesGuard',
            'category': 'Chronic Disease',
            'description': '📊 Smart diabetes management with CGM integration',
            'features': ['Glucose Monitoring', 'Medication Reminders', 'Diet Tracking', 'Doctor Connect'],
            'clinical_score': 4.9,
            'ux_score': 4.8,
            'security_score': 4.9,
            'integration_score': 4.7,
            'fda_status': 'FDA Cleared',
            'testimonial': "Revolutionized my diabetes care routine!",
            'active_users': 25000,
            'success_rate': '92%'
        },
        {
            'id': 3,
            'name': 'SleepHarmony',
            'category': 'Sleep',
            'description': '😴 Advanced sleep therapy and tracking',
            'features': ['Sleep Analysis', 'Relaxation Exercises', 'Smart Alarm', 'Sleep Scores'],
            'clinical_score': 4.7,
            'ux_score': 4.9,
            'security_score': 4.8,
            'integration_score': 4.5,
            'fda_status': 'FDA Registered',
            'testimonial': "Finally getting quality sleep!",
            'active_users': 10000,
            'success_rate': '83%'
        }
    ])
    
    # Prescriptions data
    st.session_state.prescriptions = pd.DataFrame([
        {
            'id': 1,
            'app_name': 'DiabetesGuard',
            'prescribed_by': 'Dr. Sarah Smith',
            'prescribed_to': 'John Davis',
            'status': 'Active',
            'prescribed_date': datetime.now() - timedelta(days=30),
            'next_review': datetime.now() + timedelta(days=60),
            'adherence_rate': 85,
            'progress_notes': 'Good progress in glucose management'
        },
        {
            'id': 2,
            'app_name': 'MindfulPath',
            'prescribed_by': 'Dr. James Wilson',
            'prescribed_to': 'Sarah Chen',
            'status': 'Active',
            'prescribed_date': datetime.now() - timedelta(days=15),
            'next_review': datetime.now() + timedelta(days=75),
            'adherence_rate': 92,
            'progress_notes': 'Excellent engagement with daily exercises'
        }
    ])
    
    # Messages data
    st.session_state.messages = pd.DataFrame([
        {
            'id': 1,
            'sender': 'Dr. Smith',
            'content': 'Great progress with your glucose management! Keep it up! 🌟',
            'app': 'DiabetesGuard',
            'date': datetime.now() - timedelta(days=2),
            'read': False
        },
        {
            'id': 2,
            'sender': 'Dr. Wilson',
            'content': 'Your meditation streak is impressive! How are you feeling?',
            'app': 'MindfulPath',
            'date': datetime.now() - timedelta(days=1),
            'read': True
        }
    ])
    
    st.session_state.initialized = True

def show_app_card(app):
    with st.container():
        # Main app card
        st.markdown(f"""
            <div class="card">
                <div style="display: flex; justify-content: space-between; align-items: center;">
                    <h3>{app['name']} {'✨' if app['fda_status'] == 'FDA Cleared' else '🔄'}</h3>
                    <div class="status-badge status-active">{app['fda_status']}</div>
                </div>
                <p style="color: #666; margin-bottom: 1rem;">{app['category']}</p>
                <p>{app['description']}</p>
                
                <div style="margin-top: 1rem;">
                    {''.join([f'<span class="feature-badge">{feature}</span>' for feature in app['features']])}
                </div>
            </div>
        """, unsafe_allow_html=True)
        
        # Metrics and actions
        col1, col2 = st.columns([3,1])
        
        with col1:
            # Create metrics chart
            metrics_df = pd.DataFrame({
                'Metric': ['Clinical', 'UX', 'Security', 'Integration'],
                'Score': [
                    app['clinical_score'],
                    app['ux_score'],
                    app['security_score'],
                    app['integration_score']
                ]
            })
            st.bar_chart(metrics_df.set_index('Metric'))
            
        with col2:
            st.markdown(f"""
                <div class="metric-container">
                    <div class="big-number">{app['success_rate']}</div>
                    <div class="metric-label">Success Rate</div>
                </div>
            """, unsafe_allow_html=True)
            
            if st.button("✨ Try Now", key=f"try_{app['id']}"):
                st.balloons()
                st.success(f"Starting your journey with {app['name']}!")
            
            if st.button("📋 More Info", key=f"info_{app['id']}"):
                st.info("Detailed information coming soon!")

def show_patient_dashboard():
    st.title("🌟 Your Health Journey")
    
    # Quick stats with enhanced visuals
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown("""
            <div class="metric-container">
                <div class="big-number">2</div>
                <div class="metric-label">Active Therapies</div>
                <div style="color: #4CAF50; font-size: 0.9rem;">↑ 1 new this month</div>
            </div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown("""
            <div class="metric-container">
                <div class="big-number">89%</div>
                <div class="metric-label">Adherence Score</div>
                <div style="color: #4CAF50; font-size: 0.9rem;">↑ 12% improvement</div>
            </div>
        """, unsafe_allow_html=True)
    with col3:
        st.markdown("""
            <div class="metric-container">
                <div class="big-number">7</div>
                <div class="metric-label">Days to Review</div>
                <div style="color: #FF9800; font-size: 0.9rem;">📅 Upcoming</div>
            </div>
        """, unsafe_allow_html=True)

    # Main content tabs
    tabs = st.tabs(["📱 My Apps", "🔍 Discover", "💌 Messages"])
    
    with tabs[0]:
        st.header("Your Digital Therapies")
        
        for _, prescription in st.session_state.prescriptions.iterrows():
            app = st.session_state.apps[st.session_state.apps['name'] == prescription['app_name']].iloc[0]
            
            with st.expander(f"✨ {app['name']} - Prescribed by {prescription['prescribed_by']}"):
                col1, col2 = st.columns([2,1])
                
                with col1:
                    st.markdown(f"""
                        <div style="padding: 1rem; background: linear-gradient(135deg, #F8F9FE 0%, #E8EAF6 100%); border-radius: 10px;">
                            <h4>{app['description']}</h4>
                            <p>Prescribed: {prescription['prescribed_date'].strftime('%
