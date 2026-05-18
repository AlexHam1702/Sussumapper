import json
import os
import requests
import time

DOSSIER_ACTUEL = os.path.dirname(os.path.abspath(__file__))

fichiers_villes = {
    'bordeaux.json': 'Bordeaux',
    'lille.json': 'Lille',
    'lyon.json': 'Lyon',
    'paris.json': 'Paris'
}

def get_arcgis_coordinates(station_name, city):
    """Utilise l'API d'ArcGIS pour trouver les coordonnées sans blocage."""
    url = "https://geocode.arcgis.com/arcgis/rest/services/World/GeocodeServer/findAddressCandidates"
    
    if city in ["Paris", "Lille", "Lyon"]:
        query = f"station métro {station_name}, {city}, France"
    else:
        query = f"station tramway {station_name}, {city}, France"
        
    params = {
        'f': 'json',
        'singleLine': query,
        'maxLocations': 1
    }
    
    try:
        response = requests.get(url, params=params, timeout=10)
        if response.status_code == 200:
            data = response.json()
            if "candidates" in data and len(data["candidates"]) > 0:
                location = data["candidates"][0]["location"]
                # ArcGIS renvoie x (longitude) et y (latitude)
                return location["y"], location["x"]
    except Exception as e:
        print(f"  [Erreur réseau] {e}")
            
    return None, None

def process_files():
    for filename, city_name in fichiers_villes.items():
        chemin_complet = os.path.join(DOSSIER_ACTUEL, filename)
        
        if not os.path.exists(chemin_complet):
            continue
            
        print(f"\n--- Traitement de {filename} ({city_name}) avec ArcGIS ---")
        
        with open(chemin_complet, 'r', encoding='utf-8') as f:
            data = json.load(f)
            
        if "stations_info" not in data:
            data["stations_info"] = {}
            
        lignes = data.get("lignes", {})
        for id_ligne, infos_ligne in lignes.items():
            for station in infos_ligne.get("stations", []):
                if station not in data["stations_info"]:
                    data["stations_info"][station] = {"lat": None, "lon": None}
                    
        stations_info = data["stations_info"]
        updated_count = 0
        
        print(f"Recherche de {len(stations_info)} stations...")
        
        for station in stations_info.keys():
            lat, lon = get_arcgis_coordinates(station, city_name)
            
            if lat is not None and lon is not None:
                stations_info[station]["lat"] = round(lat, 6)
                stations_info[station]["lon"] = round(lon, 6)
                updated_count += 1
                print(f"  ✅ {station} -> ({lat:.4f}, {lon:.4f})")
            else:
                print(f"  ❌ {station}")
            
            # ArcGIS est tolérant, mais on garde une petite pause de sécurité
            time.sleep(0.5)
                
        chemin_sortie = os.path.join(DOSSIER_ACTUEL, f"updated_{filename}")
        with open(chemin_sortie, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
            
        print(f"-> Terminé. {updated_count}/{len(stations_info)} trouvées pour {city_name}.")

if __name__ == "__main__":
    print("Démarrage du scanner avec ArcGIS...")
    process_files()