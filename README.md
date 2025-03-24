News Summarization and Text-to-Speech (TTS) Application

Objective

This project is a web-based application that extracts key details from multiple news articles related to a given company, performs sentiment analysis, conducts a comparative analysis, and generates a text-to-speech (TTS) output in Hindi.

Features

News Extraction: Scrapes and displays the title, summary, and other metadata from at least 10 news articles related to the company.

Sentiment Analysis: Analyzes the sentiment of each news article (Positive, Negative, Neutral).

Comparative Analysis: Evaluates how the company is covered across different news articles.

Hindi Text-to-Speech: Converts summarized content into Hindi speech.

User Interface: Built with Streamlit for interactive user experience.

API Development: Implements FastAPI to manage backend services.

Deployment: Hosted on Hugging Face Spaces.

Technologies Used

Python

Streamlit (for UI)

FastAPI (for API development)

BeautifulSoup (bs4) (for web scraping)

Transformers (for sentiment analysis)

gTTS (for Hindi TTS conversion)

Uvicorn (for running FastAPI server)

Installation and Setup

1) Clone the repository:
   git clone <repository-url>
   cd <repository-folder>
2) Install dependencies:
  pip install -r requirements.txt

3) Run the FastAPI backend:
   uvicorn run:app --host 0.0.0.0 --port 8000

4) Run the Streamlit frontend:
   streamlit run run.py

API Endpoints

POST /analyze: Accepts JSON input { "company_name": "Tesla" }, returns article details, sentiment analysis, and Hindi TTS audio file.

Usage

Enter a company name in the Streamlit interface.

Click on "Analyze News" to fetch articles and perform sentiment analysis.

View structured sentiment insights and listen to the Hindi TTS summary.

Deployment

Hosted on Hugging Face Spaces: Deployment Link (Replace with actual link)

Assumptions & Limitations

News scraping is limited to non-JS-based web pages.

Sentiment analysis is based on article summaries.

Accuracy of TTS depends on the gTTS model.

Contribution

Feel free to raise issues and contribute to improving the project.
