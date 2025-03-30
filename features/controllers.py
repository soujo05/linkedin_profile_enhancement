import json
import os
import requests
from fastapi import HTTPException
from dotenv import load_dotenv
from features.prompts import EDUCATION_PROMPT, GENERAL_PROMPT, EMPTY_SECTION_PROMPT
from langchain_google_genai import ChatGoogleGenerativeAI

# load_dotenv()
# Constants
JSON_FILE_PATH = r"features/retrieved_linkedin_data.json"
SCRAPIN_API_KEY = "sk_13916974ff66aee3d4768ffb67031c2a17c3a549"
SCRAPIN_API_URL = "https://api.scrapin.io/enrichment/profile"

# Fetch API Key for Gemini
gemini_api_key = "AIzaSyCK6YT332KT79i2JvgJ6Jjes76R2I1Dtk8"
if not gemini_api_key:
    raise ValueError("GEMINI_API_KEY is not set in environment variables.")

# Optimized LLM configuration
llm = ChatGoogleGenerativeAI(
    model="gemini-1.5-flash",
    api_key=gemini_api_key,
    temperature=0.1,
    timeout=300,
    max_retries=3,
    max_tokens=7000
)

# Function to fetch LinkedIn profile data using Scrapin.io
def fetch_profile_data(profile_url):
    try:
        params = {
            "apikey": SCRAPIN_API_KEY,
            "linkedInUrl": profile_url  
        }

        response = requests.get(SCRAPIN_API_URL, params=params)

        if response.status_code != 200:
            raise HTTPException(status_code=response.status_code, detail=f"Error fetching profile data: {response.text}")

        profile_data = response.json()

        # Debugging: Print API response
        print(f"Fetched LinkedIn Profile Data for {profile_url}:", profile_data)

        if not profile_data:
            raise HTTPException(status_code=500, detail="Scrapin.io API returned empty profile data.")

        # Save to JSON file for reference
        with open(JSON_FILE_PATH, "w", encoding="utf-8") as file:
            json.dump(profile_data, file, indent=4, ensure_ascii=False)

        return profile_data
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching profile data: {str(e)}")


# Function to get suggestions from Gemini API
def get_suggestions_from_gemini(section: str, section_content: str, summary_content: str):
    try:
        if section == "education":
            prompt = EDUCATION_PROMPT.format(education_details=json.dumps(section_content, indent=4))
        elif section_content and section_content.strip():
            prompt = GENERAL_PROMPT.format(section=section, section_content=section_content, summary_content=summary_content)
        else:
            prompt = EMPTY_SECTION_PROMPT.format(section=section, summary_content=summary_content)

        # Invoke Gemini API
        response = llm.invoke(prompt)

        # Ensure proper response extraction
        if isinstance(response, str):
            return response.strip()
        elif hasattr(response, "content"):
            return response.content.strip()
        else:
            return "No suggestion provided."

    except Exception as e:
        print(f" Error in get_suggestions_from_gemini for {section}: {str(e)}")
        return f"Error generating suggestions for {section}: {str(e)}"




