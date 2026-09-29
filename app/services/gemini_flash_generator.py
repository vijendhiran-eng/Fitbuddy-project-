from ..config import get_settings
from .gemini_client import generate_text
def _demo_tip(goal):
    return {"weight loss":"Prioritize regular meals, vegetables, protein-rich foods, water and adequate sleep rather than extreme restriction.","muscle gain":"Include a protein source in meals and combine strength training with enough food, hydration and recovery.","general wellness":"Aim for a balanced diet, regular movement, hydration and a consistent sleep schedule."}[goal]
def generate_nutrition_tip_with_flash(goal):
    s=get_settings()
    if s.ai_mode=="mock" or (s.ai_mode=="auto" and not s.gemini_api_key): return _demo_tip(goal)
    prompt=(f'Give one concise, practical general nutrition or recovery tip for someone whose fitness goal is "{goal}". '
            "Keep it suitable for a general audience. Do not prescribe supplements or medication or recommend extreme dieting. Maximum 80 words.")
    return generate_text(s.gemini_tip_model,prompt)
