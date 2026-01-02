import requests
import xml.etree.ElementTree as ET
from datetime import datetime

def format_time(iso_str):
    try:
        if iso_str.endswith('Z'): iso_str = iso_str.replace('Z', '+00:00')
        return datetime.fromisoformat(iso_str).strftime("%d/%m %H:%M")
    except:
        return "?"

#https://nap.dgt.es/dataset/incidencias-dgt-datex2-v3-6
url = "https://nap.dgt.es/datex2/v3/dgt/SituationPublication/datex2_v36.xml"

try:
    resp = requests.get(url, stream=True, timeout=30)
    resp.raise_for_status()
    resp.raw.decode_content = True
    
    context = ET.iterparse(resp.raw, events=("end",))
    beacons = []
    
    sense_map = {"positive": "Creciente", "negative": "Decreciente", "both": "Ambos"}

    for _, elem in context:
        if elem.tag.endswith("situationRecord"):
            def get(s):
                node = next((c for c in elem.iter() if c.tag.endswith(s) and c.text), None)
                return node.text if node is not None else "?"

            if get("sourceIdentification") == "DGT3.0":
                try:
                    record_id = elem.get("id") or "?"
                    raw_sense = get("tpegDirectionRoad")
                    sense = sense_map.get(raw_sense, raw_sense)

                    beacons.append({
                        "id": record_id,
                        "time": format_time(get("overallStartTime")),
                        "road": get("roadName"),
                        "km": get("kilometerPoint"),
                        "town": get("municipality"),
                        "prov": get("province"),
                        "sense": sense
                    })
                except ValueError:
                    pass
            elem.clear()
            
    print(f"\n{'ID':<10} {'FECHA':<12} {'VIA':<12} {'PK':<8} {'SENTIDO':<16} {'MUNICIPIO':<20} {'PROVINCIA'}")
    print("-" * 110)
    
    for b in beacons:
        print(f"{b['id']:<10} {b['time']:<12} {b['road']:<12} {b['km']:<8} {b['sense'][:15]:<16} {b['town'][:19]:<20} {b['prov']}")

    print(f"\nTotal Activas: {len(beacons)}")

except Exception as e:
    print(f"Error: {e}")
