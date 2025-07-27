from datetime import datetime
from passlib.context import CryptContext
from sqlalchemy.orm import Session
from uuid import UUID
from typing import List, Optional
from . import models, schemas

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)

def create_user(db: Session, user: schemas.UserCreate):
    db_user = models.User(
        username=user.username,
        email=user.email,
        hashed_password=get_password_hash(user.password)
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

# ---------------------
# AGENTS
# ---------------------

def create_agent(db: Session, agent: schemas.AgentCreate) -> models.Agent:
    db_agent = models.Agent(**agent.dict())
    db.add(db_agent)
    db.commit()
    db.refresh(db_agent)
    return db_agent

def get_agent(db: Session, agent_id: UUID) -> Optional[models.Agent]:
    return db.query(models.Agent).filter(models.Agent.id == agent_id).first()

def get_all_agents(db: Session, name: Optional[str] = None, status: Optional[str] = None) -> List[models.Agent]:
    query = db.query(models.Agent)
    if name:
        query = query.filter(models.Agent.name.ilike(f"%{name}%"))
    if status:
        query = query.filter(models.Agent.status == status)
    return query.all()

def update_agent(db: Session, agent_id: UUID, update_data: schemas.AgentUpdate) -> Optional[models.Agent]:
    db_agent = get_agent(db, agent_id)
    if not db_agent:
        return None
    for key, value in update_data.dict(exclude_unset=True).items():
        setattr(db_agent, key, value)
    db.commit()
    db.refresh(db_agent)
    return db_agent

def delete_agent(db: Session, agent_id: UUID) -> bool:
    db_agent = get_agent(db, agent_id)
    if not db_agent:
        return False
    db.delete(db_agent)
    db.commit()
    return True


# ---------------------
# EXECUTIONS
# ---------------------

def create_execution(db: Session, execution: schemas.ExecutionCreate) -> models.Execution:
    db_exec = models.Execution(**execution.dict())
    db.add(db_exec)
    db.commit()
    db.refresh(db_exec)
    return db_exec

def get_executions_by_agent(db: Session, agent_id: UUID, start_time: Optional[datetime] = None, end_time: Optional[datetime] = None):
    query = db.query(models.Execution).filter(models.Execution.agent_id == agent_id)
    if start_time:
        query = query.filter(models.Execution.start_time >= start_time)
    if end_time:
        query = query.filter(models.Execution.end_time <= end_time)
    return query.all()


# ---------------------
# EXECUTION LOGS
# ---------------------

def get_logs_for_execution(db: Session, execution_id: UUID):
    return db.query(models.ExecutionLog).filter(models.ExecutionLog.execution_id == execution_id).all()


# ---------------------
# FLOWCHART
# ---------------------

def save_flowchart_nodes(db: Session, nodes: List[schemas.FlowchartNodeCreate]):
    db_nodes = [models.FlowchartNode(**node.dict()) for node in nodes]
    db.add_all(db_nodes)
    db.commit()
    return db_nodes

def save_flowchart_edges(db: Session, edges: List[schemas.FlowchartEdgeCreate]):
    db_edges = [models.FlowchartEdge(**edge.dict()) for edge in edges]
    db.add_all(db_edges)
    db.commit()
    return db_edges

def get_flowchart_by_agent(db: Session, agent_id: UUID):
    nodes = db.query(models.FlowchartNode).filter(models.FlowchartNode.agent_id == agent_id).all()
    edges = db.query(models.FlowchartEdge).filter(models.FlowchartEdge.agent_id == agent_id).all()
    return {"nodes": nodes, "edges": edges}
