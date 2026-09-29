from ..config import get_settings
from .gemini_client import generate_text
def _demo_plan(username,age,weight,goal,intensity):
    level={"low":"gentle","medium":"moderate","high":"challenging"}[intensity]
    focus={"weight loss":"steady cardio and full-body strength","muscle gain":"progressive strength training with recovery","general wellness":"balanced mobility, cardio and strength"}[goal]
    days=[
        ("Day 1",f"Warm-up 7 min; {level} full-body: squats 3x10, incline push-ups 3x8, glute bridges 3x12; cooldown 5 min."),
        ("Day 2",f"Warm-up 5 min; {level} cardio walk/cycle 25 min; mobility 10 min."),
        ("Day 3",f"Warm-up 7 min; {level} upper body: rows 3x10, incline push-ups 3x10, shoulder mobility; cooldown 5 min."),
        ("Day 4","Recovery day: easy walk 15-20 min and gentle stretching."),
        ("Day 5",f"Warm-up 7 min; {level} lower body: squats 3x10, step-ups 3x8/side, calf raises 3x12; cooldown 5 min."),
        ("Day 6",f"Warm-up 5 min; {level} mixed cardio 20-30 min plus dead bug 3x8/side and bird dog 3x8/side."),
        ("Day 7","Rest and recovery: relaxed movement, hydration and sleep routine.")
    ]
    return f"FitBuddy demo plan for {username} ({age} years, {weight:g} kg)\nGoal: {goal} | Intensity: {intensity}\nFocus: {focus}.\n\n"+"\n".join(f"{d}: {p}" for d,p in days)
def generate_workout_gemini(username,age,weight,goal,intensity):
    s=get_settings()
    if s.ai_mode=="mock" or (s.ai_mode=="auto" and not s.gemini_api_key):
        return _demo_plan(username,age,weight,goal,intensity)
    prompt=("You are FitBuddy, an educational general-wellness fitness assistant.\n"
            f"Create a safe, realistic 7-day beginner-friendly workout plan for: Name: {username}; Age: {age}; Weight: {weight} kg; Goal: {goal}; Preferred intensity: {intensity}.\n"
            "Return plain text with Day 1 through Day 7. For each day include warm-up (5-10 minutes), main workout with exercise names and sets/reps or time, and cool-down/recovery guidance. "
            "Include rest/recovery. Do not diagnose conditions, prescribe medication, recommend dangerous challenges, or encourage exercising through pain.")
    return generate_text(s.gemini_workout_model,prompt)
