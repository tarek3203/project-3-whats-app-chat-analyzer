import streamlit as st
import preprocessor , helper
import matplotlib.pyplot as plt
from collections import Counter
# import beta_columns

st.sidebar.title("whatsapp chat analyzer")

uploaded_file = st.sidebar.file_uploader("Choose a file")
if uploaded_file is not None:
    # To read file as bytes:
    bytes_data = uploaded_file.getvalue()
    data = bytes_data.decode("utf-8")
    # st.text(data)
    df = preprocessor.preprocess(data)

    st.dataframe(df)

    # fetch unique users

    user_list = df['user'].unique().tolist()
    user_list.remove('Group_Notification')
    user_list.sort()
    user_list.insert(0, 'overall') # insert on 0 th index
    selected_user = st.sidebar.selectbox("show analysis", user_list)
    # st.sidebar.selectbox("show analysis", user_list)

    if st.sidebar.button("Show analysis"):
        # stats area
        num_messages, words, media_messages, num_links = helper.fetch_stats(selected_user, df)

        st.title("Top Statistics")

        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.header("Total Messages")
            st.title(num_messages)
        with col2:
            st.header("Total words")
            st.title(words)
        with col3:
            st.header("Total Media Messages")
            st.title(media_messages)

        with col4:
            st.header("Total number of links")
            st.title(num_links)

        # timeline analysis
        st.title("Monthly Timeline")
        timeline = helper.monthly_timeline(selected_user, df)
        fig, ax = plt.subplots()
        ax.plot(timeline['time'], timeline['message'], color = 'green')
        plt.xticks(rotation='vertical')
        st.pyplot(fig)

        # daily timeline analysis
        st.title("daily timeline")
        daily_timeline = helper.daily_timeline_helper(selected_user, df)
        fig, ax = plt.subplots()
        ax.plot(daily_timeline['only_date'], daily_timeline['message'])
        plt.xticks(rotation='vertical')
        st.pyplot(fig)


        # weekly and monthly timeline analysis

        col1, col2 = st.columns(2)

        with col1:
            st.title("weekly timeline")
            weekly_timeline = helper.weekly_timeline_helper(selected_user, df)
            fig, ax = plt.subplots()
            ax.bar(weekly_timeline['day_name'], weekly_timeline['message'])
            plt.xticks(rotation='vertical')
            st.pyplot(fig)
        with col2 :
            st.title("most busiest month")
            busy_month = helper.monthly_timeline_helper(selected_user, df)
            fig, ax = plt.subplots()
            ax.bar(busy_month['month'], busy_month['message'])
            plt.xticks(rotation='vertical')
            st.pyplot(fig)



        # finding the busiest person in the group()

        if selected_user == 'overall':
            st.title("most busy users")
            x, new_df = helper.most_busy_users(df)
            fig, ax = plt.subplots()

            col1, col2 = st.columns(2)

            with col1:
                ax.bar(x.index, x.values, color = 'red')
                plt.xticks(rotation = 'vertical')
                st.pyplot(fig)
            with col2:
                st.dataframe(new_df)

        # word cloud
        st.title("Word Cloud")
        df_wc = helper.create_wordcloud(selected_user, df)
        fig, ax = plt.subplots()
        ax.imshow(df_wc)
        st.pyplot(fig)

        # most common words
        st.title("most common 25 words")
        return_words = helper.most_common_words(selected_user, df)

        fig, ax = plt.subplots()
        ax.barh(return_words[0], return_words[1])
        plt.xticks(rotation = 'vertical')

        st.pyplot(fig)

        # emoji analysis
        st.title("most common emojis")
        emoji_df = helper.emoji_helper(selected_user, df)

        col1, col2 =  st.columns(2)

        with col1:
            st.dataframe(emoji_df)

        with col2:
            fig, ax = plt.subplots()
            ax.pie(emoji_df[1], labels = emoji_df[0] ,autopct='%0.2f')
            st.pyplot(fig)

