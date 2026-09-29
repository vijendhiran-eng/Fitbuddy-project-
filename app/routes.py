from pathlib import Path
from fastapi import APIRouter,Depends,Form,HTTPException,Request
from fastapi.responses import HTMLResponse,RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy import select
from sqlalchemy.orm import Session
from .config import BASE_DIR,get_settings
from .database import get_db
from .models import User
from .schemas import FeedbackRequest,UserInput
from .services.gemini_flash_generator import generate_nutrition_tip_with_flash
from .services.gemini_generator import generate_workout_gemini
from .services.updated_plan import update_workout_plan
router=APIRouter()
templates=Jinja2Templates(directory=Path(BASE_DIR)/"templates")
def render(request,name,**context): return templates.TemplateResponse(request=request,name=name,context=context)
@router.get("/",response_class=HTMLResponse)
def home(request:Request): return render(request,"index.html")
@router.post("/generate-workout",response_class=HTMLResponse)
def generate_workout(request:Request,username:str=Form(...),user_id:str=Form(...),age:int=Form(...),weight:float=Form(...),goal:str=Form(...),intensity:str=Form(...),db:Session=Depends(get_db)):
    try:
        data=UserInput(username=username,user_id=user_id,age=age,weight=weight,goal=goal,intensity=intensity)
        if db.scalar(select(User).where(User.user_id==data.user_id)): raise HTTPException(409,"That User ID already exists.")
        plan=generate_workout_gemini(data.username,data.age,data.weight,data.goal,data.intensity)
        tip=generate_nutrition_tip_with_flash(data.goal)
        user=User(user_id=data.user_id,username=data.username,age=data.age,weight=data.weight,goal=data.goal,intensity=data.intensity,original_plan=plan,nutrition_tip=tip)
        db.add(user); db.commit()
        return RedirectResponse(f"/result/{user.user_id}",status_code=303)
    except HTTPException: raise
    except Exception as exc: return render(request,"error.html",title="Generation error",message=str(exc))
@router.get("/result/{user_id}",response_class=HTMLResponse)
def result(request:Request,user_id:str,db:Session=Depends(get_db)):
    user=db.scalar(select(User).where(User.user_id==user_id))
    if not user: raise HTTPException(404,"User not found.")
    return render(request,"result.html",user=user)
@router.get("/feedback/{user_id}",response_class=HTMLResponse)
def feedback_page(request:Request,user_id:str,db:Session=Depends(get_db)):
    user=db.scalar(select(User).where(User.user_id==user_id))
    if not user: raise HTTPException(404,"User not found.")
    return render(request,"feedback.html",user=user)
@router.post("/submit-feedback",response_class=HTMLResponse)
def submit_feedback(request:Request,user_id:str=Form(...),feedback:str=Form(...),db:Session=Depends(get_db)):
    try:
        data=FeedbackRequest(user_id=user_id,feedback=feedback)
        user=db.scalar(select(User).where(User.user_id==data.user_id))
        if not user: raise HTTPException(404,"User not found.")
        user.updated_plan=update_workout_plan(user.original_plan,data.feedback,user.username,user.age,user.weight,user.goal,user.intensity)
        user.feedback=data.feedback; db.commit()
        return RedirectResponse(f"/result/{user.user_id}",status_code=303)
    except HTTPException: raise
    except Exception as exc: return render(request,"error.html",title="Update error",message=str(exc))
@router.get("/view-all-users",response_class=HTMLResponse)
def view_all_users(request:Request,admin_key:str="",db:Session=Depends(get_db)):
    if admin_key!=get_settings().admin_key: return render(request,"admin_login.html",error="Enter the configured admin key.")
    return render(request,"all_users.html",users=db.scalars(select(User).order_by(User.created_at.desc())).all())
@router.get("/api/users")
def api_users(admin_key:str="",db:Session=Depends(get_db)):
    if admin_key!=get_settings().admin_key: raise HTTPException(403,"Invalid admin key.")
    users=db.scalars(select(User).order_by(User.created_at.desc())).all()
    return [{"user_id":u.user_id,"username":u.username,"age":u.age,"weight":u.weight,"goal":u.goal,"intensity":u.intensity,"has_updated_plan":bool(u.updated_plan)} for u in users]
@router.get("/health")
def health(): return {"status":"ok","service":"fitbuddy"}
