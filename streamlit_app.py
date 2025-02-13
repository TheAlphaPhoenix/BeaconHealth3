import streamlit as st
import pandas as pd
from datetime import datetime, timedelta

# Initialize session state for demo data
if 'initialized' not in st.session_state:
    st.session_state.apps = pd.DataFrame([
        {
            'id': 1,
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
            'certification_details': 'FDA Class II Medical Device, HIPAA Certified',
            'clinical_studies': '4 RCTs, 8 Peer-reviewed publications',
            'integration_details': 'Epic, Cerner, Dexcom'
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
            'certification_details': 'FDA Registered, HIPAA Compliant',
            'clinical_studies': '2 RCTs, 4 Peer-reviewed publications',
            'integration_details': 'Apple Health, Google Fit'
        }
    ])
    
    st.session_state.prescriptions = pd.DataFrame([
        {
            'id': 1,
            'app_name': 'DiabetesGuard',
            'prescribed_by': 'Dr. Smith',
            'prescribed_to': 'Demo Patient',
            'status': 'Active',
            'prescribed_date': datetime.now() - timedelta(days=30)
        },
        {
            'id': 2,
            'app_name': 'MindfulPath',
            'prescribed_by': 'Dr. Johnson',
            'prescribed_to': 'Demo Patient',
            'status': 'Active',
            'prescribed_date': datetime.now() - timedelta(days=15)
        }
    ])
    
    st.session_state.messages = pd.DataFrame([
        {
            'id': 1,
            'sender_role': 'provider',
            'recipient_role': 'patient',
            'subject': 'DiabetesGuard Progress',
            'message': 'How are you finding the glucose tracking features?',
            'app_name': 'DiabetesGuard',
            'date': datetime.now() - timedelta(days=2)
        },
        {
            'id': 2,
            'sender_role': 'patient',
            'recipient_role': 'provider',
            'subject': 'MindfulPath Question',
            'message': 'When is the best time to use the meditation exercises?',
            'app_name': 'MindfulPath',
            'date': datetime.now() - timedelta(days=1)
        }
    ])
    
    st.session_state.initialized = True

def show_app_card(app, for_patient=True):
    with st.container():
        st.markdown(f"""
            <div style="padding: 20px; border: 1px solid #ddd; border-radius: 10px; margin-bottom: 20px;">
                <h3>{app['name']}</h3>
                <p><strong>Category:</strong> {app['category']}</p>
                <p>{app['description']}</p>
            </div>
        """, unsafe_allow_html=True)
        
        col1, col2 = st.columns([2,1])
        
        with col1:
            st.write("#### Certification Status")
            st.markdown(f"""
                - 🏆 {app['fda_status']}
                - 🔒 HIPAA Compliant
                - ⭐ Overall Score: {app['overall_score']}/5.0
            """)
            
            with st.expander("Clinical Evidence"):
                st.write(app['clinical_studies'])
            
            with st.expander("Integration Details"):
                st.write(app['integration_details'])
        
        with col2:
            st.write("#### Trust Scores")
            st.metric("Clinical", f"{app['clinical_score']}/5.0")
            st.metric("Security", f"{app['security_score']}/5.0")
            
            if for_patient:
                if st.button("Request Access", key=f"request_{app['id']}"):
                    st.success("Request sent to your healthcare provider")
            else:
                if st.button("Prescribe", key=f"prescribe_{app['id']}"):
                    st.success(f"Prescribed {app['name']}")

def show_patient_dashboard():
    st.title("Patient Dashboard")
    
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
                with col2:
                    st.button("Launch App", key=f"launch_{app['id']}")
                    st.button("Message Provider", key=f"msg_{app['id']}")
    
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
            show_app_card(app, for_patient=True)
    
    with tabs[2]:
        st.header("Messages")
        # New Message
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
                        'date': datetime.now()
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
                st.write(f"**From:** {msg['sender_role'].capitalize()}")
                st.write(f"**To:** {msg['recipient_role'].capitalize()}")
                if msg['app_name']:
                    st.write(f"**Related App:** {msg['app_name']}")
                st.write(f"**Message:** {msg['message']}")

