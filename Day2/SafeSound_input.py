"""
Sound Safety Analyzer
A program that combines multiple sine waves and analyzes their safety for humans, dogs, and cats.
"""

import numpy as np
import matplotlib.pyplot as plt
from typing import List, Tuple, Dict
import math

class SineWave:
    """Represents a single sine wave with customizable parameters."""
    
    def __init__(self, amplitude: float, frequency: float, phase_shift: float = 0, duration: float = 1.0):
        """
        Initialize a sine wave.
        
        Args:
            amplitude: Amplitude multiplier (affects volume/intensity)
            frequency: Frequency in Hz (cycles per second)
            phase_shift: Phase shift in radians
            duration: Duration of the wave in seconds
        """
        self.amplitude = amplitude
        self.frequency = frequency
        self.phase_shift = phase_shift
        self.duration = duration
    
    def generate(self, time_array: np.ndarray) -> np.ndarray:
        """Generate the sine wave values for given time points."""
        return self.amplitude * np.sin(2 * np.pi * self.frequency * time_array + self.phase_shift)

class SoundSafetyAnalyzer:
    """Analyzes sound safety for different species."""
    
    # Hearing frequency ranges (Hz) for different species
    HEARING_RANGES = {
        'human': (20, 20000),
        'dog': (67, 45000),
        'cat': (48, 85000)
    }
    
    # Safe amplitude thresholds (relative units)
    # These are simplified thresholds - in reality, safety depends on frequency and exposure time
    SAFE_AMPLITUDE_THRESHOLDS = {
        'human': 1.0,     # Reference safe level
        'dog': 0.8,       # Dogs are more sensitive
        'cat': 0.7        # Cats are most sensitive
    }
    
    # Frequency-specific danger zones (frequencies that are particularly sensitive)
    SENSITIVE_FREQUENCIES = {
        'human': [(1000, 4000)],      # Most sensitive hearing range
        'dog': [(8000, 16000)],       # Ultrasonic sensitivity
        'cat': [(2000, 6000), (16000, 32000)]  # Multiple sensitive ranges
    }
    
    def __init__(self):
        self.waves = []
    
    def add_wave(self, wave: SineWave):
        """Add a sine wave to the collection."""
        self.waves.append(wave)
    
    def combine_waves(self, sample_rate: int = 44100) -> Tuple[np.ndarray, np.ndarray]:
        """
        Combine all sine waves into a single waveform.
        
        Args:
            sample_rate: Sampling rate in Hz
            
        Returns:
            Tuple of (time_array, combined_amplitude_array)
        """
        if not self.waves:
            return np.array([]), np.array([])
        
        # Find the maximum duration
        max_duration = max(wave.duration for wave in self.waves)
        
        # Create time array
        time_array = np.linspace(0, max_duration, int(sample_rate * max_duration))
        
        # Initialize combined wave
        combined_wave = np.zeros_like(time_array)
        
        # Add each wave to the combination
        for wave in self.waves:
            # Only add the wave for its specified duration
            wave_samples = int(sample_rate * wave.duration)
            if wave_samples <= len(time_array):
                wave_time = time_array[:wave_samples]
                wave_values = wave.generate(wave_time)
                combined_wave[:wave_samples] += wave_values
        
        return time_array, combined_wave
    
    def analyze_safety(self) -> Dict[str, Dict]:
        """
        Analyze the safety of the combined sound for each species.
        
        Returns:
            Dictionary with safety analysis for each species
        """
        time_array, combined_wave = self.combine_waves()
        
        if len(combined_wave) == 0:
            return {}
        
        # Calculate overall amplitude metrics
        max_amplitude = np.max(np.abs(combined_wave))
        rms_amplitude = np.sqrt(np.mean(combined_wave**2))
        
        results = {}
        
        for species in ['human', 'dog', 'cat']:
            species_result = {
                'safe': True,
                'warnings': [],
                'max_amplitude': max_amplitude,
                'rms_amplitude': rms_amplitude,
                'frequencies_present': []
            }
            
            # Check amplitude safety
            threshold = self.SAFE_AMPLITUDE_THRESHOLDS[species]
            if max_amplitude > threshold:
                species_result['safe'] = False
                species_result['warnings'].append(
                    f"Amplitude too high: {max_amplitude:.2f} > {threshold:.2f} (safe limit)"
                )
            
            # Analyze frequency content
            for wave in self.waves:
                freq = wave.frequency
                amp = wave.amplitude
                
                # Check if frequency is in audible range
                min_freq, max_freq = self.HEARING_RANGES[species]
                if min_freq <= freq <= max_freq:
                    species_result['frequencies_present'].append(freq)
                    
                    # Check if frequency is in sensitive range
                    for sensitive_range in self.SENSITIVE_FREQUENCIES[species]:
                        if sensitive_range[0] <= freq <= sensitive_range[1]:
                            if amp > threshold * 0.5:  # More strict for sensitive frequencies
                                species_result['safe'] = False
                                species_result['warnings'].append(
                                    f"High amplitude ({amp:.2f}) at sensitive frequency {freq:.1f} Hz"
                                )
            
            results[species] = species_result
        
        return results
    
    def print_safety_report(self):
        """Print a comprehensive safety report."""
        results = self.analyze_safety()
        
        print("=" * 60)
        print("SOUND SAFETY ANALYSIS REPORT")
        print("=" * 60)
        
        if not results:
            print("No waves to analyze.")
            return
        
        # Print wave summary
        print(f"\nWAVE SUMMARY:")
        print(f"Number of waves: {len(self.waves)}")
        for i, wave in enumerate(self.waves, 1):
            print(f"  Wave {i}: Amplitude={wave.amplitude:.2f}, "
                  f"Frequency={wave.frequency:.1f} Hz, "
                  f"Phase={wave.phase_shift:.2f} rad, "
                  f"Duration={wave.duration:.1f}s")
        
        # Print safety analysis for each species
        for species, result in results.items():
            print(f"\n{species.upper()} SAFETY:")
            status = "✓ SAFE" if result['safe'] else "⚠ POTENTIALLY DANGEROUS"
            print(f"  Status: {status}")
            print(f"  Max Amplitude: {result['max_amplitude']:.3f}")
            print(f"  RMS Amplitude: {result['rms_amplitude']:.3f}")
            
            if result['frequencies_present']:
                audible_freqs = result['frequencies_present']
                print(f"  Audible frequencies: {[f'{f:.1f}' for f in audible_freqs]} Hz")
            else:
                print("  No audible frequencies detected")
            
            if result['warnings']:
                print("  Warnings:")
                for warning in result['warnings']:
                    print(f"    - {warning}")
        
        print("\n" + "=" * 60)
    
    def plot_waveform(self, show_plot: bool = True):
        """Plot the combined waveform."""
        time_array, combined_wave = self.combine_waves()
        
        if len(combined_wave) == 0:
            print("No waves to plot.")
            return
        
        plt.figure(figsize=(12, 8))
        
        # Plot individual waves
        plt.subplot(2, 1, 1)
        for i, wave in enumerate(self.waves):
            wave_samples = int(44100 * wave.duration)
            wave_time = time_array[:wave_samples]
            wave_values = wave.generate(wave_time)
            plt.plot(wave_time, wave_values, alpha=0.7, 
                    label=f'Wave {i+1}: {wave.frequency:.1f} Hz')
        
        plt.title('Individual Sine Waves')
        plt.xlabel('Time (seconds)')
        plt.ylabel('Amplitude')
        plt.legend()
        plt.grid(True, alpha=0.3)
        
        # Plot combined wave
        plt.subplot(2, 1, 2)
        plt.plot(time_array, combined_wave, 'b-', linewidth=1.5)
        plt.title('Combined Waveform')
        plt.xlabel('Time (seconds)')
        plt.ylabel('Amplitude')
        plt.grid(True, alpha=0.3)
        
        # Add safety threshold lines
        for species, threshold in self.SAFE_AMPLITUDE_THRESHOLDS.items():
            plt.axhline(y=threshold, color='red', linestyle='--', alpha=0.7, 
                       label=f'{species.capitalize()} threshold')
            plt.axhline(y=-threshold, color='red', linestyle='--', alpha=0.7)
        
        plt.legend()
        plt.tight_layout()
        
        if show_plot:
            plt.show()
        
        return plt.gcf()


