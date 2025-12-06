import requests
from bs4 import BeautifulSoup
import datetime
import statistics

def get_word_of_the_day():
    try:
        url = "https://www.dictionary.com/e/word-of-the-day/"
        headers = {'User-Agent': 'Mozilla/5.0'}
        r = requests.get(url, headers=headers)
        soup = BeautifulSoup(r.content, 'html.parser')
        
        word = "N/A"
        pos = "N/A"
        definition = "N/A"
        pronunciation = "N/A"
        
        headers = soup.find_all('h1')
        for h in headers:
            text = h.get_text(strip=True)
            if "word" in text.lower() and "day" in text.lower():
                continue
            
            word = text
            
            # Go to parent, then siblings
            parent = h.parent
            if parent:
                curr = parent.find_next_sibling()
                while curr:
                    txt = curr.get_text(strip=True)
                    
                    # Pronunciation check (often first sibling)
                    if pronunciation == "N/A" and ("IPA" in txt or "[" in txt or "/" in txt):
                         # Extract clean pronunciation text "kou-chuh nt"
                         # usually first part before split
                         clean_pron = txt.split('[')[0].strip()
                         if not clean_pron: # If empty (maybe brackets start line file [ /kaʊ... ])
                             clean_pron = txt.strip()
                         pronunciation = clean_pron
                         curr = curr.find_next_sibling()
                         continue
                    
                    # POS & Def
                    full_text = curr.get_text(separator=' ', strip=True)
                    common_pos = ['noun', 'verb', 'adjective', 'adverb', 'pronoun', 'preposition', 'conjunction', 'interjection']
                    
                    found_pos = False
                    for cp in common_pos:
                        if full_text.lower().startswith(cp):
                            pos = cp.capitalize()
                            definition = full_text[len(cp):].strip()
                            if definition.startswith(',') or definition.startswith('-') or definition.startswith(':'):
                                definition = definition[1:].strip()
                            found_pos = True
                            break
                    
                    if not found_pos:
                         # Fallback if we haven't found a clear POS block yet
                         pass
                    
                    if definition.endswith("Look it up"):
                        definition = definition[:-10].strip()
                    
                    if found_pos:
                        break # Done
                        
                    curr = curr.find_next_sibling()
            
            break 
            
        return {
            "word": word,
            "pronunciation": pronunciation,
            "type": pos,
            "definition": definition
        }
    except Exception as e:
        return {"error": str(e)}

def parse_weather_row(row):
    try:
        time_cell = row.find('th')
        if not time_cell: return None
        
        time_str = time_cell.get_text(strip=True)
        if ":" not in time_str: return None
        
        clean_time = ''.join(filter(str.isdigit, time_str.split(':')[0]))
        if not clean_time: return None
        hour = int(clean_time)
        
        cols = row.find_all('td')
        if len(cols) < 7: return None
        
        temp_str = cols[1].get_text(strip=True).split()[0]
        temp_clean = ''.join(c for c in temp_str if c.isdigit() or c in '.-')
        if not temp_clean: return None
        temp = int(float(temp_clean))
        
        weather = cols[2].get_text(strip=True)
        
        hum_str = cols[6].get_text(strip=True).replace('%', '')
        humidity = int(float(hum_str))
        
        return {
            "hour": hour,
            "temp": temp,
            "weather": weather,
            "humidity": humidity
        }
    except Exception as e:
        return None

def get_tel_aviv_weather_forecast():
    try:
        url = "https://www.timeanddate.com/weather/israel/tel-aviv/hourly"
        headers = {'User-Agent': 'Mozilla/5.0'}
        r = requests.get(url, headers=headers)
        soup = BeautifulSoup(r.content, 'html.parser')
        
        table = soup.find(id='wt-hbh')
        if not table: return None
        rows = table.find_all('tr')
        
        buckets = {
            "Morning (06:00 - 12:00)": [],
            "Afternoon (12:00 - 18:00)": [],
            "Evening (18:00 - 00:00)": []
        }
        
        for row in rows:
            data = parse_weather_row(row)
            if data:
                h = data['hour']
                if 6 <= h < 12:
                    buckets["Morning (06:00 - 12:00)"].append(data)
                elif 12 <= h < 18:
                    buckets["Afternoon (12:00 - 18:00)"].append(data)
                elif 18 <= h <= 23:
                    buckets["Evening (18:00 - 00:00)"].append(data)
        
        report = {}
        for period, data_list in buckets.items():
            if not data_list:
                report[period] = "No data available (Past or too far ahead)"
                continue
                
            avg_temp = statistics.mean([d['temp'] for d in data_list])
            min_temp = min(d['temp'] for d in data_list)
            max_temp = max(d['temp'] for d in data_list)
            avg_hum = statistics.mean([d['humidity'] for d in data_list])
            
            weather_counts = {}
            for d in data_list:
                w = d['weather'].split('.')[0].strip()
                weather_counts[w] = weather_counts.get(w, 0) + 1
            common_weather = max(weather_counts, key=weather_counts.get)
            
            rec = "Comfortable clothes."
            if avg_temp < 15:
                rec = "Wear a coat or warm jacket."
            elif avg_temp < 20:
                rec = "Long sleeves or a light jacket recommended."
            elif avg_temp > 25:
                rec = "Short sleeves and light fabrics."
                
            if "rain" in common_weather.lower() or "shower" in common_weather.lower() or "tstorm" in common_weather.lower():
                rec += " Don't forget an umbrella!"
                
            report[period] = {
                "Temp Range": f"{min_temp}°C - {max_temp}°C",
                "Avg Temp": f"{avg_temp:.1f}°C",
                "Weather": common_weather,
                "Humidity": f"{avg_hum:.0f}%",
                "Dress Code": rec
            }
            
        return report
    except Exception as e:
        print(f"Weather Fetch Error: {e}")
        return None