def show_provider_dashboard():
    st.title("Provider Dashboard")
    
    tabs = st.tabs(["Patients", "Prescribe Apps", "Messages"])
    
    with tabs[0]:
        st.header("My Patients")
        patients = [
            {"name": "John Smith", "age": 45, "condition": "Type 2 Diabetes"},
            {"name": "Sarah Johnson", "age": 32, "condition": "Anxiety"},
            {"name": "Michael Chen", "age": 58, "condition": "Hypertension"}
        ]
        
        for patient in patients:
            with st.expander(f"{patient['name']} - Age {patient['age']}"):
                st.write(f"**Condition:** {patient['condition']}")
                col1, col2 = st.columns(2)
                with col1:
                    st.button("View Details", key=f"view_{patient['name']}")
                with col2:
                    st.button("Prescribe App", key=f"prescribe_to_{patient['name']}")
    
    with tabs[1]:
        st.header("Prescribe Digital Therapeutics")
        for _, app in st.session_state.apps.iterrows():
            show_app_card(app, for_patient=False)
    
    with tabs[2]:
        st.header("Messages")
        show_messages("provider")

def show_admin_dashboard():
    st.title("Admin Dashboard")
    
    tabs = st.tabs(["App Management", "Analytics"])
    
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
            
            if st.form_submit_button("Add App"):
                st.success("App added successfully!")
    
    with tabs[1]:
        st.header("Platform Analytics")
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Total Apps", len(st.session_state.apps))
            st.metric("Active Prescriptions", len(st.session_state.prescriptions))
        with col2:
            st.metric("FDA Cleared Apps", 
                     len(st.session_state.apps[st.session_state.apps['fda_status'] == 'FDA Cleared']))
            st.metric("Total Messages", len(st.session_state.messages))
        with col3:
            st.metric("Avg Clinical Score", 
                     f"{st.session_state.apps['clinical_score'].mean():.1f}")
            st.metric("Avg Engagement", "87%")

def show_messages(role):
    # New Message
    with st.expander("New Message"):
        with st.form("new_message_provider"):
            subject = st.text_input("Subject")
            message = st.text_area("Message")
            app = st.selectbox("Related App", ["None"] + list(st.session_state.apps['name']))
            
            if st.form_submit_button("Send Message"):
                st.success("Message sent!")
    
    # Message History
    st.subheader("Message History")
    role_messages = st.session_state.messages[
        (st.session_state.messages['sender_role'] == role) |
        (st.session_state.messages['recipient_role'] == role)
    ]
    
    for _, msg in role_messages.iterrows():
        with st.expander(f"{msg['subject']} - {msg['date'].strftime('%Y-%m-%d %H:%M')}"):
            st.write(f"**From:** {msg['sender_role'].capitalize()}")
            st.write(f"**To:** {msg['recipient_role'].capitalize()}")
            if msg['app_name']:
                st.write(f"**Related App:** {msg['app_name']}")
            st.write(f"**Message:** {msg['message']}")

