import json
import heapq
import os

class TransportNetwork:
    import json
import heapq
import os

class TransportNetwork:
    def __init__(self):
        # Adjacency list: {station: [(neighbor, time, line), ...]}
        self.graph = {}
        self.stations = set()
        self.lines = {}
        self.station_coords = {} # NOUVEAU : Dictionnaire pour stocker les GPS
        self.transfer_penalty = 120
        
    def load_from_json(self, filepath):
        """Loads network data from the structured French JSON file."""
        self.graph = {}
        self.stations = set()
        self.lines = {}
        self.station_coords = {} # Réinitialisation
        
        with open(filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)
            
        self.lines = data.get("lignes", {})
        
        # NOUVEAU : Chargement des coordonnées GPS
        stations_info = data.get("stations_info", {})
        for station, info in stations_info.items():
            lat = info.get("lat")
            lon = info.get("lon")
            if lat is not None and lon is not None:
                self.station_coords[station] = (lat, lon)
        
        default_time = data.get("temps_moyen", 90)
        
        # 1. Generate connections dynamically from the ordered lists of stations
        for line_id, line_info in self.lines.items():
            stations_list = line_info.get("stations", [])
            for i in range(len(stations_list) - 1):
                dep = stations_list[i]
                arr = stations_list[i+1]
                # Add bidirectional edges with the default time
                self.add_edge(dep, arr, default_time, line_id)
                self.add_edge(arr, dep, default_time, line_id)
        
        # 2. Add explicit connections if the "connexions" array ever contains any
        for conn in data.get("connexions", []):
            # Using .get() allows fallback for varying structures
            dep = conn.get("depart") or conn.get("departure")
            arr = conn.get("arrivee") or conn.get("arrival")
            time = conn.get("temps") or conn.get("time")
            line_id = conn.get("ligne") or conn.get("line")
            
            if dep and arr and time and line_id:
                self.add_edge(dep, arr, time, line_id)
                self.add_edge(arr, dep, time, line_id)
            
    def add_edge(self, source, destination, time, line):
        if source not in self.graph:
            self.graph[source] = []
        self.graph[source].append((destination, time, line))
        self.stations.add(source)
        self.stations.add(destination)

    def bfs(self, start_station):
        """Breadth-First Search to find paths with the fewest stops."""
        if start_station not in self.stations:
            return None
        visited = set([start_station])
        queue = [[start_station]]
        
        while queue:
            path = queue.pop(0)
            node = path[-1]
            
            for neighbor, _, _ in self.graph.get(node, []):
                if neighbor not in visited:
                    visited.add(neighbor)
                    new_path = list(path)
                    new_path.append(neighbor)
                    queue.append(new_path)
        return visited

    def dijkstra(self, start, end):
        """Finds the shortest path in travel time using Dijkstra's Algorithm."""
        if start not in self.stations or end not in self.stations:
            return None

        # Priority queue: (total_time, current_station, current_line, path_history)
        pq = [(0, start, None, [])]
        
        # Track minimum times: { (station, line): min_time }
        min_times = {}

        while pq:
            current_time, current_station, current_line, path = heapq.heappop(pq)
            
            # Reconstruct path format: (station, line, accumulated_time)
            new_path = path + [(current_station, current_line, current_time)]

            if current_station == end:
                return new_path

            state = (current_station, current_line)
            if state in min_times and min_times[state] <= current_time:
                continue
            min_times[state] = current_time

            for neighbor, edge_time, next_line in self.graph.get(current_station, []):
                time_cost = current_time + edge_time
                
                # Apply 120s transfer penalty if switching lines (and not the first station)
                if current_line is not None and current_line != next_line:
                    time_cost += self.transfer_penalty

                heapq.heappush(pq, (time_cost, neighbor, next_line, new_path))
                
        return None

def format_route(route):
    """Formats the route output for maximum readability."""
    if not route or len(route) < 2:
        print("❌ No route found or invalid stations. Please check your spelling.")
        return

    print("\n" + "="*40)
    print("🛤️  YOUR ITINERARY")
    print("="*40)
    
    # route[0] is start, route[1] is the first hop
    start_station = route[0][0]
    start_line = route[1][1] 
    
    print(f"📍 Board at {start_station}, line {start_line}")
    
    current_line = start_line
    
    # Loop through the intermediate stations
    for i in range(1, len(route) - 1):
        current_station = route[i][0]
        next_line = route[i+1][1] # Look ahead to the line used for the next hop
        
        if next_line != current_line:
            print(f"   ↓ Arrive at {current_station}")
            print(f"🔄 Transfer at {current_station}, take line {next_line}")
            current_line = next_line
        else:
            print(f"   ↓ Continue through {current_station}")
            
    final_station, final_line, total_time = route[-1]
    print(f"🏁 Alight at {final_station}, line {current_line}")
    print("-" * 40)
    
    mins, secs = divmod(total_time, 60)
    print(f"⏱️  Estimated total time: {mins} minutes {secs} seconds")
    print("="*40 + "\n")

def list_available_cities(data_dir):
    """Scans the data directory and returns a list of JSON files."""
    if not os.path.exists(data_dir):
        os.makedirs(data_dir)
        print(f"📁 Created '{data_dir}' folder. Please place your JSON files inside it.")
        return []
    
    files = [f for f in os.listdir(data_dir) if f.endswith('.json')]
    return files

