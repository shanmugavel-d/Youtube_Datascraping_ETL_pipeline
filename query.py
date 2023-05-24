import mysql.connector
import streamlit as st
import pandas as pd

mydb = mysql.connector.connect(
host="127.0.0.1",
user="root",
password="1234",
database="Youtube_Databases"
)

mycursor = mydb.cursor()
 
queries = {
    "1. What are the names of all the videos and their corresponding channels?": '''
        SELECT v.video_name, p.channel_name
        FROM videos v
        JOIN playlists p ON v.playlist_id = p.playlist_ids
        JOIN channels c ON p.channel_id = c.id;
    ''',
    "2. Which channels have the most number of videos, and how many videos do they have?": '''
        SELECT p.channel_name, COUNT(v.video_ids) AS video_count
        FROM playlists p
        JOIN videos v ON p.playlist_ids = v.playlist_id
        GROUP BY p.channel_name
        ORDER BY video_count DESC;
    ''',
    "3. What are the top 10 most viewed videos and their respective channels?": '''
        SELECT v.video_name, p.channel_name, v.view_count
        FROM videos v
        JOIN playlists p ON v.playlist_id = p.playlist_ids
        JOIN channels c ON p.channel_id = c.id
        ORDER BY v.view_count DESC
        LIMIT 10;
    ''',
    "4. How many comments were made on each video, and what are their corresponding video names?": '''
        SELECT v.video_name, COUNT(c.comment_ids) AS comment_count
        FROM videos v
        LEFT JOIN comments c ON v.video_ids = c.video_id
        GROUP BY v.video_name;
    ''',
    "5. Which videos have the highest number of likes, and what are their corresponding channel names?": '''
        SELECT v.video_name, p.channel_name, v.like_count
        FROM videos v
        JOIN playlists p ON v.playlist_id = p.playlist_ids
        JOIN channels c ON p.channel_id = c.id
        ORDER BY v.like_count DESC;
    ''',
    "7. What is the total number of views for each channel, and what are their corresponding channel names?": '''
        SELECT p.channel_name, SUM(v.view_count) AS total_views
        FROM channels c
        JOIN playlists p ON c.id = p.channel_id
        JOIN videos v ON p.playlist_ids = v.playlist_id
        GROUP BY p.channel_name;
    ''',
    "8. What are the names of all the channels that have published videos in the year 2022?": '''
        SELECT DISTINCT p.channel_name
        FROM channels c
        JOIN playlists p ON c.id = p.channel_id
        JOIN videos v ON p.playlist_ids = v.playlist_id
        WHERE strftime('%Y', v.published_at) = '2022';
    ''',
    "9. What is the average duration of all videos in each channel, and what are their corresponding channel names?": '''
        SELECT p.channel_name, AVG(v.duration) AS average_duration
        FROM channels c
        JOIN playlists p ON c.id = p.channel_id
        JOIN videos v ON p.playlist_ids = v.playlist_id
        GROUP BY p.channel_name;
    ''',
    "10. Which videos have the highest number of comments, and what are their corresponding channel names?": '''
        SELECT v.video_name, p.channel_name, COUNT(c.comment_ids) AS comment_count
        FROM videos v
        JOIN playlists p ON v.playlist_id = p.playlist_ids
        JOIN channels c ON p.channel_id = c.id
        JOIN comments cm ON v.video_ids = cm.video_id
        GROUP BY v.video_name, p.channel_name
        ORDER BY comment_count DESC;
    '''
}






