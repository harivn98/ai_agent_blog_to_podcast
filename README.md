# Blog to Podcast Agent

## Overview
This project is a Streamlit application that converts blog posts into podcast-style audio summaries. It scrapes blog content using the Firecrawl API, processes it with a Groq language model, and generates audio using ElevenLabs text-to-speech.

## Features
- Scrapes blog content from a provided URL
- Generates concise, conversational podcast summaries
- Converts summaries to audio using ElevenLabs
- Supports multiple Groq models with automatic fallback
- Provides a web interface for user input and audio playback

## Requirements
- Python 3.8+
- Streamlit
- Requests
- agno (custom library for agent functionality)
- API keys for:
  - Groq (language model)
  - ElevenLabs (text-to-speech)
  - Firecrawl (web scraping)

## Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/your-username/blog-to-podcast-agent.git
   cd blog-to-podcast-agent
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Set up environment variables:
   - Create a `.env` file or set the following environment variables:
     ```
     GROQ_API_KEY=your_groq_api_key
     ELEVEN_LABS_API_KEY=your_elevenlabs_api_key
     FIRECRAWL_API_KEY=your_firecrawl_api_key
     ```

## Usage
1. Run the Streamlit app:
   ```bash
   streamlit run ai_blog_to_podcast_agent.py
   ```
2. Open the provided local URL in a browser.
3. Enter your API keys in the sidebar.
4. Select a Groq model and configure fallback settings.
5. Input a blog URL and click "Generate Podcast."
6. Listen to the generated audio and download the WAV file.

## Project Structure
- `app.py`: Main Streamlit application
- `audio_generations/`: Directory for generated audio files
- `requirements.txt`: Project dependencies

## Notes
- The application truncates scraped content to 4000 characters to avoid API rate limits.
- Audio files are saved in WAV format.
- Ensure API keys are kept secure and not exposed in version control.

## License
MIT License
