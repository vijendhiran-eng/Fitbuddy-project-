from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase,sessionmaker
from .config import BASE_DIR,get_settings
s=get_settings()
if s.database_url.startswith("sqlite:///./"):
    p=BASE_DIR/s.database_url.removeprefix("sqlite:///./"); p.parent.mkdir(parents=True,exist_ok=True); URL=f"sqlite:///{p.as_posix()}"
else: URL=s.database_url
engine=create_engine(URL,connect_args={"check_same_thread":False} if URL.startswith("sqlite") else {},future=True)
SessionLocal=sessionmaker(bind=engine,autoflush=False,autocommit=False,future=True)
class Base(DeclarativeBase): pass
def init_db():
    from . import models
    Base.metadata.create_all(bind=engine)
def get_db():
    db=SessionLocal()
    try: yield db
    finally: db.close()
