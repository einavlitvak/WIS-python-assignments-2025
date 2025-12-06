# SafeSound: Sound Safety Analyzer

SafeSound is a tool designed to analyze the safety of combined sound waves for different species (humans, dogs, and cats). It allows you to input multiple sine waves with specific parameters, combines them, and evaluates whether the resulting sound exceeds safe amplitude thresholds or enters sensitive frequency ranges.

## Promt used
copy the SafeSound_GUI from Day2 folder to Day3. Separate them to the bussiness logic and the user interface. 


## Table of Contents
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Usage](#usage)
  - [Command Line Interface (CLI)](#command-line-interface-cli)
  - [Graphical User Interface (GUI)](#graphical-user-interface-gui)
- [Parameters Explained](#parameters-explained)

## Prerequisites

To run this project, you need Python installed on your system. You also need the following external libraries:

- `numpy` (for numerical operations)
- `matplotlib` (for plotting waveforms)

Note: `tkinter` is used for the GUI, which typically comes pre-installed with Python on Windows and macOS.

## Installation

1.  Open your terminal or command prompt.
2.  Install the required libraries using pip:

    ```bash
    pip install -r requirements.txt
    ```
    
    Or manually:

    ```bash
    pip install numpy matplotlib
    ```

## Usage

### Command Line Interface (CLI)

The CLI version allows you to specify waves directly as arguments when running the script.

**Navigating to the folder:**
Make sure you are in the directory containing the files:
```bash
cd Day2
```

**Running the script:**
Execute the script using Python, followed by groups of 4 parameters for each wave you want to add.

**Syntax:**
```bash
python SafeSound_cmdline.py <amplitude> <frequency> <shift> <seconds> [<amplitude> <frequency> <shift> <seconds> ...]
```

**Example:**
To create two waves:
1.  Wave 1: Amplitude 0.5, Frequency 440 Hz, Phase Shift 0, Duration 2.0 seconds
2.  Wave 2: Amplitude 0.8, Frequency 880 Hz, Phase Shift 1.57, Duration 1.5 seconds

Run:
```bash
python SafeSound_cmdline.py 0.5 440 0 2.0 0.8 880 1.57 1.5
```

### Graphical User Interface (GUI)

The GUI version provides a user-friendly window to add waves interactively.

**Running the script:**
```bash
python SafeSound_GUI.py
```

**How to use:**
1.  **Add Sine Wave**: Enter the values for Amplitude, Frequency, Phase Shift, and Duration in the "Add Sine Wave" section.
2.  Click **Add Wave** to add it to the list.
3.  Repeat step 1-2 for as many waves as you like.
4.  Click **Analyze Safety** to see a report on whether the sound is safe for humans, dogs, and cats.
5.  Click **Show Plot** to visualize the individual and combined waveforms.

## Parameters Explained

The program requires the following numeric parameters for each sound wave:

*   **Amplitude**: A multiplier for the wave's strength (volume).
    *   *Input*: A float value (e.g., 0.5, 1.0).
    *   *Significance*: Higher values mean louder/stronger sounds. > 1.0 is generally considered potentially unsafe for humans in this model.
*   **Frequency**: The pitch of the sound in Hertz (Hz).
    *   *Input*: A float value (e.g., 440 for A4 note, 1000).
    *   *Significance*: Determines if the sound is audible or falls into sensitive ranges for different species.
*   **Phase Shift**: The horizontal shift of the wave in radians.
    *   *Input*: A float value (e.g., 0 for no shift, 3.14 for pi).
    *   *Significance*: Affects how waves align when combined (constructive or destructive interference).
*   **Duration**: How long the sound lasts in seconds.
    *   *Input*: A float value (e.g., 1.0, 2.5).
    *   *Significance*: Determines the length of the generated sound clip.

## Safety Criteria

The program checks:
1.  **Max Amplitude**: If the combined wave's peak exceeds the species threshold.
2.  **Sensitive Frequencies**: If loud sounds exist in frequencies where ears are most sensitive.
