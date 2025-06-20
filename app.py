import streamlit as st
import utils

st.set_page_config(page_title="YouTube Video Summarizer", layout="centered")
st.title("YouTube Video Summarizer")

st.write("Enter a YouTube video URL to get a summary of its subtitles.")

video_url = st.text_input("YouTube Video URL", "")

if st.button("Fetch & Summarize"):
    if not video_url:
        st.error("Please enter a YouTube video URL.")
    else:
        with st.spinner("Fetching subtitles and generating summary..."):
            try:
                raw_text = utils.fetch_subtitles(video_url)
                cleaned_text = utils.clean_text(raw_text)
                summary = utils.hf_api_summarize(cleaned_text)
                st.subheader("Summary of given video:")
                st.write(summary)
            except Exception as e:
                st.error(f"Error: {e}") 