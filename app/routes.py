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


# Add node
@router.post("/nodes")
def add_node(
    node: NodeCreate,
    db: Session = Depends(get_db)
):

    if not node.name or not node.name.strip():
        raise HTTPException(
            status_code=400,
            detail="Name missing or duplicate"
        )

    existing = db.query(Node).filter(
        Node.name == node.name
    ).first()

    if existing:
        raise HTTPException(
            status_code=400,
            detail="Name missing or duplicate"
        )

    new_node = Node(
        name=node.name
    )

    db.add(new_node)
    db.commit()
    db.refresh(new_node)

    return new_node


# Get nodes
@router.get("/nodes")
def get_nodes(
    db: Session = Depends(get_db)
):
    return db.query(Node).all()


# Add edge
@router.post("/edges")
def add_edge(
    edge: EdgeCreate,
    db: Session = Depends(get_db)
):

    if not edge.source or not edge.destination:
        raise HTTPException(
            status_code=400,
            detail="Source/destination missing"
        )

    if edge.latency <= 0:
        raise HTTPException(
            status_code=400,
            detail="Latency must be greater than 0"
        )

    source = db.query(Node).filter(
        Node.name == edge.source
    ).first()

    destination = db.query(Node).filter(
        Node.name == edge.destination
    ).first()

    if not source or not destination:
        raise HTTPException(
            status_code=400,
            detail="Source or destination node not found"
        )

    existing_edge = db.query(Edge).filter(
        Edge.source_id == source.id,
        Edge.destination_id == destination.id
    ).first()

    if existing_edge:
        raise HTTPException(
            status_code=400,
            detail="Edge already exists"
        )

    new_edge = Edge(
        source_id=source.id,
        destination_id=destination.id,
        latency=edge.latency
    )

    db.add(new_edge)
    db.commit()
    db.refresh(new_edge)

    return {
        "id": new_edge.id,
        "source": edge.source,
        "destination": edge.destination,
        "latency": edge.latency
    }


# Get edges
@router.get("/edges")
def get_edges(
    db: Session = Depends(get_db)
):

    edges = db.query(Edge).all()

    result = []

    for edge in edges:

        source = db.query(Node).filter(
            Node.id == edge.source_id
        ).first()

        destination = db.query(Node).filter(
            Node.id == edge.destination_id
        ).first()

        result.append({
            "id": edge.id,
            "source": source.name,
            "destination": destination.name,
            "latency": edge.latency
        })

    return result


# Shortest route
@router.post("/routes/shortest")
def find_route(
    request: RouteRequest,
    db: Session = Depends(get_db)
):

    source_node = db.query(Node).filter(
        Node.name == request.source
    ).first()

    destination_node = db.query(Node).filter(
        Node.name == request.destination
    ).first()

    if not source_node or not destination_node:
        raise HTTPException(
            status_code=400,
            detail="Invalid or non-existent nodes"
        )

    all_edges = []

    edge_rows = db.query(Edge).all()

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
        return {
            "error": f"No path exists between {request.source} and {request.destination}"
        }

    history = RouteHistory(
        source=request.source,
        destination=request.destination,
        total_latency=result["total_latency"],
        path=json.dumps(result["path"])
    )

    db.add(history)
    db.commit()

    return result


# Route history
@router.get("/routes/history")
def get_history(
    db: Session = Depends(get_db)
):

    history = db.query(RouteHistory).all()

    result = []

    for item in history:

        result.append({
            "id": item.id,
            "source": item.source,
            "destination": item.destination,
            "total_latency": item.total_latency,
            "path": json.loads(item.path),
            "created_at": item.created_at
        })

    return result


# Delete node
@router.delete("/nodes/{node_id}")
def delete_node(
    node_id: int,
    db: Session = Depends(get_db)
):
    node = db.query(Node).filter(
        Node.id == node_id
    ).first()

    if not node:
        raise HTTPException(
            status_code=404,
            detail="Node not found"
        )

    db.delete(node)
    db.commit()

    return {
        "message": "Node deleted"
    }


# Delete edge
@router.delete("/edges/{edge_id}")
def delete_edge(
    edge_id: int,
    db: Session = Depends(get_db)
):
    edge = db.query(Edge).filter(
        Edge.id == edge_id
    ).first()

    if not edge:
        raise HTTPException(
            status_code=404,
            detail="Edge not found"
        )

    db.delete(edge)
    db.commit()

    return {
        "message": "Edge deleted"
    }