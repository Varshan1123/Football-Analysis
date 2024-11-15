import pandas as pd
import re
import webcolors

# Load the CSV file
df = pd.read_csv('output_videos/player_tracking.csv')

# Function to calculate the center position of the bounding box
def calculate_center_position(position):
    x1, y1, x2, y2 = map(float, position.strip('[]').split(', '))
    center_x = (x1 + x2) / 2
    center_y = (y1 + y2) / 2
    return f'({center_x:.2f}, {center_y:.2f})'

# Function to parse the RGB values from the given format
def parse_rgb(color_str):
    return list(map(float, re.findall(r'\d+\.\d+', color_str)))

# Function to convert RGB to the closest color name
def rgb_to_color_name(rgb):
    rgb_int = tuple(map(int, rgb))
    try:
        return webcolors.rgb_to_name(rgb_int)
    except ValueError:
        closest_name = min(webcolors.CSS3_HEX_TO_NAMES, key=lambda name: sum((a - b) ** 2 for a, b in zip(webcolors.hex_to_rgb(name), rgb_int)))
        return webcolors.CSS3_HEX_TO_NAMES[closest_name]

# Apply the functions to the respective columns
df['Team Color'] = df['Team Color'].apply(lambda x: rgb_to_color_name(parse_rgb(x)))
df['Position'] = df['Position'].apply(calculate_center_position)

# Save the modified DataFrame to a new CSV file
df.to_csv('output_videos/player_tracking_modified.csv', index=False)

