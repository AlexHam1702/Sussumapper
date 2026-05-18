# **🚇 Sussumapper**

**MVP Status:** v0.67

**Group Members:** Noa Thams, Baptiste Lhors, Eleanor Cortes-Sommaro, Alexandre Hamard


## **🎯 Project Overview**

Sussumapper is a desktop application designed to help commuters find the fastest routes through urban transit networks. It processes metropolitan transit data (stations, lines, and connections) and uses optimized algorithms to compute shortest paths while accounting for transfer times and line changes.

The application provides both a **command-line interface** for route queries and a **modern PyQt5 GUI** for an enhanced user experience. The core engine uses **Dijkstra's Algorithm** to find time-optimal routes, while supporting multiple transit lines and realistic transfer penalties.


## **🚀 Quick Start (Architect Level: < 60s Setup)**

Instructions on how to get this project running on a fresh machine.

1. **Clone the repo:**
   ```bash
   git clone [your-repo-link]
   cd PBL-3
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
  - `dijkstra()`: Implements Dijkstra's Algorithm to find shortest-time routes
  - `bfs()`: Breadth-First Search for finding paths with minimum stops
  - `format_route()`: Formats and displays route information with transfers and timing
  - **Transfer Penalty System**: Applies a 120-second penalty when switching transit lines to reflect realistic connection times

* **gui.py**: PyQt5-based graphical user interface
  - `RoutePlannerGUI`: Main window managing the user interface
  - **City Selection Panel**: Load and switch between different metropolitan networks
  - **Station Auto-completion**: Provides intelligent station name suggestions as users type
  - **Route Display**: Visual presentation of itineraries with stops, transfers, and travel times
  - **Modern Styling**: Rounded corners, focus states, and professional color scheme
  - **Error Handling**: User-friendly dialogs for validation and feedback

### **Algorithm Highlights:**

- **Dijkstra's Algorithm**: Finds the optimal route minimizing total travel time
- **Line Switching Logic**: Automatically detects and penalizes transfers between different transit lines
- **State Tracking**: Uses `(station, line)` tuples to prevent inefficient revisits on the same line
- **Bidirectional Edges**: Ensures all transit connections work in both directions
- **Station & Line Closures**: Simulates real-world conditions by allowing stations and lines to be temporarily closed
  - The routing algorithm automatically avoids closed stations and lines
  - Routes are recalculated to find viable alternatives
  - Perfect for simulating maintenance, breakdowns, or emergency situations


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
Normal route: La Défense → Concorde → Châtelet → Gare de Lyon
If Châtelet is closed: La Défense → Tuileries → Hôtel de Ville → Bastille → Gare de Lyon
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

### **Automated Testing** (using pytest)

Expected test cases:

* **Route Finding**: Verify Dijkstra correctly finds shortest paths
* **Transfer Penalties**: Confirm line changes add 120-second penalties
* **Input Validation**: Ensure invalid stations are handled gracefully
* **Edge Cases**: Test single-stop routes, disconnected stations, and large networks
* **BFS Alternative**: Verify paths with fewest stops when applicable


## **📦 Dependencies**

* **PyQt5**: Modern GUI framework for desktop applications
  - Provides widgets, layouts, and event handling
  - Enables auto-completion and styled components

* **Python Standard Library:**
  - `json`: Parses network data files
  - `heapq`: Priority queue for Dijkstra's Algorithm
  - `os`: File system operations for data loading
  - `sys`: System-level operations

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

## **📄 License**

Educational project for PBL-3 course.
