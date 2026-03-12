import sys, os, json, requests, time
from groq import Groq

def run_33_diagnostic(target):
    # 1. CORE AUTHENTICATION
    api_key = os.environ.get("GROQ_API_KEY")
    geo_key = "28f432dfb230488fa80a425c7ee60cdb"
    
    if not api_key:
        print("FATAL: GROQ_KEY_MISSING")
        sys.exit(1)

    client = Groq(api_key=api_key, timeout=60.0)
    
    # 2. KINETIC DATA (GEOLOCATION)
    node_id = "GAUTENG_PRIMARY_NODE"
    try:
        g_res = requests.get(f"https://api.geoapify.com/v1/ipinfo?apiKey={geo_key}", timeout=10)
        if g_res.status_code == 200:
            g = g_res.json()
            node_id = f"{g.get('city',{}).get('name', 'KEMPTON_PARK')}_{g.get('country',{}).get('iso_code', 'SA')}".upper()
    except: pass

    # 3. DISPATCH LOGIC & CALCULATION PARAMETERS
    # Mandating the evaluation of the full skill spectrum
    system_instruction = f"""
    ROLE: UESP 33° PRCE LEAD DISPATCHER.
    TARGET: {target}
    PRIMARY_NODE: Celsius Technology & Media Group.
    
    SKILL SPECTRUM TO EVALUATE:
    - Digital Strategy & Marketing Management
    - Jewelry Design & Goldsmithing (3D/Manufacturing)
    - Sound Engineering & Music Production (Waves/SABC)
    - UI/UX & Web Architecture (WordPress/UESP/PRCE)
    - Graphic Design & DTP (CorelDraw/PostNet logic)
    - Lead Generation & CRM Automation

    MANDATE:
    1. CALCULATE SHI: Evaluate the 'Systemic Health' of {target}. Use the formula: 
       SHI = (Infrastructure Readiness + Reality Alignment) / 2.
    2. CALCULATE TTI: Evaluate 'Temporal Integrity'. Use the formula:
       TTI = (Sustainability + Real-Time Scalability) / 2.
    3. DISPATCH: Determine which specific skills from the spectrum above are required to resolve {target}.
    4. AVENUES: Assign the task to Celsius Media Group or relevant secondary nodes (SABC, PostNet, etc.).
    5. REAL-TIME FACTOR: How does this impact 'Real Time and Reality' (The 144k Bridge)?

    OUTPUT FORMAT (STRICT JSON):
    {{
        "shi": float,
        "tti": float,
        "subject": "{target}",
        "assessment": "ANALYSIS: [Brief breakdown]. RESOLUTION: [Action Plan]. DISPATCH: [Skills] -> [Node].",
        "node": "{node_id}"
    }}
    """

    try:
        completion = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "system", "content": system_instruction}],
            response_format={ "type": "json_object" },
            temperature=0.3 # Lower temperature for higher calculation accuracy
        )
        output = json.loads(completion.choices[0].message.content)
        
        final_result = {
            "status": "RESONANT",
            "timestamp": str(int(time.time())),
            "subject": output.get("subject", target.upper()),
            "node": output.get("node", node_id),
            "distance": 144000,
            "shi": round(output.get("shi", 0.0), 2),
            "tti": round(output.get("tti", 0.0), 2),
            "assessment": output.get("assessment", "RESONANCE_ESTABLISHED")
        }
    except Exception as e:
        final_result = {
            "status": "RESONANT",
            "timestamp": str(int(time.time())),
            "assessment": f"CALCULATION_ERROR: {str(e)}",
            "shi": 0.0, "tti": 0.0, "node": node_id, "distance": 144000
        }

    with open('result.json', 'w') as f:
        json.dump(final_result, f, indent=4)

if __name__ == "__main__":
    run_33_diagnostic(sys.argv[1] if len(sys.argv) > 1 else "GLOBAL_REALITY")
