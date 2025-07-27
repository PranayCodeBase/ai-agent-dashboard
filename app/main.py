from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from typing import List
from . import models, schemas, database, crud, auth
from .database import SessionLocal, engine
from datetime import timedelta

from fastapi.middleware.cors import CORSMiddleware

models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="AI Agent Dashboard")

# Optional CORS if testing with frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Change to specific domains in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# -------------------------
# Dependency
# -------------------------
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# -------------------------
# Auth - /register
# -------------------------
@app.post("/register")
def register_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    return crud.create_user(db, user)

# -------------------------
# Auth - /login
# -------------------------
@app.post("/login", response_model=schemas.Token)
def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = auth.authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    access_token = auth.create_access_token(
        data={"sub": user["username"]},
        expires_delta=timedelta(minutes=auth.ACCESS_TOKEN_EXPIRE_MINUTES),
    )
    return {"access_token": access_token, "token_type": "bearer"}

# -------------------------
# Agents
# -------------------------
@app.post("/agents", response_model=schemas.AgentOut)
def create_agent(agent: schemas.AgentCreate, db: Session = Depends(get_db), user=Depends(auth.get_current_user)):
    return crud.create_agent(db, agent)

@app.get("/agents", response_model=List[schemas.AgentOut])
def get_agents(name: str = None, status: str = None, db: Session = Depends(get_db), user=Depends(auth.get_current_user)):
    return crud.get_all_agents(db, name, status)

@app.put("/agents/{agent_id}", response_model=schemas.AgentOut)
def update_agent(agent_id: str, update_data: schemas.AgentUpdate, db: Session = Depends(get_db), user=Depends(auth.get_current_user)):
    agent = crud.update_agent(db, agent_id, update_data)
    if not agent:
        raise HTTPException(status_code=404, detail="Agent not found")
    return agent

@app.delete("/agents/{agent_id}")
def delete_agent(agent_id: str, db: Session = Depends(get_db), user=Depends(auth.get_current_user)):
    success = crud.delete_agent(db, agent_id)
    if not success:
        raise HTTPException(status_code=404, detail="Agent not found")
    return {"detail": "Deleted"}

# -------------------------
# Executions
# -------------------------
@app.post("/executions", response_model=schemas.ExecutionOut)
def create_execution(exec_data: schemas.ExecutionCreate, db: Session = Depends(get_db), user=Depends(auth.get_current_user)):
    return crud.create_execution(db, exec_data)

@app.get("/executions/{agent_id}", response_model=List[schemas.ExecutionOut])
def get_executions(agent_id: str, db: Session = Depends(get_db), user=Depends(auth.get_current_user)):
    return crud.get_executions_by_agent(db, agent_id)

# -------------------------
# Logs
# -------------------------
@app.get("/logs/{execution_id}", response_model=List[schemas.ExecutionLogOut])
def get_logs(execution_id: str, db: Session = Depends(get_db), user=Depends(auth.get_current_user)):
    return crud.get_logs_for_execution(db, execution_id)

# -------------------------
# Flowchart
# -------------------------
@app.post("/flowchart/nodes")
def save_nodes(nodes: List[schemas.FlowchartNodeCreate], db: Session = Depends(get_db), user=Depends(auth.get_current_user)):
    return crud.save_flowchart_nodes(db, nodes)

@app.post("/flowchart/edges")
def save_edges(edges: List[schemas.FlowchartEdgeCreate], db: Session = Depends(get_db), user=Depends(auth.get_current_user)):
    return crud.save_flowchart_edges(db, edges)

@app.get("/flowchart/{agent_id}")
def get_flowchart(agent_id: str, db: Session = Depends(get_db), user=Depends(auth.get_current_user)):
    return crud.get_flowchart_by_agent(db, agent_id)
