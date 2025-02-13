import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
import sqlite3

def init_db():
    conn = sqlite3.connect('beacon_health.db')
    c = conn.cursor()
    
    # Create tables
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
    
    c.execute('''
        CREATE TABLE IF NOT EXISTS messages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            sender_role TEXT NOT NULL,
            recipient_role TEXT NOT NULL,
            subject TEXT NOT NULL,
            message TEXT NOT NULL,
            app_name TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    c.execute('''
        CREATE TABLE IF NOT EXISTS prescriptions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            app_name TEXT NOT NULL,
            prescribed_by TEXT NOT NULL,
            prescribed_to TEXT NOT NULL,
            status TEXT NOT NULL,
            notes TEXT,
            prescribed_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            follow_up_date TIMESTAMP
        )
    ''')
    
    # Check if apps table is empty
    if c.execute('SELECT COUNT(*) FROM apps').fetchone()[0] == 0:
        # Insert demo apps
        demo_apps = [
            ('MindfulPath', 'Mental Health', 'AI-powered CBT therapy platform', 
             'NeuroTech', 4.8, 4.7, 4.9, 4.6, 4.75, 'FDA Cleared', 'CE Marked', 1,
             'Subscription', 'FDA Class II, HIPAA, GDPR', '3 RCTs, 5 Publications', 
             'Epic, Cerner, Apple Health'),
            ('DiabetesGuard', 'Chronic Disease', 'Diabetes management with CGM integration', 
             'HealthTech', 4.9, 4.8, 4.9, 4.7, 4.83, 'FDA Cleared', 'CE Marked', 1,
             'Insurance', 'FDA Class II, HIPAA', '4 RCTs, 8 Publications', 
             'Epic, Cerner, Dexcom'),
            ('SleepHarmony', 'Sleep', 'Advanced sleep therapy', 
             'DreamTech', 4.7, 4.9, 4.8, 4.5, 4.73, 'FDA Registered', 'CE Marked', 1,
             'Freemium', 'FDA Registered, HIPAA', '2 RCTs, 4 Publications', 
             'Apple Health, Google Fit')
        ]
        
        c.executemany('''
            INSERT INTO apps (
                name, category, description, developer,
                clinical_score, ux_score, security_score,
                integration_score, overall_score,
                fda_status, ce_status, hipaa_compliant,
                price_model, certification_details,
                clinical_studies, integration_details
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', demo_apps)
        
        # Insert demo prescriptions
        demo_prescriptions = [
            ('DiabetesGuard', 'Dr. Smith', 'Demo Patient', 'Active', 
             'Initial prescription', datetime.now()),
            ('MindfulPath', 'Dr. Johnson', 'Demo Patient', 'Active',
             'For anxiety management', datetime.now()),
            ('SleepHarmony', 'Dr. Smith', 'Demo Patient', 'Pending',
             'For sleep improvement', datetime.now())
        ]
        
        c.executemany('''
            INSERT INTO prescriptions (
                app_name, prescribed_by, prescribed_to, status, notes, prescribed_date
            ) VALUES (?, ?, ?, ?, ?, ?)
        ''', demo_prescriptions)
    
    conn.commit()
    conn.close()

def show_patient_dashboard():
    st.title("Patient Dashboard")
    
    tabs = st.tabs(["My Apps", "Browse Apps", "Messages"])
    
    with tabs[0]:
        show_my_apps()
    
    with tabs[1]:
        show_app_directory(for_patient=True)
    
    with tabs[2]:
        show_messages("patient")

def show_provider_dashboard():
    st.title("Provider Dashboard")
    
    tabs = st.tabs(["Patients", "Prescribe Apps", "Messages"])
    
    with tabs[0]:
        show_patients()
    
    with tabs[1]:
        show_app_directory(for_patient=False)
    
    with tabs[2]:
        show_messages("provider")

def show_admin_dashboard():
    st.title("Admin Dashboard")
    
    tabs = st.tabs(["App Management", "User Management", "Analytics"])
    
    with tabs[0]:
        show_app_management()
    
    with tabs[1]:
        show_user_management()
    
    with tabs[2]:
        show_analytics()

def show_my_apps():
    st.header("My Digital Therapeutics")
    
    conn = sqlite3.connect('beacon_health.db')
    prescriptions = pd.read_sql('''
        SELECT p.*, a.description, a.clinical_score, a.fda_status 
        FROM prescriptions p 
        JOIN apps a ON p.app_name = a.name 
        WHERE prescribed_to = 'Demo Patient'
    ''', conn)
    conn.close()
    
    for _, app in prescriptions.iterrows():
        with st.expander(f"{app['app_name']} - Prescribed by {app['prescribed_by']}"):
            col1, col2 = st.columns([2,1])
            with col1:
                st.write(f"**Description:** {app['description']}")
                st.write(f"**Status:** {app['status']}")
                st.write(f"**Clinical Score:** {app['clinical_score']}/5.0")
                st.write(f"**FDA Status:** {app['fda_status']}")
            with col2:
                st.button("Launch App", key=f"launch_{app['id']}")
                st.button("Message Provider", key=f"msg_{app['id']}")

def show_app_directory(for_patient=True):
    st.header("Digital Therapeutics Directory")
    
    conn = sqlite3.connect('beacon_health.db')
    apps = pd.read_sql('SELECT * FROM apps', conn)
    conn.close()
    
    for _, app in apps.iterrows():
        with st.expander(f"{app['name']} - {app['category']}"):
            col1, col2 = st.columns([2,1])
            with col1:
                st.write(f"**Developer:** {app['developer']}")
                st.write(f"**Description:** {app['description']}")
                st.write(f"**Clinical Score:** {app['clinical_score']}/5.0")
                st.write(f"**FDA Status:** {app['fda_status']}")
                
                with st.expander("View Certification Details"):
                    st.write(f"**Clinical Studies:** {app['clinical_studies']}")
                    st.write(f"**Certification Details:** {app['certification_details']}")
                    st.write(f"**Integration Details:** {app['integration_details']}")
            
            with col2:
                if for_patient:
                    if st.button("Request Access", key=f"request_{app['id']}"):
                        st.success("Request sent to your healthcare provider")
                else:
                    if st.button("Prescribe", key=f"prescribe_{app['id']}"):
                        st.success(f"Prescribed {app['name']}")

def show_messages(role):
    st.header("Messages")
    
    with st.form("new_message"):
        subject = st.text_input("Subject")
        message = st.text_area("Message")
        if st.form_submit_button("Send Message"):
            st.success("Message sent!")

def show_patients():
    st.header("My Patients")
    
    patients = [
        {"name": "John Smith", "apps": 2, "status": "Active"},
        {"name": "Sarah Johnson", "apps": 1, "status": "Active"},
        {"name": "Michael Chen", "apps": 3, "status": "Active"}
    ]
    
    for patient in patients:
        with st.expander(patient["name"]):
            st.write(f"Active Apps: {patient['apps']}")
            st.write(f"Status: {patient['status']}")
            st.button("View Details", key=f"view_{patient['name']}")
            st.button("Prescribe App", key=f"prescribe_{patient['name']}")

def show_app_management():
    st.header("App Management")
    
    with st.form("add_app"):
        st.subheader("Add New App")
        name = st.text_input("App Name")
        category = st.selectbox("Category", ["Mental Health", "Chronic Disease", "Sleep"])
        clinical_score = st.slider("Clinical Score", 0.0, 5.0, 4.0)
        if st.form_submit_button("Add App"):
            st.success("App added successfully!")

def show_user_management():
    st.header("User Management")
    st.info("User management interface coming soon!")

def show_analytics():
    st.header("Analytics")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Total Apps", "6")
    with col2:
        st.metric("Active Users", "124")
    with col3:
        st.metric("Total Prescriptions", "45")

def main():
    st.set_page_config(page_title="Beacon Health", layout="wide")
    
    init_db()
    
    with st.sidebar:
        st.title("Beacon Health")
        role = st.selectbox("Select Role", ["Patient", "Provider", "Admin"])
        st.info("Demo Mode: Roles can be switched freely")
    
    if role == "Patient":
        show_patient_dashboard()
    elif role == "Provider":
        show_provider_dashboard()
    else:
        show_admin_dashboard()

if __name__ == "__main__":
    main()

