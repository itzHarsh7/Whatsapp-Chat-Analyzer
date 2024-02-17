import streamlit as st
import pandas as pd
from preprocessor import preprocess
import helper
import matplotlib.pyplot as plt
import seaborn as sns

st.sidebar.title('Whatsapp Chat Analyzer')

uploaded_file = st.sidebar.file_uploader('Choose File')
if uploaded_file is not None:
    bytes_data = uploaded_file.getvalue()
    data = bytes_data.decode("utf-8")

    df = preprocess(data)

    st.dataframe(df)

    user_list = df['user'].unique().tolist()
    user_list.remove('group_notification')
    user_list.sort()
    user_list.insert(0, 'All Users')
    selected_user = st.sidebar.selectbox('Show Analysis w.r.t',user_list)

    if st.sidebar.button('Show Analysis'):
        st.title(f'User: {selected_user}')
        num_messages,words,num_media_messages,num_urls = helper.fetch_stats(selected_user,df)
        col1,col2,col3,col4 = st.columns(4)
        with col1:
            st.header(f'Total Messages: ')
            st.write(f'{num_messages}')

        with col2:
            st.header(f'Total Words: ')
            st.write(f'{words}')
        with col3:
            st.header(f'Total Media Shared: ')
            st.write(f'{num_media_messages}')
        with col4:
            st.header(f'Total URL\'s Shared: ')
            st.write(f'{num_urls}')


        st.header('Busy Users:')
        if selected_user == 'All Users':
            fig,ax =plt.subplots()
            x,new_df = helper.most_busy_users(df)
            col1,col2 = st.columns(2)
            with col1:
                ax.bar(x.index,x.values,color='red')
                plt.xticks(rotation='vertical')
                st.pyplot(fig)
            with col2:
                st.dataframe(new_df)

        st.title('WordCloud')
        df_wc = helper.create_wordcloud(selected_user,df)
        fig,ax = plt.subplots()
        ax.imshow(df_wc)
        st.pyplot(fig)

        most_common_df = helper.most_common_words(selected_user,df)
        fig,ax = plt.subplots()
        ax.barh(most_common_df[0],most_common_df[1])
        plt.xticks(rotation = 'vertical')
        st.title('Most Common Words')
        st.pyplot(fig)


        emoji_df = helper.emoji_helper(selected_user,df)
        st.title('Emoji Analysis')
        col1,col2 = st.columns(2)
        with col1:
            st.dataframe(emoji_df)
        with col2:
            fig,ax = plt.subplots()
            ax.pie(emoji_df[1].head(10),labels=emoji_df[0].head(10),autopct = '%0.2f')
            st.pyplot(fig)
