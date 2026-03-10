import sys
import os
import json
import requests
import random
import time
from groq import Groq

def run_universal_audit(target):
    # 1. AUTHENTICATION RECOVERY
    # The engine looks for GROQ_API_KEY in the GitHub Environment
    api_key = os.environ.get("GROQ_API_KEY")
    ip_token = os.environ.get("IP_TOKEN")

    # 2. SEEDING SYSTEMIC METRICS
    # Generating the SHI and TTI indices for the 33° baseline
    shi = round(random.uniform(94.2, 99.8), 1)
    tti = round((shi * random.uniform(0.96, 0.99)), 1)
    
    # 3. THE 33° LPU DIRECTIVE
    # Forcing Groq to use its internal intelligence for a step-by-step audit
    system_instruction = f"""
    You are the UESP Universal Auditor for Celsius Technology & Media Group.
    Execute a 33° Structural Penetration on Vector: {target}.
    
    STEP-BY-STEP EXECUTION PROTOCOL:
    1. DIAGNOSE ENTROPY: Identify 3 [SINS] (Systemic frictions/inefficiencies).
    2. ARCHITECTURAL RESOLUTION: Provide 3 [VIRTUES] (Professional resolutions).
    3. STABILITY VERDICT: Provide 1 [VERDICT] (Long-term strategic resonance).
    
    TONE: Strategic Architect / Lead Consultant. No conversational filler.
    """

    try:
        # Check for Key Presence before initiating the Stab
        if not api_key:
            raise ValueError("AUTH_EMPTY: GROQ_API_KEY is missing from the Environment.")

        client = Groq(api_key=api_key, timeout=60.0)
        
        # PURE LPU ENGAGEMENT
        completion = client.chat.completions.create(
            model="llama3-70b-8192",
            messages=[
                {"role": "system", "content": system_instruction},
                {"role": "user", "content": f"Audit Vector: {target}"}
            ],
            temperature=0.15 # Minimal variance for maximum architectural precision
        )
        assessment = completion.choices[0].message.content

    except Exception as e:
        # TELEMETRY OVERWRITE: Reports the exact "Sin" preventing the Dispatch
        error_type = type(e).__name__
        assessment = f"LPU DISPATCH FAIL // ERROR_TYPE: {error_type} // MSG: {str(e)[:100]}"

    # 4. DATA PERSISTENCE
    # Formatting the final payload for the WordPress HUD
    result = {
        "subject": target.upper(),
        "location": "Primary Protocol Node (Gauteng)",
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
