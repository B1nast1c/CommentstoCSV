import os
from dotenv import load_dotenv
from googleapiclient.discovery import build
from converter.comments import process_comments, make_csv

load_dotenv()
API_KEY = os.getenv("API_KEY")
youtube = build("youtube", "v3", developerKey=API_KEY)

def search_result(query):
    request = youtube.search().list(
        part="snippet",
        q=query,
        maxResults=10,
    )

    return request.execute()

def comment_threads(channelID, to_csv=False):    
    comments_list = []
    
    request = youtube.commentThreads().list(
        part='id,replies,snippet',
        videoId=channelID,
    )
    response = request.execute()
    comments_list.extend(process_comments(response['items']))

    # if there is nextPageToken, then keep calling the API
    while response.get('nextPageToken', None):
        request = youtube.commentThreads().list(
            part='id,replies,snippet',
            videoId=channelID,
            pageToken=response['nextPageToken']
        )
        response = request.execute()
        comments_list.extend(process_comments(response['items']))
    
    if to_csv:
        make_csv(comments_list)
    
    return comments_list

if __name__ == '__main__':
    pyscriptVidId = 'Qo8dXyKXyME'

    # response = search_result("pyscript")
    response = comment_threads(pyscriptVidId, to_csv=True)

    print(response)
