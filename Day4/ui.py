import logic
import customtkinter as ctk
from datetime import datetime
import threading

ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")

class DailyBriefingApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        
        self.title("Daily Israeli Briefing")
        self.geometry("900x700") 
        
        # Grid layout for main window
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1) 
        self.grid_rowconfigure(2, weight=0) 
        
        # --- HEADER ---
        self.header_frame = ctk.CTkFrame(self, corner_radius=0, fg_color="#1a1a1a", height=70)
        self.header_frame.grid(row=0, column=0, sticky="ew")
        self.header_frame.grid_propagate(False) 
        
        ctk.CTkLabel(self.header_frame, text="Hey, Einav!", font=("Roboto Medium", 22)).pack(pady=(12, 0))
        ctk.CTkLabel(self.header_frame, text="It's a great day for great things today.", 
                     font=("Roboto", 14), text_color="gray").pack()
        
        # --- CONTENT AREA (2x2 Grid) ---
        self.main_content = ctk.CTkFrame(self, fg_color="transparent")
        self.main_content.grid(row=1, column=0, sticky="nsew", padx=20, pady=20)
        
        # Uniform 2x2 grid
        self.main_content.grid_columnconfigure(0, weight=1, uniform="group1")
        self.main_content.grid_columnconfigure(1, weight=1, uniform="group1")
        self.main_content.grid_rowconfigure(0, weight=1, uniform="group1")
        self.main_content.grid_rowconfigure(1, weight=1, uniform="group1")
        
        # Loading Indicator
        self.loading_label = ctk.CTkLabel(self.main_content, text="Fetching data... Please wait...", font=("Roboto", 18))
        self.loading_label.grid(row=0, column=0, columnspan=2, pady=100)
        
        # --- FOOTER ---
        self.footer_frame = ctk.CTkFrame(self, corner_radius=0, height=60, fg_color="transparent")
        self.footer_frame.grid(row=2, column=0, sticky="ew", pady=(0, 20))
        
        self.btn_close = ctk.CTkButton(self.footer_frame, text="Have a great day!", command=self.destroy,
                      font=("Roboto Medium", 14), height=40, fg_color="#2b2b2b", hover_color="#3a3a3a", border_width=1, border_color="gray")
        self.btn_close.pack(padx=250, fill="x")
        
        # Start data fetch
        threading.Thread(target=self.fetch_data, daemon=True).start()

    def fetch_data(self):
        try:
            weather = logic.get_tel_aviv_weather_forecast()
            word = logic.get_word_of_the_day()
            
            self.after(0, lambda: self.display_data(weather, word))
        except Exception as e:
            self.after(0, lambda: self.show_error(str(e)))

    def display_data(self, weather_data, word_data):
        self.loading_label.destroy()
        
        if not weather_data: weather_data = {}

        # --- Top Left: Morning ---
        self.create_weather_card(
            0, 0,
            "Morning (06:00 - 12:00)", 
            weather_data.get("Morning (06:00 - 12:00)"), 
            "#FFC107" # Amber
        )
        
        # --- Top Right: Afternoon ---
        self.create_weather_card(
            0, 1,
            "Afternoon (12:00 - 18:00)", 
            weather_data.get("Afternoon (12:00 - 18:00)"), 
            "#2196F3" # Blue
        )
        
        # --- Bottom Left: Evening ---
        self.create_weather_card(
            1, 0,
            "Evening (18:00 - 00:00)", 
            weather_data.get("Evening (18:00 - 00:00)"), 
            "#AB47BC" # Light Purple
        )
        
        # --- Bottom Right: Word of the Day ---
        self.create_word_card(1, 1, word_data)

    def create_weather_card(self, row, col, title, data, color):
        # Increased corner radius and width to help rendering
        card = ctk.CTkFrame(self.main_content, fg_color="#2b2b2b", corner_radius=15, border_color=color, border_width=2)
        card.grid(row=row, column=col, sticky="nsew", padx=10, pady=10)
        
        ctk.CTkLabel(card, text=title, font=("Roboto Medium", 15), text_color=color).pack(pady=(15, 5))
        
        if not data or isinstance(data, str):
            text = data if isinstance(data, str) else "No Data"
            ctk.CTkLabel(card, text=text, text_color="gray").pack(expand=True)
            return
            
        data_frame = ctk.CTkFrame(card, fg_color="transparent")
        data_frame.pack(fill="x", padx=20)
        data_frame.grid_columnconfigure(1, weight=1)
        
        self.add_row(data_frame, 0, "Weather:", data['Weather'])
        self.add_row(data_frame, 1, "Temp:", f"{data['Temp Range']}")
        self.add_row(data_frame, 2, "Humidity:", data['Humidity'])
        
        rec_label = ctk.CTkLabel(card, text=f"💡 {data['Dress Code']}", font=("Roboto", 15), 
                                 wraplength=320, text_color="#d1d1d1")
        rec_label.pack(side="bottom", pady=20, padx=15)

    def create_word_card(self, row, col, word_data):
        card = ctk.CTkFrame(self.main_content, fg_color="#2b2b2b", corner_radius=15, border_color="#00E5FF", border_width=2)
        card.grid(row=row, column=col, sticky="nsew", padx=10, pady=10)
        
        # Removed grid_propagate(False) to let it size naturally with content
        # Padding should ensure borders are drawn
        
        ctk.CTkLabel(card, text="Word of the Day", font=("Roboto Medium", 15), text_color="#00E5FF").pack(pady=(15, 5))
        
        if "error" in word_data:
             ctk.CTkLabel(card, text="Fetch Error").pack(expand=True)
             return

        content = ctk.CTkFrame(card, fg_color="transparent")
        content.pack(expand=True, fill="both", padx=10, pady=5)
        
        # 1. Word
        ctk.CTkLabel(content, text=word_data.get('word', 'N/A'), font=("Merriweather", 26, "bold"), text_color="white").pack(pady=(5, 5))
        
        # 2. Pronunciation
        pron = word_data.get('pronunciation', '')
        if pron:
             ctk.CTkLabel(content, text=pron, font=("Roboto", 14, "italic"), text_color="gray").pack(pady=(0, 2))
        
        # 3. Type
        w_type = word_data.get('type', 'N/A')
        if w_type:
            ctk.CTkLabel(content, text=w_type, font=("Roboto", 13, "bold"), text_color="#888888").pack(pady=(0, 8))
        
        # 4. Definition
        defn = word_data.get('definition', 'N/A')
        if len(defn) > 120: defn = defn[:117] + "..."
        ctk.CTkLabel(content, text=defn, font=("Georgia", 16), wraplength=340).pack()

    def add_row(self, parent, row, label, value):
        ctk.CTkLabel(parent, text=label, font=("Roboto", 12, "bold"), text_color="gray", anchor="w").grid(row=row, column=0, sticky="w", pady=3)
        ctk.CTkLabel(parent, text=value, font=("Roboto", 12), anchor="w").grid(row=row, column=1, sticky="w", padx=10, pady=3)

    def show_error(self, message):
        self.loading_label.configure(text=f"Error: {message}")

if __name__ == "__main__":
    app = DailyBriefingApp()
    app.mainloop()
