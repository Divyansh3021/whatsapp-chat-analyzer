from urlextract import URLExtract
from wordcloud import WordCloud

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
    if selected_user != "Overall":
        df = df[df['user'] == selected_user]

    wc = WordCloud(width=500, height=500, min_font_size=10, background_color='white')
    df_wc = wc.generate(df['message'].str.cat(sep=" "))
    return df_wc