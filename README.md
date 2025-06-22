# YouTube Video Summarizer

A simple Streamlit web app that fetches subtitles from a YouTube video and generates a concise summary using the Hugging Face Transformers API.

## Features

- Enter any YouTube video URL to get a summary of its subtitles.
- Automatically fetches and cleans subtitles using `youtube-transcript-api`.
- Summarizes long transcripts using Hugging Face's BART model.
- Clean, user-friendly interface built with Streamlit.

## Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/yourusername/your-repo.git
   cd your-repo
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up Hugging Face API key:**
   - Create a file at `.streamlit/secrets.toml` with the following content:
     ```toml
     [hf_api]
     key = "YOUR_HUGGINGFACE_API_KEY"
     ```
   - You can get a free API key from [Hugging Face](https://huggingface.co/settings/tokens).

## Usage

Run the app with:
```bash
streamlit run app.py
```

- Enter a YouTube video URL.
- Click "Fetch & Summarize".
- View the generated summary.

## File Structure

- `app.py` — Main Streamlit app.
- `utils.py` — Helper functions for fetching, cleaning, and summarizing subtitles.
- `requirements.txt` — Python dependencies.
- `.streamlit/secrets.toml` — (Not included) Store your Hugging Face API key here.

## Requirements

- Python 3.7+

## Troubleshooting

### Error: Could not fetch subtitles
If you see an error like:

```
Could not fetch subtitles: Could not retrieve a transcript for the video ...
YouTube is blocking requests from your IP.
```

This is caused by YouTube blocking requests from your IP address. Common reasons:
- Too many requests from your IP.
- Using a cloud/VPS IP (AWS, GCP, Azure, etc.), which YouTube often blocks.

**Solutions:**
- Try running the app from a different network (e.g., your home computer).
- Use a VPN or residential proxy to change your IP address.
- Wait and try again later (the block may be temporary).

## License

MIT License
