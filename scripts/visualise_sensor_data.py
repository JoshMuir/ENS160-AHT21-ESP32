import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import re
from datetime import datetime, timedelta
import os


def visualize_data(df, output_folder="plots"):
    """Create visualizations from the data."""
    
    # Create output folder if it doesn't exist
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    
    # Set up the time formatter for x-axis
    time_fmt = mdates.DateFormatter('%H:%M:%S')
    
    # Plot 1: Air Quality Metrics
    plt.figure(figsize=(12, 6))
    plt.plot(df['Timestamp'], df['AQI'], label='AQI UBA', linewidth=2)
    plt.plot(df['Timestamp'], df['TVOC'] / 10, label='TVOC (ppb/10)', alpha=0.8)
    plt.plot(df['Timestamp'], df['ECO2'] / 100, label='ECO2 (ppm/100)', alpha=0.8)
    plt.xlabel('Time')
    plt.ylabel('Value')
    plt.title('Air Quality Metrics Over Time')
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.gca().xaxis.set_major_formatter(time_fmt)
    plt.tight_layout()
    plt.savefig(f"{output_folder}/air_quality_metrics.png")
    
    # Plot 2: Resistance Values
    plt.figure(figsize=(12, 6))
    plt.plot(df['Timestamp'], df['RS0'] / 1000, label='RS0 (k)', alpha=0.8)
    plt.plot(df['Timestamp'], df['RS2'] / 1000, label='RS2 (k)', alpha=0.8)
    plt.plot(df['Timestamp'], df['RS3'] / 1000, label='RS3 (k)', alpha=0.8)
    # RS1 is always 1, so we skip it
    plt.xlabel('Time')
    plt.ylabel('Resistance (kΩ)')
    plt.title('Sensor Resistance Values Over Time')
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.gca().xaxis.set_major_formatter(time_fmt)
    plt.tight_layout()
    plt.savefig(f"{output_folder}/resistance_values.png")
    
    # Plot 3: Temperature and Humidity
    fig, ax1 = plt.subplots(figsize=(12, 6))
    color = 'tab:red'
    ax1.set_xlabel('Time')
    ax1.set_ylabel('Temperature (°C)', color=color)
    ax1.plot(df['Timestamp'], df['Temperature'], color=color)
    ax1.tick_params(axis='y', labelcolor=color)
    
    ax2 = ax1.twinx()
    color = 'tab:blue'
    ax2.set_ylabel('Humidity (%)', color=color)
    ax2.plot(df['Timestamp'], df['Humidity'], color=color)
    ax2.tick_params(axis='y', labelcolor=color)
    
    plt.title('Temperature and Humidity Over Time')
    plt.grid(True, alpha=0.3)
    ax1.xaxis.set_major_formatter(time_fmt)
    fig.tight_layout()
    plt.savefig(f"{output_folder}/temperature_humidity.png")
    
    # Plot 4: TVOC vs ECO2
    plt.figure(figsize=(10, 8))
    scatter = plt.scatter(df['TVOC'], df['ECO2'], c=df['AQI'], cmap='viridis', alpha=0.7)
    plt.colorbar(scatter, label='AQI Value')
    plt.xlabel('TVOC (ppb)')
    plt.ylabel('ECO2 (ppm)')
    plt.title('Correlation Between TVOC and ECO2')
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig(f"{output_folder}/tvoc_vs_eco2.png")
    
    # Plot 5: AQI Distribution
    plt.figure(figsize=(8, 6))
    aqi_counts = df['AQI'].value_counts().sort_index()
    aqi_labels = {
        1: 'Excellent',
        2: 'Good',
        3: 'Moderate',
        4: 'Poor',
        5: 'Unhealthy'
    }
    labels = [aqi_labels.get(aqi, str(aqi)) for aqi in aqi_counts.index]
    plt.bar(labels, aqi_counts.values)
    plt.xlabel('AQI UBA Category')
    plt.ylabel('Count')
    plt.title('Distribution of Air Quality Index Readings')
    plt.tight_layout()
    plt.savefig(f"{output_folder}/aqi_distribution.png")

    # Plot 6: Heatmap of sensors with AQI
    plt.figure(figsize=(12, 8))
    
    # Create a time index for better visualization
    time_index = range(len(df))
    
    # Create a 2D array where each row represents a sensor and each column a time point
    data = np.array([
        df['TVOC'].values / df['TVOC'].max(),
        df['ECO2'].values / df['ECO2'].max(),
        df['RS0'].values / df['RS0'].max(),
        df['RS2'].values / df['RS2'].max(),
        df['RS3'].values / df['RS3'].max(),
        df['AQI'].values / df['AQI'].max(),
    ])
    
    plt.imshow(data, aspect='auto', cmap='magma')
    plt.colorbar(label='Normalized Value')
    plt.yticks(range(6), ['TVOC', 'ECO2', 'RS0', 'RS2', 'RS3', 'AQI'])
    # Only show a few time ticks for clarity
    tick_positions = np.linspace(0, len(df) - 1, 10).astype(int)
    plt.xticks(tick_positions, [df['Timestamp'].iloc[i].strftime('%H:%M:%S') for i in tick_positions])
    plt.xlabel('Time')
    plt.title('Sensor Reading Patterns Over Time (Normalized)')
    plt.tight_layout()
    plt.savefig(f"{output_folder}/sensor_patterns_heatmap.png")
    
    print(f"Plots have been saved to the '{output_folder}' directory.")
    
    return

