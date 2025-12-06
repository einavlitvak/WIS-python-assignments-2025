"""
Sound Safety Analyzer - GUI Version
A program that combines multiple sine waves and analyzes their safety for humans, dogs, and cats.
"""

import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
from SafeSound_Logic import SineWave, SoundSafetyAnalyzer

class SafeSoundGUI:
    """GUI application for the Sound Safety Analyzer."""
    
    def __init__(self, root):
        self.root = root
        self.root.title("SafeSound - Sound Safety Analyzer")
        self.root.geometry("800x900")
        
        self.analyzer = SoundSafetyAnalyzer()
        self.waves_data = []
        
        self.setup_gui()
    
    def setup_gui(self):
        """Set up the GUI components."""
        # Main frame
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Title
        title_label = ttk.Label(main_frame, text="SafeSound - Sound Safety Analyzer", 
                                font=("Arial", 16, "bold"))
        title_label.grid(row=0, column=0, columnspan=4, pady=(0, 20))
        
        # Wave input section
        input_frame = ttk.LabelFrame(main_frame, text="Add Sine Wave", padding="10")
        input_frame.grid(row=1, column=0, columnspan=4, sticky=(tk.W, tk.E), pady=(0, 10))
        
        # Input fields
        ttk.Label(input_frame, text="Amplitude:").grid(row=0, column=0, sticky=tk.W, padx=(0, 5))
        self.amplitude_var = tk.StringVar()
        ttk.Entry(input_frame, textvariable=self.amplitude_var, width=15).grid(row=0, column=1, padx=(0, 10))
        
        ttk.Label(input_frame, text="Frequency (Hz):").grid(row=0, column=2, sticky=tk.W, padx=(0, 5))
        self.frequency_var = tk.StringVar()
        ttk.Entry(input_frame, textvariable=self.frequency_var, width=15).grid(row=0, column=3, padx=(0, 10))
        
        ttk.Label(input_frame, text="Phase Shift (rad):").grid(row=1, column=0, sticky=tk.W, padx=(0, 5))
        self.phase_var = tk.StringVar(value="0")
        ttk.Entry(input_frame, textvariable=self.phase_var, width=15).grid(row=1, column=1, padx=(0, 10))
        
        ttk.Label(input_frame, text="Duration (sec):").grid(row=1, column=2, sticky=tk.W, padx=(0, 5))
        self.duration_var = tk.StringVar()
        ttk.Entry(input_frame, textvariable=self.duration_var, width=15).grid(row=1, column=3, padx=(0, 10))
        
        # Buttons
        button_frame = ttk.Frame(input_frame)
        button_frame.grid(row=2, column=0, columnspan=4, pady=(10, 0))
        
        ttk.Button(button_frame, text="Add Wave", command=self.add_wave).pack(side=tk.LEFT, padx=(0, 10))
        ttk.Button(button_frame, text="Clear All", command=self.clear_waves).pack(side=tk.LEFT, padx=(0, 10))
        ttk.Button(button_frame, text="Analyze Safety", command=self.analyze_safety).pack(side=tk.LEFT, padx=(0, 10))
        ttk.Button(button_frame, text="Show Plot", command=self.show_plot).pack(side=tk.LEFT)
        
        # Waves list
        waves_frame = ttk.LabelFrame(main_frame, text="Current Waves", padding="10")
        waves_frame.grid(row=2, column=0, columnspan=4, sticky=(tk.W, tk.E), pady=(0, 10))
        
        self.waves_listbox = tk.Listbox(waves_frame, height=6)
        self.waves_listbox.pack(fill=tk.BOTH, expand=True)
        
        # Results area
        results_frame = ttk.LabelFrame(main_frame, text="Safety Analysis Results", padding="10")
        results_frame.grid(row=3, column=0, columnspan=4, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0, 10))
        
        self.results_text = scrolledtext.ScrolledText(results_frame, height=15, width=80)
        self.results_text.pack(fill=tk.BOTH, expand=True)
        
        # Configure grid weights
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(0, weight=1)
        main_frame.rowconfigure(3, weight=1)
        results_frame.columnconfigure(0, weight=1)
        results_frame.rowconfigure(0, weight=1)
    
    def add_wave(self):
        """Add a wave from the input fields."""
        try:
            amplitude = float(self.amplitude_var.get())
            frequency = float(self.frequency_var.get())
            phase_shift = float(self.phase_var.get()) if self.phase_var.get() else 0.0
            duration = float(self.duration_var.get())
            
            wave = SineWave(amplitude, frequency, phase_shift, duration)
            self.analyzer.add_wave(wave)
            
            # Add to display list
            wave_text = f"Wave {len(self.analyzer.waves)}: A={amplitude:.2f}, F={frequency:.1f}Hz, P={phase_shift:.2f}rad, D={duration:.1f}s"
            self.waves_listbox.insert(tk.END, wave_text)
            
            # Clear input fields
            self.amplitude_var.set("")
            self.frequency_var.set("")
            self.phase_var.set("0")
            self.duration_var.set("")
            
        except ValueError:
            messagebox.showerror("Input Error", "Please enter valid numeric values for all fields.")
    
    def clear_waves(self):
        """Clear all waves."""
        self.analyzer = SoundSafetyAnalyzer()
        self.waves_listbox.delete(0, tk.END)
        self.results_text.delete(1.0, tk.END)
    
    def analyze_safety(self):
        """Analyze the safety and display results."""
        if len(self.analyzer.waves) == 0:
            messagebox.showwarning("No Waves", "Please add at least one wave before analyzing.")
            return
        
        report = self.analyzer.get_safety_report()
        self.results_text.delete(1.0, tk.END)
        self.results_text.insert(1.0, report)
    
    def show_plot(self):
        """Show the waveform plot in a new window."""
        if len(self.analyzer.waves) == 0:
            messagebox.showwarning("No Waves", "Please add at least one wave before plotting.")
            return
        
        # Create plot window
        plot_window = tk.Toplevel(self.root)
        plot_window.title("Waveform Plot")
        plot_window.geometry("800x600")
        
        # Create matplotlib figure
        fig = plt.Figure(figsize=(10, 6))
        self.analyzer.plot_waveform(fig)
        
        # Embed plot in tkinter
        canvas = FigureCanvasTkAgg(fig, plot_window)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)


def main():
    """Main function to run the GUI application."""
    root = tk.Tk()
    app = SafeSoundGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()
