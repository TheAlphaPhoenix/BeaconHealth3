import streamlit as st
import sqlite3
import pandas as pd
from datetime import datetime

# Initialize and connect to SQLite database (cached for performance)
@st.cache_resource
def get_connection():
    return sqlite3.connect('beacon_health.db', check_same_thread=False)

conn = get_connection()
cursor = conn.cursor()

def init_db():
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS apps (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            description TEXT,
            category TEXT,
            fda_cleared TEXT,
            clinical_evidence_score REAL,
            user_experience_score REAL,
            security_compliance_score REAL,
            integration_capabilities_score REAL
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS prescriptions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            patient_name TEXT,
            provider_name TEXT,
            app_id INTEGER,
            prescription_date TEXT
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS messages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            sender TEXT,
            receiver TEXT,
            message TEXT,
            timestamp TEXT
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS progress (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            patient_name TEXT,
            app_id INTEGER,
            progress_percent INTEGER
        )
    ''')
    conn.commit()

def load_demo_data():
    df_apps = pd.read_sql_query("SELECT * FROM apps", conn)
    if df_apps.empty:
        apps_demo = [
            ("MindRelax", "A mindfulness and meditation app.", "Mental Health", "FDA Cleared", 4.5, 4.2, 4.8, 4.0),
            ("FitTrack", "A fitness and activity tracking app.", "Wellness", "Pending", 4.0, 4.0, 4.5, 3.8),
            ("SleepWell", "An app to improve sleep quality.", "Sleep Health", "FDA Cleared", 4.8, 4.6, 4.9, 4.5)
        ]
        cursor.executemany('''
            INSERT INTO apps (name, description, category, fda_cleared, clinical_evidence_score, user_experience_score, security_compliance_score, integration_capabilities_score)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', apps_demo)
        conn.commit()

    df_prescriptions = pd.read_sql_query("SELECT * FROM prescriptions", conn)
    if df_prescriptions.empty:
        prescriptions_demo = [
            ("John Doe", "Dr. Smith", 1, datetime.now().strftime("%Y-%m-%d")),
            ("John Doe", "Dr. Adams", 3, datetime.now().strftime("%Y-%m-%d"))
        ]
        cursor.executemany('''
            INSERT INTO prescriptions (patient_name, provider_name, app_id, prescription_date)
            VALUES (?, ?, ?, ?)
        ''', prescriptions_demo)
        conn.commit()

    df_progress = pd.read_sql_query("SELECT * FROM progress", conn)
    if df_progress.empty:
        progress_demo = [
            ("John Doe", 1, 50),
            ("John Doe", 3, 70)
        ]
        cursor.executemany('''
            INSERT INTO progress (patient_name, app_id, progress_percent)
            VALUES (?, ?, ?)
        ''', progress_demo)
        conn.commit()

    df_messages = pd.read_sql_query("SELECT * FROM messages", conn)
    if df_messages.empty:
        messages_demo = [
            ("John Doe", "Dr. Smith", "I have some questions about my prescription.", datetime.now().strftime("%Y-%m-%d %H:%M:%S")),
            ("Dr. Smith", "John Doe", "Sure, feel free to ask!", datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        ]
        cursor.executemany('''
            INSERT INTO messages (sender, receiver, message, timestamp)
            VALUES (?, ?, ?, ?)
        ''', messages_demo)
        conn.commit()

init_db()
load_demo_data()

# Custom CSS for a modern UI look
st.markdown(
    """
    <style>
    .stButton>button {
        background-color: #4CAF50;
        color: white;
        border: none;
        border-radius: 4px;
        padding: 10px 20px;
        font-size: 16px;
    }
    .stTextInput>div>input, .stTextArea>div>textarea {
        padding: 10px;
        border: 1px solid #ccc;
        border-radius: 4px;
    }
    </style>
    """,
    unsafe_allow_html=True
)

def patient_view():
    st.header("Patient Dashboard")
    
    st.subheader("Digital Therapeutics Directory")
    apps_df = pd.read_sql_query("SELECT * FROM apps", conn)
    st.dataframe(apps_df[['name', 'description', 'category', 'fda_cleared',
                            'clinical_evidence_score', 'user_experience_score', 'security_compliance_score', 'integration_capabilities_score']])
    
    st.subheader("My Prescriptions")
    patient_name = "John Doe"
    prescriptions_df = pd.read_sql_query("""
        SELECT prescriptions.*, apps.name as app_name 
        FROM prescriptions 
        JOIN apps ON prescriptions.app_id = apps.id 
        WHERE patient_name=?
    """, conn, params=(patient_name,))
    st.dataframe(prescriptions_df[['provider_name', 'app_name', 'prescription_date']])
    
    st.subheader("My Progress")
    progress_df = pd.read_sql_query("""
        SELECT progress.*, apps.name as app_name 
        FROM progress 
        JOIN apps ON progress.app_id = apps.id 
        WHERE patient_name=?
    """, conn, params=(patient_name,))
    st.dataframe(progress_df[['app_name', 'progress_percent']])
    
    st.subheader("Messages")
    messages_df = pd.read_sql_query("""
        SELECT * FROM messages 
        WHERE sender=? OR receiver=?
    """, conn, params=(patient_name, patient_name))
    st.dataframe(messages_df[['sender', 'receiver', 'message', 'timestamp']])
    
    st.markdown("### Send a Message")
    with st.form("patient_message_form"):
        message = st.text_area("Your message to your provider")
        submit = st.form_submit_button("Send")
        if submit and message:
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            cursor.execute("INSERT INTO messages (sender, receiver, message, timestamp) VALUES (?, ?, ?, ?)", 
                           (patient_name, "Provider", message, timestamp))
            conn.commit()
            st.success("Message sent!")
            st.experimental_rerun()

def provider_view():
    st.header("Provider Dashboard")
    
    st.subheader("Prescribe Digital Therapeutics")
    apps_df = pd.read_sql_query("SELECT * FROM apps", conn)
    with st.form("prescription_form"):
        patient_name = st.text_input("Patient Name", "John Doe")
        app_name = st.selectbox("Select App", apps_df['name'].tolist())
        submit = st.form_submit_button("Prescribe")
        if submit:
            app_id = pd.read_sql_query("SELECT id FROM apps WHERE name=?", conn, params=(app_name,)).iloc[0]['id']
            prescription_date = datetime.now().strftime("%Y-%m-%d")
            cursor.execute("INSERT INTO prescriptions (patient_name, provider_name, app_id, prescription_date) VALUES (?, ?, ?, ?)", 
                           (patient_name, "Dr. Smith", app_id, prescription_date))
            conn.commit()
            st.success(f"Prescribed {app_name} to {patient_name}!")
            st.experimental_rerun()
    
    st.subheader("Patient Progress")
    progress_df = pd.read_sql_query("""
        SELECT progress.*, apps.name as app_name 
        FROM progress 
        JOIN apps ON progress.app_id = apps.id 
        WHERE patient_name=?
    """, conn, params=("John Doe",))
    st.dataframe(progress_df[['patient_name', 'app_name', 'progress_percent']])
    
    st.subheader("Patient Messages")
    messages_df = pd.read_sql_query("SELECT * FROM messages WHERE receiver=?", conn, params=("Dr. Smith",))
    st.dataframe(messages_df[['sender', 'message', 'timestamp']])

def admin_view():
    st.header("Admin Dashboard")
    
    st.subheader("Manage App Certifications")
    apps_df = pd.read_sql_query("SELECT * FROM apps", conn)
    st.dataframe(apps_df[['name', 'fda_cleared', 'clinical_evidence_score', 'user_experience_score', 'security_compliance_score', 'integration_capabilities_score']])
    
    with st.form("update_cert_form"):
        app_to_update = st.selectbox("Select App to Update", apps_df['name'].tolist())
        fda_status = st.text_input("FDA/Cleared Status", "FDA Cleared")
        clinical_score = st.number_input("Clinical Evidence Score", 0.0, 5.0, step=0.1, value=4.5)
        ux_score = st.number_input("User Experience Score", 0.0, 5.0, step=0.1, value=4.5)
        security_score = st.number_input("Security & Compliance Score", 0.0, 5.0, step=0.1, value=4.5)
        integration_score = st.number_input("Integration Capabilities Score", 0.0, 5.0, step=0.1, value=4.5)
        submit = st.form_submit_button("Update Certification")
        if submit:
            cursor.execute("""
                UPDATE apps 
                SET fda_cleared=?, clinical_evidence_score=?, user_experience_score=?, security_compliance_score=?, integration_capabilities_score=?
                WHERE name=?
            """, (fda_status, clinical_score, ux_score, security_score, integration_score, app_to_update))
            conn.commit()
            st.success("App certification updated!")
            st.experimental_rerun()
    
    st.subheader("User Management")
    # Demo user list
    users_data = {
        "Name": ["John Doe", "Dr. Smith", "Admin User"],
        "Role": ["Patient", "Provider", "Admin"]
    }
    st.table(pd.DataFrame(users_data))
    
    st.subheader("Analytics")
    total_apps = pd.read_sql_query("SELECT COUNT(*) as count FROM apps", conn).iloc[0]['count']
    total_prescriptions = pd.read_sql_query("SELECT COUNT(*) as count FROM prescriptions", conn).iloc[0]['count']
    total_messages = pd.read_sql_query("SELECT COUNT(*) as count FROM messages", conn).iloc[0]['count']
    col1, col2, col3 = st.columns(3)
    col1.metric("Total Apps", total_apps)
    col2.metric("Total Prescriptions", total_prescriptions)
    col3.metric("Total Messages", total_messages)

def main():
    st.set_page_config(page_title="Beacon Health", layout="wide")
    st.title("Beacon Health")
    
    # Role switching for demo purposes (no login required)
    role = st.sidebar.selectbox("Select Role", ["Patient", "Provider", "Admin"])
    
    if role == "Patient":
        patient_view()
    elif role == "Provider":
        provider_view()
    elif role == "Admin":
        admin_view()

if __name__ == "__main__":
    main()
