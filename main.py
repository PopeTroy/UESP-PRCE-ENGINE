import sys
import json
import requests
import random
import os
from groq import Groq

# RECALLING SECRETS FROM VAULT
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
IP_TOKEN = os.getenv("IP_TOKEN")
DM_API_KEY = os.getenv("DM_API_KEY")
APIFY_TOKEN = os.getenv("APIFY_TOKEN")

def run_universal_audit(target):
    client = Groq(api_key=GROQ_API_KEY)
    
    # 1. LIVE INTEL: APIFY NEWS SCRAPER
    # Pulling recent headlines for the target vector to find "Sins"
    news_context = ""
    try:
        apify_url = f"https://api.apify.com/v2/acts/apify~google-news-scraper/run-sync-get-dataset-items?token={APIFY_TOKEN}"
        news_res = requests.post(apify_url, json={"queries": [f"{target} problems inefficiencies"]})
        news_items = news_res.json()
        news_context = " ".join([item.get('title', '') for item in news_items[:3]])
    except:
        news_context = "Standard systemic friction detected."

    # 2. NODE LOCALIZATION
    try:
        ip_data = requests.get(f"https://ipinfo.io/json?token={IP_TOKEN}").json()
        location = f"{ip_data.get('city', 'Kempton Park')}, {ip_data.get('region', 'Gauteng')}"
    except:
        location = "Gauteng Protocol Node"

    # 3. UNIVERSAL RESOLUTION ENGINE (Groq LPU)
    try:
        completion = client.chat.completions.create(
            model="llama3-70b-8192",
            messages=[
                {"role": "system", "content": "You are the UESP Universal Auditor. Use the provided news context to identify real-world Sins (inefficiencies) and Virtues (work-class resolutions)."},
                {"role": "user", "content": f"Vector: {target}. Location: {location}. News Context: {news_context}. Synthesize an overwrite."}
            ]
        )
        assessment = completion.choices[0].message.content
    except:
        assessment = f"Manual Audit: Vector {target} requires structural intervention."

    # 4. HUD DATA SYNTHESIS
    shi = round(random.uniform(85, 98), 1)
    tti = round((shi * random.uniform(0.92, 0.99)), 1)

    result = {
        "subject": target.upper(),
        "location": location,
        "shi": shi,
        "tti": tti,
        "news_anchor": news_context[:100] + "...",
        "assessment": assessment,
        "sins": ["CENTRALIZATION", "FRICTION", "DELAY", "OBSCURITY", "STAGNATION", "COMPLIANCE", "LIMITATION"],
        "virtues": ["SYNTHESIS", "RESONANCE", "FLOW", "CLARITY", "VELOCITY", "SOVEREIGNTY", "EXPANSION"]
    }
    
    with open('result.json', 'w') as f:
        json.dump(result, f, indent=4)

if __name__ == "__main__":
    target_vector = sys.argv[1] if len(sys.argv) > 1 else "Global"
    run_universal_audit(target_vector)
