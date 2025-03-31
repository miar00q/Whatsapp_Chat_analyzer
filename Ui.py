# Ui.py
import streamlit as st


def add_gradient_background():
    gradient_bg = """
    <style>
    /* Main Gradient Background */
    [data-testid="stAppViewContainer"] {
        background: linear-gradient(135deg, #20002c, #4c215d, #282858);
        color: white;
    }

    /* Sidebar Enhanced Styling */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #282858, #4c215d, #20002c);
        box-shadow: 4px 0px 12px rgba(0, 0, 0, 0.6);
        padding-top: 15px;
        border-top-right-radius: 12px;
        border-bottom-right-radius: 12px;
    }

    /* Sidebar Text Styling */
    [data-testid="stSidebar"] div, [data-testid="stSidebar"] h2, [data-testid="stSidebar"] h3, [data-testid="stSidebar"] h4 {
        color: #ffffff;
    }

    /* Buttons and Inputs Styling */
    .stButton>button, .stFileUploader label {
        width: 100%;
        background-color: #643b7a;
        color: #fff;
        border-radius: 10px;
        border: none;
        padding: 8px;
        margin-top: 10px;
        transition: background-color 0.3s ease-in-out;
    }

    .stButton>button:hover {
        background-color: #855fa8;
    }

    .stFileUploader div span {
        color: #ffffff;
    }

    /* General Markdown Styling */
    div.stMarkdown {
        color: #f0f0f0;
    }

    h1, h2, h3, h4, h5, h6 {
        color: #d4af37;
    }
    </style>
    """
    st.markdown(gradient_bg, unsafe_allow_html=True)



def display_homepage():
    add_gradient_background()

    if 'button_clicked' not in st.session_state:
        st.session_state.button_clicked = False

    if not st.session_state.button_clicked:
        st.title("📱💬 WhatsApp Chat Analyzer")

        st.markdown("""
        ## Welcome to WhatsApp Chat Analyzer!

        This application helps you visualize and analyze your WhatsApp chats effortlessly.
        Optimize your group's communication, track chat activities, visualize common words, emojis, and more!

        #### 🚀 Steps to get started:

        1. **📤 Upload Your Chat File:**
            - Export your WhatsApp chat:  
              *(Open WhatsApp → go to chat → tap on the name → scroll down → Export Chat)*
            - Choose **"Without Media"** option to make analysis faster.
            - Upload this file using the sidebar on the left.

        2. **👤 Select User:**
            - After uploading, select a specific user from the group or choose **"Overall"** to see analysis for the entire group.

        3. **📊 Analyze:**
            - View insightful visualizations about message frequency, popular emojis, active days/hours, and frequent words.

        ---
        ### ✨ Features Include:
        - Monthly and Daily activity timelines 📅
        - Most Active Users 🏆
        - Word Cloud of Frequently Used Words 🌥️
        - Emoji Usage Analysis 😄
        """)

        st.markdown("---")

        st.markdown("""
        ### 📢 Quick Tips:
        - **Larger chats** might take a little longer to process.
        - Ensure your exported file format is standard WhatsApp format (.txt).

        ---
        💼 **Navigate to sidebar to begin!**
        """)

        # Add a helpful button
        if st.button("👉 Open Sidebar"):
            st.info(
                "👋 Please click on the **arrow icon** (➜) at the top-left corner of the screen to open the sidebar!")

