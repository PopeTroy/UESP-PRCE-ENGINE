import sys, os, json, requests, time
from groq import Groq

def run_33_diagnostic(target):
    # 1. CORE AUTHENTICATION
    api_key = os.environ.get("GROQ_API_KEY")
    apify_token = os.environ.get("APIFY_TOKEN")
    geo_key = "28f432dfb230488fa80a425c7ee60cdb"
    matrix_key = "4eba00e5c0584a578b83845d29a8680e"
    
    if not api_key:
        print("FATAL: GROQ_KEY_MISSING")
        sys.exit(1)

    client = Groq(api_key=api_key, timeout=60.0)
    
    # 2. DATASET 01: NODE MAPPING (IP GEOLOCATION)
    node_id = "GAUTENG_PRIMARY_NODE"
    try:
        g_res = requests.get(f"https://api.geoapify.com/v1/ipinfo?apiKey={geo_key}", timeout=10)
        if g_res.status_code == 200:
            g = g_res.json()
            node_id = f"{g.get('city',{}).get('name')}_{g.get('country',{}).get('iso_code')}".upper()
    except: pass

    # 3. DATASET 02: KINETIC MATRIX (ROUTING)
    metrics = {"distance": 0, "time": 0}
    try:
        m_url = f"https://api.geoapify.com/v1/routematrix?apiKey={matrix_key}"
        payload = {
            "mode": "drive",
            "sources": [{"location": [28.2323, -26.1384]}], # Kempton Park Node
            "targets": [{"location": [28.0436, -26.2023]}]  # JHB Target
        }
        m_res = requests.post(m_url, json=payload, timeout=10)
        if m_res.status_code == 200:
            m_data = m_res.json()['sources_to_targets'][0][0]
            metrics = {"distance": m_data.get('distance'), "time": m_data.get('time')}
    except: pass

    # 4. DATASET 03: APIFY INTEL (SCRAPER)
    intel_log = "LIVE_INTEL_STREAM_ACTIVE"
    if apify_token:
        try:
            run_url = f"https://api.apify.com/v2/acts/apify~web-scraper/runs?token={apify_token}"
            requests.post(run_url, json={"startUrls": [{"url": f"https://www.google.com/search?q={target}+systemic+risk"}]}, timeout=10)
        except: intel_log = "STREAM_OFFLINE"

    # 5. THE 33° PRCE SYNTHESIS (GROQ DATABASE)
    system_instruction = f"""
    SYSTEM_ROLE: UESP 33° PRCE DIAGNOSTIC ENGINE.
    VECTOR_TARGET: {target}
    NODE_ID: {node_id}
    KINETIC_METRICS: {json.dumps(metrics)}
    INTEL_LOG: {intel_log}
    EDUCATIONAL_DB: ProQuest Academic / Jewelry Design / UJ Architecture
    
    DIAGNOSTIC MANDATE:
    1. EXTRACT 3 [SINS]: Identify core systemic frictions.
    2. ENGINEER 3 [VIRTUES]: Provide structural resolutions.
    3. CALCULATE SHI (Systemic Health Index) & TTI (Temporal Integrity).
    4. VERDICT: Final resonance status.

    FORMAT: Return ONLY a valid JSON object.
    {{
        "shi": float,
        "tti": float,
        "assessment": "Raw technical diagnostic breakdown",
        "node": "{node_id}",
        "distance": {metrics['distance']}
    }}
    """

    try:
        completion = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "system", "content": system_instruction}],
            response_format={ "type": "json_object" },
            temperature=0.1
        )
        output = json.loads(completion.choices[0].message.content)
        
        final_result = {
            "subject": target.upper(),
            "node": output.get("node", node_id),
            "distance": output.get("distance", metrics['distance']),
            "shi": output.get("shi", 0.0),
            "tti": output.get("tti", 0.0),
            "assessment": output.get("assessment", "DIAGNOSTIC_NULL"),
            "status": "RESONANT",
            "timestamp": str(int(time.time()))
        }
    except Exception as e:
        final_result = {"status": "ERROR", "assessment": str(e), "timestamp": str(int(time.time()))}

    with open('result.json', 'w') as f:
        json.dump(final_result, f, indent=4)

if __name__ == "__main__":
    run_33_diagnostic(sys.argv[1] if len(sys.argv) > 1 else "Global")
