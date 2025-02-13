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
    .big-number {
        font-size: 2.5rem;
        font-weight: bold;
        color: #2196F3;
        text-align: center;
    }
    .metric-label {
        font-size: 1rem;
        color: #666;
        text-align: center;
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
        {
            'id': 2,
            'name': 'DiabetesGuard',
            'category': 'Chronic Disease',
            'description': 'Comprehensive diabetes management with CGM integration',
            'developer': 'HealthTech',
            'clinical_score': 4.9,
            'ux_score': 4.8,
            'security_score': 4.9,
            'integration_score': 4.7,
            'overall_score': 4.83,
            'fda_status': 'FDA Cleared',
            'ce_status': 'CE Marked',
            'hipaa_compliant': True,
            'price_model': 'Insurance',
            'monthly_price': 79.99,
            'certification_details': 'FDA Class II Medical Device, HIPAA Certified',
            'clinical_studies': '4 RCTs, 8 Peer-reviewed publications',
            'integration_details': 'Epic, Cerner, Dexcom',
            'active_users': 25000,
            'avg_satisfaction': 4.8
        },
        {
            'id': 3,
            'name': 'SleepHarmony',
            'category': 'Sleep',
            'description': 'Advanced sleep therapy using cognitive behavioral techniques',
            'developer': 'DreamTech',
            'clinical_score': 4.7,
            'ux_score': 4.9,
            'security_score': 4.8,
            'integration_score': 4.5,
            'overall_score': 4.73,
            'fda_status': 'FDA Registered',
            'ce_status': 'CE Marked',
            'hipaa_compliant': True,
            'price_model': 'Freemium',
            'monthly_price': 0,
            'certification_details': 'FDA Registered, HIPAA Compliant',
            'clinical_studies': '2 RCTs, 4 Peer-reviewed publications',
            'integration_details': 'Apple Health, Google Fit',
            'active_users': 10000,
            'avg_satisfaction': 4.6
        }
    ])
    
    # Generate 30 days of usage data
    dates = [datetime.now() - timedelta(days=x) for x in range(30)]
    st.session_state.usage_data = pd.DataFrame({
        'date': dates,
        'daily_active_users': [random.randint(800, 1200) for _ in range(30)],
        'prescriptions_made': [random.randint(50, 150) for _ in range(30)],
        'messages_sent': [random.randint(200, 500) for _ in range(30)]
    })
    
    # Set up demo prescriptions
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
        {
            'id': 2,
            'app_name': 'MindfulPath',
            'prescribed_by': 'Dr. James Wilson',
            'prescribed_to': 'Sarah Chen',
            'status': 'Active',
            'prescribed_date': datetime.now() - timedelta(days=15),
            'next_review': datetime.now() + timedelta(days=75),
            'notes': 'Daily meditation and mood tracking',
            'adherence_rate': 92
        }
    ])
    
    # Set up demo messages
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
        {
            'id': 2,
            'sender_role': 'patient',
            'recipient_role': 'provider',
            'subject': 'Question about meditation timing',
            'message': 'Is it better to do the exercises in the morning or evening?',
            'app_name': 'MindfulPath',
            'date': datetime.now() - timedelta(days=1),
            'priority': 'Normal',
            'read_status': False
        }
    ])
    
    st.session_state.initialized = True

def show_app_card(app):
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
            st.write("#### Scores")
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
            
        with col2:
            st.write("#### Certifications")
            st.markdown(f"""
                <div style="padding: 8px; background-color: #E3F2FD; border-radius: 5px; margin-bottom: 8px;">
                    ✓ {app['fda_status']}
                </div>
                <div style="padding: 8px; background-color: #E3F2FD; border-radius: 5px; margin-bottom: 8px;">
                    ✓ {app['ce_status']}
                </div>
                <div style="padding: 8px; background-color: #E3F2FD; border-radius: 5px;">
                    ✓ HIPAA Compliant
                </div>
            """, unsafe_allow_html=True)
                
        with col3:
            st.write("#### Actions")
            st.button("View Details", key=f"view_{app['id']}")
            if st.button("Request Access", key=f"request_{app['id']}"):
                st.success(f"Access request for {app['name']} sent to your provider!")

