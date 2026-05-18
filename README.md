# **🚇 Sussumapper**

**MVP Status:** v0.67

**Group Members:** Noa Thams, Baptiste Lhors, Eleanor Cortes-Sommaro, Alexandre Hamard


## **🎯 Project Overview**

Sussumapper is a desktop application designed to help commuters find the fastest routes through urban transit networks. It processes metropolitan transit data (stations, lines, and connections) and uses optimized algorithms to compute shortest paths while accounting for transfer times and line changes.

The application provides both a **command-line interface** for route queries and a **modern PyQt5 GUI** for an enhanced user experience. The core engine uses **Dijkstra's Algorithm** to find time-optimal routes, while supporting multiple transit lines and realistic transfer penalties.

---

## **✨ Key Features**

### **🗺️ Route Planning**
- **Shortest Time Routing**: Dijkstra's Algorithm finds the fastest route between any two stations
- **Smart Transfer Penalties**: Adds realistic 120-second penalty for line changes
- **Multi-line Support**: Seamlessly handles routes across multiple transit lines
- **Interactive Map Display**: Visual representation of routes with folium integration

### **🚨 Real-World Conditions**
- **Station Closures**: Simulate maintenance or emergencies by closing individual stations
- **Line Closures**: Temporarily disable entire transit lines for network disruptions
- **Dynamic Adaptation**: Routes automatically recalculate to avoid closed infrastructure
- **Easy Management**: One-click closure reset to restore full network

### **💻 User Experience**
- **Modern GUI**: Professional PyQt5 interface with rounded corners and intuitive layout
- **Auto-completion**: Intelligent station name suggestions as you type
- **City Switching**: Load and switch between multiple metropolitan transit networks
- **Real-time Status**: Visual indicators showing current state of closures and routes
- **Error Handling**: User-friendly validation and helpful error messages

### **📊 Data Flexibility**
- **JSON-based Data**: Easy to load and modify transit network data
- **Multi-city Support**: Support for any metropolitan network with proper data format
- **GPS Coordinates**: Integrated station location data for map rendering
- **Structured Format**: Organized line and station information for reliable parsing

---

## **🚀 Quick Start (Architect Level: < 60s Setup)**

Instructions on how to get this project running on a fresh machine.

1. **Clone the repo:**
   ```bash
   git clone [your-repo-link]
   cd Sussumapper
   ```

2. **Setup Virtual Environment:**
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

3. **Install Dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the GUI Application:**
   ```bash
   python gui.py
   ```

5. **Prepare Data Files:**
   - Place your JSON transit network files in the `data/` folder
   - The app will automatically detect and load available cities


## **🛠️ Technical Architecture**

This application is built using **Object-Oriented Programming (OOP)** principles with a clear separation between the core routing engine and user interfaces.

### **Core Components:**

* **main.py**: The core routing engine containing the `TransportNetwork` class
  - `TransportNetwork`: Manages the graph-based transit network with stations and connections
  - `load_from_json()`: Parses metropolitan transit data from structured JSON files
  - `dijkstra()`: Implements Dijkstra's Algorithm to find shortest-time routes with closure awareness
  - `bfs()`: Breadth-First Search for finding paths with minimum stops
  - `format_route()`: Formats and displays route information with transfers and timing
  - **Closure Management**: 
    - `close_station()` / `open_station()`: Manage individual station availability
    - `close_line()` / `open_line()`: Manage entire line availability
    - `get_open_stations()` / `get_open_lines()`: Retrieve available infrastructure
  - **Transfer Penalty System**: Applies a 120-second penalty when switching transit lines to reflect realistic connection times

* **gui.py**: PyQt5-based graphical user interface
  - `RoutePlannerGUI`: Main window managing the user interface
  - **City Selection Panel**: Load and switch between different metropolitan networks
  - **Closure Management Panel**: Control station and line closures
  - **Station Auto-completion**: Provides intelligent station name suggestions as users type
  - **Route Display**: Visual presentation of itineraries with stops, transfers, and travel times
  - **Map Integration**: Interactive folium-based map showing routes with markers and paths
  - **Modern Styling**: Rounded corners, focus states, and professional color scheme
  - **Error Handling**: User-friendly dialogs for validation and feedback

### **Algorithm Highlights:**

- **Dijkstra's Algorithm**: Finds the optimal route minimizing total travel time
- **Line Switching Logic**: Automatically detects and penalizes transfers between different transit lines
- **State Tracking**: Uses `(station, line)` tuples to prevent inefficient revisits on the same line
- **Bidirectional Edges**: Ensures all transit connections work in both directions
- **Closure-Aware Routing**: Dynamically avoids closed stations and lines during pathfinding
  - Checks closure status for each edge traversal
  - Skips unavailable infrastructure automatically
  - Finds viable alternate routes when needed

### **Application Workflow:**

```
1. Launch gui.py
   ↓
2. Select city from dropdown
   ↓
3. (Optional) Close stations/lines in "Manage Closures" panel
   ↓
4. Enter departure and arrival stations
   ↓
5. Click "Find Route"
   ↓
6. View route details and interactive map
   ↓
7. (Optional) Adjust closures and recalculate routes
```


## **🚨 Real-World Conditions: Station & Line Closures**

