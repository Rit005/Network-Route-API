import json

from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException

from sqlalchemy.orm import Session

from app.database import get_db

from app.models import Node
from app.models import Edge
from app.models import RouteHistory

from app.schemas import NodeCreate
from app.schemas import EdgeCreate
from app.schemas import RouteRequest

from app.dijkstra import build_graph
from app.dijkstra import shortest_path

router = APIRouter()

# Add nodes
@router.post("/nodes")
def add_node(
    node: NodeCreate,
    db: Session = Depends(get_db)
):

    existing = db.query(Node).filter(
        Node.name ==node.name
    ).first()

    if existing:
        raise HTTPException(
            status_code=400,
            detail="Node already exists"
        )

    new_node =Node(
        name=node.name
    )

    db.add(new_node)
    db.commit()
    db.refresh(new_node)

    return new_node

# add edges
@router.post("/edges")
def add_edge(
    edge: EdgeCreate,
    db: Session =Depends(get_db)
):

    source = db.query(Node).filter(
        Node.name== edge.source
    ).first()

    destination = db.query(Node).filter(
        Node.name==edge.destination
    ).first()

    if not source or not destination:

        raise HTTPException(
            status_code=404,
            detail="Node not found"
        )
    new_edge = Edge(
        source_id=source.id,
        destination_id=destination.id,
        latency=edge.latency
    )

    db.add(new_edge)
    db.commit()

    return {
        "message": "Edge added"
    }

# shortest route
@router.post("/routes/shortest")
def find_route(
    request: RouteRequest,
    db: Session = Depends(get_db)
):

    all_edges = []

    edge_rows = db.query(
        Edge
    ).all()

    for edge in edge_rows:

        source = db.query(Node).filter(
            Node.id == edge.source_id
        ).first()

        destination = db.query(Node).filter(
            Node.id == edge.destination_id
        ).first()

        all_edges.append(
            (
                source.name,
                destination.name,
                edge.latency
            )
        )

    graph = build_graph(all_edges)

    result = shortest_path(
        graph,
        request.source,
        request.destination
    )

    if not result:

        raise HTTPException(
            status_code=404,
            detail="No path found"
        )

    history = RouteHistory(
        source=request.source,
        destination=request.destination,
        total_latency=result["total_latency"],
        path=json.dumps(
            result["path"]
        )
    )

    db.add(history)
    db.commit()

    return result

# route history
@router.get("/routes/history")
def get_history(
    db: Session = Depends(get_db)
):

    history = db.query(
        RouteHistory
    ).all()

    return history