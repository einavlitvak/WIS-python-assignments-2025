# Day 4: Daily Briefing Program

This program fetches live weather data for Tel Aviv and the "Word of the Day" from online sources, aggregates the data into day segments (Morning, Afternoon, Evening), and creates a daily briefing report.

## How it Works
1.  **Logic (`logic.py`)**: 
    *   Scrapes `timeanddate.com` for Tel Aviv's hourly weather forecast.
    *   Calculates average temperature, humidity, and dominant weather for 6-hour blocks (06-12, 12-18, 18-00).
    *   Scrapes `dictionary.com` for the Word of the Day.
2.  **UI (`ui.py`)**:
    *   Displays the data in a readable CLI format.
    *   Saves the output to `Daily_Briefing.txt`.

## Usage
Run the program from the `Day4` folder using your configured Python environment:

```bash
python ui.py
```

## Dependencies
*   `requests`
*   `beautifulsoup4`
*   `customtkinter`
*   `packaging` (dependency of customtkinter)


## Prompt Used
> i want to use an israeli weather channel. I want to get the type of weather expected for morning, afternoon and evening (kind of an average of the by hour, from 6 am to 12 pm, from 12pm to 6pm and from 6pm to 12 am). for each of the day frames, give low-high temperature, type of weather (sunny, cloudy, rainy,etc), humidity. then give recomendations for how to dress aproppiately, and from thesaurus.com also get the word of the day and include it with the definition. 
> add a readme file explaining the new program adding as par of the markdown the promt used
> great, id like to re-add the pronounciation of the word as a fourth row! Instead of a txt, i would like to get a nice pop up window with all this information. i would like to get a 'Hey, Einav! Its a great day for great things today.... Here is what to expect of the weather' and then all the info
> great! lets change the format a bit. make the four panels be in a 2x2 grid and mke sure there is no need to scroll to see all the info


## New Features (v2)
*   **Modern UI**: Uses `customtkinter` for a sleek dark-mode interface.
*   **Grid Layout**: Displays information in a compact 2x2 grid (Morning, Afternoon, Evening, Word).
*   **Color Coding**: Visual distinction between time periods (Amber, Blue, Purple).
*   **Word Analytics**: Includes pronunciation, type, and definition in a stacked layout.

