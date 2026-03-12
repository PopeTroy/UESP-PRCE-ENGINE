import sys, os, json, requests, time
from groq import Groq

def run_33_diagnostic(target):
    # 1. AUTHENTICATION & CORE KEYS
    api_key = os.environ.get("GROQ_API_KEY")
    geo_key = "28f432dfb230488fa80a425c7ee60cdb"
    
    if not api_key:
        print("FATAL: GROQ_KEY_MISSING")
        sys.exit(1)

    client = Groq(api_key=api_key, timeout=60.0)
    
    # 2. NODE MAPPING
    node_id = "GAUTENG_PRIMARY_NODE"
    try:
        g_res = requests.get(f"https://api.geoapify.com/v1/ipinfo?apiKey={geo_key}", timeout=10)
        if g_res.status_code == 200:
            g = g_res.json()
            node_id = f"{g.get('city',{}).get('name', 'KEMPTON_PARK')}_{g.get('country',{}).get('iso_code', 'SA')}".upper()
    except: pass

    # 3. THE CALCULATION MANDATE (SUBJECT-SPECIFIC)
    system_instruction = f"""
    ROLE: UESP 33° PRCE GLOBAL STRATEGIC AUDITOR.
    SUBJECT_INSERTION: {target}
    
    CALCULATION PROTOCOL:
    You must calculate SHI and TTI based on the specific friction of the SUBJECT.
    
    1. IDENTIFY FRICTIONS: Analyze bottlenecks, regulatory filters, and systemic resistance inherent to "{target}".
    2. SHI CALCULATION: (0.0 to 100.0)
       SHI = (Global Infrastructure Readiness - Localized Subject Friction) / Systemic Resilience.
    3. TTI CALCULATION: (0.0 to 100.0)
       TTI = (Deployment Velocity / Subject Complexity) * Real-Time Alignment.
    
    DISPATCH MANDATE:
    - Dispatch skills from the Global Spectrum (Creative, Technical, Operational, Labor, Intellectual).
    - Map resolutions to Global Industry Avenues.

    OUTPUT FORMAT (STRICT JSON):
    {{
        "shi": float,
        "tti": float,
        "subject": "{target}",
        "metrics": {{
            "friction_level": "High/Medium/Low",
            "bottleneck_type": "string"
        }},
        "assessment": "ANALYSIS: [Bottleneck Breakdown]. RESOLUTION: [Protocol Deployment]. DISPATCH: [Skills] -> [Global Avenues].",
        "node": "{node_id}"
    }}
    """

    try:
        completion = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "system", "content": system_instruction}],
            response_format={ "type": "json_object" },
            temperature=0.1 # Absolute analytical rigidity
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
            "assessment": output.get("assessment", "GLOBAL_PIERCE_SUCCESSFUL")
        }
    except Exception as e:
        final_result = {
            "status": "RESONANT",
            "timestamp": str(int(time.time())),
            "assessment": f"CALCULATION_FAILURE: {str(e)}",
            "shi": 0.0, "tti": 0.0, "node": node_id, "distance": 144000
        }

    with open('result.json', 'w') as f:
        json.dump(final_result, f, indent=4)

if __name__ == "__main__":
    run_33_diagnostic(sys.argv[1] if len(sys.argv) > 1 else "GLOBAL_STABILITY_AUDIT")
