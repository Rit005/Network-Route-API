from app.dijkstra import build_graph
from app.dijkstra import shortest_path

edges = [

    ("A", "B", 14),
    ("A", "C", 7),
    ("C", "D", 5),
    ("B", "D", 10)

]

graph = build_graph(edges)

result = shortest_path(
    graph,
    "A",
    "D"
)

print(result)