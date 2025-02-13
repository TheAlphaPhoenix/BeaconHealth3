import streamlit as st
import pandas as pd
from datetime import datetime
import sqlite3

# Set page configuration and styling
st.set_page_config(
    page_title="Beacon Health",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better UI
st.markdown("""
    <style>
    .main {
        padding: 0rem 1rem;
    }
    .stTabs {
        background-color: #f8f9fa;
        padding: 10px;
        border-radius: 5px;
    }
    .stButton > button {
        width: 100%;
    }
    .css-1d391kg {
        padding: 1rem;
    }
    .certification-badge {
        background-color: #e7f3fe;
        border-left: 3px solid #2196F3;
        padding: 10px;
        margin: 10px 0;
    }
    .metric-card {
        background-color: white;
        padding: 20px;
        border-radius: 10px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    .app-card {
        background-color: white;
        padding: 20px;
        border-radius: 10px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        margin: 10px 0;
    }
    </style>
""", unsafe_allow_html=True)

def init_db():
    """Initialize SQLite database with enhanced schema"""
    conn = sqlite3.connect('beacon_health.db')
    c = conn.cursor()
    
    # Apps table with certification fields
    c.execute('''
        CREATE TABLE IF NOT EXISTS apps (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            category TEXT NOT NULL,
            description TEXT,
            developer TEXT,
            clinical_score FLOAT,
            ux_score FLOAT,
            security_score FLOAT,
            integration_score FLOAT,
            overall_score FLOAT,
            fda_status TEXT,
            ce_status TEXT,
            hipaa_compliant BOOLEAN,
            price_model TEXT,
            certification_details TEXT,
            clinical_studies TEXT,
            integration_details TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Other tables (messages, prescriptions) remain the same...
    [Previous database initialization code...]
    
    # Insert enhanced demo apps with certification details
    if c.execute('SELECT COUNT(*) FROM apps').fetchone()[0] == 0:
        demo_apps = [
            {
                'name': 'MindfulPath',
                'category': 'Mental Health',
                'description': 'AI-powered CBT therapy platform with personalized interventions',
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
                'certification_details': 'FDA Class II Medical Device, HIPAA, GDPR, ISO 27001',
                'clinical_studies': '3 RCTs, 5 Peer-reviewed publications',
                'integration_details': 'Epic, Cerner, Apple Health'
            },
            # Add more demo apps with similar detailed structure
            [Previous demo apps with enhanced certification details...]
        ]
        
        for app in demo_apps:
            c.execute('''
                INSERT INTO apps (
                    name, category, description, developer,
                    clinical_score, ux_score, security_score,
                    integration_score, overall_score,
                    fda_status, ce_status, hipaa_compliant,
                    price_model, certification_details,
                    clinical_studies, integration_details
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                app['name'], app['category'], app['description'],
                app['developer'], app['clinical_score'], app['ux_score'],
                app['security_score'], app['integration_score'],
                app['overall_score'], app['fda_status'], app['ce_status'],
                app['hipaa_compliant'], app['price_model'],
                app['certification_details'], app['clinical_studies'],
                app['integration_details']
            ))
    
    conn.commit()
    conn.close()

def show_app_card(app, for_patient=True):
    """Enhanced app display card with certification details"""
    with st.container():
        st.markdown(f"""
            <div class="app-card">
                <h3>{app['name']}</h3>
                <p><strong>Category:</strong> {app['category']}</p>
            </div>
        """, unsafe_allow_html=True)
        
        col1, col2 = st.columns([2, 1])
        
        with col1:
            st.write("### Overview")
            st.write(app['description'])
            st.write(f"**Developer:** {app['developer']}")
            
            # Certification Badge
            st.markdown(f"""
                <div class="certification-badge">
                    <h4>Certification Status</h4>
                    <p>🏆 {app['fda_status']}</p>
                    <p>🔒 HIPAA Compliant</p>
                    <p>📊 Clinical Evidence Score: {app['clinical_score']}/5.0</p>
                </div>
            """, unsafe_allow_html=True)
            
            with st.expander("View Detailed Certifications"):
                st.write("#### Clinical Evidence")
                st.write(app['clinical_studies'])
                st.write("#### Security & Compliance")
                st.write(app['certification_details'])
                st.write("#### Integration Capabilities")
                st.write(app['integration_details'])
        
        with col2:
            # Scores visualization
            st.write("### Trust Scores")
            scores_df = pd.DataFrame({
                'Metric': ['Clinical', 'UX', 'Security', 'Integration'],
                'Score': [
                    app['clinical_score'],
                    app['ux_score'],
                    app['security_score'],
                    app['integration_score']
                ]
            })
            st.bar_chart(scores_df.set_index('Metric'))
            
            if for_patient:
                st.button("Request Access", key=f"request_{app['id']}")
            else:
                st.button("Prescribe", key=f"prescribe_{app['id']}")

def show_certification_metrics():
    """Display certification standards and requirements"""
    st.header("Digital Therapeutics Certification Standards")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
            ### Clinical Evidence Requirements
            - 🔬 Randomized Controlled Trials (RCTs)
            - 📚 Peer-reviewed Publications
            - 📊 Real-world Evidence
            - 🏥 Clinical Validation Studies
        """)
        
        st.markdown("""
            ### Security & Compliance
            - 🔒 HIPAA Compliance
            - 🛡️ Data Encryption
            - 📝 Audit Logging
            - 🔐 Access Controls
        """)
    
    with col2:
        st.markdown("""
            ### User Experience Standards
            - 👥 Accessibility Guidelines
            - 📱 Cross-platform Support
            - 🎯 Usability Testing
            - 🔄 Regular Updates
        """)
        
        st.markdown("""
            ### Integration Requirements
            - 🏥 EHR Compatibility
            - 📊 FHIR Compliance
            - 🔄 API Standards
            - 📱 Mobile Integration
        """)

def show_admin_dashboard():
    st.title("Admin Dashboard")
    
    tabs = st.tabs([
        "App Certification",
        "Platform Management",
        "Analytics"
    ])
    
    with tabs[0]:
        st.header("Digital Therapeutics Certification Management")
        
        # Add new app with certification
        with st.form("certify_app"):
            st.subheader("New App Certification")
            
            col1, col2 = st.columns(2)
            with col1:
                name = st.text_input("App Name")
                developer = st.text_input("Developer")
                category = st.selectbox("Category", [
                    "Mental Health",
                    "Chronic Disease",
                    "Sleep",
                    "Pain Management"
                ])
            
            with col2:
                fda_status = st.selectbox("FDA Status", [
                    "FDA Cleared",
                    "FDA Registered",
                    "FDA Pending"
                ])
                hipaa = st.checkbox("HIPAA Compliant")
                ce_marked = st.checkbox("CE Marked")
            
            st.subheader("Certification Scores")
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                clinical = st.slider("Clinical Evidence", 0.0, 5.0, 4.0)
            with col2:
                ux = st.slider("User Experience", 0.0, 5.0, 4.0)
            with col3:
                security = st.slider("Security", 0.0, 5.0, 4.0)
            with col4:
                integration = st.slider("Integration", 0.0, 5.0, 4.0)
            
            clinical_studies = st.text_area("Clinical Studies Evidence")
            certification_details = st.text_area("Additional Certification Details")
            
            if st.form_submit_button("Certify App"):
                # Add app to database with certification details
                pass
    
    with tabs[1]:
        st.header("Platform Management")
        
        col1, col2 = st.columns(2)
        with col1:
            st.subheader("User Management")
            # User management interface
            
        with col2:
            st.subheader("System Settings")
            # System settings interface
    
    with tabs[2]:
        st.header("Platform Analytics")
        show_platform_analytics()

def show_platform_analytics():
    """Enhanced analytics display"""
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
            <div class="metric-card">
                <h3>Users</h3>
                <h2>1,234</h2>
                <p>↑ 12% this month</p>
            </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
            <div class="metric-card">
                <h3>Certified Apps</h3>
                <h2>45</h2>
                <p>↑ 5 new this month</p>
            </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
            <div class="metric-card">
                <h3>Active Prescriptions</h3>
                <h2>892</h2>
                <p>↑ 8% this month</p>
            </div>
        """, unsafe_allow_html=True)
    
    # Add more analytics visualizations...
    [Previous analytics code with enhanced styling...]

def main():
    init_db()
    
    # Enhanced sidebar
    with st.sidebar:
        st.title("🏥 Beacon Health")
        st.write("Digital Therapeutics Platform")
        
        role = st.selectbox(
            "Select Role",
            ["Patient", "Provider", "Admin"],
            format_func=lambda x: f"📋 {x}"
        )
        
        st.markdown("---")
        st.info("Demo Mode: Roles can be switched freely")
        
        if st.button("About Platform"):
            st.write("""
                Beacon Health is a certified digital therapeutics 
                marketplace connecting providers and patients with 
                validated health applications.
            """)
    
    # Main content based on role
    if role == "Patient":
        show_patient_experience()
    elif role == "Provider":
        show_provider_experience()
    else:
        show_admin_dashboard()

if __name__ == "__main__":
    main()
