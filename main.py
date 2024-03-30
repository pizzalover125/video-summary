from flask import Flask, render_template, redirect, url_for, request
import pathlib
import textwrap
import google.generativeai as genai
from youtube_transcript_api import YouTubeTranscriptApi
from pytube import extract

genai.configure(api_key="AIzaSyANzX-sliAGKaJsw0Ic_VKdrkhZXkbFLn0")
model = genai.GenerativeModel('gemini-pro')

def generateResponse(input):
    response = model.generate_content(input)
    return response.text

    
def videoSummary(vidURL):
    vidID = extract.video_id(vidURL)
    transcript = YouTubeTranscriptApi.get_transcript(vidID)
    return [generateResponse(f"I have the transcript of a Youtube Video. Using the transcript below, summarize the video. Please make it long. Transcript: {transcript}"), vidID]

app = Flask(__name__)
@app.route('/', methods=["POST", "GET"])
def main():
    if request.method == "POST":
        user_input = request.form['userInput']
        try:
            response = videoSummary(user_input)
            return render_template("index.html", response=response[0])
        except:
            return render_template("index.html", response="Error occured. Please try a URL with audio.")

        
    else:
        return render_template("index.html")

if __name__ == '__main__':
    app.run()