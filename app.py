import streamlit as st
import requests
from dotenv import load_dotenv
import os

load_dotenv()

# Airtable API settings
AIRTABLE_BASE_ID = os.getenv('AIRTABLE_BASE_ID')
AIRTABLE_API_KEY = os.getenv('AIRTABLE_API_KEY')
AIRTABLE_TABLE_NAME = 'Feedback'

# Airtable API URL
url = f'https://api.airtable.com/v0/{AIRTABLE_BASE_ID}/{AIRTABLE_TABLE_NAME}'

# Hugging Face API
API_URL = "https://api-inference.huggingface.co/models/"
HEADERS = {"Authorization": f"Bearer {os.getenv('HUGGING_FACE_API_KEY')}"}

# critical keywords for flagging
CRITICAL_KEYWORDS = [
    "security breach", "data breach", "privacy issue", "hack", "broken feature", "security", "vulnerability",
    "crash", "bug", "problem", "error", "fail", "malfunction", "malware", "unauthorized access", "account compromise"
]


# API call function with retry logic
def query_huggingface_with_retry(model, payload):
    response = requests.post(
        API_URL + model,
        headers=HEADERS,
        json={"inputs": payload},
    )
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f"API request failed: {response.json()}")


# Sentiment Analysis
def analyze_sentiment(feedback):
    result = query_huggingface_with_retry("nlptown/bert-base-multilingual-uncased-sentiment", feedback)

    # Extract the label with the highest score from the response
    if isinstance(result, list) and len(result) > 0:
        sorted_result = sorted(result[0], key=lambda x: x['score'], reverse=True)
        top_label = sorted_result[0] 
        label = top_label['label'] 
        score = top_label['score'] 

        # Map the star ratings to more understandable sentiment labels
        if label == "5 stars" or label == "4 stars":
            sentiment = "Positive"
        elif label == "3 stars":
            sentiment = "Neutral"
        else:
            sentiment = "Negative"

        if sentiment == "Positive":
            sentiment_description = "Highly Positive 😍" if score > 0.8 else "Positive 😊"
        elif sentiment == "Neutral":
            sentiment_description = "Neutral 😐"
        else:
            sentiment_description = "Negative 😞"

        return sentiment_description
    else:
        raise Exception("Unexpected response structure for sentiment analysis")

#summary
def summarize_feedback(feedback):
    result = query_huggingface_with_retry("google/pegasus-large", feedback)

    if isinstance(result, list) and len(result) > 0 and "summary_text" in result[0]:
        summary = result[0]["summary_text"]  
        return summary
    else:
        raise Exception("Unexpected response structure for summarization")


# Categorizing Feedback
def categorize_feedback(feedback):
    categories = {
        "Content Quality": ['quality', 'feature', 'content', 'useful', 'helpful'],
        "High Latency": ['slow', 'lag', 'delay', 'latency'],
        "Application Errors": ['error', 'crash', 'bug', 'problem', 'issue']
    }

    feedback_lower = feedback.lower()

    for category, keywords in categories.items():
        if any(keyword in feedback_lower for keyword in keywords):
            return category

    return "Other"



# Flagging Critical Keywords
def flag_critical_keywords(feedback):
    feedback_lower = feedback.lower()

    flagged_keywords = [keyword for keyword in CRITICAL_KEYWORDS if keyword in feedback_lower]

    # Return a list of flagged keywords or None if no critical keywords found
    if flagged_keywords:
        return flagged_keywords
    return None


#  feedback to Airtable
def save_to_airtable(feedback, sentiment, summary, category, flagged_keywords):
    data = {
        "fields": {
            "Feedback": feedback,
            "Sentiment": sentiment,
            "Summary": summary,
            "Category": category,
            "Flagged Keywords": ', '.join(flagged_keywords) if flagged_keywords else "None"
        }
    }

    headers = {
        "Authorization": f"Bearer {AIRTABLE_API_KEY}",
        "Content-Type": "application/json"
    }

    response = requests.post(url, json=data, headers=headers)

    # if response.status_code == 201:
    #     print("Feedback saved successfully!")
    # else:
    #     print(f"Failed to save feedback. Error: {response.text}")


# app
def main():
    st.title("User Feedback Analysis 🗣️")

    feedback = st.text_area("Enter your feedback:", height=150, max_chars=1000)
    analyze_button = st.button("Analyze Feedback")

    if analyze_button:
        if feedback:
            with st.spinner("Analyzing your feedback..."):
                try:
                    # Sentiment Analysis
                    sentiment = analyze_sentiment(feedback)
                    st.markdown(f"### Feedback Sentiment: {sentiment}")

                    # Summarization
                    summary = summarize_feedback(feedback)
                    st.subheader("Summarization:")
                    st.write(f"**Summary:** {summary}")

                    # Categorizing Feedback
                    category = categorize_feedback(feedback)
                    st.subheader("Feedback Category:")
                    st.write(f"**Category:** {category}")

                    # Flagging Critical Keywords
                    flagged_keywords = flag_critical_keywords(feedback)
                    st.subheader("Critical Keywords🚨:")
                    if flagged_keywords:
                        st.write(f"**Flagged Keywords:** {', '.join(flagged_keywords)}")
                    else:
                        st.write("**No critical issues found.**")

                    save_to_airtable(feedback, sentiment, summary, category, flagged_keywords)
                    st.success("Feedback Saved Successfully! 🎉")

                except Exception as e:
                    st.error(f"An error occurred: {e}")
        else:
            st.warning("Please enter feedback to analyze.")


if __name__ == "__main__":
    main()
