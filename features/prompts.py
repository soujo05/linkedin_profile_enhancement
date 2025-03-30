import json

#  Prompt for the Education Section (Detailed Sentences for Coursework)
EDUCATION_PROMPT = """
The user has provided their education details:
{education_details}

**Instructions:**
- Format the response in a **clean simple format**.
- Provide **full sentences** for coursework and experiences, not just keywords.
- Ensure each entry highlights **degree, field of study, duration, and key experiences**.
- Keep descriptions **concise yet informative**.

**Example Output:**
"""

#  Prompt for General Sections (Experience, Skills, Volunteer, etc.)
GENERAL_PROMPT = """
You are a LinkedIn profile optimization expert. Your task is to enhance the **{section}** section 
of a professional LinkedIn profile. The current content is:

"{section_content}"

🔹 **Key points from the user's profile summary:**  
"{summary_content}"

🔹 Provide **exactly** 4 concise, impactful improvement suggestions.  
🔹 Each suggestion should be a **ready-to-use phrase**, not an explanation.  
🔹 Make the wording engaging, professional, and aligned with industry best practices.  
🔹 Avoid generic responses—tailor suggestions to reflect the profile's strengths.  

**Format your response as follows:**
- Suggestion 1
- Suggestion 2
- Suggestion 3
- Suggestion 4
"""

#  Prompt for Empty Sections (If User Has No Content in a Section)
EMPTY_SECTION_PROMPT = """
The **{section}** section is currently empty. Based on the user's summary:  
"{summary_content}"

🔹 Suggest **exactly** 4 professional, attention-grabbing content ideas for this section.  
🔹 Each suggestion should be a **directly usable phrase**, without additional explanations.  
🔹 Ensure relevance to the user’s industry, skills, and career goals.  

**Format your response as follows:**
- Suggestion 1
- Suggestion 2
- Suggestion 3
- Suggestion 4
"""
