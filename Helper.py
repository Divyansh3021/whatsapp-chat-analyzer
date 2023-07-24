from urlextract import URLExtract
from wordcloud import WordCloud
import pandas as pd
from collections import Counter

extract = URLExtract()

def fetch_stats(selected_user, df):
    if selected_user != "Overall":
        df = df[df['user'] == selected_user]
    num_messages = df.shape[0]
    words = []
    for message in df['message']:
        words.extend(message.split())

    links = []
    for message in df['message']:
        links.extend(extract.find_urls(message))

    num_media_msg = df[df['message'] == "<Media omitted>"].shape[0]
    
    return num_messages, len(words), num_media_msg, len(links)

def most_active_users(df):
    x = df['user'].value_counts().head()
    return x

def create_wordcloud(selected_user, df):
    
    f = open("stop_hinglish.txt", "r")
    stop_words = f.read()

    if selected_user != "Overall":
        df = df[df['user'] == selected_user]

    temp = df[df['user'] != 'group notification']
    temp = temp[temp['message'] != "<Media omitted>"]


    def remove_stopwords(message):
        y = []
        for word in message.lower().split():
            if word not in stop_words:
                y.append(word)

        return " ".join(y)

    wc = WordCloud(width=500, height=500, min_font_size=10, background_color='white')
    temp['message'] = temp['message'].apply(remove_stopwords)
    df_wc = wc.generate(temp['message'].str.cat(sep=" "))
    return df_wc

def most_common_words(selected_user, df):

    f = open("stop_hinglish.txt", "r")
    stop_words = f.read()

    if selected_user != "Overall":
        df = df[df['user'] == selected_user]

    temp = df[df['user'] != 'group notification']
    temp = temp[temp['message'] != "<Media omitted>"]

    words = []

    for message in temp['message']:
        for word in message.lower().split():
            if word not in stop_words:
                words.append(word)
    
    return_df = pd.DataFrame(Counter(words).most_common(20))
    return return_df