import streamlit as st
import streamlit.components.v1 as components
from datetime import date
import urllib.parse
import pandas as pd

# CSS styles as a separate string
CSS_STYLES = """
    body {
        background-color: #f9f9f9;
        margin: 0;
        padding: 0;
        display: flex;
        justify-content: center;
        align-items: center;
        height: 100vh;
        font-family: 'Roboto', sans-serif;
    }
    .badge {
        width: 400px;
        height: 400px;
        border-radius: 50%;
        background: linear-gradient(135deg, #1F2937, #4B5563);
        position: relative;
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.2);
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        padding: 20px;
        color: #fff;
        text-align: center;
        overflow: hidden;
    }
    .badge::before {
        content: "";
        position: absolute;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        border-radius: 50%;
        background: rgba(255, 255, 255, 0.1);
        mix-blend-mode: overlay;
        pointer-events: none;
    }
    .badge-content {
        position: relative;
        z-index: 2;
        padding: 0 20px;
    }
    .recipient {
        font-family: 'Great Vibes', cursive;
        font-size: 42px;
        margin-bottom: 10px;
    }
    .achievement {
        font-size: 20px;
        font-weight: 300;
        margin-bottom: 8px;
    }
    .issue-date {
        font-size: 16px;
        margin-bottom: 8px;
    }
    .notes {
        font-size: 14px;
        margin-bottom: 8px;
    }
    .qr-code {
        position: absolute;
        bottom: 20px;
        right: 20px;
        width: 80px;
        height: 80px;
        border: 3px solid #fff;
        border-radius: 50%;
        overflow: hidden;
        background: #fff;
    }
    .qr-code img {
        width: 100%;
        height: 100%;
        object-fit: cover;
    }
"""

def create_badge_html(recipient_name, achievement, category, issue_date, notes, qr_url):
    """Create the HTML for the badge with proper escaping"""
    html_template = """
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">
        <title>Achievement Badge</title>
        <link href="https://fonts.googleapis.com/css2?family=Roboto:wght@300;400;500&family=Great+Vibes&display=swap" rel="stylesheet">
        <style>
        {css_styles}
        </style>
    </head>
    <body>
        <div class="badge">
            <div class="badge-content">
                <div class="recipient">{recipient}</div>
                <div class="achievement">{achievement}<br>({category})</div>
                <div class="issue-date">Issued on: {issue_date}</div>
                <div class="notes">{notes}</div>
            </div>
            <div class="qr-code">
                <img src="{qr_url}" alt="QR Code">
            </div>
        </div>
    </body>
    </html>
    """
    return html_template.format(
        css_styles=CSS_STYLES,
        recipient=recipient_name,
        achievement=achievement,
        category=category,
        issue_date=issue_date.strftime('%B %d, %Y'),
        notes=notes if notes else "",
        qr_url=qr_url
    )

def init_session_state():
    """Initialize session state variables"""
    if "achievements" not in st.session_state:
        st.session_state["achievements"] = []

def main():
    st.title("BadgeForge - Professional Achievement Badge Generator")
    
    # Initialize session state
    init_session_state()

    # Achievement categories and specific achievements
    achievements_dict = {
        "Reading Progress Milestones": [
            "Started first book",
            "Completed 1 book",
            "Completed 5 books",
            "Completed 10 books",
            "Completed 20 books"
        ],
        "Volunteer Milestones": [
            "Completed 10 Hours Community Service",
            "Completed 25 Hours Mentoring",
            "Completed 50 Hours Social Impact",
            "Volunteer of the Month"
        ],
        "Pharmacy Informatics APPE Rotations": [
            "Completed Basic Informatics Rotation",
            "Completed Advanced Informatics Rotation",
            "Completed Informatics Research Project",
            "Exemplary Performance in APPE Rotation"
        ],
        "Well-being Initiatives": [
            "Well-being Book Club Participation",
            "Mindfulness Program Completion",
            "Health & Wellness Champion"
        ]
    }

    # User Input Section
    st.header("Enter Achievement Details")
    
    with st.form("badge_form"):
        recipient_name = st.text_input("Recipient Name")
        categories = list(achievements_dict.keys())
        category = st.selectbox("Achievement Category", categories)
        achievement = st.selectbox("Select Specific Achievement", achievements_dict[category])
        issue_date = st.date_input("Issue Date", date.today())
        notes = st.text_area("Optional Notes or Evidence")
        evidence = st.file_uploader("Upload Evidence (optional)", type=["jpg", "png", "pdf"])
        
        submit_button = st.form_submit_button("Generate Badge")

        if submit_button:
            if not recipient_name:
                st.error("Please enter a recipient name.")
            else:
                try:
                    # Generate QR code URL
                    qr_data = f"Name: {recipient_name}\nAchievement: {achievement}\nDate: {issue_date}"
                    qr_encoded = urllib.parse.quote(qr_data)
                    qr_url = f"https://api.qrserver.com/v1/create-qr-code/?data={qr_encoded}&size=100x100"

                    # Generate badge HTML
                    badge_html = create_badge_html(
                        recipient_name,
                        achievement,
                        category,
                        issue_date,
                        notes,
                        qr_url
                    )

                    st.success("Badge generated successfully!")
                    
                    # Display badge
                    components.html(badge_html, height=500, scrolling=True)

                    # Export options
                    st.download_button(
                        "Download Badge as HTML",
                        badge_html,
                        file_name="badge.html",
                        mime="text/html"
                    )

                    # Update achievement tracking
                    st.session_state["achievements"].append({
                        "Name": recipient_name,
                        "Category": category,
                        "Achievement": achievement,
                        "Issue Date": issue_date.strftime("%Y-%m-%d")
                    })

                except Exception as e:
                    st.error(f"An error occurred while generating the badge: {str(e)}")

    # Achievement Tracking Dashboard
    st.header("Achievement Tracking Dashboard")
    if st.session_state["achievements"]:
        df = pd.DataFrame(st.session_state["achievements"])
        st.dataframe(df)
    else:
        st.info("No achievements generated yet.")

if __name__ == "__main__":
    main()

