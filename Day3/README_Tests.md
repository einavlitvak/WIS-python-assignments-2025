# SafeSound Testing Documentation

This project uses **pytest** to ensure the reliability of both the business logic and the user interface. The tests are split into two files to separate concerns.

## How to Run Tests

From the `Day3` directory, run:

```bash
.\run_tests.bat
```
*(This script ensures the correct virtual environment `Python_course_env` is used)*

---

## 1. Logic Tests (`test_logic.py`)
These tests verify the core mathematical rules and safety thresholds defined in `SafeSound_Logic.py`.

| Test Name | What it Validates |
| :--- | :--- |
| **`test_single_safe_wave`** | **Baseline Safety**: Verifies that a standard, low-volume sound (Amplitude 0.5, 440Hz) is correctly marked as **SAFE** for all species (Human, Dog, Cat). |
| **`test_unsafe_amplitude_human`** | **Loudness Thresholds**: Verifies that a sound exceeding the Human threshold (Amplitude 1.2 > 1.0) is correctly flagged as **UNSAFE** with a specific warning message. |
| **`test_species_hearing_ranges`** | **Frequency Hearing Ranges**: Verifies species-specific hearing capabilities. A 30,000 Hz sound should be:<br>• **Silent** (Not present) for Humans (Max 20kHz)<br>• **Audible** for Dogs (Max 45kHz)<br>• **Audible** for Cats (Max 85kHz) |
| **`test_sensitive_frequencies`** | **Sensitivity Zones**: checks strict rules for sensitive ranges. For Humans (1000-4000Hz), the safety threshold drops to 0.5. This test confirms that an amplitude of 0.6 (usually safe) is marked **UNSAFE** if the frequency is 3000Hz. |
| **`test_combined_waves_interference`** | **Wave Construction**: Verifies that two "safe" waves (Amp 0.6) can combine to form an **UNSAFE** wave (Amp 1.2) due to constructive interference, ensuring the math correctly sums the waveforms. |

---

## 2. GUI Tests (`test_gui.py`)
These tests verify the functionality of the user interface actions in `SafeSound_GUI.py` without requiring a physical screen (headless testing).

| Test Name | What it Validates |
| :--- | :--- |
| **`test_initial_state`** | **Clean Start**: Ensures the application launches with an empty list of waves and valid default state. |
| **`test_add_wave_via_gui`** | **Wiring & Integration**: Simulates a user typing "0.5" and "440" and clicking "Add Wave". Verifies that:<br>1. The underlying logic receives the correct numbers.<br>2. The UI Listbox updates to show the new wave.<br>3. The input fields are cleared after adding. |
| **`test_add_wave_invalid_input`** | **Error Handling**: Simulates typing text ("NotANumber") instead of numbers. Verifies that the app **raises an error message** (mocked) and **does not** crash or add corrupt data. |
| **`test_clear_waves`** | **Reset Functionality**: Simulates clicking "Clear All". Verifies that all waves are removed from both the logic engine and the visual list. |

## Promt used
Create a new program that will test both the logic and the GUI programs. Use pytest to run it. Explain what the test do.

add another readme for the tests, explain what each of them is for like you did before with the charts. 