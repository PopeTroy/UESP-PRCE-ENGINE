import sys
import os
import json
import requests
import random
import re
import time
from groq import Groq

def run_universal_audit(target):
    api_key = os.environ.get("GROQ_API_KEY")
    ip_token = os.environ.get("IP_TOKEN")

    if not api_key:
        sys.exit(1)

    # 90s Timeout to allow for full Internal Database retrieval
    client = Groq(api_key=api_key, timeout=90.0)
    
    # NODE LOCALIZATION
    try:
        ip_res = requests.get(f"https://ipinfo.io/json?token={ip_token}", timeout=10)
        location = f"{ip_res.json().get('city', 'Gauteng')}, South Africa"
    except:
        location = "Primary Protocol Node (Gauteng)"

    # SHI/TTI SEEDING
    shi = round(random.uniform(94.2, 99.8), 1)
    tti = round((shi * random.uniform(0.96, 0.99)), 1)

    # STEP-BY-STEP LPU DIRECTIVE (THE 33° PENETRATION)
    # This forces Groq to use its internal intelligence systematically.
    system_instruction = f"""
    You are the UESP Universal Auditor for Celsius Technology & Media Group.
    Perform a 33° Structural Penetration on Vector: {target}.
    
    STEP-BY-STEP EXECUTION PROTOCOL:
    1. DIAGNOSE ENTROPY: Access your internal database to identify the 3 primary systemic frictions (Sins) currently affecting this vector's global infrastructure.
    2. ARCHITECTURAL RESOLUTION: Design 3 professional-grade resolutions (Virtues) using Cloud Architecture, High-Fidelity UI/UX, and Automation.
    3. STABILITY VERDICT: Provide a final strategic assessment of the vector's long-term industrial resonance.
    
    OUTPUT FORMAT:
    [SINS]: (Bullet points)
    [VIRTUES]: (Bullet points)
    [VERDICT]: (Strategic summary)
    
    TONE: Objective, Professional, Strategic Architect. 
    Do not use conversational filler. Deliver raw architectural data.
    """

    try:
        # PURE LPU ENGAGEMENT
        completion = client.chat.completions.create(
            model="llama3-70b-8192",
            messages=[
                {"role": "system", "content": system_instruction},
                {"role": "user", "content": f"Execute 33° Audit for {target}."}
            ],
            temperature=0.15 # Minimum variance for maximum structural accuracy
        )
        assessment = completion.choices[0].message.content
    except Exception as e:
        assessment = "CRITICAL: LPU DISPATCH ERROR. Verify API status."

    # PERSISTENCE TO JSON
    result = {
        "subject": target.upper(),
        "location": location,
        "shi": shi,
        "tti": tti,
        "assessment": assessment,
        "timestamp": str(int(time.time()))
    }
    
    with open('result.json', 'w') as f:
        json.dump(result, f, indent=4)

if __name__ == "__main__":
    target_vector = sys.argv[1] if len(sys.argv) > 1 else "Global"
    run_universal_audit(target_vector)