def show_patient_dashboard():
    st.title("🏥 Patient Dashboard")
    
    # Quick stats at the top
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown("""
            <div class="metric-container">
                <div class="big-number">2</div>
                <div class="metric-label">Active Prescriptions</div>
            </div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown("""
            <div class="metric-container">
                <div class="big-number">85%</div>
                <div class="metric-label">Average Adherence</div>
            </div>
        """, unsafe_allow_html=True)
    with col3:
        st.markdown("""
            <div class="metric-container">
                <div class="big-number">7 days</div>
                <div class="metric-label">Until Next Review</div>
            </div>
        """, unsafe_allow_html=True)

    # Main dashboard tabs
    tabs = st.tabs(["My Apps", "Browse Apps", "Messages"])
    
    with tabs[0]:
        st.header("My Digital Therapeutics")
        for _, prescription in st.session_state.prescriptions.iterrows():
            app = st.session_state.apps[st.session_state.apps['name'] == prescription['app_name']].iloc[0]
            with st.expander(f"{app['name']} - Prescribed by {prescription['prescribed_by']}"):
                col1, col2 = st.columns([2,1])
                with col1:
                    st.write(f"**Description:** {app['description']}")
                    st.write(f"**Status:** {prescription['status']}")
                    st.write(f"**Prescribed Date:** {prescription['prescribed_date'].strftime('%Y-%m-%d')}")
                    st.write(f"**Next Review:** {prescription['next_review'].strftime('%Y-%m-%d')}")
                    st.progress(prescription['adherence_rate'] / 100)
                    st.write(f"Adherence Rate: {prescription['adherence_rate']}%")
                with col2:
                    st.button("Launch App", key=f"launch_{app['id']}")
                    if st.button("Message Provider", key=f"msg_{app['id']}"):
                        st.info(f"Opening message composer for {app['name']}...")
    
    with tabs[1]:
        st.header("Browse Digital Therapeutics")
        # Filters
        col1, col2 = st.columns(2)
        with col1:
            category = st.selectbox(
                "Category",
                ["All"] + list(st.session_state.apps['category'].unique())
            )
        with col2:
            fda_status = st.selectbox(
                "FDA Status",
                ["All"] + list(st.session_state.apps['fda_status'].unique())
            )
        
        filtered_apps = st.session_state.apps
        if category != "All":
            filtered_apps = filtered_apps[filtered_apps['category'] == category]
        if fda_status != "All":
            filtered_apps = filtered_apps[filtered_apps['fda_status'] == fda_status]
        
        for _, app in filtered_apps.iterrows():
            show_app_card(app)
    
    with tabs[2]:
        st.header("Messages")
        # New Message Form
        with st.expander("New Message"):
            with st.form("new_message"):
                subject = st.text_input("Subject")
                message = st.text_area("Message")
                app = st.selectbox("Related App", ["None"] + list(st.session_state.apps['name']))
                
                if st.form_submit_button("Send Message"):
                    new_message = {
                        'id': len(st.session_state.messages) + 1,
                        'sender_role': 'patient',
                        'recipient_role': 'provider',
                        'subject': subject,
                        'message': message,
                        'app_name': app if app != "None" else None,
                        'date': datetime.now(),
                        'priority': 'Normal',
                        'read_status': False
                    }
                    st.session_state.messages = pd.concat([
                        st.session_state.messages,
                        pd.DataFrame([new_message])
                    ], ignore_index=True)
                    st.success("Message sent!")
        
        # Message History
        st.subheader("Message History")
        patient_messages = st.session_state.messages[
            (st.session_state.messages['sender_role'] == 'patient') |
            (st.session_state.messages['recipient_role'] == 'patient')
        ]
        
        for _, msg in patient_messages.iterrows():
            with st.expander(f"{msg['subject']} - {msg['date'].strftime('%Y-%m-%d %H:%M')}"):
                st.markdown(f"""
                    <div style='background-color: {"#E3F2FD" if msg["read_status"] else "#FFF3E0"}; padding: 1rem; border-radius: 5px;'>
                        <strong>From:</strong> {msg['sender_role'].capitalize()}<br>
                        <strong>To:</strong> {msg['recipient_role'].capitalize()}<br>
                        {f"<strong>Related App:</strong> {msg['app_name']}<br>" if msg['app_name'] else ""}
                        <strong>Priority:</strong> {msg['priority']}<br>
                        <div style='margin-top: 10px;'>{msg['message']}</div>
                    </div>
                """, unsafe_allow_html=True)

def show_provider_dashboard():
    st.title("👩‍⚕️ Provider Dashboard")
    
    # Quick stats for provider
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown("""
            <div class="metric-container">
                <div class="big-number">12</div>
                <div class="metric-label">Active Patients</div>
            </div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown("""
            <div class="metric-container">
                <div class="big-number">8</div>
                <div class="metric-label">Active Prescriptions</div>
            </div>
        """, unsafe_allow_html=True)
    with col3:
        st.markdown("""
            <div class="metric-container">
                <div class="big-number">3</div>
                <div class="metric-label">Pending Reviews</div>
            </div>
        """, unsafe_allow_html=True)

    # Main dashboard tabs
    tabs = st.tabs(["Patients", "Prescribe Apps", "Messages"])
    
    with tabs[0]:
        st.header("My Patients")
        # Demo patient data
        patients = [
            {
                "name": "John Davis",
                "age": 45,
                "condition": "Type 2 Diabetes",
                "prescribed_apps": ["DiabetesGuard"],
                "last_check": "2024-02-01",
                "adherence": 85
            },
            {
                "name": "Sarah Chen",
                "age": 32,
                "condition": "Anxiety",
                "prescribed_apps": ["MindfulPath"],
                "last_check": "2024-02-10",
                "adherence": 92
            },
            {
                "name": "Michael Brown",
                "age": 58,
                "condition": "Insomnia",
                "prescribed_apps": ["SleepHarmony"],
                "last_check": "2024-02-05",
                "adherence": 78
            }
        ]
        
        for patient in patients:
            with st.expander(f"{patient['name']} - Age {patient['age']}"):
                col1, col2 = st.columns([2,1])
                with col1:
                    st.write(f"**Condition:** {patient['condition']}")
                    st.write(f"**Prescribed Apps:** {', '.join(patient['prescribed_apps'])}")
                    st.write(f"**Last Check:** {patient['last_check']}")
                    st.progress(patient['adherence'] / 100)
                    st.write(f"Overall Adherence: {patient['adherence']}%")
                with col2:
                    st.button("View Details", key=f"view_{patient['name']}")
                    if st.button("Send Message", key=f"msg_to_{patient['name']}"):
                        st.info(f"Opening message composer for {patient['name']}...")
    
    with tabs[1]:
        st.header("Prescribe Digital Therapeutics")
        # App filters
        col1, col2 = st.columns(2)
        with col1:
            category_filter = st.selectbox(
                "Filter by Category",
                ["All"] + list(st.session_state.apps['category'].unique())
            )
        with col2:
            status_filter = st.selectbox(
                "Filter by FDA Status",
                ["All"] + list(st.session_state.apps['fda_status'].unique())
            )
        
        filtered_apps = st.session_state.apps
        if category_filter != "All":
            filtered_apps = filtered_apps[filtered_apps['category'] == category_filter]
        if status_filter != "All":
            filtered_apps = filtered_apps[filtered_apps['fda_status'] == status_filter]
        
        for _, app in filtered_apps.iterrows():
            show_app_card(app)
    
    with tabs[2]:
        st.header("Messages")
        show_messages("provider")

def show_admin_dashboard():
    st.title("⚙️ Admin Dashboard")
    
    # Quick stats for admin
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown("""
            <div class="metric-container">
                <div class="big-number">3</div>
                <div class="metric-label">Total Apps</div>
            </div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown("""
            <div class="metric-container">
                <div class="big-number">85%</div>
                <div class="metric-label">Platform Uptime</div>
            </div>
        """, unsafe_allow_html=True)
    with col3:
        st.markdown("""
            <div class="metric-container">
                <div class="big-number">50K</div>
                <div class="metric-label">Total Users</div>
            </div>
        """, unsafe_allow_html=True)

    # Main dashboard tabs
    tabs = st.tabs(["App Management", "Analytics", "System Status"])
    
    with tabs[0]:
        st.header("Digital Therapeutics Management")
        
        with st.form("add_app"):
            st.subheader("Add New App")
            col1, col2 = st.columns(2)
            
            with col1:
                name = st.text_input("App Name")
                category = st.selectbox("Category", [
                    "Mental Health",
                    "Chronic Disease",
                    "Sleep",
                    "Pain Management"
                ])
                description = st.text_area("Description")
                developer = st.text_input("Developer")
            
            with col2:
                clinical_score = st.slider("Clinical Evidence Score", 0.0, 5.0, 4.0)
                fda_status = st.selectbox("FDA Status", [
                    "FDA Cleared",
                    "FDA Registered",
                    "FDA Pending"
                ])
                price_model = st.selectbox("Price Model", [
                    "Free",
                    "Subscription",
                    "Insurance"
                ])
                monthly_price = st.number_input("Monthly Price", min_value=0.0, value=49.99)
            
            if st.form_submit_button("Add App"):
                st.success("App added successfully!")
                st.balloons()
    
    with tabs[1]:
        st.header("Platform Analytics")
        
        # Usage trends
        st.subheader("Usage Trends")
        usage_df = st.session_state.usage_data
        st.line_chart(usage_df.set_index('date')['daily_active_users'])
        
        # App performance
        st.subheader("App Performance")
        app_metrics = st.session_state.apps[['name', 'clinical_score', 'ux_score', 'security_score']]
        st.bar_chart(app_metrics.set_index('name'))
    
    with tabs[2]:
        st.header("System Status")
        col1, col2 = st.columns(2)
        with col1:
            st.metric("API Response Time", "120ms", "-10ms")
            st.metric("Database Load", "42%", "5%")
        with col2:
            st.metric("Error Rate", "0.02%", "-0.01%")
            st.metric("Storage Usage", "68%", "2%")

def show_messages(role):
    # New Message
    with st.expander("New Message"):
        with st.form("new_message_provider"):
            subject = st.text_input("Subject")
            message = st.text_area("Message")
            recipient = st.selectbox("Recipient", ["John Davis", "Sarah Chen", "Michael Brown"])
            app = st.selectbox("Related App", ["None"] + list(st.session_state.apps['name']))
            
            if st.form_submit_button("Send Message"):
                st.success("Message sent successfully!")
    
    # Message History
    st.subheader("Message History")
    role_messages = st.session_state.messages[
        (st.session_state.messages['sender_role'] == role) |
        (st.session_state.messages['recipient_role'] == role)
    ]
    
    for _, msg in role_messages.iterrows():
        with st.expander(f"{msg['subject']} - {msg['date'].strftime('%Y-%m-%d %H:%M')}"):
            st.markdown(f"""
                <div style='background-color: {"#E3F2FD" if msg["read_status"] else "#FFF3E0"}; padding: 1rem; border-radius: 5px;'>
                    <strong>From:</strong> {msg['sender_role'].capitalize()}<br>
                    <strong>To:</strong> {msg['recipient_role'].capitalize()}<br>
                    {f"<strong>Related App:</strong> {msg['app_name']}<br>" if msg['app_name'] else ""}
                    <strong>Priority:</strong> {msg['priority']}<br>
                    <div style='margin-top: 10px;'>{msg['message']}</div>
                </div>
            """, unsafe_allow_html=True)

def main():
    # Sidebar navigation
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
        
        st.markdown("---")
        
        # Role-specific sidebar content
        if role == "Patient":
            st.info("👤 Patient View: Browse and manage your digital therapeutic apps")
        elif role == "Provider":
            st.info("👩‍⚕️ Provider View: Prescribe and monitor digital therapeutics")
        else:
            st.info("⚙️ Admin View: Manage apps and platform analytics")
        
        st.markdown("---")
        st.caption("Demo Mode: Roles can be switched freely")
        
        # About section in sidebar
        with st.expander("About Beacon Health"):
            st.write("""
                Beacon Health is a certified digital therapeutics marketplace 
                connecting healthcare providers and patients with validated 
                health applications. Our platform ensures all apps meet strict 
                clinical evidence and security standards.
            """)
    
    # Main content based on selected role
    if role == "Patient":
        show_patient_dashboard()
    elif role == "Provider":
        show_provider_dashboard()
    else:
        show_admin_dashboard()

if __name__ == "__main__":
    main()
