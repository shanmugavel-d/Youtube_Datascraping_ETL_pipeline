from googleapiclient.discovery import build
import google_auth_oauthlib.flow
import googleapiclient.discovery
import googleapiclient.errors
import pandas as pd

api_keys =  "AIzaSyBnptkW1hwBA4goB5a2zvemb4YUknZOuhE"
youtube = build('youtube', 'v3', developerKey=api_keys)

def get_channel_data(channel_ids):
    all_data = []

    response = youtube.channels().list(
        part='snippet,contentDetails,statistics',
        id=channel_ids
    ).execute()

    channel = response['items'][0]
    channel_data = {
        'Channel Name': channel['snippet']['title'],
        'Channel ID': channel['id'],
        'Subscription Count': channel['statistics']['subscriberCount'],
        'Channel Views': channel['statistics']['viewCount'],
        "totalvideos": channel["statistics"]["videoCount"],
        'Channel Description': channel['snippet']['description'],
        "playlistId": channel["contentDetails"]["relatedPlaylists"]["uploads"],
    }
    all_data.append(channel_data)
    
    df1 = pd.DataFrame(all_data)
    
    playlist_id = df1["playlistId"][0]

    return (playlist_id,channel_data,df1)
def get_video_detail(playlist_id):
    video_ids = []

    request = youtube.playlistItems().list(
        part="snippet,contentDetails",
        playlistId=playlist_id,
        maxResults = 50
    )
    response = request.execute()

    for item in response['items']:
        video_ids.append(item['contentDetails']['videoId'])

    next_page_token = response.get('nextPageToken')
    while next_page_token is not None:
        request = youtube.playlistItems().list(
                    part='contentDetails',
                    playlistId = playlist_id,
                    maxResults = 50,
                    pageToken = next_page_token)
        response = request.execute()

        for item in response['items']:
            video_ids.append(item['contentDetails']['videoId'])

        next_page_token = response.get('nextPageToken')

    video_id =video_ids

    all_video_info = []

    for i in range(0, len(video_id), 50):
        request = youtube.videos().list(
            part="snippet,contentDetails,statistics",
            id=','.join(video_ids[i:i+50])
        )
        response = request.execute() 

        for video in response['items']:
            stats_to_keep = {'snippet': ['channelTitle', 'title', 'description', 'tags', 'publishedAt'],
                             'statistics': ['viewCount', 'likeCount', 'favouriteCount', 'commentCount'],
                             'contentDetails': ['duration', 'definition', 'caption']
                            }
            video_info = {"playlist_id":playlist_id}
            video_info['video_id'] = video['id']

            for k in stats_to_keep.keys():
                for v in stats_to_keep[k]:
                    try:
                        video_info[v] = video[k][v]
                    except:
                        video_info[v] = None

            all_video_info.append(video_info)

    video_data = pd.DataFrame(all_video_info )

    video_i = video_data["video_id"]

    return (video_i,all_video_info,video_data)
def get_all_video_comments(video_id):
    comments = []
    page_token = None
    
    while True:
        for i in range(len(video_id)):
            response = youtube.commentThreads().list(
                part='snippet',
                videoId=video_id[i],
                maxResults=100,
                pageToken=page_token
            ).execute()
            
            for item in response['items']:
                comment = item['snippet']['topLevelComment']['snippet']
                comment_data = {
                    "comment_id" : item["id"],
                    'Comment': comment['textDisplay'],
                    'Replies': [],
                    'Comment Author': comment['authorDisplayName'],
                    'Comment Published At': comment['publishedAt']
                }
                
                # Check if the comment has replies
                if 'replies' in item:
                    for reply in item['replies']['comments']:
                        reply_data = {
                            'Reply': reply['snippet']['textDisplay'],
                            'Reply Author': reply['snippet']['authorDisplayName'],
                            'Reply Published At': reply['snippet']['publishedAt']
                        }
                        comment_data['Replies'].append(reply_data)
                
                comments.append([video_id[i],comment_data])
            
            page_token = response.get('nextPageToken')
            
            if not page_token:
                break
    

        return {
            "comment_detail": comments
        }
def get_data(channel_ids):
    a =get_channel_data(channel_ids)
    playlist_id = a[0]
    b= get_video_detail(playlist_id)
    api_keys = "AIzaSyDyYizNqZLmxA7E-LJCov25tq4pWSLi5AY"
    youtube = build('youtube', 'v3', developerKey=api_keys)
    video_id = b[0]
    c = get_all_video_comments(video_id)

    return {
    "channel_detail":[a[1], b[1], c]
}