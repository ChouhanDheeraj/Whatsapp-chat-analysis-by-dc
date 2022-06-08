from email import message
from urlextract import URLExtract
import matplotlib.pyplot as plt
from wordcloud import WordCloud
import wordcloud
from collections import Counter
import pandas as pd
import emoji

def fetch_stats(selected_user,dk):
    if selected_user != 'Overall':
        dk= dk[dk['user'] == selected_user]
        # fetching total number of messages
    num_messages = dk.shape[0]
     # fetchinh number of words
    words = []
    for message in dk['message']:
        words.extend(message.split())
    # fetching number of media messages
    num_media_msg = dk[dk['message'] == '<Media omitted>'].shape[0]

    # fetching number of URLS
    extractor = URLExtract()
    links = []
    for message in dk['message']:
        links.extend(extractor.find_urls(message))
    return num_messages, len(words), num_media_msg,len(links)

def most_vella_user(dk):
    x = dk.user.value_counts().head()
    df = round((dk.user.value_counts()/dk.shape[0])*100,2).reset_index().rename(columns ={'index':'Name','user':'Percent'})
    return x,df
   
def create_wordcloud(selected_user,dk):    
    if selected_user != 'Overall':
        dk= dk[dk['user'] == selected_user]
    temp  = dk[dk['user'] != 'group_notification' ]
    new_temp = temp[temp['message'] != '<Media omitted>']
    f = open('hinglish.txt','r')
    stop_words = f.read()
    stop_word = stop_words.split('\n')
    words = []
    def remove_stop_Words(message):
        y = []
        for word in message.lower().split():
            if word not in stop_word:
                y.append(word)
        return ' '.join(y)
    new_temp['message'] = new_temp['message'].apply(remove_stop_Words)
    wc = WordCloud(width=500,height=400,min_font_size=5,background_color='white')
    dk_wc = wc.generate(new_temp['message'].str.cat(sep = ' '))
    return dk_wc
       
    
def most_common_word(selected_user,dk):
    if selected_user != 'Overall':
        dk= dk[dk['user'] == selected_user]
    temp  = dk[dk['user'] != 'group_notification' ]
    new_temp = temp[temp['message'] != '<Media omitted>']
    f = open('hinglish.txt','r')
    stop_words = f.read()
    stop_word = stop_words.split('\n')
    words = []
    for message in new_temp['message']:
        for word in message.lower().split():
            if word not in stop_word:
                words.append(word)
    return_df =  pd.DataFrame(Counter(words).most_common(20))
    return return_df

def emojis_number(selected_user,dk):
    if selected_user != 'Overall':
        dk= dk[dk['user'] == selected_user]
    emojis = []
    for message in dk['message']:
        emojis.extend([c for c in message if c in emoji.UNICODE_EMOJI['en']])
    emoji_dk = pd.DataFrame(Counter(emojis).most_common(len(Counter(emojis))))

    return emoji_dk

def monthly_timeline(selected_user,dk):
    if selected_user != 'Overall':
        dk= dk[dk['user'] == selected_user]
    Timeline = dk.groupby(['Year','Month_num','Month']).count()['message'].reset_index()
    time = []
    for i in range(Timeline.shape[0]):
        time.append(Timeline['Month'][i]+ '-' + str(Timeline['Year'][i]))
    Timeline['Time'] = time
    return Timeline

def user_daily_timeline(selected_user,dk):
    if selected_user != 'Overall':
        dk= dk[dk['user'] == selected_user]
    daily_timeline = dk.groupby('only_date').count()['message'].reset_index()
    return daily_timeline

def weekly_activity_analysis(selected_user,dk):
    if selected_user != 'Overall':
        dk= dk[dk['user'] == selected_user]
    return dk['day_name'].value_counts(sort = True)

def monthly_activity_analysis(selected_user,dk):
    if selected_user != 'Overall':
        dk= dk[dk['user'] == selected_user]
    return dk['Month'].value_counts(sort = True)

def Activity(selected_user,dk):
    if selected_user != 'Overall':
        dk= dk[dk['user'] == selected_user]
    activity_heatmap = dk.pivot_table(index = 'day_name',columns = 'Period', values = 'message',aggfunc='count').fillna(0)
    return activity_heatmap