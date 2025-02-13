import streamlit as st
st.set_page_config(page_title="Beacon Health", layout="wide")  # Must be the first Streamlit command

import sqlite3
import pandas as pd
from datetime import datetime

# ------------------------------------------------------------------------------
# Database Setup and Demo Data Functions
# ------------------------------------------------------------------------------

@st.cache_resource
def get_connection():
    return sqlite3.connect('beacon_health.db', check_same_thread=False)

conn = get_connection()
cursor = conn.cursor()

def init_db():
    """Initialize database tables if they do not exist."""
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS apps (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            description TEXT,
            category TEXT,
            fda_status TEXT,
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
    """Load demo placeholder data for apps, prescriptions, progress, and messages."""
    # Load health and wellness demo apps
    df_apps = pd.read_sql_query("SELECT * FROM apps", conn)
    if df_apps.empty:
        apps_demo = [
            ("MindRelax", "A mindfulness and meditation app to reduce stress.", "Mental Health", "FDA Cleared", 4.5, 4.2, 4.8, 4.0),
            ("FitTrack", "A fitness tracking app to monitor activities and workouts.", "Wellness", "Pending", 4.0, 4.0, 4.5, 3.8),
            ("SleepWell", "An app designed to improve sleep quality through personalized routines.", "Sleep Health", "FDA Cleared", 4.8, 4.6, 4.9, 4.5),
            ("NutriGuide", "Nutrition guidance and meal planning for a balanced diet.", "Nutrition", "FDA Cleared", 4.2, 4.3, 4.7, 4.2),
            ("YogaFlow", "Offering yoga routines and wellness tips for everyday balance.", "Fitness", "Pending", 4.3, 4.4, 4.6, 4.1)
        ]
        cursor.executemany('''
            INSERT INTO apps 
            (name, description, category, fda_status, clinical_evidence_score, user_experience_score, security_compliance_score, integration_capabilities_score)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', apps_demo)
        conn.commit()

    # Load demo prescriptions
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

    # Load demo progress tracking data
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

    # Load demo messages for communication system
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

def reset_demo_data():
    """Reset the demo data by dropping and reinitializing all tables."""
    cursor.execute("DROP TABLE IF EXISTS apps")
    cursor.execute("DROP TABLE IF EXISTS prescriptions")
    cursor.execute("DROP TABLE IF EXISTS messages")
    cursor.execute("DROP TABLE IF EXISTS progress")
    conn.commit()
    init_db()
    load_demo_data()
    st.success("Demo data has been reset.")

def check_schema():
    """Verify that the 'apps' table contains the expected columns; reset if not."""
    expected_columns = {
        "name", "description", "category", "fda_status", 
        "clinical_evidence_score", "user_experience_score", 
        "security_compliance_score", "integration_capabilities_score"
    }
    cur = conn.execute("PRAGMA table_info(apps)")
    current_columns = {row[1] for row in cur.fetchall()}
    if not expected_columns.issubset(current_columns):
        st.warning("Apps table schema mismatch detected. Resetting demo data...")
        reset_demo_data()

# Initialize DB and load demo data on app start
init_db()
load_demo_data()
check_schema()

# ------------------------------------------------------------------------------
# Custom CSS for a Modern, Clean UI
# ------------------------------------------------------------------------------
st.markdown(
    """
    <style>
    /* Button styling */
    .stButton>button {
        background-color: #4CAF50;
        color: white;
        border: none;
        border-radius: 4px;
        padding: 10px 20px;
        font-size: 16px;
        cursor: pointer;
    }
    .stButton>button:hover {
        background-color: #45a049;
    }
    /* Input styling */
    .stTextInput>div>input, .stTextArea>div>textarea, .stSelectbox>div>div>div>input {
        padding: 10px;
        border: 1px solid #ccc;
        border-radius: 4px;
    }
    /* Sidebar styling */
    .css-1d391kg {  
        background-color: #f0f2f6;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# ------------------------------------------------------------------------------
# Role-Based Views
# ------------------------------------------------------------------------------

def patient_view():
    st.header("Patient Dashboard")
    
    st.subheader("Digital Therapeutics Directory")
    apps_df = pd.read_sql_query("SELECT * FROM apps", conn)
    # Ensure only the expected columns are displayed if they exist
    expected_cols = [
        'name', 'description', 'category', 'fda_status',
        'clinical_evidence_score', 'user_experience_score', 
        'security_compliance_score', 'integration_capabilities_score'
    ]
    available_cols = [col for col in expected_cols if col in apps_df.columns]
    st.dataframe(apps_df[available_cols])
    
    st.subheader("My Prescriptions")
    patient_name = "John Doe"  # Placeholder patient name
    prescriptions_df = pd.read_sql_query("""
        SELECT prescriptions.*, apps.name AS app_name 
        FROM prescriptions 
        JOIN apps ON prescriptions.app_id = apps.id 
        WHERE patient_name=?
    """, conn, params=(patient_name,))
    if not prescriptions_df.empty:
        st.dataframe(prescriptions_df[['provider_name', 'app_name', 'prescription_date']])
    else:
        st.info("No prescriptions found.")
    
    st.subheader("My Progress")
    progress_df = pd.read_sql_query("""
        SELECT progress.*, apps.name AS app_name 
        FROM progress 
        JOIN apps ON progress.app_id = apps.id 
        WHERE patient_name=?
    """, conn, params=(patient_name,))
    if not progress_df.empty:
        st.dataframe(progress_df[['app_name', 'progress_percent']])
    else:
        st.info("No progress updates available.")
    
    st.subheader("Messages")
    messages_df = pd.read_sql_query("""
        SELECT * FROM messages 
        WHERE sender=? OR receiver=?
        ORDER BY timestamp DESC
    """, conn, params=(patient_name, patient_name))
    if not messages_df.empty:
        st.dataframe(messages_df[['sender', 'receiver', 'message', 'timestamp']])
    else:
        st.info("No messages found.")
    
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
            app_id_row = pd.read_sql_query("SELECT id FROM apps WHERE name=?", conn, params=(app_name,))
            if not app_id_row.empty:
                app_id = app_id_row.iloc[0]['id']
                prescription_date = datetime.now().strftime("%Y-%m-%d")
                cursor.execute("INSERT INTO prescriptions (patient_name, provider_name, app_id, prescription_date) VALUES (?, ?, ?, ?)", 
                               (patient_name, "Dr. Smith", app_id, prescription_date))
                conn.commit()
                st.success(f"Prescribed {app_name} to {patient_name}!")
                st.experimental_rerun()
            else:
                st.error("Selected app not found.")
    
    st.subheader("Patient Progress")
    progress_df = pd.read_sql_query("""
        SELECT progress.*, apps.name AS app_name 
        FROM progress 
        JOIN apps ON progress.app_id = apps.id 
        WHERE patient_name=?
    """, conn, params=("John Doe",))
    if not progress_df.empty:
        st.dataframe(progress_df[['patient_name', 'app_name', 'progress_percent']])
    else:
        st.info("No progress updates available.")
    
    st.subheader("Patient Messages")
    messages_df = pd.read_sql_query("SELECT * FROM messages WHERE receiver=?", conn, params=("Dr. Smith",))
    if not messages_df.empty:
        st.dataframe(messages_df[['sender', 'message', 'timestamp']])
    else:
        st.info("No messages from patients.")

def admin_view():
    st.header("Admin Dashboard")
    
    st.subheader("Manage App Certifications")
    apps_df = pd.read_sql_query("SELECT * FROM apps", conn)
    expected_cols = [
        'name', 'fda_status', 'clinical_evidence_score', 
        'user_experience_score', 'security_compliance_score', 
        'integration_capabilities_score'
    ]
    available_cols = [col for col in expected_cols if col in apps_df.columns]
    st.dataframe(apps_df[available_cols])
    
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
                SET fda_status=?, clinical_evidence_score=?, user_experience_score=?, security_compliance_score=?, integration_capabilities_score=?
                WHERE name=?
            """, (fda_status, clinical_score, ux_score, security_score, integration_score, app_to_update))
            conn.commit()
            st.success("App certification updated!")
            st.experimental_rerun()
    
    st.subheader("User Management")
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
    
    st.subheader("Reset Demo Data")
    if st.button("Reset All Demo Data"):
        reset_demo_data()

# ------------------------------------------------------------------------------
# Main App Function with Role Switching
# ------------------------------------------------------------------------------

def main():
    st.title("Beacon Health - Digital Therapeutics Marketplace")
    
    # Sidebar for role switching and developer notes
    st.sidebar.header("Demo Role Selector")
    role = st.sidebar.selectbox("Select Role", ["Patient", "Provider", "Admin"])
    
    st.sidebar.info("Note: Role switching is for demo purposes only. Future versions will include full authentication.")
    st.sidebar.markdown("""
    **Developer To-Do:**
    - Integrate real user authentication.
    - Expand messaging system for multi-party communication.
    - Enhance analytics with interactive charts.
    - Improve UI/UX with advanced theming and custom components.
    """)
    
    if role == "Patient":
        patient_view()
    elif role == "Provider":
        provider_view()
    elif role == "Admin":
        admin_view()

if __name__ == "__main__":
    main()



