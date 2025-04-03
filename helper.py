from collections import Counter
import pandas as pd
from wordcloud import WordCloud
import emoji

from urlextract import URLExtract
extract = URLExtract()

def fetch_stats(selected_user, df):

    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    #fetch the number of messages
    num_messages = df.shape[0]

    #fetch the number of words
    words = df['message'].dropna().astype(str).str.split().str.len().sum()

    #fetch the number of media
    num_media_messages = df[df['message'] == '<Media omitted>\n'].shape[0]

    #fetch the number links
    links = []
    for message in df['message']:
        links.extend(extract.find_urls(message))

    return num_messages, words, num_media_messages, len(links)


def most_busy_user(df):
    x = df['user'].value_counts()
    df = round((df['user'].value_counts()/df.shape[0])*100, 2).reset_index().rename(
        columns={'index':'user', 0:'percentage'})
    return x.head(25), df

def crate_word_cloud(selected_user, df):

    f = open('stop_hinglish.txt', 'r')
    stop_words = f.read()

    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    temp = df[df['user'] != 'group_notification']
    temp = temp[temp['message'] != '<Media omitted>\n']
    temp = temp[temp['message'] != 'null']
    temp = temp[temp['message'] != '<this']

    text = ' '.join(temp['message'])
    wordcloud = WordCloud(width=500, height=500,
                          background_color='white',
                          min_font_size=10).generate(text)
    return wordcloud

def most_common_words(selected_user, df):

    f = open('stop_hinglish.txt', 'r')
    stop_words = f.read()

    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    temp = df[df['user'] != 'group_notification']
    temp = temp[temp['message'] != '<Media omitted>\n']

    words = []

    for message in temp['message']:
        for word in message.lower().split():
            if word not in stop_words:
                words.append(word)

    # Counter.most_common() returns a list of tuples (word, count)
    most_common_word_list = Counter(words).most_common(20)

    # Create DataFrame with clear column names
    most_common_df = pd.DataFrame(most_common_word_list, columns=['Word', 'Count'])

    return most_common_df

def emoji_count(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    emoji_list = []
    for message in df['message']:
        # Updated approach to detect emojis using emoji.is_emoji
        emoji_list.extend([c for c in message if emoji.is_emoji(c)])

    # Create DataFrame with column names
    emoji_counts = Counter(emoji_list).most_common(len(Counter(emoji_list)))
    emoji_df = pd.DataFrame(emoji_counts, columns=['Emoji', 'Count'])

    return emoji_df

def monthly_timeline(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    timeline = df.groupby(['year', 'month_num']).size().reset_index(name='message')
    timeline['datetime'] = pd.to_datetime(timeline['year'].astype(str) + '-' +
                                          timeline['month_num'].astype(str).str.zfill(2) + '-01')
    timeline.sort_values('datetime', inplace=True)

    return timeline


def daily_timeline(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    daily_timeline = df.groupby('only_date').size().reset_index(name='message')
    daily_timeline['only_date'] = pd.to_datetime(daily_timeline['only_date'])
    daily_timeline.sort_values('only_date', inplace=True)

    return daily_timeline

def week_activity(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    return df['day_name'].value_counts()

def month_activity(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    return df['month'].value_counts()

def activity_heatmap(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    user_heatmap = df.pivot_table(index='day_name', columns='period', values='message', aggfunc='count').fillna(0)

    return user_heatmap