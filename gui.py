import sys
import os
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
                             QLabel, QLineEdit, QPushButton, QComboBox, QTextEdit, 
                             QGroupBox, QMessageBox, QGridLayout, QCompleter)
from PyQt5.QtGui import QFont, QColor
from PyQt5.QtCore import Qt, QStringListModel
import io
import folium
from PyQt5.QtWebEngineWidgets import QWebEngineView
from main import TransportNetwork, list_available_cities


class RoutePlannerGUI(QMainWindow):
    """GUI application for Sussumapper using PyQt5."""
    
    def __init__(self):
        super().__init__()
        
        self.network = TransportNetwork()
        self.data_dir = "data"
        self.current_city = None
        
        self.init_ui()

    def reset_map(self, lat=48.8566, lon=2.3522):
        """Affiche une carte par défaut centrée."""
        m = folium.Map(location=[lat, lon], zoom_start=12, tiles="CartoDB positron")
        # On utilise render() pour générer directement le code HTML en texte
        html_content = m.get_root().render()
        self.map_view.setHtml(html_content)

    def draw_route_on_map(self, path):
        """Dessine le trajet sur la carte de manière propre et centrée."""
        coords = []
        station_names = [] # On garde les noms pour les afficher sur la carte
        
        for step in path:
            station_name = step[0] if isinstance(step, tuple) else step 
            if station_name in self.network.station_coords:
                coords.append(self.network.station_coords[station_name])
                station_names.append(station_name)
                
        if not coords:
            return

        # On crée la carte (CartoDB positron donne ce look gris/épuré moderne)
        m = folium.Map(tiles="CartoDB positron")
        
        # 1. Dessiner la ligne épaisse du trajet
        folium.PolyLine(
            coords, 
            color="#14C371",
            weight=5, 
            opacity=0.9
        ).add_to(m)
        
        # 2. Ajouter les marqueurs pour TOUTES les stations
        for i, (coord, name) in enumerate(zip(coords, station_names)):
            if i == 0:
                # Gros marqueur Vert pour le Départ
                folium.Marker(
                    coord, 
                    popup=f"Départ: {name}", 
                    icon=folium.Icon(color="green", icon="play")
                ).add_to(m)
            elif i == len(coords) - 1:
                # Gros marqueur Rouge pour l'Arrivée
                folium.Marker(
                    coord, 
                    popup=f"Arrivée: {name}", 
                    icon=folium.Icon(color="red", icon="flag")
                ).add_to(m)
            else:
                # Petits points blancs entourés de vert pour les arrêts intermédiaires
                folium.CircleMarker(
                    location=coord,
                    radius=5,
                    popup=name,
                    color="#14C371",
                    weight=2,
                    fill=True,
                    fill_color="white",
                    fill_opacity=1
                ).add_to(m)
        
        # 3. LA MAGIE : Demander à la carte de dézoomer/zoomer exactement sur le trajet
        if len(coords) > 1:
            m.fit_bounds(m.get_bounds())
        
        # 4. Afficher
        html_content = m.get_root().render()
        self.map_view.setHtml(html_content)
        
    def init_ui(self):
        """Initialize the user interface."""
        self.setWindowTitle("Sussumapper")
        self.setGeometry(100, 100, 900, 700)
        
        # Set modern stylesheet with rounded corners
        self.setStyleSheet("""
            QMainWindow {
                background-color: #f5f5f5;
            }
            QGroupBox {
                border: 1px solid #ddd;
                border-radius: 8px;
                margin-top: 10px;
                padding-top: 10px;
                font-weight: bold;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 3px 0 3px;
            }
            QLineEdit {
                border: 1px solid #ccc;
                border-radius: 6px;
                padding: 5px;
                background-color: white;
                font-size: 11px;
            }
            QLineEdit:focus {
                border: 2px solid #0078d4;
                background-color: #f9f9f9;
            }
            QPushButton {
                border: none;
                border-radius: 6px;
                padding: 6px 12px;
                background-color: #0078d4;
                color: white;
                font-weight: bold;
                font-size: 11px;
            }
            QPushButton:hover {
                background-color: #1084d8;
            }
            QPushButton:pressed {
                background-color: #005a9e;
            }
            QTextEdit {
                border: 1px solid #ccc;
                border-radius: 6px;
                background-color: white;
                font-size: 10px;
            }
            QLabel {
                font-size: 11px;
            }
            QComboBox {
                border: 1px solid #ccc;
                border-radius: 6px;
                padding: 5px;
                background-color: white;
                font-size: 11px;
            }
            QComboBox:focus {
                border: 2px solid #0078d4;
            }
            QComboBox::drop-down {
                border: none;
                width: 20px;
            }
        """)
        
        # Create central widget and main layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)
        main_layout.setSpacing(10)
        main_layout.setContentsMargins(10, 10, 10, 10)
        
        # ===== HEADER =====
        title_font = QFont('Helvetica', 16, QFont.Bold)
        title_label = QLabel("🚇 Sussumapper")
        title_label.setFont(title_font)
        main_layout.addWidget(title_label)
        
        # ===== CITY SELECTION GROUP =====
        city_group = QGroupBox("1. Load City Data")
        city_layout = QGridLayout()
        
        city_layout.addWidget(QLabel("Select a city:"), 0, 0)
        
        self.city_combo = QComboBox()
        self.city_combo.currentTextChanged.connect(self.on_city_selected)
        city_layout.addWidget(self.city_combo, 0, 1)
        
        self.refresh_btn = QPushButton("Refresh List")
        self.refresh_btn.clicked.connect(self.refresh_cities)
        city_layout.addWidget(self.refresh_btn, 0, 2)
        
        self.status_label = QLabel("No city loaded")
        self.status_label.setStyleSheet("color: gray; font-size: 10px;")
        city_layout.addWidget(self.status_label, 1, 0, 1, 3)
        
        city_group.setLayout(city_layout)
        main_layout.addWidget(city_group)
        
        # ===== CLOSURE MANAGEMENT GROUP =====
        closure_group = QGroupBox("2. Manage Closures (Real Conditions)")
        closure_layout = QGridLayout()
        
        # Stations section
        closure_layout.addWidget(QLabel("Close Stations:"), 0, 0)
        self.station_closure_combo = QComboBox()
        closure_layout.addWidget(self.station_closure_combo, 0, 1)
        
        self.close_station_btn = QPushButton("Close Station")
        self.close_station_btn.clicked.connect(self.close_selected_station)
        closure_layout.addWidget(self.close_station_btn, 0, 2)
        
        # Lines section
        closure_layout.addWidget(QLabel("Close Lines:"), 1, 0)
        self.line_closure_combo = QComboBox()
        closure_layout.addWidget(self.line_closure_combo, 1, 1)
        
        self.close_line_btn = QPushButton("Close Line")
        self.close_line_btn.clicked.connect(self.close_selected_line)
        closure_layout.addWidget(self.close_line_btn, 1, 2)
        
        # Reset button
        self.reset_closures_btn = QPushButton("Reset All Closures")
        self.reset_closures_btn.clicked.connect(self.reset_all_closures)
        closure_layout.addWidget(self.reset_closures_btn, 2, 2)
        
        # Status display
        closure_layout.addWidget(QLabel("Closed Stations:"), 3, 0)
        self.closed_stations_label = QLabel("None")
        self.closed_stations_label.setStyleSheet("color: red; font-weight: bold;")
        closure_layout.addWidget(self.closed_stations_label, 3, 1, 1, 2)
        
        closure_layout.addWidget(QLabel("Closed Lines:"), 4, 0)
        self.closed_lines_label = QLabel("None")
        self.closed_lines_label.setStyleSheet("color: red; font-weight: bold;")
        closure_layout.addWidget(self.closed_lines_label, 4, 1, 1, 2)
        
        closure_group.setLayout(closure_layout)
        main_layout.addWidget(closure_group)
        
        # ===== ROUTE SEARCH GROUP =====
        search_group = QGroupBox("3. Find Shortest Route")
        search_layout = QGridLayout()
        
        # Departure station
        search_layout.addWidget(QLabel("Departure station:"), 0, 0)
        self.start_entry = QLineEdit()
        self.station_completer = QCompleter([])
        self.station_completer.setCaseSensitivity(Qt.CaseInsensitive)
        self.start_entry.setCompleter(self.station_completer)
        search_layout.addWidget(self.start_entry, 0, 1)
        
        # Arrival station
        search_layout.addWidget(QLabel("Arrival station:"), 1, 0)
        self.end_entry = QLineEdit()
        self.station_completer_end = QCompleter([])
        self.station_completer_end.setCaseSensitivity(Qt.CaseInsensitive)
        self.end_entry.setCompleter(self.station_completer_end)
        search_layout.addWidget(self.end_entry, 1, 1)
        
        # Buttons on the right
        buttons_layout = QVBoxLayout()
        
        self.search_btn = QPushButton("Find Route")
        self.search_btn.clicked.connect(self.find_route)
        buttons_layout.addWidget(self.search_btn)
        
        self.clear_btn = QPushButton("Clear")
        self.clear_btn.clicked.connect(self.clear_search)
        buttons_layout.addWidget(self.clear_btn)
        
        buttons_layout.addStretch()
        search_layout.addLayout(buttons_layout, 0, 2, 2, 1)
        
        # Result display area
        search_layout.addWidget(QLabel("Route Details:"), 2, 0, 1, 3)
        
        self.result_text = QTextEdit()
        self.result_text.setReadOnly(True)
        self.result_text.setMinimumHeight(250)
        search_layout.addWidget(self.result_text, 3, 0, 1, 3)
        
        search_group.setLayout(search_layout)
        main_layout.addWidget(search_group, 1)  # Add stretch factor
        
        # ===== BOTTOM FRAME =====
        bottom_layout = QHBoxLayout()
        
        self.info_label = QLabel("Ready to plan your route!")
        self.info_label.setStyleSheet("color: blue; font-size: 9px;")
        bottom_layout.addWidget(self.info_label)
        
        bottom_layout.addStretch()
        
        exit_btn = QPushButton("Exit")
        exit_btn.clicked.connect(self.close)
        bottom_layout.addWidget(exit_btn)
        
        main_layout.addLayout(bottom_layout)
        
        # Initialize city list
        self.refresh_cities()

        # Création du widget de la carte
        self.map_view = QWebEngineView()
        self.map_view.setMinimumWidth(600) # Pour être sûr qu'elle a de la place
        
        # --- ASSEMBLAGE ---
        main_layout.addWidget(self.map_view, 2) # Carte (2/3 de l'espace)
        
        # Afficher une carte vide par défaut au lancement
        self.reset_map()
    
    def refresh_cities(self):
        """Refresh the list of available cities."""
        available_files = list_available_cities(self.data_dir)
        cities = [f.replace('.json', '') for f in available_files]
        
        self.city_combo.clear()
        self.city_combo.addItems(cities)
        
        if not cities:
            QMessageBox.warning(self, "No Cities", 
                              f"No JSON files found in the '{self.data_dir}' folder.\n"
                              "Please place your JSON files inside it.")
    
    def on_city_selected(self, city_name):
        """Auto-load city when selected from dropdown."""
        if city_name:  # Only load if a valid city is selected
            self.load_city(city_name)
    
    def load_city(self, city_name=None):
        """Load the selected city."""
        if city_name is None:
            city_name = self.city_combo.currentText()
        
        if not city_name:
            QMessageBox.warning(self, "Selection Required", "Please select a city.")
            return
        
        filepath = os.path.join(self.data_dir, f"{city_name}.json")
        
        try:
            self.network.load_from_json(filepath)
            self.current_city = city_name
            
            station_count = len(self.network.stations)
            self.status_label.setText(
                f"✅ {city_name.capitalize()} loaded with {station_count} stations"
            )
            self.status_label.setStyleSheet("color: green; font-size: 10px;")
            
            # Update autocomplete with station names
            stations_list = sorted(list(self.network.stations))
            model = QStringListModel(stations_list)
            self.station_completer.setModel(model)
            self.station_completer_end.setModel(QStringListModel(stations_list))
            
            # Update closure combo boxes
            self.update_closure_combos()
            self.update_closure_status()
            
            self.update_info(f"Loaded {city_name} with {station_count} stations")
        except FileNotFoundError:
            QMessageBox.critical(self, "Error", f"Could not find file: {filepath}")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to load city:\n{str(e)}")
    
    def find_route(self):
        """Find the shortest route between two stations."""
        if not self.network.stations:
            QMessageBox.warning(self, "No City Loaded", 
                              "Please load a city first (Step 1)!")
            return
        
        start_station = self.start_entry.text().strip()
        end_station = self.end_entry.text().strip()
        
        if not start_station or not end_station:
            QMessageBox.warning(self, "Missing Input", 
                              "Please enter both departure and arrival stations.")
            return
        
        try:
            route = self.network.dijkstra(start_station, end_station)
            self.display_route(route)
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error finding route:\n{str(e)}")
    
    def display_route(self, route):
        """Display the route in the result text area."""
        if not route or len(route) < 2:
            result_text = "❌ No route found or invalid stations.\nPlease check your spelling."
            self.update_info("No route found")
            
            # (Optionnel) Réinitialiser la carte s'il n'y a pas de trajet
            self.reset_map()
        else:
            # Format route manually for GUI display
            start_station = route[0][0]
            start_line = route[1][1]
            
            result_text = "=" * 50 + "\n"
            result_text += "🛤️  YOUR ITINERARY\n"
            result_text += "=" * 50 + "\n"
            result_text += f"📍 Board at {start_station}, line {start_line}\n\n"
            
            current_line = start_line
            
            # Loop through intermediate stations
            for i in range(1, len(route) - 1):
                current_station = route[i][0]
                next_line = route[i + 1][1]
                
                if next_line != current_line:
                    result_text += f"   ↓ Arrive at {current_station}\n"
                    result_text += f"🔄 Transfer at {current_station}, take line {next_line}\n\n"
                    current_line = next_line
                else:
                    result_text += f"   ↓ Continue through {current_station}\n"
            
            final_station, final_line, total_time = route[-1]
            result_text += f"\n🏁 Arrived at {final_station}, line {current_line}\n"
            result_text += "-" * 50 + "\n"
            
            mins, secs = divmod(total_time, 60)
            result_text += f"⏱️  Estimated total time: {mins} minutes {secs} seconds\n"
            result_text += "=" * 50
            
            self.update_info(f"Route found: {mins}m {secs}s")
            
            # === NOUVEAU : C'EST ICI QU'ON DESSINE LA CARTE ! ===
            # On passe l'itinéraire complet à la fonction que nous avons créée plus tôt
            self.draw_route_on_map(route)
            
        self.result_text.setText(result_text)
    
    def clear_search(self):
        """Clear search fields and results."""
        self.start_entry.clear()
        self.end_entry.clear()
        self.result_text.clear()
        
        self.update_info("Search cleared")
    
    def update_closure_combos(self):
        """Update the dropdown lists for station and line closures."""
        # Update stations combo
        stations_list = self.network.get_all_stations()
        self.station_closure_combo.clear()
        self.station_closure_combo.addItems(stations_list)
        
        # Update lines combo with line names and IDs
        lines_list = self.network.get_all_lines()
        line_display_items = []
        for line_id in lines_list:
            line_name = self.network.lines.get(line_id, {}).get("nom", f"Line {line_id}")
            line_display_items.append(f"{line_id}: {line_name}")
        
        self.line_closure_combo.clear()
        self.line_closure_combo.addItems(line_display_items)
    
    def update_closure_status(self):
        """Update the display of closed stations and lines."""
        closed_stations = self.network.closed_stations
        closed_lines = self.network.closed_lines
        
        # Update closed stations display
        if closed_stations:
            stations_text = ", ".join(sorted(list(closed_stations)))
            self.closed_stations_label.setText(stations_text)
        else:
            self.closed_stations_label.setText("None")
        
        # Update closed lines display
        if closed_lines:
            lines_display = []
            for line_id in sorted(list(closed_lines)):
                line_name = self.network.lines.get(line_id, {}).get("nom", f"Line {line_id}")
                lines_display.append(f"{line_id} ({line_name})")
            lines_text = ", ".join(lines_display)
            self.closed_lines_label.setText(lines_text)
        else:
            self.closed_lines_label.setText("None")
    
    def close_selected_station(self):
        """Close the selected station."""
        station = self.station_closure_combo.currentText()
        if station and self.network.close_station(station):
            self.update_closure_status()
            # Remove it from the combo and add to available stations
            self.update_closure_combos()
            self.update_info(f"Station '{station}' is now closed")
            QMessageBox.information(self, "Station Closed", f"Station '{station}' has been closed and will be avoided in route calculations.")
        else:
            QMessageBox.warning(self, "Error", f"Could not close station '{station}'")
    
    def close_selected_line(self):
        """Close the selected line."""
        current_text = self.line_closure_combo.currentText()
        line_id = current_text.split(":")[0]  # Extract line ID from "ID: Name"
        
        if line_id and self.network.close_line(line_id):
            self.update_closure_status()
            self.update_closure_combos()
            line_name = self.network.lines.get(line_id, {}).get("nom", f"Line {line_id}")
            self.update_info(f"Line {line_id} ({line_name}) is now closed")
            QMessageBox.information(self, "Line Closed", f"Line {line_id} ({line_name}) has been closed and will be avoided in route calculations.")
        else:
            QMessageBox.warning(self, "Error", f"Could not close line '{line_id}'")
    
    def reset_all_closures(self):
        """Reset all closures and reopen all stations and lines."""
        self.network.closed_stations.clear()
        self.network.closed_lines.clear()
        self.update_closure_status()
        self.update_closure_combos()
        self.update_info("All closures have been reset")
        QMessageBox.information(self, "Closures Reset", "All stations and lines are now open.")
    
    def update_info(self, message):
        """Update the info label at the bottom."""
        self.info_label.setText(message)
        self.info_label.setStyleSheet("color: blue; font-size: 9px;")


def main():
    app = QApplication(sys.argv)
    window = RoutePlannerGUI()
    window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
