from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import Float
from sqlalchemy import ForeignKey
from sqlalchemy import DateTime

from datetime import datetime

from app.database import Base

class Node(Base):
    __tablename__ = "nodes"

    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True, nullable=False)

class Edge(Base):
    __tablename__ = "edges"

    id = Column(Integer, primary_key=True)

    source_id = Column(
        Integer,
        ForeignKey("nodes.id")
    )

    destination_id = Column(
        Integer,
        ForeignKey("nodes.id")
    )

    latency = Column(Float, nullable=False)


class RouteHistory(Base):
    __tablename__ = "route_history"

    id = Column(Integer, primary_key=True)

    source = Column(String)

    destination = Column(String)

    total_latency = Column(Float)

    path = Column(String)

    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )