import  streamlit as st
import text_preprocessing
import Helper
import matplotlib.pyplot as plt

st.sidebar.title("Whatsapp Chat Analyzer")

uploaded_file = st.sidebar.file_uploader("Choose a file")
if uploaded_file is not None:
    bytes_data = uploaded_file.getvalue()
    data = bytes_data.decode("utf-8")
    # st.text(data)

    df = text_preprocessing.preprocess(data)
    st.dataframe(df)

    #fetch unique users
    user_list = df['user'].unique().tolist()
    user_list.remove("group notification")
    user_list.sort()
    user_list.insert(0, "Overall")
    selected_user = st.sidebar.selectbox("Show analysis wrt", user_list)

    if st.sidebar.button("Show Analysis"):

        num_msg, num_words, num_media_msg, num_links = Helper.fetch_stats(selected_user, df)

        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.header("Total Messages")
            st.title(num_msg)
        with col2:
            st.header("Total words")
            st.title(num_words)
        with col3:
            st.header("Total media messages")
            st.title(num_media_msg)
        with col4:
            st.header("Links shared")
            st.title(num_links)

        if selected_user == "Overall":
            st.title("Most active users")
            col1, col2 = st.columns(2)

            x = Helper.most_active_users(df)
            fig, ax = plt.subplots()
            
            with col1:
                ax.bar(x.index, x.values)
                plt.xticks(rotation="vertical")
                st.pyplot(fig)


        st.title("WordCloud")
        df_wc = Helper.create_wordcloud(selected_user, df)
        fig, ax = plt.subplots()
        ax.imshow(df_wc)
        ax.axis('off')
        st.pyplot(fig)


        #Most common words
        st.title("Most Common words")
        most_common_df = Helper.most_common_words(selected_user, df)

        fig, ax = plt.subplots()

        ax.barh(most_common_df[0], most_common_df[1])
        st.pyplot(fig)
        plt.xticks(rotation = "vertical")