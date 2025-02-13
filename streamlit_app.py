import streamlit as st
import streamlit.components.v1 as components
from datetime import date
import urllib.parse
import pandas as pd

st.title("BadgeForge - Professional Achievement Badge Generator")

# ----- User Input Section -----
st.header("Enter Achievement Details")
recipient_name = st.text_input("Recipient Name")

# Define achievement categories and specific achievements
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

categories = list(achievements_dict.keys())
category = st.selectbox("Achievement Category", categories)
achievement = st.selectbox("Select Specific Achievement", achievements_dict[category])

issue_date = st.date_input("Issue Date", date.today())
notes = st.text_area("Optional Notes or Evidence")
evidence = st.file_uploader("Upload Evidence (optional)", type=["jpg", "png", "pdf"])

# ----- Badge Generation and Preview -----
if st.button("Generate Badge"):
    if not recipient_name:
        st.error("Please enter a recipient name.")
    else:
        # Generate QR code URL using an online service.
        qr_data = f"Name: {recipient_name}\nAchievement: {achievement}\nDate: {issue_date}"
        qr_encoded = urllib.parse.quote(qr_data)
        qr_url = f"https://api.qrserver.com/v1/create-qr-code/?data={qr_encoded}&size=100x100"

        # Create the circular badge as an HTML string with a modern and sleek design.
        badge_html = f"""<!DOCTYPE html>
<html>
<head>
  <meta charset="UTF-8">
  <title>Achievement Badge</title>
  <link href="https://fonts.googleapis.com/css2?family=Roboto:wght@300;400;500&family=Great+Vibes&display=swap" rel="stylesheet">
  <style>
    body {{
      background-color: #f9f9f9;
      margin: 0;
      padding: 0;
      display: flex;
      justify-content: center;
      align-items: center;
      height: 100vh;
      font-family: 'Roboto', sans-serif;
    }}
    .badge {{
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
    }}
    .badge::before {{
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
    }}
    .badge-content {{
      position: relative;
      z-index: 2;
      padding: 0 20px;
    }}
    .recipient {{
      font-family: 'Great Vibes', cursive;
      font-size: 42px;
      margin-bottom: 10px;
    }}
    .achievement {{
      font-size: 20px;
      font-weight: 300;
      margin-bottom: 8px;
    }}
    .issue-date {{
      font-size: 16px;
      margin-bottom: 8px;
    }}
    .notes {{
      font-size: 14px;
      margin-bottom: 8px;
    }}
    .qr-code {{
      position: absolute;
      bottom: 20px;
      right: 20px;
      width: 80px;
      height: 80px;
      border: 3px solid #fff;
      border-radius: 50%;
      overflow: hidden;
      background: #fff;
    }}
    .qr-code img {{
      width: 100%;
      height: 100%;
      object-fit: cover;
    }}
  </style>
</head>
<body>
  <div class="badge">
    <div class="badge-content">
      <div class="recipient">{recipient_name}</div>
      <div class="achievement">{achievement} <br>({category})</div>
      <div class="issue-date">Issued on: {issue_date.strftime('%B %d, %Y')}</div>
      <div class="notes">{notes if notes else ""}</div>
    </div>
    <div class="qr-code">
      <img src="{qr_url}" alt="QR Code">
    </div>
  </div>
</body>
</html>"""
        st.success("Badge generated successfully!")

        # Preview the badge in the app.
        components.html(badge_html, height=500, scrolling=True)

        # ----- Export Options -----
        st.download_button("Download Badge as HTML",
                           badge_html,
                           file_name="badge.html",
                           mime="text/html")

        # ----- Achievement Tracking Dashboard -----
        if "achievements" not in st.session_state:
            st.session_state["achievements"] = []
        st.session_state["achievements"].append({
            "Name": recipient_name,
            "Category": category,
            "Achievement": achievement,
            "Issue Date": issue_date.strftime("%Y-%m-%d")
        })

# ----- Achievement Tracking Dashboard Display -----
st.header("Achievement Tracking Dashboard")
if "achievements" in st.session_state and st.session_state["achievements"]:
    df = pd.DataFrame(st.session_state["achievements"])
    st.dataframe(df)
else:
    st.info("No achievements generated yet.")
