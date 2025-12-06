"""
Sound Safety Analyzer - Logic Module
This module contains the business logic for the Sound Safety Analyzer program.
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
    
    def get_safety_report(self) -> str:
        """Get a comprehensive safety report as a string."""
        results = self.analyze_safety()
        
        report = "=" * 60 + "\n"
        report += "SOUND SAFETY ANALYSIS REPORT\n"
        report += "=" * 60 + "\n\n"
        
        if not results:
            return report + "No waves to analyze.\n"
        
        # Wave summary
        report += f"WAVE SUMMARY:\n"
        report += f"Number of waves: {len(self.waves)}\n"
        for i, wave in enumerate(self.waves, 1):
            report += f"  Wave {i}: Amplitude={wave.amplitude:.2f}, "
            report += f"Frequency={wave.frequency:.1f} Hz, "
            report += f"Phase={wave.phase_shift:.2f} rad, "
            report += f"Duration={wave.duration:.1f}s\n"
        
        # Safety analysis for each species
        for species, result in results.items():
            report += f"\n{species.upper()} SAFETY:\n"
            status = "✓ SAFE" if result['safe'] else "⚠ POTENTIALLY DANGEROUS"
            report += f"  Status: {status}\n"
            report += f"  Max Amplitude: {result['max_amplitude']:.3f}\n"
            report += f"  RMS Amplitude: {result['rms_amplitude']:.3f}\n"
            
            if result['frequencies_present']:
                audible_freqs = result['frequencies_present']
                report += f"  Audible frequencies: {[f'{f:.1f}' for f in audible_freqs]} Hz\n"
            else:
                report += "  No audible frequencies detected\n"
            
            if result['warnings']:
                report += "  Warnings:\n"
                for warning in result['warnings']:
                    report += f"    - {warning}\n"
        
        report += "\n" + "=" * 60
        return report
    
    def plot_waveform(self, figure=None):
        """Plot the combined waveform."""
        time_array, combined_wave = self.combine_waves()
        
        if len(combined_wave) == 0:
            return None
        
        if figure is None:
            figure = plt.figure(figsize=(12, 8))
        else:
            figure.clear()
        
        # Plot individual waves
        ax1 = figure.add_subplot(2, 1, 1)
        for i, wave in enumerate(self.waves):
            wave_samples = int(44100 * wave.duration)
            wave_time = time_array[:wave_samples]
            wave_values = wave.generate(wave_time)
            ax1.plot(wave_time, wave_values, alpha=0.7, 
                    label=f'Wave {i+1}: {wave.frequency:.1f} Hz')
        
        ax1.set_title('Individual Sine Waves')
        ax1.set_xlabel('Time (seconds)')
        ax1.set_ylabel('Amplitude')
        ax1.legend()
        ax1.grid(True, alpha=0.3)
        
        # Plot combined wave
        ax2 = figure.add_subplot(2, 1, 2)
        ax2.plot(time_array, combined_wave, 'b-', linewidth=1.5)
        ax2.set_title('Combined Waveform')
        ax2.set_xlabel('Time (seconds)')
        ax2.set_ylabel('Amplitude')
        ax2.grid(True, alpha=0.3)
        
        # Add safety threshold lines
        for species, threshold in self.SAFE_AMPLITUDE_THRESHOLDS.items():
            ax2.axhline(y=threshold, color='red', linestyle='--', alpha=0.7, 
                       label=f'{species.capitalize()} threshold')
            ax2.axhline(y=-threshold, color='red', linestyle='--', alpha=0.7)
        
        ax2.legend()
        figure.tight_layout()
        
        return figure
