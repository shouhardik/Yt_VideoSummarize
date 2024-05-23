import streamlit as st
from dotenv import load_dotenv

load_dotenv()
import os
import google.generativeai as genai
from youtube_transcript_api import YouTubeTranscriptApi

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

prompt="""You are Yotube video summarizer. You will be taking the transcript text
and summarizing the entire video and providing the important summary in points
within 250 words. Please provide the summary of the text given here:  """

def generateTranscripts(videoUrl):
    try:
        
        videoId=videoUrl.split("=")[1] # only get the ID after = in the youtube video url
        entireText=YouTubeTranscriptApi.get_transcript(videoId) # a List
        transcript=""
        for i in entireText:
            transcript+= " "+i["text"]

        return transcript
    except Exception as e:
        raise e

def generateContent(transcript, prompt):
    model=genai.GenerativeModel("gemini-pro")
    response=model.generate_content(prompt+transcript)
    return response.text
       
st.title("YouTube Transcript to Detailed Notes Converter")
youtube_link = st.text_input("Enter YouTube Video Link:")

if youtube_link:
    video_id = youtube_link.split("=")[1]
    print(video_id)
    st.image(f"http://img.youtube.com/vi/{video_id}/0.jpg", use_column_width=True)

if st.button("Get Detailed Notes"):
    transcript_text=generateTranscripts(youtube_link)

    if transcript_text:
        summary=generateContent(transcript_text,prompt)
        st.markdown("## Detailed Notes:")
        st.write(summary)
        

