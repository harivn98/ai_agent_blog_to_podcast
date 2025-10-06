import os
from uuid import uuid4
from agno.agent import Agent
from agno.models.groq import Groq as GroqModel
from agno.tools.eleven_labs import ElevenLabsTools
from agno.agent import RunResponse
from agno.utils.audio import write_audio_to_file
from agno.utils.log import logger
import streamlit as st
import requests

# ----------------------------
# Custom Firecrawl Tool (Fixed)
# ----------------------------
from agno.tools import Toolkit

class CustomFirecrawlTools(Toolkit):
    def __init__(self):
        super().__init__(name="firecrawl_tools")
        self.register(self.scrape_website)
    
    def scrape_website(self, url: str) -> str:
        """Scrape a website and return its content using Firecrawl API.
        
        Args:
            url: The URL to scrape
            
        Returns:
            The scraped content as markdown text (truncated to 4000 chars max)
        """
        api_key = os.getenv("FIRECRAWL_API_KEY")
        if not api_key:
            return "Error: FIRECRAWL_API_KEY not found in environment variables"
        
        api_url = "https://api.firecrawl.dev/v1/scrape"
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }
        payload = {
            "url": url,
            "formats": ["markdown"],
            "onlyMainContent": True
        }
        
        try:
            response = requests.post(api_url, headers=headers, json=payload, timeout=60)
            response.raise_for_status()
            data = response.json()
            
            if data.get("success"):
                if "data" in data and isinstance(data["data"], dict):
                    content = data["data"].get("markdown", "") or data["data"].get("content", "")
                elif "markdown" in data:
                    content = data.get("markdown", "")
                else:
                    content = data.get("content", "")
                
                if content:
                    # Truncate to max 4000 characters (~1000 tokens) to avoid rate limits
                    max_chars = 4000
                    if len(content) > max_chars:
                        content = content[:max_chars] + "\n\n[Content truncated due to length...]"
                    return content
                else:
                    return "Error: No content found in response"
            else:
                error_msg = data.get("error", "Unknown error")
                return f"Error: Firecrawl API failed - {error_msg}"
                
        except requests.exceptions.RequestException as e:
            return f"Error: Request failed - {str(e)}"
        except Exception as e:
            return f"Error: {str(e)}"

# ----------------------------
# Streamlit Page Setup
# ----------------------------
st.set_page_config(page_title="📰 ➡️ 🎙️ Blog to Podcast Agent", page_icon="🎙️")
st.title("📰 ➡️ 🎙️ Blog to Podcast Agent")

# ----------------------------
# Sidebar: API Keys
# ----------------------------
st.sidebar.header("🔑 API Keys")
groq_api_key = st.sidebar.text_input("Groq API Key", type="password")
elevenlabs_api_key = st.sidebar.text_input("ElevenLabs API Key", type="password")
firecrawl_api_key = st.sidebar.text_input("Firecrawl API Key", type="password")

# Model selection with fallback (4 models - removed compound as it doesn't support tool calling)
st.sidebar.header("🤖 Model Settings")
GROQ_MODELS = [
    ("llama-3.3-70b-versatile", "Llama 3.3 70B (Most capable)"),
    ("llama-3.1-8b-instant", "Llama 3.1 8B (Fastest)"),
    ("openai/gpt-oss-120b", "GPT-OSS 120B (Large)"),
    ("openai/gpt-oss-20b", "GPT-OSS 20B (Medium)"),
]

selected_model = st.sidebar.selectbox(
    "Primary Model",
    options=[m[0] for m in GROQ_MODELS],
    format_func=lambda x: next(m[1] for m in GROQ_MODELS if m[0] == x),
    index=0
)

enable_fallback = st.sidebar.checkbox("Enable automatic fallback", value=True)

keys_provided = all([groq_api_key, elevenlabs_api_key, firecrawl_api_key])

# ----------------------------
# Input: Blog URL
# ----------------------------
url = st.text_input("Enter the Blog URL:", "")
generate_button = st.button("🎙️ Generate Podcast", disabled=not keys_provided)

if not keys_provided:
    st.warning("Please enter all required API keys to enable podcast generation.")

