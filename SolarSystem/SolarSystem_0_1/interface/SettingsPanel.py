from PySide6.QtWidgets import QWidget, QVBoxLayout, QPushButton, QScrollArea, QCheckBox, QLabel, QFrame, QSizePolicy, QLayout



class SettingsPanel(QWidget):
    
    def __init__(self, loader, parent=None):
        super().__init__(parent)
        self.loader = loader
        self.parent = parent
        self.setFixedWidth(200)
        self.setup_ui()
        
    def setup_ui(self):
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(5, 5, 5, 5)
        self.layout.setSpacing(5)
        
        self.orbit_btn = QPushButton("Орбиты")
        self.trajectory_btn = QPushButton("Траектории")
        self.visibiliti_btn = QPushButton("Выделение")
        self.back_btn = QPushButton("Назад")
        self.back_btn.hide()
        
        self.orbit_btn.clicked.connect(self.show_orbit_settings)
        self.trajectory_btn.clicked.connect(self.show_trajectory_settings)
        self.visibiliti_btn.clicked.connect(self.show_visibiliti_settings)
        self.back_btn.clicked.connect(self.show_main_buttons)
        
        self.layout.addWidget(self.orbit_btn)
        self.layout.addWidget(self.trajectory_btn)
        self.layout.addWidget(self.visibiliti_btn)
        self.layout.addWidget(self.back_btn)
        self.layout.addStretch()
        
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_content = QWidget()
        self.scroll_layout = QVBoxLayout(self.scroll_content)
        self.scroll_content.setLayout(self.scroll_layout)
        self.scroll_area.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.scroll_area.setWidget(self.scroll_content)
        self.scroll_area.hide()
        
        self.layout.addWidget(self.scroll_area)

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self.scroll_content.setMinimumHeight(self.height() - self.back_btn.height() - 50)
        
    def show_main_buttons(self):
        
        self.scroll_area.hide()
        self.back_btn.hide()
        self.orbit_btn.show()
        self.trajectory_btn.show()
        
    def show_orbit_settings(self):
        self.current_mode = "orbit"
        self.setup_visibility_settings()
        
    def show_trajectory_settings(self):
        self.current_mode = "trajectory"
        self.setup_visibility_settings()

    def show_visibiliti_settings(self):
        self.current_mode = "visibiliti"
        self.setup_visibility_settings()
        
    def setup_visibility_settings(self):

        init_data = {}
        for obj in self.loader.objects:
            init_data[obj.name] = {
                "orbit": obj.is_simulate_orbit,
                "trajectory": obj.is_simulate_traectory,
                "visibiliti": obj.is_visibiliti
                }



        while self.scroll_layout.count():
            child = self.scroll_layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()

        title = QLabel("Видимость орбит" if self.current_mode == "orbit" else "Видимость траекторий")
        self.scroll_layout.addWidget(title)

        all_checkbox = QCheckBox("Все")
        all_checkbox.stateChanged.connect(self.toggle_all_objects)
        self.scroll_layout.addWidget(all_checkbox)
    

        separator = QFrame()
        separator.setFrameShape(QFrame.HLine)
        separator.setFrameShadow(QFrame.Sunken)
        self.scroll_layout.addWidget(separator)
    

        self.checkboxes = {}
        planets_data = self.loader.json_data.get("planets", {})
        for planet_key, planet_data in planets_data.items():
            planet_name = planet_data.get("name", planet_key)
        
            planet_checkbox = QCheckBox(planet_name.capitalize())
            planet_checkbox.setObjectName(planet_name)
            planet_checkbox.stateChanged.connect(self.on_checkbox_changed)
            planet_checkbox.setChecked(init_data[planet_name][self.current_mode])
            self.scroll_layout.addWidget(planet_checkbox)
            self.checkboxes[planet_name] = planet_checkbox
        
            satellites = planet_data.get("satellites", {})
            for satellite_key, satellite_data in satellites.items():
                satellite_name = satellite_data.get("name", satellite_key)
            
                satellite_checkbox = QCheckBox(satellite_name.capitalize())
                satellite_checkbox.setObjectName(satellite_name)
                satellite_checkbox.stateChanged.connect(self.on_checkbox_changed)
                satellite_checkbox.setChecked(init_data[satellite_name][self.current_mode])
                satellite_checkbox.setStyleSheet("padding-left: 20px;")
                self.scroll_layout.addWidget(satellite_checkbox)
                self.checkboxes[satellite_name] = satellite_checkbox
    
        self.scroll_layout.addStretch()
    
        self.orbit_btn.hide()
        self.trajectory_btn.hide()
        self.back_btn.show()
        self.scroll_area.show()
        
    def toggle_all_objects(self, state):
        for checkbox in self.checkboxes.values():
            checkbox.setChecked(state == 2)
        
            
    def on_checkbox_changed(self, state):
        sender = self.sender()
        planet_name = sender.objectName()
        is_checked = sender.isChecked()
            
        if self.current_mode == "orbit":
            self.loader.objects_dict[planet_name].is_simulate_orbit = is_checked
        elif self.current_mode == "trajectory":
            self.loader.objects_dict[planet_name].is_simulate_traectory = is_checked
        else: self.loader.objects_dict[planet_name].is_visibiliti = is_checked