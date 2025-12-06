# SafeSound Pro: Advanced Sound Safety Analyzer

SafeSound Pro is a modern GUI application designed to synthesize, visualize, and analyze sound waves. Its primary purpose is to determine if a combination of sound waves is safe for Humans, Dogs, and Cats based on amplitude thresholds and frequency sensitivity.

## Promt used
are there any 3rd prty libraries or modules that we could implement for the GUI? If so, first tell me what they are and then I'll decide which one i want to implement. 

create a new file called SafeSound_GUI_W_libraries. and add all these changes. about the soundplayback: add it but as a button that says 'play sound' and if it is out of range, add a warning box that says 'Warning! this sound has been deemed not safe for [list of species]! We do NOT recomend playing'. And then give the option to play it or not

add a readme file that explains the upgrades done by using external libraries, add examples of waves that when summed will be safe for all species and another example that will not be safe.

## Features & Improvements

This version (`SafeSound_GUI_W_libraries.py`) is a significant upgrade over the original prototype, incorporating professional-grade Python libraries for better performance and user experience.

*   **Modern Interface**: Built with **`customtkinter`**, offering a sleek dark-mode UI with high-DPI support.
*   **Vectorized Math**: Uses **`numpy`** for blazing-fast waveform generation and analysis, replacing slow manual loops.
*   **Real-time Plotting**: Integrates **`matplotlib`** to visualize the combined waveform directly in the application window.
*   **Sound Playback**: Uses **`simpleaudio`** to play the generated sound. Includes a **Safety Interlock** that warns you before playing sounds deemed unsafe for any species.
*   **Input Validation**: Uses **`pydantic`** to strictly validate user inputs, preventing crashes from invalid data.

## Installation

Ensure you have the required libraries installed in your environment:

```bash
pip install customtkinter numpy matplotlib pydantic simpleaudio
```

## Usage

Run the application:

```bash
python SafeSound_GUI_W_libraries.py
```

1.  **Add Waves**: Enter Amplitude, Frequency, Phase, and Duration in the sidebar and click "Add Wave".
2.  **View Analysis**: The "Results" section updates automatically, showing Safety Status (SAFE/UNSAFE) for each species.
3.  **Visualize**: The waveform plot updates in real-time.
4.  **Play**: Click "Play Sound" to hear the result (if safe).

## Examples

### ✅ Safe Combination
This combination sums to a maximum amplitude of 0.6, which is below the strictest threshold (Cat: 0.7).

*   **Wave 1**: Amplitude `0.3`, Frequency `440` Hz (A4), Duration `2.0` s
*   **Wave 2**: Amplitude `0.3`, Frequency `550` Hz (C#5), Duration `2.0` s

### ⚠ Unsafe Combination
This combination sums to 1.2, exceeding the safety threshold for all species (Human: 1.0, Dog: 0.8, Cat: 0.7).

*   **Wave 1**: Amplitude `0.6`, Frequency `440` Hz, Duration `2.0` s
*   **Wave 2**: Amplitude `0.6`, Frequency `440` Hz, Duration `2.0` s (Constructive Interference)

*Note: Even a single wave of Amplitude `0.6` at `3000` Hz can be unsafe for Humans due to sensitive frequency ranges.*