def print_statistics(df):
    """Print some basic statistics about the data."""
    print("\n===== Sensor Data Statistics =====")
    print(f"Total readings: {len(df)}")
    print("\n--- Air Quality ---")
    print(f"Average AQI UBA: {df['AQI'].mean():.2f} (min: {df['AQI'].min()}, max: {df['AQI'].max()})")
    print(f"Average TVOC: {df['TVOC'].mean():.2f} ppb (min: {df['TVOC'].min()}, max: {df['TVOC'].max()})")
    print(f"Average ECO2: {df['ECO2'].mean():.2f} ppm (min: {df['ECO2'].min()}, max: {df['ECO2'].max()})")
    print("\n--- Resistance Values ---")
    print(f"Average RS0: {df['RS0'].mean():.2f} Ω")
    print(f"Average RS2: {df['RS2'].mean():.2f} Ω")
    print(f"Average RS3: {df['RS3'].mean():.2f} Ω")
    print("\n--- Environmental Conditions ---")
    print(f"Average Temperature: {df['Temperature'].mean():.2f}°C (min: {df['Temperature'].min()}, max: {df['Temperature'].max()})")
    print(f"Average Humidity: {df['Humidity'].mean():.2f}% (min: {df['Humidity'].min()}, max: {df['Humidity'].max()})")
    print("\n--- AQI Distribution ---")
    aqi_dist = df['AQI'].value_counts(normalize=True).sort_index() * 100
    for aqi, percentage in aqi_dist.items():
        if aqi == 1:
            quality = "Excellent"
        elif aqi == 2:
            quality = "Good"
        elif aqi == 3:
            quality = "Moderate"
        elif aqi == 4:
            quality = "Poor"
        elif aqi == 5:
            quality = "Unhealthy"
        else:
            quality = "Unknown"
        print(f"AQI {aqi} ({quality}): {percentage:.2f}%")
            
