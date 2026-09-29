from ..config import get_settings
from .gemini_client import generate_text
def update_workout_plan(original_plan,feedback,username,age,weight,goal,intensity):
    s=get_settings()
    if s.ai_mode=="mock" or (s.ai_mode=="auto" and not s.gemini_api_key):
        return original_plan+"\n\nUPDATED USING FEEDBACK\nUser feedback: "+feedback+"\nDemo mode recorded the feedback. Add a Gemini API key for AI regeneration."
    prompt=(f"Revise this general-wellness 7-day plan. User: {username}, age {age}, weight {weight} kg, goal {goal}, intensity {intensity}.\n"
            f"Original plan:\n{original_plan}\nUser feedback:\n{feedback}\n"
            "Return a complete revised Day 1-Day 7 plan. Honor reasonable feedback while keeping it safe. "
            "Do not diagnose conditions, prescribe medication, or recommend dangerous exercise. Include recovery.")
    return generate_text(s.gemini_workout_model,prompt)
