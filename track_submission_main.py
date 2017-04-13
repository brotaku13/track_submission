import config
import praw
from datetime import datetime
from datetime import timedelta
import matplotlib.pyplot as plt
import matplotlib.dates as dates
import time

def login():
    print('logging in...')
    r = praw.Reddit(client_id=config.client_id,
                    client_secret=config.client_secret,
                    user_agent=config.user_agent,
                    username=config.username,
                    password=config.password)
    print('logged in!')
    return r

def log_submission_timestamps(r, submission_id):
    timestamps = {}

    post = r.submission(id=submission_id)
    post_created = datetime.fromtimestamp(post.created_utc)

    print('getting comments for {}, num comments: {}, date created {}'.format(post.title, post.num_comments, post_created))
    post.comments.replace_more(limit=None)
    for comment in post.comments.list():
        timestamps[comment.id] = comment.created_utc

    print('comment dictionary created.')
    return timestamps

def display_graph_by_minute(r, timestamp_dict, submission_id):
    post = r.submission(id=submission_id)
    post_created = datetime.fromtimestamp(post.created_utc)
    datetime_list = []
    for value in timestamp_dict.values():
        datetime_list.append(datetime.fromtimestamp(value))  # fills a list with datetime timestamps

    # creates a dictionary with minute values and number of timestamps at that value {timestamp.minute : number of timestamps at that minute}
    comment_timestamp_dict = {}
    for time in datetime_list:
        if time.minute in comment_timestamp_dict:
            comment_timestamp_dict[time.minute] += 1
        else:
            comment_timestamp_dict[time.minute] = 1
    print(comment_timestamp_dict)

    # empty the dictionary into 2 lists
    xaxis_timestamps = []
    yaxis_num_comments = []

    for key, value in comment_timestamp_dict.items():
        xaxis_timestamps.append(key)
        yaxis_num_comments.append(value)

    # simple plot, don't want to spend too much time on this
    plt.plot(xaxis_timestamps, yaxis_num_comments)
    plt.show()

def display_graph_by_hour(r, time_dict, submission_id):
    post = r.submission(id=submission_id)
    datetime_list = []
    for value in time_dict.values():
        datetime_list.append(datetime.fromtimestamp(value))  # fills a list with datetime timestamps

    timestamp_dict = {}
    for timestamp in datetime_list:
        ts = timestamp.replace(minute=0, second=0, microsecond=0)
        if ts in timestamp_dict:
            timestamp_dict[ts] += 1
        else:
            timestamp_dict[ts] = 1
    print(timestamp_dict)
    xaxis_timestamps = []
    yaxis_num_comments = []

    for key in sorted(timestamp_dict.keys()):
        xaxis_timestamps.append(key)
        yaxis_num_comments.append(timestamp_dict[key])

    xaxis = [datetime.strptime(str(d), '%Y-%m-%d %H:%M:%S') for d in xaxis_timestamps]

    xs = dates.date2num(xaxis)
    hfmt = dates.DateFormatter('%m-%d %H: %M')

    fig = plt.figure()
    ax = fig.add_subplot(1,1,1)
    ax.xaxis.set_major_formatter(hfmt)
    plt.setp(ax.get_xticklabels(), rotation=15)
    ax.plot(xs, yaxis_num_comments)
    plt.grid(True)
    plt.show()






def main():
    r = login()
    submission_id = '64rgb9'
    timestamp_dict = log_submission_timestamps(r, submission_id)
    # display_graph_by_minute(r, timestamp_dict, submission_id)
    display_graph_by_hour(r, timestamp_dict, submission_id)


main()