The application now supports simulating realistic network conditions where stations or entire lines are temporarily unavailable.

### **Features:**

- **Close Individual Stations**: Mark specific stations as out of service (e.g., for maintenance)
- **Close Entire Lines**: Temporarily disable a complete transit line
- **Dynamic Route Adaptation**: The algorithm automatically finds alternate routes avoiding closed infrastructure
- **Easy Reset**: Clear all closures with one button to restore the full network

### **How to Use (GUI):**

1. Load a city and its transit network
2. Go to the **"Manage Closures (Real Conditions)"** section
3. **To close a station:**
   - Select a station from the dropdown
   - Click "Close Station"
   - The status display updates to show closed stations
   - Routes will now avoid this station

4. **To close a line:**
   - Select a line from the dropdown
   - Click "Close Line"
   - The status display updates to show closed lines
   - Routes will use alternative lines to reach destinations

5. **To restore service:**
   - Click "Reset All Closures" to reopen everything
   - Or manually reopen individual stations/lines as they return to service

### **Example Scenario:**

```
Normal route: La Défense → Concorde → Châtelet → Gare de Lyon (35m 30s)
If Châtelet is closed: La Défense → Tuileries → Hôtel de Ville → Bastille → Gare de Lyon (44m 30s)
```

---

## **📊 Data Format**

The application expects JSON files with the following structure:

```json
{
  "temps_moyen": 90,
  "lignes": {
    "line_id": {
      "stations": ["Station A", "Station B", "Station C"]
    }
  },
  "connexions": []
}
```

- `temps_moyen`: Average travel time between consecutive stations (in seconds)
- `lignes`: Dictionary of transit lines with ordered station sequences
- `connexions`: Array of explicit connections (optional, for future extensions)


## **🧪 Testing & Validation**

### **Manual GUI Testing**

1. Run `python gui.py` to launch the interface
2. Select a city from the dropdown (JSON files in `data/` folder)
3. Enter a departure station (autocomplete assists)
4. Enter an arrival station
5. Click "Find Route" to compute the shortest path
6. **Validation Criteria:**
   - Route displays all necessary station stops
   - Transfer information is accurate and highlighted
   - Total travel time calculation is correct
   - No crashes on invalid input

### **Testing Closures (Real Conditions)**

1. After loading a city, go to **"Manage Closures"** section
2. Close a station and verify:
   - Status display updates with closed station
   - New routes avoid the closed station
   - Alternative paths are found
3. Close a line and verify:
   - Status display updates with closed line
   - Routes use alternative lines
   - Transit options are recalculated
4. Click "Reset All Closures" and verify:
   - All closures cleared
   - Routes return to optimal paths
   - Normal routing resumes

### **Automated Testing**

Run the test suite:
```bash
python test_closures.py
```

This validates:
- ✅ Routes work normally without closures
- ✅ Closed stations force alternate routes  
- ✅ Closed lines are properly avoided
- ✅ Closures can be reset to restore full network
- ✅ Algorithm correctly adapts to network changes

### **Unit Test Coverage:**

* **Route Finding**: Verify Dijkstra correctly finds shortest paths
* **Transfer Penalties**: Confirm line changes add 120-second penalties
* **Input Validation**: Ensure invalid stations are handled gracefully
* **Closure Logic**: Test station and line closure functionality
* **Network Adaptation**: Verify routes change when infrastructure closes
* **Edge Cases**: Test single-stop routes, disconnected stations, and large networks


## **📦 Dependencies**

All dependencies are listed in `requirements.txt` and can be installed with:
```bash
pip install -r requirements.txt
```

### **External Libraries:**

* **PyQt5 (5.15.9)**: Modern GUI framework for desktop applications
  - `QtWidgets`: UI components (windows, buttons, dialogs, text fields)
  - `QtGui`: Font and color management
  - `QtCore`: Signals, slots, and core functionality
  - `QtWebEngineWidgets`: Web engine for rendering HTML content

* **PyQtWebEngine (5.15.6)**: Web rendering support for PyQt5
  - Enables embedded web views for map display

* **folium (0.14.0)**: Leaflet.js Python wrapper
  - Creates interactive maps with custom markers and routes
  - Integrates with PyQtWebEngineView for seamless map display

### **Python Standard Library (Built-in):**

- `json`: Parses network data files and configurations
- `heapq`: Priority queue implementation for Dijkstra's Algorithm
- `os`: File system operations for data loading and path management
- `sys`: System-level operations
- `io`: String buffer handling for map HTML generation

### **System Requirements:**

- **Python**: 3.7 or higher
- **OS**: Windows, macOS, or Linux
- **RAM**: Minimum 512 MB (more for larger networks)
- **Disk**: 100 MB for application + data files

---

## **🔮 Future Roadmap (v2.0)**

* **Multi-modal Transport**: Support buses, trains, and cycling integration
* **Real-time Updates**: Live traffic and delay information
* **Fare Calculation**: Compute costs alongside time optimization
* **Accessibility Features**: Screen reader support, high contrast themes
* **Mobile App**: React Native or Flutter version
* **Performance Optimization**: Implement A* or contraction hierarchies for larger networks
* **Trip Planning**: Multi-stop itineraries and schedule optimization

---

