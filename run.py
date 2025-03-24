import streamlit as st
import requests
from bs4 import BeautifulSoup
from collections import defaultdict
from gtts import gTTS
from transformers import pipeline
import os
from fastapi import FastAPI
from pydantic import BaseModel
import uvicorn
import threading

# Initialize FastAPI app
app = FastAPI()
# Initialize sentiment analysis pipeline
sentiment_pipeline = pipeline("sentiment-analysis")

class CompanyRequest(BaseModel):
    company_name: str

def scrape_news(company_name):
    """Scrapes news articles related to the given company."""
    url = f"https://www.bbc.co.uk/search?q={company_name}"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    articles = []
    for item in soup.find_all('div', class_='ssrcss-1f3bvyz-Stack e1y4nx260'): 
        title = item.find('a').text.strip()
        link = "https://www.bbc.co.uk" + item.find('a')['href']
        summary = item.find('p').text.strip() if item.find('p') else "No summary available."
        articles.append({"title": title, "link": link, "summary": summary})
        if len(articles) >= 10:
            break
    return articles

def analyze_sentiment(text):
    """Performs sentiment analysis on the given text."""
    result = sentiment_pipeline(text)
    return result[0]['label']

def comparative_analysis(articles):
    """Generates comparative insights from sentiment analysis results."""
    sentiment_count = defaultdict(int)
    for article in articles:
        sentiment = article['sentiment']
        sentiment_count[sentiment] += 1
    return {
        "sentiment_distribution": dict(sentiment_count),
        "overall_sentiment": max(sentiment_count, key=sentiment_count.get, default="NEUTRAL")
    }

def generate_hindi_tts(text, filename="output.mp3"):
    """Generates Hindi speech from text and saves it as an audio file."""
    tts = gTTS(text=text, lang='hi')
    tts.save(filename)
    return filename

@app.post("/analyze")
def analyze_news(data: CompanyRequest):
    company_name = data.company_name
    articles = scrape_news(company_name)
    for article in articles:
        article['sentiment'] = analyze_sentiment(article['summary'])
    insights = comparative_analysis(articles)
    summary_text = (
        f"{company_name} के बारे में समाचारों का सारांश: "
        f"कुल {len(articles)} लेखों में से {insights['sentiment_distribution'].get('POSITIVE', 0)} सकारात्मक, "
        f"{insights['sentiment_distribution'].get('NEGATIVE', 0)} नकारात्मक, "
        f"{insights['sentiment_distribution'].get('NEUTRAL', 0)} तटस्थ हैं।"
    )
    tts_filename = generate_hindi_tts(summary_text)
    return {"articles": articles, "insights": insights, "tts_filename": tts_filename}

def run_api():
    uvicorn.run(app, host="0.0.0.0", port=8000)

# Start FastAPI server in a separate thread
threading.Thread(target=run_api, daemon=True).start()

# Streamlit Web Interface
st.title("📊 News Sentiment Analysis & Hindi TTS")
st.write("Enter a company name to fetch news articles and analyze sentiment.")

company_name = st.text_input("Enter Company Name")
if st.button("Analyze News") and company_name:
    response = requests.post("http://127.0.0.1:8000/analyze", json={"company_name": company_name})
    if response.status_code == 200:
        data = response.json()
        articles = data['articles']
        insights = data['insights']
        tts_filename = data['tts_filename']
        
        for article in articles:
            st.subheader(article['title'])
            st.write(f"**Summary:** {article['summary']}")
            st.write(f"**Sentiment:** {article['sentiment']}")
            st.markdown(f"[Read more]({article['link']})")
            st.divider()
        
        st.subheader("📊 Comparative Sentiment Analysis")
        st.write(f"Sentiment Distribution: {insights['sentiment_distribution']}")
        st.write(f"Overall Sentiment: {insights['overall_sentiment']}")
        
        st.audio(tts_filename, format='audio/mp3')
        os.remove(tts_filename)  # Clean up after playback
    else:
        st.error("Error fetching data. Try again.")
