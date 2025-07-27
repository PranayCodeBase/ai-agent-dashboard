from typing import Optional, List
from datetime import datetime
from uuid import UUID
from pydantic import BaseModel, Field, EmailStr
import enum


# Enums must match models
class AgentStatus(str, enum.Enum):
    Running = "Running"
    Idle = "Idle"
    Error = "Error"

class ExecutionStatus(str, enum.Enum):
    Success = "Success"
    Failure = "Failure"

class NodeType(str, enum.Enum):
    Start = "Start"
    Process = "Process"
    Decision = "Decision"
    End = "End"


# ------------------------
# Agent
# ------------------------

class AgentBase(BaseModel):
    name: str
    description: Optional[str] = None
    status: AgentStatus = AgentStatus.Idle
    enabled: bool = True
    created_by: str

class AgentCreate(AgentBase):
    pass

class AgentUpdate(BaseModel):
    description: Optional[str]
    status: Optional[AgentStatus]
    enabled: Optional[bool]
    last_active_at: Optional[datetime]

class AgentOut(AgentBase):
    id: UUID
    created_at: datetime
    last_active_at: datetime

    class Config:
        from_attributes = True


# ------------------------
# Execution
# ------------------------

class ExecutionCreate(BaseModel):
    agent_id: UUID
    status: ExecutionStatus
    start_time: datetime
    end_time: datetime

class ExecutionOut(BaseModel):
    id: UUID
    agent_id: UUID
    status: ExecutionStatus
    start_time: datetime
    end_time: datetime

    class Config:
        from_attributes = True


# ------------------------
# Execution Logs
# ------------------------

class ExecutionLogOut(BaseModel):
    id: UUID
    execution_id: UUID
    log_text: str

    class Config:
        from_attributes = True


# ------------------------
# Flowchart
# ------------------------

class FlowchartNodeCreate(BaseModel):
    agent_id: UUID
    type: NodeType
    label: str
    position_x: str
    position_y: str

class FlowchartNodeOut(FlowchartNodeCreate):
    id: UUID

    class Config:
        from_attributes = True

class FlowchartEdgeCreate(BaseModel):
    agent_id: UUID
    from_node: UUID
    to_node: UUID

class FlowchartEdgeOut(FlowchartEdgeCreate):
    id: UUID

    class Config:
        from_attributes = True


# ------------------------
# Auth
# ------------------------

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Optional[str] = None

class LoginInput(BaseModel):
    username: str
    password: str

class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str

class UserOut(BaseModel):
    id: str
    username: str
    email: EmailStr

    class Config:
        from_attributes = True  # if you're on Pydantic v2