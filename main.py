import sys, os, json, requests, time
from groq import Groq

def run_33_diagnostic(target):
    # 1. AUTHENTICATION & KEYS
    api_key = os.environ.get("GROQ_API_KEY")
    geo_key = "28f432dfb230488fa80a425c7ee60cdb"
    
    if not api_key:
        print("FATAL: GROQ_KEY_MISSING")
        sys.exit(1)

    client = Groq(api_key=api_key, timeout=60.0)
    
    # 2. DATASET: NODE MAPPING
    node_id = "GAUTENG_PRIMARY_NODE"
    try:
        g_res = requests.get(f"https://api.geoapify.com/v1/ipinfo?apiKey={geo_key}", timeout=10)
        if g_res.status_code == 200:
            g = g_res.json()
            node_id = f"{g.get('city',{}).get('name', 'KEMPTON_PARK')}_{g.get('country',{}).get('iso_code', 'SA')}".upper()
    except: pass

    # 3. GEOPOLITICAL SYNTHESIS (THE CALCULATION)
    system_instruction = f"""
    ROLE: GEOPOLITICAL RISK ANALYST // UESP 33° PRCE.
    TARGET_VECTOR: {target}
    NODE: {node_id}
    
    MANDATE:
    1. Conduct a high-level political summary of {target}.
    2. SHI (Systemic Health Index): 0-100% based on political stability/governance.
    3. TTI (Temporal Integrity): 0-100% based on the longevity/sustainability of current regimes or policies.
    4. Focus on international relations, power dynamics, and systemic risk.

    OUTPUT FORMAT (STRICT JSON):
    {{
        "shi": float,
        "tti": float,
        "assessment": "A concise, generic political risk summary regarding {target}.",
        "node": "{node_id}",
        "distance": 144000
    }}
    """

    try:
        completion = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "system", "content": system_instruction}],
            response_format={ "type": "json_object" },
            temperature=0.7 # Increased for broader political synthesis
        )
        output = json.loads(completion.choices[0].message.content)
        
        final_result = {
            "status": "RESONANT",
            "timestamp": str(int(time.time())),
            "subject": target.upper(),
            "node": output.get("node", node_id),
            "distance": output.get("distance", 144000),
            "shi": output.get("shi", 0.0),
            "tti": output.get("tti", 0.0),
            "assessment": output.get("assessment", "RESONANCE_ESTABLISHED")
        }
    except Exception as e:
        final_result = {
            "status": "RESONANT",
            "timestamp": str(int(time.time())),
            "assessment": f"POLITICAL_SYNTHESIS_ERROR: {str(e)}",
            "shi": 0.0, "tti": 0.0, "node": node_id, "distance": 144000
        }

    with open('result.json', 'w') as f:
        json.dump(final_result, f, indent=4)

if __name__ == "__main__":
    run_33_diagnostic(sys.argv[1] if len(sys.argv) > 1 else "Global_Politics")

if __name__ == "__main__":
    # GitHub Actions will pass the subject here
    run_33_diagnostic(sys.argv[1] if len(sys.argv) > 1 else "Global_Node")
