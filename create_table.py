from app import *
from edit_file import *
from pymongo import MongoClient
import mysql.connector

client = MongoClient()
db = client.Youtube_data
collection = db.Database

def send_data(a):
    client = MongoClient()
    db = client.Youtube_data
    collection = db.Database
    

    # Insert a document
    collection.insert_one(a)

def migrate_data():
    client = MongoClient()
    db = client.Youtube_data
    collection = db.Database


    mongo = list(collection.find())

    mydb = mysql.connector.connect(
    host="127.0.0.1",
    user="root",
    password="1234",
    database="Youtube_Databases"
    )

    mycursor = mydb.cursor()


    channel_table = '''
    CREATE TABLE IF NOT EXISTS channels (
        id VARCHAR(255) NOT NULL ,
        channel_name VARCHAR(255),
        subscription_count INT(11),
        views INT(11),
        description TEXT,
        PRIMARY KEY (id)
    );
    '''
    mycursor = mydb.cursor()
    mycursor.execute(channel_table)
    mydb.commit()

    channel_detail = mongo[-1]["channel_detail"][0]
    channel_detail = convert_str_to_int(channel_detail)

    mycursor = mydb.cursor()


    query = '''
    INSERT INTO channels (id, channel_name, subscription_count, views, description) 
    VALUES (%s, %s, %s, %s,%s)
    '''


    values = (channel_detail['Channel ID'],channel_detail['Channel Name'],channel_detail['Subscription Count'] , channel_detail['Channel Views'], channel_detail[ 'Channel Description'])
    mycursor.execute(query, values)
    mydb.commit()

    playlist_table = '''
    CREATE TABLE IF NOT EXISTS playlists (
        playlist_ids VARCHAR(255) NOT NULL, 
        channel_id VARCHAR(255),
        channel_name VARCHAR(255),
        PRIMARY KEY (playlist_ids),
        FOREIGN KEY (channel_id) REFERENCES channels(id)
    );
    '''
    mycursor = mydb.cursor()
    mycursor.execute(playlist_table)
    mydb.commit()

    mycursor = mydb.cursor()

    query = '''
    INSERT INTO playlists (playlist_ids, channel_id, channel_name)
    VALUES (%s, %s, %s)
    '''
    values = (channel_detail['playlistId'], channel_detail['Channel ID'], channel_detail['Channel Name'])
    mycursor.execute(query, values)
    mydb.commit()

    video_table = '''
    CREATE TABLE IF NOT EXISTS videos (
        video_ids VARCHAR(255) NOT NULL,
        playlist_id VARCHAR(255),
        video_name VARCHAR(255),
        video_description TEXT,
        published_at DATETIME,
        view_count INT(11),
        like_count INT(11),
        favorite_count INT(11),
        comment_count INT(11),
        duration INT(11),
        thumbnail TEXT,
        caption_status VARCHAR(255),
        PRIMARY KEY (video_ids),
        FOREIGN KEY (playlist_id) REFERENCES playlists(playlist_ids)
    );
    '''
    mycursor = mydb.cursor()
    mycursor.execute(video_table)
    mydb.commit()

    video_detail = mongo[-1]["channel_detail"][1]

    video_details =[]
    video_time = []
    video_date = []

    for i in range(len(video_detail)):
        v = video_detail[i]
        v = convert_str_to_int(v)
        video_details.append(v)
        t = video_detail[i]['duration']
        t = convert_duration_to_seconds(t)
        video_time.append(t)
        d = video_detail[i]['publishedAt']
        d = convert_to_mysql_datetime(d)
        video_date.append(d)

    mycursor = mydb.cursor()
    for i in range(len(video_detail)):
        mycursor = mydb.cursor()
        query = '''
        INSERT INTO videos (video_ids,playlist_id, video_name, video_description, published_at, view_count, like_count,
                            favorite_count, comment_count, duration, thumbnail, caption_status)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        '''
        values = (
            video_details[i]['video_id'],
            video_details[i]['playlist_id'],
            video_details[i]['title'],
            video_details[i]['description'],
            video_date[i],
            video_details[i]['viewCount'],
            video_details[i][ 'likeCount'],
            video_details[i]['favouriteCount'],
            video_details[i]['commentCount'],
            video_time[i],
            "None",
            video_details[i][ 'caption']
        )
        mycursor.execute(query, values)
        

    mydb.commit()

    comment_table = '''
    CREATE TABLE IF NOT EXISTS comments (
        comment_ids VARCHAR(255) NOT NULL,
        video_id VARCHAR(255),
        comment TEXT,
        reply TEXT,
        author VARCHAR(255),
        published_at DATETIME,
        PRIMARY KEY (comment_ids),
        FOREIGN KEY (video_id) REFERENCES videos(video_ids)
    );
    '''
    mycursor = mydb.cursor()
    mycursor.execute(comment_table)
    mydb.commit()

    comment_detail = mongo[-1]["channel_detail"][2]["comment_detail"]
    comment_video_id = []
    comment_details = []
    comment_date = []
    for i in range(len(comment_detail)):
        id = comment_detail[i][0]
        comment_video_id.append(id)
        date = comment_detail[i][1]['Comment Published At']
        date = convert_to_mysql_datetime(date)
        comment_date.append(date)
        comment = comment_detail[i][1]
        comment_details.append(comment)

    for i in range(len(comment_detail)):
        mycursor = mydb.cursor()
        query = '''
        INSERT INTO comments ( comment_ids,video_id, comment, reply, author, published_at)
        VALUES (%s, %s, %s, %s, %s,%s)
        '''
        values = (comment_details[i]['comment_id'],comment_video_id[i],comment_details[i]['Comment'],"None",comment_details[i]['Comment Author'],comment_date[i])
        mycursor.execute(query, values)
        

    mydb.commit()