def get_user_input():
    """Get sine wave parameters from user input."""
    analyzer = SoundSafetyAnalyzer()
    
    print("Sound Safety Analyzer")
    print("=" * 40)
    print("Enter sine wave parameters. Press Enter with empty input to finish.")
    print()
    
    wave_count = 0
    while True:
        wave_count += 1
        print(f"Wave {wave_count}:")
        
        try:
            # Get amplitude
            amp_input = input("  Amplitude (multiplier, e.g., 1.0): ").strip()
            if not amp_input:
                break
            amplitude = float(amp_input)
            
            # Get frequency
            freq_input = input("  Frequency in Hz (e.g., 440): ").strip()
            if not freq_input:
                break
            frequency = float(freq_input)
            
            # Get phase shift (optional)
            phase_input = input("  Phase shift in radians (optional, default 0): ").strip()
            phase_shift = float(phase_input) if phase_input else 0.0
            
            # Get duration
            duration_input = input("  Duration in seconds (e.g., 2.0): ").strip()
            if not duration_input:
                break
            duration = float(duration_input)
            
            # Create and add wave
            wave = SineWave(amplitude, frequency, phase_shift, duration)
            analyzer.add_wave(wave)
            print(f"  ✓ Added wave: {amplitude}*sin(2π*{frequency}*t + {phase_shift})")
            print()
            
        except ValueError:
            print("  Invalid input. Please enter numeric values.")
            wave_count -= 1
            continue
        except KeyboardInterrupt:
            print("\nExiting...")
            break
    
    return analyzer


def main():
    """Main program function."""
    print("Welcome to the Sound Safety Analyzer!")
    print("This program combines sine waves and checks their safety for humans, dogs, and cats.\n")
    
    # Get user input
    analyzer = get_user_input()
    
    if len(analyzer.waves) == 0:
        print("No waves entered. Exiting.")
        return
    
    # Analyze safety
    print("\nAnalyzing sound safety...")
    analyzer.print_safety_report()
    
    # Ask if user wants to see the plot
    try:
        plot_choice = input("\nWould you like to see a plot of the waveforms? (y/n): ").strip().lower()
        if plot_choice in ['y', 'yes']:
            analyzer.plot_waveform()
    except:
        pass  # Skip plotting if there's an issue


if __name__ == "__main__":
    main()