from io import StringIO
import streamlit as st
from preprosing import preprosesar, getDatapoint, date_time
import analysis_code
from urlextract import URLExtract
import matplotlib.pyplot as plt
import seaborn as sns

st.sidebar.title('Whatsapp Chat Analyzer')

uploaded_file = st.sidebar.file_uploader("Choose a file")
if uploaded_file is not None:
     # To read file as bytes:
     #string_data = StringIO(uploaded_file.getvalue())
     # st.write(string_data)
     bytes_data = uploaded_file.getvalue()
     file = bytes_data.decode('utf-8')
     with open('conversation txt', 'w', encoding='utf-8') as f:
         content = f.write(file)
     dk = preprosesar('conversation txt')
     # st.dataframe(dk)
     user_list = dk['user'].unique().tolist()
     user_list.remove('group_notification')
     user_list.sort()
     user_list.insert(0, 'Overall')
     selected_user = st.sidebar.selectbox("Show analysis wrt", user_list)
     if st.sidebar.button('Show Analysis'):
         num_messages, words, num_media_msg, links = analysis_code.fetch_stats(
             selected_user, dk)
         col1, col2, col3, col4 = st.columns(4)
         with col1:
             st.header('Total Messages')
             st.title(num_messages)
         with col2:
             st.header('Total Words')
             st.title(words)
         with col3:
             st.header('Total Media Shared')
             st.title(num_media_msg)
         with col4:
             st.header('Total Links Shared')
             st.title(links)

          #Timeline
          # monthly timeline
         st.title("Monthly timeline of user")
         timeline = analysis_code.monthly_timeline(selected_user,dk)
         fig,ax = plt.subplots()
         plt.ylabel('No of Messages')
         ax.plot(timeline['Time'],timeline['message'])
         plt.xticks(rotation = 'vertical')
         st.pyplot(fig)

          # Weekly timeline
         st.title("Daily timeline of user")
         daily_timeline = analysis_code.user_daily_timeline(selected_user,dk)
         fig,ax = plt.subplots()         
         plt.ylabel('No of Messages')
         ax.plot(daily_timeline['only_date'],daily_timeline['message'])
         plt.xticks(rotation = 'vertical')
         st.pyplot(fig)

         # Activity map
         st.title('User Activity Map')
         col_1, col_2 = st.columns(2)

         with col_1:
              st.title('Most chatting day')
              busy_day = analysis_code.weekly_activity_analysis(selected_user,dk)
              fig,ax = plt.subplots()
              ax.bar(busy_day.index, busy_day.values)     
              plt.xticks(rotation='vertical')
              st.pyplot(fig)

         with col_2:
              st.title('Most chatting month')
              busy_month = analysis_code.monthly_activity_analysis(selected_user,dk)
              fig,ax = plt.subplots()
              ax.bar(busy_month.index, busy_month.values)     
              plt.xticks(rotation='vertical')
              st.pyplot(fig)
         
         st.title('Weekly activity map of user')
         fig ,ax = plt.subplots()
         heatmap_dk  = analysis_code.Activity(selected_user,dk)
         ax  =sns.heatmap(heatmap_dk)
         st.pyplot(fig)
         
         


      # Finding busiest person in the group
     if selected_user == 'Overall':
         st.title("Most Vella Person")
         x, busy_percent = analysis_code.most_vella_user(dk)
         fig, ax = plt.subplots()
 
         col_1, col_2 = st.columns(2)
 
         with col_1:
             ax.bar(x.index, x.values)
             #plt.figure(figsize=(8, 6))
             plt.xticks(rotation='vertical')
             st.pyplot(fig)
         with col_2:
             st.dataframe(busy_percent)
 
         # wordcloud
     st.title('WordCloud')
     dk_wc = analysis_code.create_wordcloud(selected_user, dk)
     fig, ax = plt.subplots()
     plt.figure(figsize=(10, 8))
     ax.imshow(dk_wc)
     st.pyplot(fig)
 
     # most common words
     st.title("Most Common Word used by user")
     most_common_dk = analysis_code.most_common_word(selected_user, dk)
     fig,ax = plt.subplots()
     ax.barh(most_common_dk[0],most_common_dk[1])
     #plt.figure(figsize=(8,10))
     plt.xticks(rotation = 'vertical')
     st.pyplot(fig)
     #st.dataframe(most_common_dk)
 
     # emoji analysis
     emoji_dk = analysis_code.emojis_number(selected_user,dk)
     st.title("User emoji analysis")
     col_1, col_2 = st.columns(2)
     with col_1:
          st.dataframe(emoji_dk)
     with col_2:
          fig,ax = plt.subplots()
          
          plt.title('Top 5 most used emoji by user' )
          ax.pie(emoji_dk[1].head(),labels = emoji_dk[0].head() ,autopct="%.2f%%")
          st.pyplot(fig)