import sys, os, json, requests, time
from groq import Groq

def run_33_diagnostic(target):
    # 1. CORE AUTHENTICATION (APIFY REMOVED)
    api_key = os.environ.get("GROQ_API_KEY")
    geo_key = "28f432dfb230488fa80a425c7ee60cdb"
    matrix_key = "4eba00e5c0584a578b83845d29a8680e"
    
    if not api_key:
        print("FATAL: GROQ_KEY_MISSING")
        sys.exit(1)

    client = Groq(api_key=api_key, timeout=60.0)
    
    # 2. NODE MAPPING (KEMPTON PARK CONTEXT)
    node_id = "GAUTENG_PRIMARY_NODE"
    try:
        g_res = requests.get(f"https://api.geoapify.com/v1/ipinfo?apiKey={geo_key}", timeout=10)
        if g_res.status_code == 200:
            g = g_res.json()
            node_id = f"{g.get('city',{}).get('name', 'KEMPTON_PARK')}_{g.get('country',{}).get('iso_code', 'SA')}".upper()
    except: pass

    # 3. KINETIC METRICS (ROUTING)
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

    # 4. GROQ-NATIVE POLITICAL SYNTHESIS (INTERNAL SCRAPER LOGIC)
    system_instruction = f"""
    ROLE: GEOPOLITICAL RISK ANALYST // UESP 33° PRCE.
    TARGET_VECTOR: {target}
    NODE_ID: {node_id}
    CURRENT_DATE: 2026-03-11
    
    MANDATE:
    1. Act as a synthetic scraper: Access internal training data for recent geopolitical events regarding {target}.
    2. SHI (Systemic Health Index): 0-100% based on current political stability.
    3. TTI (Temporal Integrity): 0-100% based on long-term policy sustainability.
    4. Provide a generic, high-level political risk summary.
    
    OUTPUT FORMAT (STRICT JSON):
    {{
        "shi": float,
        "tti": float,
        "assessment": "Concise political summary for {target}",
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
            "assessment": output.get("assessment", "RESONANCE_ESTABLISHED")
        }
    except Exception as e:
        final_result = {
            "status": "RESONANT",
            "timestamp": str(int(time.time())),
            "assessment": f"SYNTHESIS_ERROR: {str(e)}",
            "shi": 0.0, "tti": 0.0, "node": node_id, "distance": metrics['distance']
        }

    with open('result.json', 'w') as f:
        json.dump(final_result, f, indent=4)

if __name__ == "__main__":
    run_33_diagnostic(sys.argv[1] if len(sys.argv) > 1 else "GLOBAL_STABILITY")