def parse_log_file(filepath):
    """Parse the log file and extract sensor data into a DataFrame."""
    try:
        # First try with utf-8
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.readlines()
    except UnicodeDecodeError:
        try:
            # Try with latin-1 which can handle any byte value
            with open(filepath, 'r', encoding='latin-1') as f:
                content = f.readlines()
            print("Using latin-1 encoding to read the file.")
        except Exception as e:
            # If that still fails, try with error handling
            with open(filepath, 'r', encoding='utf-8', errors='replace') as f:
                content = f.readlines()
            print(f"Warning: Some characters in the log file couldn't be decoded properly.")
    
    # Modified pattern to match the actual data format in the log file
    # The line comes as two separate lines in the log file
    data = []
    
    # Keep track of successful matches for debugging
    successful_matches = 0
    total_valid_lines = 0
    
    # State variables for parsing
    aqi_line = None
    rs_line = None
    humid_temp_line = None
    
    for i, line in enumerate(content):
        line = line.strip()
        
        # Skip empty lines
        if not line:
            continue
            
        total_valid_lines += 1
        
        # Check for AQI line
        aqi_match = re.search(r'AQI UBA:(\d+)\s+TVOC:(\d+)\s+ECO2:(\d+)', line)
        if aqi_match:
            aqi_line = line
            continue
            
        # Check for RS line
        rs_match = re.search(r'RS0:(\d+)\s+RS1:(\d+)\s+RS2:(\d+)\s+RS3:(\d+)', line)
        if rs_match:
            rs_line = line
            continue
            
        # Check for Humidity/Temperature line
        ht_match = re.search(r'Humidity: (\d+\.\d+)%, Temperature: (\d+\.\d+)', line)
        if ht_match:
            humid_temp_line = line
            
            # If we have all three lines, extract the data
            if aqi_line and rs_line and humid_temp_line:
                # Extract AQI data
                aqi_data = re.search(r'AQI UBA:(\d+)\s+TVOC:(\d+)\s+ECO2:(\d+)', aqi_line)
                aqi, tvoc, eco2 = aqi_data.groups()
                
                # Extract RS data
                rs_data = re.search(r'RS0:(\d+)\s+RS1:(\d+)\s+RS2:(\d+)\s+RS3:(\d+)', rs_line)
                rs0, rs1, rs2, rs3 = rs_data.groups()
                
                # Extract Humidity and Temperature
                ht_data = re.search(r'Humidity: (\d+\.\d+)%, Temperature: (\d+\.\d+)', humid_temp_line)
                humidity, temp = ht_data.groups()
                
                successful_matches += 1
                
                # Add to data list
                data.append({
                    'AQI': int(aqi),
                    'TVOC': int(tvoc),
                    'ECO2': int(eco2),
                    'RS0': int(rs0),
                    'RS1': int(rs1),
                    'RS2': int(rs2),
                    'RS3': int(rs3),
                    'Humidity': float(humidity),
                    'Temperature': float(temp)
                })
                
                # Reset state
                aqi_line = None
                rs_line = None
                humid_temp_line = None
    
    print(f"Matched {successful_matches} complete data points out of {total_valid_lines} non-empty lines.")
    
    if not data:
        print("WARNING: No data could be extracted from the log file!")
        print("First few lines of the file:")
        for i in range(min(5, len(content))):
            print(f"Line {i+1}: {content[i].strip()}")
        
        # Debug the pattern match issue with more output
        print("\nTrying to debug pattern matching issue:")
        for i in range(min(6, len(content))):
            line = content[i].strip()
            print(f"Testing line {i+1}: {line}")
            print(f"  Contains 'AQI': {'AQI' in line}")
            print(f"  Contains 'RS0': {'RS0' in line}")
            print(f"  Contains 'Humidity': {'Humidity' in line}")
            print(f"  Contains 'Temperature': {'Temperature' in line}")
            
        return pd.DataFrame()
    
    # Create DataFrame
    df = pd.DataFrame(data)
    
    # Add a timestamp column (approximate based on line number)
    # Assume each reading is taken every second
    start_time = datetime.now().replace(microsecond=0) - timedelta(seconds=len(df))
    df['Timestamp'] = [start_time + timedelta(seconds=i) for i in range(len(df))]
    
    return df

def main():
    # Check which log file to use
    # Look in both current directory and parent directory
    log_files = []
    search_dirs = ['.', '..']
    
    # First try to find the specific log file if provided
    specific_log = 'log.main.minicom-morningreadings-30mar-9am-430.txt'
    if os.path.exists(specific_log):
        log_files.append(specific_log)
    elif os.path.exists(os.path.join('..', specific_log)):
        log_files.append(os.path.join('..', specific_log))
    else:
        # Fall back to searching for any log files
        for directory in search_dirs:
            if os.path.exists(directory):
                log_files.extend([os.path.join(directory, file) 
                                for file in os.listdir(directory) 
                                if file.startswith('log.main.') and file.endswith('.txt')])
    
    if not log_files:
        print("No log files found in current or parent directory.")
        return
    
    # Use the most recent log file if there are multiple
    log_file = sorted(log_files)[-1]
    print(f"Using log file: {log_file}")
    
    # Parse the data
    df = parse_log_file(log_file)
    
    if len(df) == 0:
        print("No data to process. Exiting.")
        return
    
    # Print some basic statistics
    print_statistics(df)
    
    # Create visualizations
    visualize_data(df)
    
    print(f"Successfully processed {len(df)} readings from {log_file}.")
    print("Check the 'plots' directory for visualization results.")

if __name__ == "__main__":
    main()