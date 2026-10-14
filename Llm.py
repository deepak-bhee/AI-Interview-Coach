# To access envirnonment variables
import os 
# To load the variables in .env file
from dotenv import load_dotenv
#To access tools to communicate with Gemini 
from google import genai
import json

# to load the api key 
load_dotenv()

#To connect to Gemini API
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

#To choose the Model 
MODEL = "gemini-3.5-flash-lite"

#define a function to send a prompt 
def ask_ai(prompt):
    response = client.models.generate_content(model=MODEL,contents=prompt)
    return response.text

# To create a json response function
def ask_ai_json(prompt):
    response = client.models.generate_content(model=MODEL,contents=prompt,config={"response_mime_type":"application/json"})
    return json.loads(response.text)