# ----------------------------
# Main Logic
# ----------------------------
if generate_button:
    if url.strip() == "":
        st.warning("Please enter a blog URL first.")
    else:
        # Set API keys as environment variables
        os.environ["GROQ_API_KEY"] = groq_api_key
        os.environ["ELEVEN_LABS_API_KEY"] = elevenlabs_api_key
        os.environ["FIRECRAWL_API_KEY"] = firecrawl_api_key

        # Determine which models to try
        if enable_fallback:
            models_to_try = [m[0] for m in GROQ_MODELS]
            # Move selected model to front
            if selected_model in models_to_try:
                models_to_try.remove(selected_model)
                models_to_try.insert(0, selected_model)
        else:
            models_to_try = [selected_model]

        status = st.empty()
        podcast = None
        successful_model = None

        # Try each model in sequence
        for idx, model_id in enumerate(models_to_try):
            try:
                status.info(f"🤖 Trying model {idx+1}/{len(models_to_try)}: {model_id}...")
                
                blog_to_podcast_agent = Agent(
                    name="Blog to Podcast Agent",
                    agent_id="blog_to_podcast_agent",
                    model=GroqModel(id=model_id),
                    tools=[
                        CustomFirecrawlTools(),
                        ElevenLabsTools(
                            voice_id="JBFqnCBsd6RMkjVDRZzb",
                            model_id="eleven_multilingual_v2",
                            target_directory="audio_generations",
                        ),
                    ],
                    description="You are an AI agent that scrapes blogs and converts them to podcasts.",
                    instructions=[
                        "When the user provides a blog URL:",
                        "1. FIRST use scrape_website() function to scrape the blog content",
                        "2. Read and analyze the scraped content carefully",
                        "3. Create a concise summary (NO MORE than 2000 characters)",
                        "4. Make the summary conversational and engaging for a podcast",
                        "5. Use ElevenLabsTools to convert the summary to audio",
                        "CRITICAL: Always scrape the URL first. Never make up content.",
                    ],
                    markdown=True,
                    debug_mode=False,
                )
                
                status.success(f"✅ Agent initialized with {model_id}")
                status.info("🔍 Scraping and processing blog content...")
                
                podcast = blog_to_podcast_agent.run(
                    f"Please scrape this URL: {url} and convert it to an engaging podcast summary."
                )
                
                successful_model = model_id
                status.success(f"✅ Successfully processed with {model_id}")
                break  # Success! Exit the loop
                
            except Exception as e:
                error_msg = str(e)
                
                # Check if it's a rate limit error
                if "rate_limit_exceeded" in error_msg or "Request too large" in error_msg:
                    status.warning(f"⚠️ {model_id} failed (token limit). Trying next model...")
                    if idx < len(models_to_try) - 1:
                        continue  # Try next model
                    else:
                        status.error(f"❌ All models failed due to rate limits")
                        st.error(f"All {len(models_to_try)} models exceeded token limits. Try a shorter blog post.")
                        st.stop()
                else:
                    # Non-rate-limit error
                    status.error(f"❌ Error with {model_id}: {error_msg}")
                    logger.error(f"Error: {e}")
                    if idx < len(models_to_try) - 1 and enable_fallback:
                        continue  # Try next model
                    else:
                        with st.expander("🐛 Show Error Details"):
                            import traceback
                            st.code(traceback.format_exc())
                        st.stop()

        # If we got here with a successful podcast, save it
        if podcast:
            try:
                status.info("💾 Saving audio file...")
                
                save_dir = "audio_generations"
                os.makedirs(save_dir, exist_ok=True)

                if podcast.audio and len(podcast.audio) > 0:
                    filename = f"{save_dir}/podcast_{uuid4()}.wav"
                    write_audio_to_file(
                        audio=podcast.audio[0].base64_audio,
                        filename=filename
                    )
                    
                    status.success(f"✅ Podcast generated successfully with {successful_model}! 🎧")
                    
                    # Display which model was used
                    st.info(f"🤖 Generated using: **{successful_model}**")
                    
                    # Display summary
                    if podcast.content:
                        st.markdown("**📝 Podcast Summary:**")
                        st.info(podcast.content)
                    
                    # Audio player
                    audio_bytes = open(filename, "rb").read()
                    st.audio(audio_bytes, format="audio/wav")

                    # Download button
                    st.download_button(
                        label="⬇️ Download Podcast",
                        data=audio_bytes,
                        file_name="generated_podcast.wav",
                        mime="audio/wav"
                    )
                else:
                    status.error("❌ No audio was generated. Please try again.")

            except Exception as e:
                status.error(f"❌ Error saving audio: {e}")
                logger.error(f"Audio save error: {e}")