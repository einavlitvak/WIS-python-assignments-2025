
import pytest
import tkinter as tk
from SafeSound_GUI import SafeSoundGUI
from SafeSound_Logic import SineWave

@pytest.fixture(scope="module")
def root_window():
    """Fixture to create a root window hidden from view."""
    root = tk.Tk()
    root.withdraw() # Hide it
    yield root
    root.destroy()

@pytest.fixture
def app(root_window):
    """Fixture to provide a fresh app instance for each test."""
    # We need to recreate the GUI frame for each test to ensure clean state
    # But we reuse the root to avoid multiple Tk instances error
    for widget in root_window.winfo_children():
        widget.destroy()
        
    return SafeSoundGUI(root_window)

def test_initial_state(app):
    """Test that the app starts with no waves."""
    assert len(app.analyzer.waves) == 0
    # Check listbox is empty (size 0)
    assert app.waves_listbox.size() == 0

def test_add_wave_via_gui(app):
    """Test adding a wave using the GUI methods."""
    # Simulate user input
    app.amplitude_var.set("0.5")
    app.frequency_var.set("440")
    app.phase_var.set("0")
    app.duration_var.set("1.0")
    
    # Trigger the add button callback
    app.add_wave()
    
    # Verify logic state
    assert len(app.analyzer.waves) == 1
    wave = app.analyzer.waves[0]
    assert wave.amplitude == 0.5
    assert wave.frequency == 440.0
    
    # Verify UI state (Listbox update)
    assert app.waves_listbox.size() == 1
    list_text = app.waves_listbox.get(0)
    assert "A=0.50" in list_text
    assert "F=440.0Hz" in list_text
    
    # Verify fields cleared
    assert app.amplitude_var.get() == ""
    assert app.frequency_var.get() == ""

def test_add_wave_invalid_input(app, monkeypatch):
    """Test that invalid input doesn't crash app or add wave."""
    app.amplitude_var.set("NotANumber")
    app.frequency_var.set("440")
    app.duration_var.set("1.0")
    
    # Mock messagebox so we don't get a popup blocking the test
    called = False
    def mock_showerror(title, message):
        nonlocal called
        called = True
        
    monkeypatch.setattr(tk.messagebox, 'showerror', mock_showerror)
    
    app.add_wave()
    assert called, "Error message should have been shown"
    assert len(app.analyzer.waves) == 0, "Should not add invalid wave"

def test_clear_waves(app):
    """Test the clear functionality."""
    # Add a dummy wave first
    app.analyzer.add_wave(SineWave(1, 440))
    app.waves_listbox.insert(tk.END, "Dummy Wave")
    app.results_text.insert(1.0, "Old Report")
    
    app.clear_waves()
    
    assert len(app.analyzer.waves) == 0
    assert app.waves_listbox.size() == 0
    # Check text area is empty (returns single newline)
    assert app.results_text.get(1.0, tk.END) == "\n"


