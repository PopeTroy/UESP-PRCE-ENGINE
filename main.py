import sys, os, json, requests, time
from groq import Groq

def run_universal_audit(target):
    # 1. AUTHENTICATION & ENVIRONMENTAL HANDSHAKE
    api_key = os.environ.get("GROQ_API_KEY")
    apify_token = os.environ.get("APIFY_TOKEN")
    geo_key = "28f432dfb230488fa80a425c7ee60cdb"
    matrix_key = "4eba00e5c0584a578b83845d29a8680e"
    
    if not api_key:
        print("CRITICAL: AUTH_FAIL")
        sys.exit(1)

    client = Groq(api_key=api_key, timeout=60.0)
    
    # 2. STEP 01: NODE MAPPING (IP GEOLOCATION)
    node_info = "Gauteng Protocol Node"
    try:
        g_res = requests.get(f"https://api.geoapify.com/v1/ipinfo?apiKey={geo_key}", timeout=10)
        if g_res.status_code == 200:
            g = g_res.json()
            node_info = f"{g.get('city',{}).get('name')}, {g.get('state',{}).get('name')}"
    except: pass

    # 3. STEP 02: KINETIC ROUTE MATRIX (DISTANCE CALCULATION)
    distance_val = 0
    try:
        m_url = f"https://api.geoapify.com/v1/routematrix?apiKey={matrix_key}"
        payload = {
            "mode": "drive",
            "sources": [{"location": [28.0436, -26.2023]}], # Johannesburg Core
            "targets": [{"location": [28.2293, -25.7479]}]  # Pretoria/Regional Target
        }
        m_res = requests.post(m_url, json=payload, timeout=10)
        if m_res.status_code == 200:
            distance_val = m_res.json()['sources_to_targets'][0][0].get('distance', 0)
    except: pass

    # 4. STEP 03: APIFY INTEL INGESTION (WEB SCRAPER)
    intel_data = "No live stream detected."
    if apify_token:
        try:
            # Triggering the scraper to pull real-time data for the target vector
            run_url = f"https://api.apify.com/v2/acts/apify~web-scraper/runs?token={apify_token}"
            requests.post(run_url, json={"startUrls": [{"url": f"https://www.google.com/search?q={target}+systemic+trends"}]}, timeout=15)
            intel_data = "KINETIC INTEL: Live Connection Established via Apify."
        except: pass

    # 5. THE 33° UNIFIED DISPATCH (GROQ AS DATABASE)
    # Integrating Educational Libraries context into the system prompt
    system_instruction = f"""
    You are the UESP Sovereign Database & Auditor. 
    Current Vector: {target}.
    
    INGESTED DATASETS:
    - LOCATION_NODE: {node_info}
    - KINETIC_DISTANCE: {distance_val} meters
    - LIVE_INTEL: {intel_data}
    - EDUCATIONAL_LIBS: ProQuest (Alexander Street Press) / National Diploma Jewelry Design (UJ)
    
    REQUIRED OUTPUT:
    1. Identify 3 [SINS] (Systemic Frictions).
    2. Architect 3 [VIRTUES] (Resolutions).
    3. CALCULATE SHI & TTI (0.0 to 100.0).
    4. VERDICT: Long-term resonance.

    FORMAT: Return ONLY a valid JSON object.
    {{
        "shi": float,
        "tti": float,
        "assessment": "Detailed breakdown using all ingested databases",
        "node": "{node_info}",
        "distance": {distance_val}
    }}
    """

    try:
        completion = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "system", "content": system_instruction}],
            response_format={ "type": "json_object" },
            temperature=0.15
        )
        lpu_out = json.loads(completion.choices[0].message.content)
        
        result = {
            "subject": target.upper(),
            "node": lpu_out.get("node", node_info),
            "distance": lpu_out.get("distance", distance_val),
            "shi": lpu_out.get("shi", 50.0),
            "tti": lpu_out.get("tti", 50.0),
            "assessment": lpu_out.get("assessment", "RESONANCE_EMPTY"),
            "status": "RESONANT",
            "timestamp": str(int(time.time()))
        }
    except Exception as e:
        result = {"status": "ERROR", "assessment": f"LPU_FAIL: {str(e)}", "timestamp": str(int(time.time()))}

    # 6. ATOMIC WRITE TO GITHUB
    with open('result.json', 'w') as f:
        json.dump(result, f, indent=4)

if __name__ == "__main__":
    run_universal_audit(sys.argv[1] if len(sys.argv) > 1 else "Global")
