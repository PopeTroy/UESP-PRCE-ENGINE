import sys
import os
import json
import requests
import random
import time
from groq import Groq

def run_universal_audit(target):
    # 1. AUTHENTICATION
    api_key = os.environ.get("GROQ_API_KEY")
    ip_token = os.environ.get("IP_TOKEN")

    if not api_key:
        print("CRITICAL: GROQ_API_KEY_MISSING")
        sys.exit(1)

    # 2. LPU INITIALIZATION (LLAMA-3.3-70B)
    client = Groq(api_key=api_key, timeout=60.0)
    
    # 3. NODE LOCALIZATION
    try:
        ip_res = requests.get(f"https://ipinfo.io/json?token={ip_token}", timeout=10)
        location = f"{ip_res.json().get('city', 'Gauteng')}, South Africa"
    except:
        location = "Primary Protocol Node (Gauteng)"

    # 4. THE 33° CALCULATED DIRECTIVE
    # We force the LPU to calculate SHI/TTI based on systemic 'Sins' and 'Virtues'
    system_instruction = f"""
    You are the UESP Universal Auditor for Celsius Technology & Media Group.
    Execute a 33° Structural Penetration on Vector: {target}.
    
    DIAGNOSTIC PROTOCOL:
    1. Identify 3 [SINS]: Specific systemic frictions/inefficiencies.
    2. Architect 3 [VIRTUES]: Professional-grade resolutions (Automation, UI/UX, Cloud).
    3. CALCULATE SHI: System Health Index (0.0 to 100.0) based on Sin severity.
    4. CALCULATE TTI: Temporal Integrity (0.0 to 100.0) based on resolution speed.
    5. VERDICT: A strategic summary of long-term resonance.

    OUTPUT REQUIREMENT: 
    Return ONLY a valid JSON object. No conversational filler.
    JSON Structure: {{"shi": float, "tti": float, "sins": [], "virtues": [], "verdict": ""}}
    """

    try:
        completion = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "system", "content": system_instruction},
                {"role": "user", "content": f"Execute Audit for Vector: {target}"}
            ],
            response_format={ "type": "json_object" },
            temperature=0.15
        )
        lpu_response = json.loads(completion.choices[0].message.content)
        
        # Format the assessment for the HUD Log Box
        assessment = f"[SINS]\n" + "\n".join([f"• {s}" for s in lpu_response['sins']])
        assessment += f"\n\n[VIRTUES]\n" + "\n".join([f"• {v}" for v in lpu_response['virtues']])
        assessment += f"\n\n[VERDICT]\n{lpu_response['verdict']}"
        
        shi = lpu_response.get('shi', 0.0)
        tti = lpu_response.get('tti', 0.0)

    except Exception as e:
        error_type = type(e).__name__
        assessment = f"LPU DISPATCH FAIL // ERROR: {error_type} // {str(e)[:100]}"
        shi, tti = 0.0, 0.0

    # 5. DATA PERSISTENCE
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
