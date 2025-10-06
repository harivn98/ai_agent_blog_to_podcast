# 📰 ➡️ 🎙️ Blog to Podcast Agent

Transform any blog post into an engaging podcast with AI! This Streamlit app uses the Agno AI framework to scrape blog content, generate a conversational summary, and convert it to natural-sounding audio.

![Python](https://img.shields.io/badge/python-3.8+-blue.svg)
![Streamlit](https://img.shields.io/badge/streamlit-1.28+-red.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)

## ✨ Features

- 🔍 **Smart Web Scraping** - Automatically extracts main content from any blog URL using Firecrawl
- 🤖 **AI Summarization** - Creates engaging, conversational summaries using Groq's powerful LLMs
- 🎙️ **Text-to-Speech** - Converts summaries to natural-sounding audio using ElevenLabs
- 🔄 **Automatic Fallback** - Tries multiple AI models if one fails due to rate limits
- 📥 **Easy Download** - Download generated podcasts as WAV files
- 🎨 **Clean UI** - Simple, intuitive Streamlit interface

## 🚀 Demo

1. Enter a blog URL (e.g., `https://collabfund.com/blog/the-psychology-of-money/`)
2. Click "Generate Podcast"
3. Listen to or download your AI-generated podcast!

## 📋 Prerequisites

- Python 3.8 or higher
- API Keys for:
  - [Groq](https://console.groq.com) (Free tier available)
  - [ElevenLabs](https://elevenlabs.io) (Free tier: 10k characters/month)
  - [Firecrawl](https://firecrawl.dev) (Free tier: 500 scrapes/month)

## 🛠️ Installation

1. **Clone the repository**
```bash
git clone https://github.com/yourusername/blog-to-podcast-agent.git
cd blog-to-podcast-agent
```

2. **Create a virtual environment**
```bash
python -m venv .venv

# Windows
.venv\Scripts\activate

# macOS/Linux
source .venv/bin/activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Create `requirements.txt`** (if not exists)
```txt
streamlit>=1.28.0
agno>=0.1.0
groq>=0.4.0
firecrawl-py>=4.3.0
requests>=2.31.0
python-dotenv>=1.0.0
```

## 🔑 API Keys Setup

### Option 1: Via Streamlit UI (Recommended)
Simply enter your API keys in the sidebar when running the app.

### Option 2: Via Environment Variables
Create a `.env` file in the project root:
```env
GROQ_API_KEY=your_groq_api_key_here
ELEVEN_LABS_API_KEY=your_elevenlabs_api_key_here
FIRECRAWL_API_KEY=your_firecrawl_api_key_here
```

## 🎯 Usage

1. **Run the Streamlit app**
```bash
streamlit run ai_blog_to_podcast_agent.py
```

2. **Open your browser**
Navigate to `http://localhost:8501`

3. **Enter API Keys**
Add your API keys in the sidebar

4. **Generate Podcast**
- Paste a blog URL
- Select your preferred AI model
- Click "🎙️ Generate Podcast"
- Wait for processing (~30-60 seconds)
- Listen and download!

## 🤖 Supported AI Models

The app includes automatic fallback across 4 Groq models:

| Model | Best For | Speed | Token Limit |
|-------|----------|-------|-------------|
| **Llama 3.3 70B** | Most capable summaries | Moderate | 12,000 TPM |
| **Llama 3.1 8B** | Fast processing | Fastest | 6,000 TPM |
| **GPT-OSS 120B** | Large context | Fast | 8,000 TPM |
| **GPT-OSS 20B** | Balanced performance | Fast | 8,000 TPM |

## 📁 Project Structure

```
blog-to-podcast-agent/
│
├── ai_blog_to_podcast_agent.py    # Main Streamlit app
├── requirements.txt                # Python dependencies
├── README.md                       # This file
├── .env.example                    # Example environment file
├── .gitignore                      # Git ignore file
└── audio_generations/              # Generated podcast files (auto-created)
```

## 🔧 Configuration

### Adjust Content Length
Modify the truncation limit in `scrape_website()`:
```python
max_chars = 4000  # Change to your desired length
```

### Change Voice
Update the ElevenLabs voice ID:
```python
voice_id="JBFqnCBsd6RMkjVDRZzb"  # Replace with your preferred voice
```

Browse voices at [ElevenLabs Voice Library](https://elevenlabs.io/voice-library)

## 🐛 Troubleshooting

### "Rate limit exceeded" errors
- ✅ **Solution**: Enable automatic fallback (checkbox in sidebar)
- The app will try smaller models automatically

### "No content found" error
- Check if the URL is publicly accessible
- Ensure Firecrawl API key is valid
- Try a different blog URL

### Audio not generating
- Verify ElevenLabs API key has remaining credits
- Check character limit (max 2000 chars for summary)

### Import errors
```bash
pip install --upgrade agno groq firecrawl-py streamlit
```

## 📊 API Usage & Costs

| Service | Free Tier | Cost After |
|---------|-----------|------------|
| **Groq** | Generous limits | Free (currently) |
| **ElevenLabs** | 10k chars/month | $5/month for 30k |
| **Firecrawl** | 500 scrapes/month | $20/month for 5k |

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- [Agno](https://agno.dev) - AI agent framework
- [Groq](https://groq.com) - Lightning-fast LLM inference
- [ElevenLabs](https://elevenlabs.io) - Natural text-to-speech
- [Firecrawl](https://firecrawl.dev) - Web scraping API
- [Streamlit](https://streamlit.io) - Web app framework

## 📧 Contact

Your Name - [@yourtwitter](https://twitter.com/yourtwitter)

Project Link: [https://github.com/yourusername/blog-to-podcast-agent](https://github.com/yourusername/blog-to-podcast-agent)

---

⭐ Star this repo if you find it helpful!

Made with ❤️ and AI
