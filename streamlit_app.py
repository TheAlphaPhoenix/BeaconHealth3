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
    
    # Messages table
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
    
    # Prescriptions table
    c.execute('''
        CREATE TABLE IF NOT EXISTS prescriptions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            app_name TEXT NOT NULL,
            prescribed_by TEXT NOT NULL,
            prescribed_to TEXT NOT NULL,
            status TEXT NOT NULL,
            prescribed_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Insert demo apps if table is empty
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
            {
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
                'certification_details': 'FDA Class II Medical Device, HIPAA, GDPR',
                'clinical_studies': '4 RCTs, 8 Peer-reviewed publications',
                'integration_details': 'Epic, Cerner, Dexcom'
            },
            {
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
                'certification_details': 'FDA Registered, HIPAA, GDPR',
                'clinical_studies': '2 RCTs, 4 Peer-reviewed publications',
                'integration_details': 'Apple Health, Google Fit'
            }
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
        
        # Insert demo prescriptions
        demo_prescriptions = [
            ('DiabetesGuard', 'Dr. Smith', 'Demo Patient', 'Active'),
            ('MindfulPath', 'Dr. Johnson', 'Demo Patient', 'Active'),
            ('SleepHarmony', 'Dr. Smith', 'Demo Patient', 'Pending')
        ]
        
        c.executemany('''
            INSERT INTO prescriptions (app_name, prescribed_by, prescribed_to, status)
            VALUES (?, ?, ?, ?)
        ''', demo_prescriptions)
        
        # Insert demo messages
        demo_messages = [
            ('provider', 'patient', 'DiabetesGuard Progress', 
             'How are you finding the glucose tracking features?', 'DiabetesGuard'),
            ('patient', 'provider', 'Question about MindfulPath', 
             'When is the best time to use the meditation exercises?', 'MindfulPath'),
            ('provider', 'patient', 'SleepHarmony Update', 
             'Here is your sleep therapy prescription', 'SleepHarmony')
        ]
        
        c.executemany('''
            INSERT INTO messages (sender_role, recipient_role, subject, message, app_name)
            VALUES (?, ?, ?, ?, ?)
        ''', demo_messages)
    
    conn.commit()
    conn.close()

[Rest of the previous code remains the same...]
