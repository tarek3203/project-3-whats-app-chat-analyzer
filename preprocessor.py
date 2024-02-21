import re
import pandas as pd
def preprocess(data) :
    pattern = '\d{1,2}/\d{1,2}/\d{2,4},\s\d{1,2}:\d{2}\s-\s'

    message = re.split(pattern, data)[1:]
    date = re.findall(pattern, data)

    df = pd.DataFrame({'message': message, 'date': date})

    df['date'] = pd.to_datetime(df['date'], format='%d/%m/%Y, %H:%M - ')

    users = []
    user_messages_list = []

    for m in df['message']:
        entry = re.split('([\w\W]+?):\s', m)

        if entry[1:]:  # User name

            users.append(entry[1])
            user_messages_list.append(entry[2])
        else:
            users.append('Group_Notification')
            user_messages_list.append(entry[0])  # the whole string

    df['user'] = users
    df.drop(columns=['message'], inplace=True)
    df['message'] = user_messages_list

    df['year'] = df['date'].dt.year

    df['month'] = df['date'].dt.month_name()

    df['day'] = df['date'].dt.day
    df['hour'] = df['date'].dt.hour
    df['minute'] = df['date'].dt.minute
    df['month_num'] = df['date'].dt.month
    df['only_date'] = df['date'].dt.date
    df['day_name'] = df['date'].dt.day_name()

    return df
