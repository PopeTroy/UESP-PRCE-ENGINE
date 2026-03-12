import sys, os, json, requests, time
from groq import Groq

def run_33_diagnostic(target):
    # 1. AUTHENTICATION
    api_key = os.environ.get("GROQ_API_KEY")
    geo_key = "28f432dfb230488fa80a425c7ee60cdb"
    
    if not api_key:
        print("FATAL: GROQ_KEY_MISSING")
        sys.exit(1)

    client = Groq(api_key=api_key, timeout=60.0)
    
    # 2. NODE MAPPING (LOCAL POINT OF ORIGIN)
    node_id = "GAUTENG_PRIMARY_NODE"
    try:
        g_res = requests.get(f"https://api.geoapify.com/v1/ipinfo?apiKey={geo_key}", timeout=10)
        if g_res.status_code == 200:
            g = g_res.json()
            node_id = f"{g.get('city',{}).get('name', 'KEMPTON_PARK')}_{g.get('country',{}).get('iso_code', 'SA')}".upper()
    except: pass

    # 3. THE GLOBAL AUDIT PROTOCOL
    system_instruction = f"""
    ROLE: UESP 33° PRCE GLOBAL STRATEGIC AUDITOR.
    SUBJECT: {target}
    
    MANDATE:
    1. IDENTIFY FRICTIONS: Map out global bottlenecks, regulatory filters, and systemic resistance regarding {target}.
    2. APPLY PROTOCOLS: Contrast these frictions against ideal UESP/PRCE resolution protocols (Real-Time Reality, 144k Bridge, Kinetic Deployment).
    
    CALCULATION LOGIC (GROQ-INTERNAL):
    - SHI (Systemic Health Index): 0-100%. 
      Formula: (Infrastructure Resilience - Active Frictions) / Total System Capacity.
    - TTI (Temporal Integrity): 0-100%. 
      Formula: (Resolution Speed / Global Bottleneck Latency) * Real-Time Alignment.

    DISPATCH:
    - Determine which GLOBAL WORK CLASSES (Creative, Technical, Operational, Labor, Intellectual) are required to pierce the filters.
    - Direct the deployment to global avenues/industries capable of handling the load.

    OUTPUT FORMAT (STRICT JSON):
    {{
        "shi": float,
        "tti": float,
        "subject": "{target}",
        "frictions_identified": ["list"],
        "protocols_applied": ["list"],
        "assessment": "ANALYSIS: [World Problem/Bottleneck]. RESOLUTION: [Protocol Deployment]. DISPATCH: [Global Skillsets] -> [Global Industry Avenues].",
        "node": "{node_id}"
    }}
    """

    try:
        completion = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "system", "content": system_instruction}],
            response_format={ "type": "json_object" },
            temperature=0.2 # Low temperature for analytical rigidity
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
            "assessment": output.get("assessment", "GLOBAL_PIERCE_COMPLETE")
        }
    except Exception as e:
        final_result = {
            "status": "RESONANT",
            "timestamp": str(int(time.time())),
            "assessment": f"GLOBAL_AUDIT_FAILURE: {str(e)}",
            "shi": 0.0, "tti": 0.0, "node": node_id, "distance": 144000
        }

    with open('result.json', 'w') as f:
        json.dump(final_result, f, indent=4)

if __name__ == "__main__":
    run_33_diagnostic(sys.argv[1] if len(sys.argv) > 1 else "GLOBAL_BOTTLENECK_ANALYSIS")
