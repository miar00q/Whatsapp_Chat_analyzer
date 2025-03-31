import pandas as pd
import re

def preprocess(data):
    pattern = r'\d{2}/\d{2}/\d{4},\s\d{1,2}:\d{2}\s(?:am|pm)\s-\s'

    messages = re.split(pattern, data)
    dates = re.findall(pattern, data)

    # Find the minimum length between the two lists
    min_length = min(len(messages), len(dates))

    # Use only the first min_length elements from each list
    df = pd.DataFrame({
        'user_message': messages[:min_length],
        'message_date': dates[:min_length]
    })

    # Remove leading/trailing whitespaces and ensure encoding issues are handled
    df['message_date'] = df['message_date'].str.strip()

    # convert messages_date type
    df['message_date'] = pd.to_datetime(df['message_date'].str.replace('\u202f', ' ').str.strip(),
                                        format='%d/%m/%Y, %I:%M %p -')

    df.rename(columns={'message_date': 'date'}, inplace=True)

    # Splitting the user and messages
    users = []
    messages = []

    for message in df['user_message']:
        # This pattern will match names that may include parentheses, followed by colon and space
        entry = re.split(r'([^:]+):\s', message)

        if entry[1:]:
            users.append(entry[1])
            messages.append(entry[2])
        else:
            users.append('group_notification')
            messages.append(entry[0])

    df['user'] = users
    df['message'] = messages
    df.drop(columns=['user_message'], inplace=True)

    df['only_date'] = df['date'].dt.date
    df['only_date'] = pd.to_datetime(df['only_date'])

    df['day_name'] = df['date'].dt.day_name()
    df['year'] = df['date'].dt.year
    df['month_num'] = df['date'].dt.month
    df['month'] = df['date'].dt.month_name()
    df['day'] = df['date'].dt.day
    df['hour'] = df['date'].dt.hour
    df['minute'] = df['date'].dt.minute

    period = []

    for hour in df[['day_name', 'hour']]['hour']:
        if hour == 23:
            period.append(str(hour)+"-"+str('00'))
        elif hour == 0:
            period.append(str('00')+"-"+str(hour + 1))
        else:
            period.append(str(hour)+"-"+str(hour + 1))

    df['period'] = period

    return df


