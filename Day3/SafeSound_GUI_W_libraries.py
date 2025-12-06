"""
SafeSound_GUI_W_libraries.py
Improved version of SafeSound GUI using:
- customtkinter (Modern UI)
- numpy (Business logic vectorization)
- pydantic (Input validation)
- simpleaudio (Sound playback)
- matplotlib (Plotting)
"""

import customtkinter as ctk
import tkinter as tk  # For some constants and messageboxes
from tkinter import messagebox
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np
import simpleaudio as sa
import math
from typing import List, Tuple, Dict, Optional
from pydantic import BaseModel, Field, ValidationError

# --- LOGIC (Integrated directly or imported, we will integrate to use numpy fully) ---

class SineWaveModel(BaseModel):
    """Pydantic model for input validation."""
    amplitude: float = Field(..., gt=0, description="Amplitude must be positive")
    frequency: float = Field(..., gt=0, description="Frequency must be positive")
    phase_shift: float = Field(default=0.0)
    duration: float = Field(..., gt=0, description="Duration must be positive")

class SineWave:
    def __init__(self, amplitude: float, frequency: float, phase_shift: float = 0, duration: float = 1.0):
        self.amplitude = amplitude
        self.frequency = frequency
        self.phase_shift = phase_shift
        self.duration = duration

    def generate(self, time_array: np.ndarray) -> np.ndarray:
        return self.amplitude * np.sin(2 * np.pi * self.frequency * time_array + self.phase_shift)

class SoundSafetyAnalyzer:
    HEARING_RANGES = {'human': (20, 20000), 'dog': (67, 45000), 'cat': (48, 85000)}
    SAFE_THRESHOLDS = {'human': 1.0, 'dog': 0.8, 'cat': 0.7}
    SENSITIVE_FREQS = {
        'human': [(1000, 4000)],
        'dog': [(8000, 16000)],
        'cat': [(2000, 6000), (16000, 32000)]
    }

    def __init__(self):
        self.waves: List[SineWave] = []

    def add_wave(self, wave: SineWave):
        self.waves.append(wave)

    def combine_waves(self, sample_rate: int = 44100) -> Tuple[np.ndarray, np.ndarray]:
        if not self.waves:
            return np.array([]), np.array([])
        
        max_duration = max(w.duration for w in self.waves)
        num_samples = int(sample_rate * max_duration)
        time_array = np.linspace(0, max_duration, num_samples, endpoint=False)
        combined_wave = np.zeros(num_samples)

        for wave in self.waves:
            wave_samples = int(sample_rate * wave.duration)
            if wave_samples > 0:
                t_slice = time_array[:wave_samples]
                combined_wave[:wave_samples] += wave.generate(t_slice)
        
        return time_array, combined_wave

    def analyze_safety(self) -> Dict[str, Dict]:
        _, combined = self.combine_waves()
        if len(combined) == 0:
            return {}

        max_amp = np.max(np.abs(combined))
        rms_amp = np.sqrt(np.mean(combined**2))
        results = {}

        for species in ['human', 'dog', 'cat']:
            res = {
                'safe': True, 
                'warnings': [], 
                'max_amplitude': float(max_amp), 
                'rms_amplitude': float(rms_amp),
                'frequencies_present': []
            }
            
            threshold = self.SAFE_THRESHOLDS[species]
            if max_amp > threshold:
                res['safe'] = False
                res['warnings'].append(f"High Amplitude: {max_amp:.2f} > {threshold}")

            for w in self.waves:
                if self.HEARING_RANGES[species][0] <= w.frequency <= self.HEARING_RANGES[species][1]:
                    res['frequencies_present'].append(w.frequency)
                    for (low, high) in self.SENSITIVE_FREQS[species]:
                        if low <= w.frequency <= high and w.amplitude > threshold * 0.5:
                            res['safe'] = False
                            res['warnings'].append(f"Sensitive Freq Warning: {w.frequency}Hz at Amp {w.amplitude}")
            results[species] = res
        return results

    def get_safety_report_text(self) -> str:
        data = self.analyze_safety()
        if not data: return "No data."
        
        report = []
        for species, info in data.items():
            status = "SAFE" if info['safe'] else "UNSAFE"
            report.append(f"{species.upper()}: {status}")
            if info['warnings']:
                report.append(f"  ⚠ {', '.join(info['warnings'])}")
        return "\n".join(report)

# --- GUI ---

ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")

class SafeSoundApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("SafeSound Pro")
        self.geometry("1000x800")
        
        self.analyzer = SoundSafetyAnalyzer()
        self.setup_ui()

    def setup_ui(self):
        # Layout: Left column (Inputs), Right column (Plot & Results)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # --- Sidebar ---
        self.sidebar = ctk.CTkFrame(self, width=300, corner_radius=0)
        self.sidebar.grid(row=0, column=0, sticky="nsew", padx=0, pady=0)
        
        ctk.CTkLabel(self.sidebar, text="SafeSound Pro", font=ctk.CTkFont(size=20, weight="bold")).pack(pady=20)

        # Inputs
        self.amp_var = ctk.StringVar()
        self.freq_var = ctk.StringVar()
        self.phase_var = ctk.StringVar(value="0")
        self.dur_var = ctk.StringVar()

        self.create_input(self.sidebar, "Amplitude:", self.amp_var)
        self.create_input(self.sidebar, "Frequency (Hz):", self.freq_var)
        self.create_input(self.sidebar, "Phase (rad):", self.phase_var)
        self.create_input(self.sidebar, "Duration (s):", self.dur_var)

        ctk.CTkButton(self.sidebar, text="Add Wave", command=self.add_wave).pack(pady=10, padx=20)
        ctk.CTkButton(self.sidebar, text="Clear All", command=self.clear_waves, fg_color="red", hover_color="darkred").pack(pady=5, padx=20)
        
        ctk.CTkLabel(self.sidebar, text="Waves List:", anchor="w").pack(fill="x", padx=20, pady=(20,0))
        self.waves_scroll = ctk.CTkTextbox(self.sidebar, height=150)
        self.waves_scroll.pack(fill="x", padx=20, pady=5)
        self.waves_scroll.configure(state="disabled")

        # --- Main Area ---
        self.main_area = ctk.CTkFrame(self)
        self.main_area.grid(row=0, column=1, sticky="nsew", padx=20, pady=20)
        
        # Plot Frame
        self.plot_frame = ctk.CTkFrame(self.main_area)
        self.plot_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Initial empty plot
        self.figure = Figure(figsize=(5, 4), dpi=100)
        self.ax = self.figure.add_subplot(111)
        self.ax.set_title("Waveform")
        self.ax.grid(True)
        self.canvas = FigureCanvasTkAgg(self.figure, master=self.plot_frame)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(fill="both", expand=True)

        # Results & Actions
        self.results_label = ctk.CTkLabel(self.main_area, text="Results will appear here...", justify="left", font=ctk.CTkFont(family="Consolas"))
        self.results_label.pack(fill="x", padx=10, pady=10)

        ctk.CTkButton(self.main_area, text="Play Sound", command=self.play_sound, font=ctk.CTkFont(size=14, weight="bold")).pack(pady=20)

    def create_input(self, parent, label, var):
        frame = ctk.CTkFrame(parent, fg_color="transparent")
        frame.pack(fill="x", padx=20, pady=5)
        ctk.CTkLabel(frame, text=label, anchor="w").pack(fill="x")
        ctk.CTkEntry(frame, textvariable=var).pack(fill="x")

    def add_wave(self):
        try:
            # Pydantic Validation
            model = SineWaveModel(
                amplitude=float(self.amp_var.get() or 0),
                frequency=float(self.freq_var.get() or 0),
                phase_shift=float(self.phase_var.get() or 0),
                duration=float(self.dur_var.get() or 0)
            )
            
            wave = SineWave(model.amplitude, model.frequency, model.phase_shift, model.duration)
            self.analyzer.add_wave(wave)
            self.update_ui()
            
            # Clear inputs
            self.amp_var.set("")
            self.freq_var.set("")
            self.dur_var.set("")
            
        except ValidationError as e:
            # Nice error formatting from Pydantic
            errors = "\n".join([err['msg'] for err in e.errors()])
            tk.messagebox.showerror("Validation Error", errors)
        except ValueError:
            tk.messagebox.showerror("Input Error", "Please enter valid numbers.")

    def clear_waves(self):
        self.analyzer = SoundSafetyAnalyzer()
        self.update_ui()

    def update_ui(self):
        # Update text list
        self.waves_scroll.configure(state="normal")
        self.waves_scroll.delete("1.0", "end")
        for i, w in enumerate(self.analyzer.waves, 1):
            self.waves_scroll.insert("end", f"{i}. {w.frequency}Hz @ {w.amplitude}\n")
        self.waves_scroll.configure(state="disabled")
        
        # Update results
        report = self.analyzer.get_safety_report_text()
        self.results_label.configure(text=report)
        
        # Update plot
        self.ax.clear()
        t, y = self.analyzer.combine_waves()
        if len(t) > 0:
            self.ax.plot(t, y)
            self.ax.set_ylim(min(y)*1.2 - 0.1, max(y)*1.2 + 0.1)
        self.ax.grid(True)
        self.ax.set_title("Combined Waveform")
        self.canvas.draw()

    def play_sound(self):
        t, y = self.analyzer.combine_waves()
        if len(y) == 0:
            tk.messagebox.showinfo("Info", "No waves to play.")
            return

        safety = self.analyzer.analyze_safety()
        unsafe_species = [s for s, res in safety.items() if not res['safe']]

        if unsafe_species:
            msg = f"WARNING! This sound is NOT SAFE for: {', '.join(unsafe_species)}.\n\nDo you still want to play it?"
            if not tk.messagebox.askyesno("Safety Warning", msg, icon='warning'):
                return

        # Normalize audio for playback (16-bit PCM)
        # Avoid clipping
        max_val = np.max(np.abs(y))
        if max_val > 0:
            norm_y = y / max_val * 32767
            audio_data = norm_y.astype(np.int16)
            play_obj = sa.play_buffer(audio_data, 1, 2, 44100)
            play_obj.wait_done()

if __name__ == "__main__":
    app = SafeSoundApp()
    app.mainloop()
