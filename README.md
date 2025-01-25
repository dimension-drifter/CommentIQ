# CommentIQ  
**AI-Powered Feedback Processing with Sentiment Analysis & Critical Alerts**

[![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?logo=streamlit&logoColor=white)](https://streamlit.io)

Automatically analyze user feedback with:
- 😊 Sentiment rating (Positive/Neutral/Negative)
- 📝 AI-generated summaries
- 🚨 Critical keyword detection
- 📂 Airtable integration
---

## Quick Start 

1. **Clone & Install**  
```bash
git clone https://github.com/your-username/feedback-analyzer.git
cd feedback-analyzer
pip install -r requirements.txt
```

2. **Add to `.env`**  
```ini
AIRTABLE_BASE_ID=your_base_id
AIRTABLE_API_KEY=your_key
HUGGING_FACE_API_KEY=your_hf_key
```

3. **Run**  
```bash
streamlit run app.py
```

---

## Key Features:

- **Instant Analysis**: Get sentiment, summary, and category in one click  
- **Security Alerts**: Flags 15+ critical terms like "data breach" or "hack"  
- **Smart Storage**: Auto-saves to Airtable with metadata  
- **AI Models**: Hugging Face's BERT (sentiment) & Pegasus (summarization)  

---

## Setup Guide:

1. **Airtable**: Create table named `Feedback` with fields:  
   `Feedback`, `Sentiment`, `Summary`, `Category`, `Flagged Keywords`  
2. **Hugging Face**: Get API token from [Account Settings](https://huggingface.co/settings/tokens)  

--- 

**MIT Licensed** • *For production use, add error handling and rate limiting.*
