import sys
import os
import json
import requests
import random
import time
from groq import Groq

def run_universal_audit(target):
    # 1. AUTHENTICATION RECOVERY
    # Extracting credentials from the GitHub Environment Vault
    api_key = os.environ.get("GROQ_API_KEY")
    ip_token = os.environ.get("IP_TOKEN")

    # 2. SEEDING SYSTEMIC METRICS
    # Generating the SHI and TTI indices for the 33° baseline
    shi = round(random.uniform(94.2, 99.8), 1)
    tti = round((shi * random.uniform(0.96, 0.99)), 1)
    
    # 3. THE 33° LPU DIRECTIVE
    # System Instruction: Forcing the LPU to use its internal database systematically
    system_instruction = f"""
    You are the UESP Universal Auditor for Celsius Technology & Media Group.
    Execute a 33° Structural Penetration on Vector: {target}.
    
    STEP-BY-STEP EXECUTION PROTOCOL:
    1. DIAGNOSE ENTROPY: Identify 3 [SINS] (Internal Database systemic friction).
    2. ARCHITECTURAL RESOLUTION: Provide 3 [VIRTUES] (Professional resolutions).
    3. STABILITY VERDICT: Provide 1 [VERDICT] (Long-term strategic resonance).
    
    TONE: Strategic Architect / Lead Consultant. No conversational filler.
    """

    try:
        if not api_key:
            raise ValueError("AUTH_EMPTY: GROQ_API_KEY is missing from the Environment.")

        # Initializing the Handshake with a 60s window for deep synthesis
        client = Groq(api_key=api_key, timeout=60.0)
        
        # MODEL UPDATE: Switching to llama-3.3-70b-versatile for 2026 Resonance
        completion = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "system", "content": system_instruction},
                {"role": "user", "content": f"Audit Vector: {target}"}
            ],
            temperature=0.15 # Minimal variance for maximum architectural precision
        )
        assessment = completion.choices[0].message.content

    except Exception as e:
        # TELEMETRY OVERWRITE: Captures the exact reason for dispatch failure
        error_type = type(e).__name__
        assessment = f"LPU DISPATCH FAIL // ERROR_TYPE: {error_type} // MSG: {str(e)[:100]}"

    # 4. DATA PERSISTENCE
    # Formatting the payload for the WordPress Systematic HUD
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
