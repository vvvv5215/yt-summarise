from youtube_transcript_api import YouTubeTranscriptApi
import re
import requests
import streamlit as st

def get_video_id(url):
    """Extract the video ID from a YouTube URL."""
    regex = r"(?:v=|youtu.be/|embed/)([\w-]{11})"
    match = re.search(regex, url)
    if match:
        return match.group(1)
    raise ValueError("Invalid YouTube URL")

def fetch_subtitles(video_url, lang='en'):
    """Fetch subtitles for a given YouTube video URL."""
    video_id = get_video_id(video_url)
    try:
        transcript = YouTubeTranscriptApi.get_transcript(video_id, languages=[lang])
        text = ' '.join([entry['text'] for entry in transcript])
        return text
    except Exception as e:
        raise RuntimeError(f"Could not fetch subtitles: {e}")

def clean_text(text):
    """Clean and process the transcript text."""
    text = re.sub(r'\s+', ' ', text)
    text = re.sub(r'\[.*?\]', '', text)  # Remove [Music], [Applause], etc.
    return text.strip()

def chunk_text(text, max_words=400):
    """Split text into chunks of up to max_words words."""
    words = text.split()
    chunks = []
    for i in range(0, len(words), max_words):
        chunk = ' '.join(words[i:i+max_words])
        chunks.append(chunk)
    return chunks

def hf_api_summarize(text, model="facebook/bart-large-cnn", max_words=400):
    """
    Summarize text using HuggingFace Inference API, handling long texts by chunking.
    If the transcript is very long, do a second summarization pass on the combined summaries.
    """
    api_key = st.secrets["hf_api"]["key"]
    endpoint = f"https://api-inference.huggingface.co/models/{model}"
    headers = {"Authorization": f"Bearer {api_key}"}
    
    # Split into manageable chunks
    chunks = chunk_text(text, max_words=max_words)
    summaries = []
    for chunk in chunks:
        payload = {"inputs": chunk}
        response = requests.post(endpoint, headers=headers, json=payload)
        if response.status_code == 200:
            result = response.json()
            if isinstance(result, list) and "summary_text" in result[0]:
                summaries.append(result[0]["summary_text"])
            else:
                raise RuntimeError(f"Unexpected API response: {result}")
        else:
            raise RuntimeError(f"HuggingFace API error: {response.status_code} {response.text}")
    combined_summary = ' '.join(summaries)
    # If the combined summary is still long, summarize again (hierarchical)
    if len(combined_summary.split()) > max_words:
        payload = {"inputs": combined_summary}
        response = requests.post(endpoint, headers=headers, json=payload)
        if response.status_code == 200:
            result = response.json()
            if isinstance(result, list) and "summary_text" in result[0]:
                return result[0]["summary_text"]
            else:
                raise RuntimeError(f"Unexpected API response: {result}")
        else:
            raise RuntimeError(f"HuggingFace API error: {response.status_code} {response.text}")
    return combined_summary 