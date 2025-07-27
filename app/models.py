from sqlalchemy import Column, String, Boolean, DateTime, Enum, ForeignKey, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from datetime import datetime
import enum
import uuid

from .database import Base


class AgentStatus(str, enum.Enum):
    RUNNING = "Running"
    IDLE = "Idle"
    ERROR = "Error"

class ExecutionStatus(str, enum.Enum):
    SUCCESS = "Success"
    FAILURE = "Failure"

class NodeType(str, enum.Enum):
    START = "Start"
    PROCESS = "Process"
    DECISION = "Decision"
    END = "End"

class Agent(Base):
    __tablename__ = "agents"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String, nullable=False, unique=True)
    description = Column(Text)
    status = Column(Enum(AgentStatus), nullable=False, default=AgentStatus.IDLE)
    enabled = Column(Boolean, default=True)
    created_by = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)
    last_active_at = Column(DateTime, default=datetime.utcnow)

    executions = relationship("Execution", back_populates="agent")
    flowchart_nodes = relationship("FlowchartNode", back_populates="agent")
    flowchart_edges = relationship("FlowchartEdge", back_populates="agent")


class Execution(Base):
    __tablename__ = "executions"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    agent_id = Column(UUID(as_uuid=True), ForeignKey("agents.id"))
    status = Column(Enum(ExecutionStatus), nullable=False)
    start_time = Column(DateTime, nullable=False)
    end_time = Column(DateTime, nullable=False)

    agent = relationship("Agent", back_populates="executions")
    logs = relationship("ExecutionLog", back_populates="execution")


class ExecutionLog(Base):
    __tablename__ = "execution_logs"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    execution_id = Column(UUID(as_uuid=True), ForeignKey("executions.id"))
    log_text = Column(Text)

    execution = relationship("Execution", back_populates="logs")


class FlowchartNode(Base):
    __tablename__ = "flowchart_nodes"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    agent_id = Column(UUID(as_uuid=True), ForeignKey("agents.id"))
    type = Column(Enum(NodeType), nullable=False)
    label = Column(String)
    position_x = Column(String)  # store as string for simplicity; can be float
    position_y = Column(String)

    agent = relationship("Agent", back_populates="flowchart_nodes")


class FlowchartEdge(Base):
    __tablename__ = "flowchart_edges"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    agent_id = Column(UUID(as_uuid=True), ForeignKey("agents.id"))
    from_node = Column(UUID(as_uuid=True), ForeignKey("flowchart_nodes.id"))
    to_node = Column(UUID(as_uuid=True), ForeignKey("flowchart_nodes.id"))

    agent = relationship("Agent", back_populates="flowchart_edges")


class User(Base):
    __tablename__ = "users"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    username = Column(String, unique=True, nullable=False)
    email = Column(String, unique=True, nullable=False)
    hashed_password = Column(String, nullable=False)