
import pytest
import numpy as np
from SafeSound_Logic import SineWave, SoundSafetyAnalyzer

@pytest.fixture
def analyzer():
    """Fixture to provide a fresh analyzer for each test."""
    return SoundSafetyAnalyzer()

def test_single_safe_wave(analyzer):
    """Test a simple wave that should be safe for everyone."""
    # Amplitude 0.5 is below all thresholds (0.7 is the lowest for cats)
    # 440Hz is audible for all but not in sensitive ranges
    wave = SineWave(amplitude=0.5, frequency=440, duration=1.0)
    analyzer.add_wave(wave)
    results = analyzer.analyze_safety()
    
    for species in ['human', 'dog', 'cat']:
        assert results[species]['safe'], f"Should be safe for {species}"
        assert len(results[species]['warnings']) == 0

def test_unsafe_amplitude_human(analyzer):
    """Test amplitude that exceeds human threshold."""
    # Threshold is 1.0
    wave = SineWave(amplitude=1.2, frequency=440)
    analyzer.add_wave(wave)
    results = analyzer.analyze_safety()
    
    assert not results['human']['safe']
    assert any("Amplitude too high" in w for w in results['human']['warnings'])

def test_species_hearing_ranges(analyzer):
    """Test frequencies audible to some species but not others."""
    # 30,000 Hz: Ultrasonic for humans (max 20k), audible for dogs/cats
    wave = SineWave(amplitude=0.5, frequency=30000)
    analyzer.add_wave(wave)
    results = analyzer.analyze_safety()
    
    # Check Human
    assert 30000 not in results['human']['frequencies_present']
    
    # Check Dog (Max 45k)
    assert 30000 in results['dog']['frequencies_present']
    
    # Check Cat (Max 85k)
    assert 30000 in results['cat']['frequencies_present']

def test_sensitive_frequencies(analyzer):
    """Test frequency in sensitive range triggering warning at lower amplitude."""
    # Human sensitive range: 1000-4000 Hz. 
    # Logic says if in sensitive range, threshold is halved.
    # Human base threshold = 1.0. Sensitive threshold = 0.5.
    
    # Case 1: Safe (0.4 amp)
    analyzer.waves = [] # Reset
    analyzer.add_wave(SineWave(amplitude=0.4, frequency=3000))
    results = analyzer.analyze_safety()
    assert results['human']['safe']
    
    # Case 2: Unsafe (0.6 amp) - Safe globally but unsafe for sensitive range
    analyzer.waves = [] # Reset
    analyzer.add_wave(SineWave(amplitude=0.6, frequency=3000))
    results = analyzer.analyze_safety()
    assert not results['human']['safe']
    assert any("sensitive frequency" in w for w in results['human']['warnings'])

def test_combined_waves_interference(analyzer):
    """Test that two safe waves can combine to be unsafe."""
    # Two waves with amp 0.6. Individually safe (threshold 1.0).
    # In phase (shift 0), they verify constructive interference => 1.2
    wave1 = SineWave(amplitude=0.6, frequency=440, phase_shift=0)
    wave2 = SineWave(amplitude=0.6, frequency=440, phase_shift=0)
    
    analyzer.add_wave(wave1)
    analyzer.add_wave(wave2)
    
    results = analyzer.analyze_safety()
    
    # Max amplitude should be around 1.2
    assert results['human']['max_amplitude'] == pytest.approx(1.2, abs=0.01)
    assert not results['human']['safe']