def main():
    st.set_page_config(
        page_title="Beacon Health",
        page_icon="🏥",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    # Custom CSS
    st.markdown("""
        <style>
        .main {padding:
        import streamlit as st
import pandas as pd
from datetime import datetime, timedelta

# Initialize session state for demo data
if 'initialized' not in st.session_state:
    st.session_state.apps = pd.DataFrame([
        {
            'id': 1,
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
            'certification_details': 'FDA Class II Medical Device, HIPAA Certified',
            'clinical_studies': '4 RCTs, 8 Peer-reviewed publications',
            'integration_details': 'Epic, Cerner, Dexcom'
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
            'certification_details': 'FDA Registered, HIPAA Compliant',
            'clinical_studies': '2 RCTs, 4 Peer-reviewed publications',
            'integration_details': 'Apple Health, Google Fit'
        }
    ])
    
    st.session_state.prescriptions = pd.DataFrame([
        {
            'id': 1,
            'app_name': 'DiabetesGuard',
            'prescribed_by': 'Dr. Smith',
            'prescribed_to': 'Demo Patient',
            'status': 'Active',
            'prescribed_date': datetime.now() - timedelta(days=30)
        },
        {
            'id': 2,
            'app_name': 'MindfulPath',
            'prescribed_by': 'Dr. Johnson',
            'prescribed_to': 'Demo Patient',
            'status': 'Active',
            'prescribed_date': datetime.now() - timedelta(days=15)
        }
    ])
    
    st.session_state.messages = pd.DataFrame([
        {
            'id': 1,
            'sender_role': 'provider',
            'recipient_role': 'patient',
            'subject': 'DiabetesGuard Progress',
            'message': 'How are you finding the glucose tracking features?',
            'app_name': 'DiabetesGuard',
            'date': datetime.now() - timedelta(days=2)
        },
        {
            'id': 2,
            'sender_role': 'patient',
            'recipient_role': 'provider',
            'subject': 'MindfulPath Question',
            'message': 'When is the best time to use the meditation exercises?',
            'app_name': 'MindfulPath',
            'date': datetime.now() - timedelta(days=1)
        }
    ])
    
    st.session_state.initialized = True

def show_app_card(app, for_patient=True):
    with st.container():
        st.markdown(f"""
            <div style="padding: 20px; border: 1px solid #ddd; border-radius: 10px; margin-bottom: 20px;">
                <h3>{app['name']}</h3>
                <p><strong>Category:</strong> {app['category']}</p>
                <p>{app['description']}</p>
            </div>
        """, unsafe_allow_html=True)
        
        col1, col2 = st.columns([2,1])
        
        with col1:
            st.write("#### Certification Status")
            st.markdown(f"""
                - 🏆 {app['fda_status']}
                - 🔒 HIPAA Compliant
                - ⭐ Overall Score: {app['overall_score']}/5.0
            """)
            
            with st.expander("Clinical Evidence"):
                st.write(app['clinical_studies'])
            
            with st.expander("Integration Details"):
                st.write(app['integration_details'])
        
        with col2:
            st.write("#### Trust Scores")
            st.metric("Clinical", f"{app['clinical_score']}/5.0")
            st.metric("Security", f"{app['security_score']}/5.0")
            
            if for_patient:
                if st.button("Request Access", key=f"request_{app['id']}"):
                    st.success("Request sent to your healthcare provider")
            else:
                if st.button("Prescribe", key=f"prescribe_{app['id']}"):
                    st.success(f"Prescribed {app['name']}")

def show_patient_dashboard():
    st.title("Patient Dashboard")
    
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
                with col2:
                    st.button("Launch App", key=f"launch_{app['id']}")
                    st.button("Message Provider", key=f"msg_{app['id']}")
    
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
            show_app_card(app, for_patient=True)
    
    with tabs[2]:
        st.header("Messages")
        # New Message
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
                        'date': datetime.now()
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
                st.write(f"**From:** {msg['sender_role'].capitalize()}")
                st.write(f"**To:** {msg['recipient_role'].capitalize()}")
                if msg['app_name']:
                    st.write(f"**Related App:** {msg['app_name']}")
                st.write(f"**Message:** {msg['message']}")

def show_provider_dashboard():
    st.title("Provider Dashboard")
    
    tabs = st.tabs(["Patients", "Prescribe Apps", "Messages"])
    
    with tabs[0]:
        st.header("My Patients")
        patients = [
            {"name": "John Smith", "age": 45, "condition": "Type 2 Diabetes"},
            {"name": "Sarah Johnson", "age": 32, "condition": "Anxiety"},
            {"name": "Michael Chen", "age": 58, "condition": "Hypertension"}
        ]
        
        for patient in patients:
            with st.expander(f"{patient['name']} - Age {patient['age']}"):
                st.write(f"**Condition:** {patient['condition']}")
                col1, col2 = st.columns(2)
                with col1:
                    st.button("View Details", key=f"view_{patient['name']}")
                with col2:
                    st.button("Prescribe App", key=f"prescribe_to_{patient['name']}")
    
    with tabs[1]:
        st.header("Prescribe Digital Therapeutics")
        for _, app in st.session_state.apps.iterrows():
            show_app_card(app, for_patient=False)
    
    with tabs[2]:
        st.header("Messages")
        show_messages("provider")

def show_admin_dashboard():
    st.title("Admin Dashboard")
    
    tabs = st.tabs(["App Management", "Analytics"])
    
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
            
            if st.form_submit_button("Add App"):
                st.success("App added successfully!")
    
    with tabs[1]:
        st.header("Platform Analytics")
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Total Apps", len(st.session_state.apps))
            st.metric("Active Prescriptions", len(st.session_state.prescriptions))
        with col2:
            st.metric("FDA Cleared Apps", 
                     len(st.session_state.apps[st.session_state.apps['fda_status'] == 'FDA Cleared']))
            st.metric("Total Messages", len(st.session_state.messages))
        with col3:
            st.metric("Avg Clinical Score", 
                     f"{st.session_state.apps['clinical_score'].mean():.1f}")
            st.metric("Avg Engagement", "87%")

def show_messages(role):
    # New Message
    with st.expander("New Message"):
        with st.form("new_message_provider"):
            subject = st.text_input("Subject")
            message = st.text_area("Message")
            app = st.selectbox("Related App", ["None"] + list(st.session_state.apps['name']))
            
            if st.form_submit_button("Send Message"):
                st.success("Message sent!")
    
    # Message History
    st.subheader("Message History")
    role_messages = st.session_state.messages[
        (st.session_state.messages['sender_role'] == role) |
        (st.session_state.messages['recipient_role'] == role)
    ]
    
    for _, msg in role_messages.iterrows():
        with st.expander(f"{msg['subject']} - {msg['date'].strftime('%Y-%m-%d %H:%M')}"):
            st.write(f"**From:** {msg['sender_role'].capitalize()}")
            st.write(f"**To:** {msg['recipient_role'].capitalize()}")
            if msg['app_name']:
                st.write(f"**Related App:** {msg['app_name']}")
            st.write(f"**Message:** {msg['message']}")

def main():
    st.set_page_config(
        page_title="Beacon Health",
        page_icon="🏥",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    # Custom CSS
    st.markdown("""
        <style>
        .main {padding: 0rem 1rem;}
        .stTabs {
            background-color: #f8f9fa;
            padding: 1rem;
            border-radius: 5px;
            margin-bottom: 1rem;
        }
        .stButton > button {
            width: 100%;
            background-color: #2196F3;
            color: white;
        }
        .stButton > button:hover {
            background-color: #1976D2;
        }
        .metric-card {
            background-color: white;
            padding: 1.5rem;
            border-radius: 10px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            margin-bottom: 1rem;
        }
        .certification-badge {
            background-color: #e3f2fd;
            border-left: 4px solid #2196F3;
            padding: 1rem;
            margin: 1rem 0;
            border-radius: 0 5px 5px 0;
        }
        .app-card {
            background-color: white;
            padding: 1.5rem;
            border-radius: 10px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            margin: 1rem 0;
            border: 1px solid #e0e0e0;
        }
        .score-pill {
            background-color: #4CAF50;
            color: white;
            padding: 0.2rem 0.5rem;
            border-radius: 15px;
            font-size: 0.9rem;
            display: inline-block;
        }
        </style>
    """, unsafe_allow_html=True)

    # Sidebar for navigation
    with st.sidebar:
        st.title("🏥 Beacon Health")
        st.write("Digital Therapeutics Platform")
        
        role = st.selectbox(
            "Select Role",
            ["Patient", "Provider", "Admin"],
            help="Switch between different user roles"
        )
        
        st.markdown("---")
        
        # Role-specific sidebar content
        if role == "Patient":
            st.info("Patient View: Browse and manage your digital therapeutic apps")
        elif role == "Provider":
            st.info("Provider View: Prescribe and monitor digital therapeutics")
        else:
            st.info("Admin View: Manage apps and platform analytics")
        
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

