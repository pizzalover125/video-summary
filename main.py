from flask import Flask, render_template, redirect, url_for, request
import pathlib
import textwrap
import google.generativeai as genai
from youtube_transcript_api import YouTubeTranscriptApi
from pytube import extract, YouTube
from translate import Translator

genai.configure(api_key="AIzaSyANzX-sliAGKaJsw0Ic_VKdrkhZXkbFLn0")
model = genai.GenerativeModel('gemini-pro')

def generateResponse(input):
    response = model.generate_content(input)
    return response.text

def get_description(url):
    yt = YouTube(url)
    for n in range(6):
        try:
            description =  yt.initial_data["engagementPanels"][n]["engagementPanelSectionListRenderer"]["content"]["structuredDescriptionContentRenderer"]["items"][1]["expandableVideoDescriptionBodyRenderer"]["attributedDescriptionBodyText"]["content"]            
            return description
        except:
            continue
    return False

def videoSummary(vidURL):
    vidID = extract.video_id(vidURL)
    description = get_description(vidURL)
    transcript = YouTubeTranscriptApi.get_transcript(vidID)
    title = YouTube(vidURL).title
    return generateResponse(f"I have the transcript, title, and description of a Youtube Video. Using the transcript below, summarize the video. Also, each sentence cannot be longer than 500 characters. Title: {title}. Transcript: {transcript}. Description: {description}")

def translate_text(text, target_lang, source_lang="en"):
    translator = Translator(from_lang=source_lang, to_lang=target_lang)
    sentences = text.split(".")
    translations = []
    for sentence in sentences:
        translation = translator.translate(sentence)
        translations.append(translation)
    return '. '.join(translations)

app = Flask(__name__)
@app.route('/', methods=["POST", "GET"])
def main():
    if request.method == "POST":
        user_input = request.form['userInput']
        lang = request.form['lang']
        try:
            response = translate_text(videoSummary(user_input), lang)
            return render_template("index.html", response=response)
        except:
            return render_template("index.html", response="Invalid URL.")

        
    else:
        return render_template("index.html")

if __name__ == '__main__':
    app.run()