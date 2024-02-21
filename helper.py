from urlextract import URLExtract
from wordcloud import WordCloud
import pandas as pd
from collections import Counter
import emoji
extractor = URLExtract()
def fetch_stats(selected_user, df):
    if selected_user != 'overall':
        df = df[df['user'] == selected_user]

    num_messages = df.shape[0]
    # number of words
    words = []
    for message in df['message'] :
        words.extend(message.split())

    media_message = df[df['message'] == '<Media omitted>\n'].shape[0]

    links = []

    for message in df['message']:
        links.extend(extractor.find_urls(message))
    num_links = len(links)
    return num_messages, len(words), media_message, num_links

def most_busy_users(df):
    x = df['user'].value_counts().head()
    df = round((df['user'].value_counts() / df.shape[0]) * 100, 3).reset_index().rename(columns={'count': 'percent'})

    return x, df

def create_wordcloud(selected_user, df):
    if selected_user != 'overall':
        df = df[df['user'] == selected_user]

    temp = df[df['user'] != 'Group_Notification']
    temp = df[df['message'] != '<Media omitted>\n']

    wc = WordCloud(width=500, height=500, min_font_size=10, background_color='white')
    df_wc = wc.generate(temp['message'].str.cat(sep=" "))

    return df_wc

def most_common_words(selected_user, df):
    if selected_user != 'overall':
        df = df[df['user'] == selected_user]

    temp = df[df['user'] != 'Group_Notification']
    temp = df[df['message'] != '<Media omitted>\n']
    words = []

    for message in temp['message']:
        words.extend(message.split())

    return_words = pd.DataFrame(Counter(words).most_common(25))
    return return_words

def emoji_helper(selected_user, df):
    if selected_user != 'overall':
        df = df[df['user'] == selected_user]
    emojis = []
    for message in df['message']:
        emojis.extend([c for c in message if c in emoji.UNICODE_EMOJI['en']])

    emoji_df = pd.DataFrame(Counter(emojis).most_common(len(Counter(emojis))))

    return emoji_df

def monthly_timeline(selected_user, df) :
    if selected_user != 'overall':
        df = df[df['user'] == selected_user]

    timeline = df.groupby(['year', 'month_num', 'month']).count()['message'].reset_index()

    time = []
    for i in range(timeline.shape[0]):
        time.append(timeline['month'][i] + "-" + str(timeline['year'][i]))

    timeline['time'] = time

    return timeline

def daily_timeline_helper(selected_user, df) :
    if selected_user != 'overall':
        df = df[df['user'] == selected_user]

    daily_timeline = df.groupby('only_date').count()['message'].reset_index()

    return daily_timeline

def weekly_timeline_helper(selected_user, df) :
    if selected_user != 'overall' :
        df = df[df['user'] == selected_user]

    weekly_timeline = df.groupby('day_name').count()['message'].reset_index()

    return weekly_timeline

def monthly_timeline_helper(selected_user, df) :
    if selected_user != 'overall' :
        df = df[df['user'] == selected_user]

    busy_month = df.groupby('month').count()['message'].reset_index()

    return busy_month