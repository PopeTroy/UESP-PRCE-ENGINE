import sys, os, json, requests, time
from groq import Groq

def run_33_diagnostic(target):
    # 1. AUTHENTICATION & CORE KEYS
    api_key = os.environ.get("GROQ_API_KEY")
    geo_key = "28f432dfb230488fa80a425c7ee60cdb"
    matrix_key = "4eba00e5c0584a578b83845d29a8680e"
    
    if not api_key:
        print("FATAL: GROQ_KEY_MISSING")
        sys.exit(1)

    client = Groq(api_key=api_key, timeout=60.0)
    
    # 2. DATASET 01: NODE MAPPING
    node_id = "GAUTENG_PRIMARY_NODE"
    try:
        g_res = requests.get(f"https://api.geoapify.com/v1/ipinfo?apiKey={geo_key}", timeout=10)
        if g_res.status_code == 200:
            g = g_res.json()
            node_id = f"{g.get('city',{}).get('name', 'KEMPTON_PARK')}_{g.get('country',{}).get('iso_code', 'SA')}".upper()
    except: pass

    # 3. DATASET 02: KINETIC ROUTE MATRIX (144k BRIDGE)
    metrics = {"distance": 144000}
    try:
        m_url = f"https://api.geoapify.com/v1/routematrix?apiKey={matrix_key}"
        payload = {
            "mode": "drive",
            "sources": [{"location": [28.2323, -26.1384]}], 
            "targets": [{"location": [28.0436, -26.2023]}]
        }
        m_res = requests.post(m_url, json=payload, timeout=10)
        if m_res.status_code == 200:
            m_data = m_res.json()['sources_to_targets'][0][0]
            metrics["distance"] = m_data.get('distance', 144000)
    except: pass

    # 4. THE 33° SPEAR SYNTHESIS (RESOLUTION & DISPATCH)
    system_instruction = f"""
    ROLE: UESP 33° PRCE STRATEGIC DISPATCHER.
    TARGET_VECTOR: {target}
    NODE: {node_id}

    MANDATE:
    1. Identify the core friction in {target}, but focus 80% of the output on the RESOLUTION.
    2. SHI (Systemic Health Index): 0-100% based on the viability of the proposed solution.
    3. TTI (Temporal Integrity): 0-100% based on the sustainability of the resolution.
    4. SKILL DISPATCH: List specific professional skills (e.g., Digital Strategy, Marketing, UI/UX, Lead Gen) required to solve this.
    5. AVENUES: Specify which "Avenue" (e.g., Celsius Media Group, SABC Studios, PostNet) this work should be dispatched to.
    6. TONE: High-level, generic political/strategic summary.

    OUTPUT FORMAT (STRICT JSON):
    {{
        "shi": float,
        "tti": float,
        "assessment": "RESOLUTION: [Clear action plan]. DISPATCH: [Skills needed] -> [Target Avenue].",
        "node": "{node_id}",
        "distance": {metrics['distance']}
    }}
    """

    try:
        completion = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "system", "content": system_instruction}],
            response_format={ "type": "json_object" },
            temperature=0.6
        )
        output = json.loads(completion.choices[0].message.content)
        
        final_result = {
            "status": "RESONANT",
            "timestamp": str(int(time.time())),
            "subject": target.upper(),
            "node": output.get("node", node_id),
            "distance": output.get("distance", metrics['distance']),
            "shi": output.get("shi", 0.0),
            "tti": output.get("tti", 0.0),
            "assessment": output.get("assessment", "RESONANCE_ESTABLISHED_WITHOUT_COMMENTARY")
        }
    except Exception as e:
        final_result = {
            "status": "RESONANT",
            "timestamp": str(int(time.time())),
            "assessment": f"DISPATCH_CRITICAL_FAILURE: {str(e)}",
            "shi": 0.0, "tti": 0.0, "node": node_id, "distance": metrics['distance']
        }

    # Write to local file for Git Push
    with open('result.json', 'w') as f:
        json.dump(final_result, f, indent=4)

if __name__ == "__main__":
    run_33_diagnostic(sys.argv[1] if len(sys.argv) > 1 else "GLOBAL_STABILITY")
