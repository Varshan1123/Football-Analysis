import os
from dotenv import load_dotenv
import google.generativeai as genai
import pandas as pd
from fpdf import FPDF

load_dotenv()
# Use the environment variable for the API key
genai.configure(api_key=os.environ.get("AI_API_KEY"))

# Create the model
generation_config = {
  "temperature": 1,
  "top_p": 0.95,
  "top_k": 64,
  "max_output_tokens": 8192,
  "response_mime_type": "text/plain",
}

model = genai.GenerativeModel(
  model_name="gemini-1.5-flash",
  generation_config=generation_config,
)

chat_session = model.start_chat(
  history=[]
)

# Read the CSV files
df_players = pd.read_csv('output_videos/player_tracking_modified.csv')
df_ball = pd.read_csv('output_videos/ball_control.csv')

# Convert the DataFrame to a string
player_data = df_players.to_string(index=False)
ball_data = df_ball.to_string(index=False)

# Format the prompt with the CSV data
# prompt = f"Generate a soccer match report based on the following player data:\n{player_data}\n\nAnd the following ball possession data:\n{ball_data}"
prompt = f"Please generate a detailed soccer match report based on the following data:\n{player_data}\n\consist of Frame,Player ID, Team, Team Color, Position, Speed (km/h), Distance (m) and Ball Data:\n{ball_data}\n\consist of team_with_ball: Array of 1 or 2, representing the team in possession of the ball (1 = Team 1, 2 = Team 2)"
# Send the prompt to the AI model
response = chat_session.send_message(prompt)

# Print the response
print(response.text)

# Save the response to a PDF file
pdf = FPDF()
pdf.add_page()
pdf.set_font("Arial", size=12)
pdf.multi_cell(0, 10, response.text)
pdf.output("soccer_match_report.pdf")