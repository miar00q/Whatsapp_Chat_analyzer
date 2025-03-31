import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns

import Ui
import preprocessor
import helper
from helper import daily_timeline

# Display gradient background always
Ui.add_gradient_background()

# Initialize button click states
if 'button_clicked' not in st.session_state:
    st.session_state.button_clicked = False



st.sidebar.title("Welcome to Chat Analysis")
st.sidebar.info(" This application is for to Analyzing the chat by uploading the chat file. ")

# Initialize session state variables if they don't exist
if 'show_chats' not in st.session_state:
    st.session_state.show_chats = False
if 'show_data' not in st.session_state:
    st.session_state.show_data = False
if 'show_analysis' not in st.session_state:
    st.session_state.show_analysis = False

uploaded_file = st.sidebar.file_uploader("Choose a file", key="file_uploader")
if uploaded_file is not None:
    # To read file as bytes:
    bytes_data = uploaded_file.getvalue()

    data = bytes_data.decode("utf-8")
    df = preprocessor.preprocess(data)

    # fetch unique users
    user_list = df['user'].unique().tolist()
    user_list.remove('group_notification')
    user_list.sort()
    user_list.insert(0, "Overall")

    # Move the user selection before the buttons
    selected_user = st.sidebar.selectbox("Select User", user_list, key="user_select")

    # Filter data based on user selection
    if selected_user != "Overall":
        filtered_df = df[df['user'] == selected_user]
        filtered_data = "\n".join(filtered_df['message'].tolist())
    else:
        filtered_df = df
        filtered_data = data


    # Button callbacks to update state
    def show_chats_clicked():
        st.session_state.show_chats = True
        st.session_state.show_data = False
        st.session_state.show_analysis = False


    def show_data_clicked():
        st.session_state.show_data = True
        st.session_state.show_chats = False
        st.session_state.show_analysis = False


    def show_analysis_clicked():
        st.session_state.show_analysis = True
        st.session_state.show_chats = False
        st.session_state.show_data = False


    # Buttons with callbacks
    st.sidebar.button("Show Chats", on_click=show_chats_clicked, key="show_chats_button")
    st.sidebar.button("Show Data", on_click=show_data_clicked, key="show_data_button")
    st.sidebar.button("Show Chat Analysis", on_click=show_analysis_clicked, key="show_analysis_button")

    # Display content based on button states
    if st.session_state.show_chats:
        st.empty()
        st.text(filtered_data)

    if st.session_state.show_data:
        st.empty()
        st.dataframe(filtered_df, use_container_width=True, height=450)

    if st.session_state.show_analysis:
        st.empty()


        #Stats Area
        num_messages, words, num_media_messages, links = helper.fetch_stats(selected_user, df)

        col1, col2, col4, col5 = st.columns(4)

        with col1:
            st.header("Total Message")
            st.text(num_messages)

        with col2:
            st.header("Total Words")
            st.text(words)

        with col4:
            st.header("Media Shared")
            st.text(num_media_messages)

        with col5:
            st.header("Links Shared")
            st.text(links)

        st.markdown("<hr style='height:3px;border:none;color:#333;background-color:#333;' />", unsafe_allow_html=True)

        ## Monthly timeline analysis
        st.title('Monthly Timeline')
        timeline = helper.monthly_timeline(selected_user, filtered_df)

        fig, ax = plt.subplots(figsize=(10, 5))
        ax.plot(timeline['datetime'], timeline['message'], marker='o')

        # Improved tick handling clearly
        ax.set_xticks(timeline['datetime'])
        ax.set_xticklabels(timeline['datetime'].dt.strftime('%b-%Y'), rotation=90)

        plt.tight_layout()
        st.pyplot(fig)

        st.markdown("<hr style='height:3px;border:none;color:#333;background-color:#333;' />", unsafe_allow_html=True)

        ## daily timeline
        st.title('Daily Timeline')
        daily = daily_timeline(selected_user, filtered_df)

        fig, ax = plt.subplots(figsize=(12, 6))
        ax.plot(daily['only_date'], daily['message'], color='green', marker='o')

        # Display every N days to make sure labels fit well clearly
        interval = max(len(daily) // 20, 1)  # Adjust number of ticks dynamically if too many labels
        ax.set_xticks(daily['only_date'][::interval])
        ax.set_xticklabels(daily['only_date'].dt.strftime('%d-%b-%Y')[::interval], rotation=90)

        plt.tight_layout()
        st.pyplot(fig)

        st.markdown("<hr style='height:3px;border:none;color:#333;background-color:#333;' />", unsafe_allow_html=True)

        ##Activity Map
        st.title('Activity Map')

        col1, col2 = st.columns(2)

        with col1:
            st.header('Most Busy Day')
            busy_day = helper.week_activity(selected_user, df)
            fig, ax = plt.subplots()
            ax.bar(busy_day.index, busy_day.values)
            plt.xticks(rotation=90)
            st.pyplot(fig)

        with col2:
            st.header('Most Busy Month')
            busy_month = helper.month_activity(selected_user, df)
            fig, ax = plt.subplots()
            ax.bar(busy_month.index, busy_month.values, color='orange')
            plt.xticks(rotation=90)
            st.pyplot(fig)

        #Acitivity heatmap
        st.markdown("<hr style='height:3px;border:none;color:#333;background-color:#333;' />", unsafe_allow_html=True)
        st.title('Activity Heatmap')
        user_heatmap = helper.activity_heatmap(selected_user, df)
        fig, ax = plt.subplots(figsize=(10, 6))
        ax = sns.heatmap(user_heatmap, annot=True, fmt=".0f", linewidths=.5, ax=ax)
        st.pyplot(fig)

        ##Findinf the busiest users in the group
        st.markdown("<hr style='height:3px;border:none;color:#333;background-color:#333;' />", unsafe_allow_html=True)

        if selected_user == 'Overall':
            st.title('Top 25 Busiest Users')
            x, new_df = helper.most_busy_user(df)

            fig, ax = plt.subplots()

            col1, col2 = st.columns(2)

            with col1:
                ax.bar(x.index, x.values, color='red')
                plt.xticks(rotation=90)
                st.pyplot(fig)

            with col2:
                st.dataframe(new_df, use_container_width=True, height = 350)


        #WordCloud
        st.title('WordCloud')
        df_wc=helper.crate_word_cloud(selected_user,df)
        fig,ax = plt.subplots()
        ax.imshow(df_wc)
        st.pyplot(fig)

        #most common words
        st.markdown("<hr style='height:3px;border:none;color:#333;background-color:#333;' />", unsafe_allow_html=True)
        st.title('Most Common Words')
        col6, col7 = st.columns(2)

        most_common_df = helper.most_common_words(selected_user,df)


        with col6:
            fig, ax = plt.subplots()
            ax.bar(most_common_df['Word'], most_common_df['Count'])
            plt.xticks(rotation=90)
            st.pyplot(fig)
        with col7:
            st.dataframe(most_common_df, use_container_width=True, height = 350)


        #emoji analysis
        st.markdown("<hr style='height:3px;border:none;color:#333;background-color:#333;' />", unsafe_allow_html=True)
        st.title('Emoji Analysis')
        col1, col2 = st.columns(2)

        emoji_df = helper.emoji_count(selected_user,df)

        with col1:
            st.dataframe(emoji_df, use_container_width=True)

        with col2:
            fig, ax = plt.subplots()
            # Use Count column for the values, and Emoji column for labels
            ax.pie(emoji_df['Count'].head(12), labels=emoji_df['Emoji'].head(12), autopct='%1.1f%%')
            st.pyplot(fig)
else:
    # Display Homepage if no button clicks yet
    Ui.display_homepage()
