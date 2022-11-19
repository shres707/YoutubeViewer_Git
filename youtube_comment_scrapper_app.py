import streamlit as st
from urllib.parse import urlparse, parse_qs
from apiclient.discovery import build
from urllib.error import HTTPError
import pandas as pd
import validators
import numpy as np


api_key = "AIzaSyAbfQaHhx_hMGjQw4DwYsdGHfSG1cUWs3E" # Replace this  api key with your own.

youtube = build('youtube', 'v3', developerKey=api_key,cache_discovery=False)

#box = [['Name', 'Comment', 'Time', 'Likes', 'Reply Count']]


def get_id(url):
    u_pars = urlparse(url)
    quer_v = parse_qs(u_pars.query).get('v')
    if quer_v:
        return quer_v[0]
    pth = u_pars.path.split('/')
    if pth:
        return pth[-1]


def scrape_comments_with_replies(url):

    box=[] 

    ret=validators.url(url)
   

    if ret != True:
      st.write("URL entered is not valid , Please enter valid one ")
      return

    ID=get_id(url)

    
    try:   
        data = youtube.commentThreads().list(part='snippet', videoId=ID, maxResults='100', textFormat="plainText").execute()

    except Exception as e:
            st.write("Url has no comments")
            return

     

    for i in data["items"]:

        name = i["snippet"]['topLevelComment']["snippet"]["authorDisplayName"]
        comment = i["snippet"]['topLevelComment']["snippet"]["textDisplay"]
        published_at = i["snippet"]['topLevelComment']["snippet"]['publishedAt']
        likes = i["snippet"]['topLevelComment']["snippet"]['likeCount']
        replies = i["snippet"]['totalReplyCount']
       

        box.append([name, comment, published_at, likes, replies])
       
        totalReplyCount = i["snippet"]['totalReplyCount']

        if totalReplyCount > 0:

            parent = i["snippet"]['topLevelComment']["id"]

            data2 = youtube.comments().list(part='snippet', maxResults='100', parentId=parent,
                                            textFormat="plainText").execute()

            for i in data2["items"]:
                name = i["snippet"]["authorDisplayName"]
                comment = i["snippet"]["textDisplay"]
                published_at = i["snippet"]['publishedAt']
                likes = i["snippet"]['likeCount']
                replies = ""

                box.append([name, comment, published_at, likes, replies])

    while ("nextPageToken" in data):

        data = youtube.commentThreads().list(part='snippet', videoId=ID, pageToken=data["nextPageToken"],
                                             maxResults='100', textFormat="plainText").execute()

        for i in data["items"]:
            name = i["snippet"]['topLevelComment']["snippet"]["authorDisplayName"]
            comment = i["snippet"]['topLevelComment']["snippet"]["textDisplay"]
            published_at = i["snippet"]['topLevelComment']["snippet"]['publishedAt']
            likes = i["snippet"]['topLevelComment']["snippet"]['likeCount']
            replies = i["snippet"]['totalReplyCount']

            box.append([name, comment, published_at, likes, replies])

            totalReplyCount = i["snippet"]['totalReplyCount']

            if totalReplyCount > 0:

                parent = i["snippet"]['topLevelComment']["id"]

                data2 = youtube.comments().list(part='snippet', maxResults='100', parentId=parent,
                                                textFormat="plainText").execute()

                for i in data2["items"]:
                    name = i["snippet"]["authorDisplayName"]
                    comment = i["snippet"]["textDisplay"]
                    published_at = i["snippet"]['publishedAt']
                    likes = i["snippet"]['likeCount']
                    replies = ''

                    box.append([name, comment, published_at, likes, replies])



    df = pd.DataFrame({'Name': [i[0] for i in box], 'Comment': [i[1] for i in box], 'Time': [i[2] for i in box],
                       'Likes': [i[3] for i in box], 'Reply Count': [i[4] for i in box]})
                       
    df.index = np.arange(1, len(df)+1)            
    
    test = df.astype(str)
    
    if test not in st.session_state:
       st.session_state.test=test 
       
       
    #st.dataframe(test)
    st.write("Comments have been Successfully Scrapped and stored as DataFrame")
    
    df.to_csv('youtube-comments_1.csv', index=False, header=True)


    #return "Successful! Check the CSV file that you have just created."

def app():
  st.title("YouTube Comment Reviewer")
  with st.form(key='myform',clear_on_submit=True):
       url = st.text_input('Enter the YouTube Url')
       submit_button = st.form_submit_button("Submit")
       if submit_button:
           scrape_comments_with_replies(url) 
           
  
        
  
  
 




