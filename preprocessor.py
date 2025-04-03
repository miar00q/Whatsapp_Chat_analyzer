import pandas as pd
import re


def preprocess(data):
    pattern = r'(\d{2}/\d{2}/\d{2,4}),\s*(\d{1,2}:\d{2}\s?[APap][Mm])\s-\s'

    messages = re.split(pattern, data)[1:]  # Skip first empty element
    parsed_data = []

    # iterate grouped elements (date, time, message)
    for i in range(0, len(messages), 3):
        date_str = messages[i]
        time_str = messages[i + 1].replace('\u202f', ' ').strip()  # remove hidden unicode spaces
        message = messages[i + 2].strip()

        parsed_data.append([date_str, time_str, message])

    df = pd.DataFrame(parsed_data, columns=['date', 'time', 'user_message'])

    # safely parsed datetime
    df['datetime'] = pd.to_datetime(df['date'] + ' ' + df['time'], dayfirst=True, errors='coerce')

    df.dropna(subset=['datetime'], inplace=True)

    # Splitting user from message safely
    def split_user_message(entry):
        parts = entry.split(': ', 1)
        if len(parts) == 2:
            return parts[0], parts[1]
        return "group_notification", entry

    df[['user', 'message']] = df['user_message'].apply(split_user_message).tolist()
    df.drop(columns=['user_message'], inplace=True)

    # Further datetime enhancements:
    df['only_date'] = df['datetime'].dt.date
    df['day_name'] = df['datetime'].dt.day_name()
    df['year'] = df['datetime'].dt.year
    df['month_num'] = df['datetime'].dt.month
    df['month'] = df['datetime'].dt.month_name()
    df['day'] = df['datetime'].dt.day
    df['hour'] = df['datetime'].dt.hour
    df['minute'] = df['datetime'].dt.minute

    df['period'] = df['hour'].apply(lambda hour: f"{hour:02}-{(hour + 1) % 24:02}")

    return df
