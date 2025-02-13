import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
import plotly.express as px
import plotly.graph_objects as go
import random

# Page config
st.set_page_config(
    page_title="Beacon Health",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS with modern UI elements
st.markdown("""
    <style>
    .stApp {
        background-color: #f8f9fa;
    }
    .main {
        padding: 1rem 2rem;
    }
    .stTabs [data-baseweb="tab-list"] {
        gap: 24px;
    }
    .stTabs [data-baseweb="tab"] {
        height: 50px;
        padding: 0px 24px;
        background-color: white;
        border-radius: 5px;
        border: 1px solid #e0e0e0;
    }
    .stTabs [data-baseweb="tab-list"] button[aria-selected="true"] {
        background-color: #2196F3;
        color: white;
    }
    div[data-testid="stExpander"] {
        background-color: white;
        border-radius: 10px;
        border: 1px solid #e0e0e0;
        margin-bottom: 1rem;
    }
    .card {
        padding: 1.5rem;
        border-radius: 10px;
        background-color: white;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        margin-bottom: 1rem;
    }
    .metric-container {
        background-color: white;
        padding: 1rem;
        border-radius: 10px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    .status-badge {
        padding: 4px 12px;
        border-radius: 15px;
        font-weight: bold;
        display: inline-block;
    }
    .status-active {
        background-color: #e3fcef;
        color: #00a86b;
    }
    .status-pending {
        background-color: #fff4e5;
        color: #ff9800;
    }
    </style>
""", unsafe_allow_html=True)

# Initialize session state for demo data
if 'initialized' not in st.session_state:
    # Enhanced apps data with more realistic details
    st.session_state.apps = pd.DataFrame([
        {
            'id': 1,
            'name': 'MindfulPath',
            'category': 'Mental Health',
            'description': 'AI-powered CBT therapy platform with personalized interventions and daily mood tracking',
            'developer': 'NeuroTech Solutions',
            'clinical_score': 4.8,
            'ux_score': 4.7,
            'security_score': 4.9,
            'integration_score': 4.6,
            'overall_score': 4.75,
            'fda_status': 'FDA Cleared',
            'ce_status': 'CE Marked',
            'hipaa_compliant': True,
            'price_model': 'Subscription',
            'monthly_price': 49.99,
            'certification_details': 'FDA Class II Medical Device, HIPAA, GDPR, ISO 27001',
            'clinical_studies': '3 RCTs, 5 Peer-reviewed publications',
            'integration_details': 'Epic, Cerner, Apple Health',
            'active_users': 15000,
            'avg_satisfaction': 4.7
        },
        # Add more apps here with similar detailed data
    ])
    
    # Enhanced prescriptions data
    st.session_state.prescriptions = pd.DataFrame([
        {
            'id': 1,
            'app_name': 'DiabetesGuard',
            'prescribed_by': 'Dr. Sarah Smith',
            'prescribed_to': 'John Davis',
            'status': 'Active',
            'prescribed_date': datetime.now() - timedelta(days=30),
            'next_review': datetime.now() + timedelta(days=60),
            'notes': 'Monitor glucose levels twice daily',
            'adherence_rate': 85
        },
        # Add more prescriptions
    ])
    
    # Enhanced messages with more context
    st.session_state.messages = pd.DataFrame([
        {
            'id': 1,
            'sender_role': 'provider',
            'recipient_role': 'patient',
            'subject': 'Weekly Progress Review',
            'message': 'Your glucose readings are showing good improvement. Keep up the great work!',
            'app_name': 'DiabetesGuard',
            'date': datetime.now() - timedelta(days=2),
            'priority': 'Normal',
            'read_status': True
        },
        # Add more messages
    ])
    
    # Add usage analytics data
    st.session_state.usage_data = pd.DataFrame([
        {
            'date': datetime.now() - timedelta(days=x),
            'daily_active_users': random.randint(800, 1200),
            'prescriptions_made': random.randint(50, 150),
            'messages_sent': random.randint(200, 500)
        } for x in range(30)
    ])
    
    st.session_state.initialized = True

def show_app_card(app):
    # Enhanced app card with modern UI
    with st.container():
        st.markdown(f"""
            <div class="card">
                <h3>{app['name']}</h3>
                <p><strong>Category:</strong> {app['category']}</p>
                <p>{app['description']}</p>
            </div>
        """, unsafe_allow_html=True)
        
        col1, col2, col3 = st.columns([2,1,1])
        
        with col1:
            st.write("#### Clinical Evidence")
            fig = go.Figure(go.Indicator(
                mode = "gauge+number",
                value = app['clinical_score'],
                domain = {'x': [0, 1], 'y': [0, 1]},
                gauge = {
                    'axis': {'range': [None, 5]},
                    'bar': {'color': "#2196F3"},
                    'steps': [
                        {'range': [0, 3], 'color': "lightgray"},
                        {'range': [3, 4], 'color': "gray"},
                        {'range': [4, 5], 'color': "#E3F2FD"}
                    ]
                }
            ))
            fig.update_layout(height=200)
            st.plotly_chart(fig, use_container_width=True)
            
        with col2:
            st.write("#### Integration Status")
            for integration in app['integration_details'].split(', '):
                st.markdown(f"""
                    <div style="padding: 8px; background-color: #E3F2FD; border-radius: 5px; margin-bottom: 8px;">
                        ✓ {integration}
                    </div>
                """, unsafe_allow_html=True)
                
        with col3:
            st.write("#### Actions")
            if st.button("View Details", key=f"view_{app['id']}"):
                st.session_state[f'show_details_{app["id"]}'] = True
            
            if st.button("Request Access", key=f"request_{app['id']}"):
                st.success("Access request sent to your provider!")

def show_patient_dashboard():
    st.title("🏥 Patient Dashboard")
    
    # Quick stats at the top
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown("""
            <div class="metric-container">
                <h3>2</h3>
                <p>Active Prescriptions</p>
            </div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown("""
            <div class="metric-container">
                <h3>85%</h3>
                <p>Average Adherence</p>
            </div>
        """, unsafe_allow_html=True)
    with col3:
        st.markdown("""
            <div class="metric-container">
                <h3>Next Review: 7 days</h3>
                <p>Upcoming Check-in</p>
            </div>
        """, unsafe_allow_html=True)

    # Rest of the dashboard implementation...
    # (Previous code continues with enhanced UI elements)

def main():
    # Sidebar navigation with improved UI
    with st.sidebar:
        st.title("🏥 Beacon Health")
        st.markdown("""
            <div style="padding: 1rem; background-color: white; border-radius: 10px; margin-bottom: 1rem;">
                Digital Therapeutics Platform
            </div>
        """, unsafe_allow_html=True)
        
        role = st.selectbox(
            "Select Role",
            ["Patient", "Provider", "Admin"]
        )
        
        # Role-specific navigation
        if role == "Patient":
            show_patient_dashboard()
        elif role == "Provider":
            show_provider_dashboard()
        else:
            show_admin_dashboard()

if __name__ == "__main__":
    main()
