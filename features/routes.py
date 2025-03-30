import json  
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from features.controllers import fetch_profile_data, get_suggestions_from_gemini
from typing import List,Optional,Dict

# Define router
router = APIRouter()

# Pydantic models

class ProfileRequest(BaseModel):
    profile_url: str  # LinkedIn profile URL
    coursework_phrases: Dict[str, List[str]]  # {Institution Name: [Courses]}

class SuggestionsResponse(BaseModel):
    suggestions: dict

# Endpoint: Fetch LinkedIn profile and generate suggestions

@router.post("/fetch-and-suggest/", response_model=SuggestionsResponse)
def fetch_and_generate_suggestions(profile_request: ProfileRequest):
    profile_url = profile_request.profile_url
    coursework_mapping = profile_request.coursework_phrases  # {Institution: [Courses]}

    try:
        profile_data = fetch_profile_data(profile_url)
        if not profile_data or "person" not in profile_data:
            raise HTTPException(status_code=500, detail="Scrapin.io API returned empty or invalid profile data.")
    except HTTPException as e:
        raise e

    person_data = profile_data.get("person", {})
    summary = person_data.get("summary", "No summary available.")

    education_list = person_data.get("schools", {}).get("educationHistory", [])
    
    formatted_education = []
    for edu in education_list:
        school_name = edu.get("schoolName", "Unknown Institution")
        coursework = coursework_mapping.get(school_name, [])  # Directly get coursework

        entry = {
            "institution": school_name,
            "degree": edu.get("degreeName", "No degree listed"),
            "field": edu.get("fieldOfStudy", "No field of study listed"),
            "duration": f"{edu.get('startEndDate', {}).get('start', {}).get('year', 'Unknown')} - {edu.get('startEndDate', {}).get('end', {}).get('year', 'Present')}",
            "coursework": coursework if coursework else ["No coursework provided"],  # Ensures a list
        }
        formatted_education.append(entry)

    sections = {
        "headline": person_data.get("headline", "No headline provided."),
        "education": formatted_education,
        "experience": person_data.get("positions", {}).get("positionHistory", []),
        "skills": ", ".join(person_data.get("skills", [])) if "skills" in person_data else "No skills listed.",
        "volunteer": person_data.get("volunteeringExperiences", {}).get("volunteeringExperienceHistory", []),
        "projects": person_data.get("projects", "No projects listed.")
    }

    # Debug: Print education details before sending to Gemini
    print(f"Final Education Data: {json.dumps(sections['education'], indent=4)}")

    # Generate suggestions using Gemini API
    suggestions = {}
    for section, content in sections.items():
        try:
            suggestions[section] = get_suggestions_from_gemini(section, json.dumps(content), summary)
        except HTTPException as e:
            suggestions[section] = f"Error generating suggestions for {section}: {str(e)}"

    return {"suggestions": suggestions}
