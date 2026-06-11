from pydantic import BaseModel

class NodeCreate(BaseModel):
    name: str

class EdgeCreate(BaseModel):
    source: str
    destination: str
    latency: float

class RouteRequest(BaseModel):
    source: str
    destination: str