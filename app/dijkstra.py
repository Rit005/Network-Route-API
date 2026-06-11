import heapq

def build_graph(edges):

    graph = {}

    for source, destination, latency in edges:

        if source not in graph:
            graph[source] = []

        if destination not in graph:
            graph[destination] = []

        graph[source].append(
            (destination, latency)
        )

    return graph


def shortest_path(
        graph,
        source,
        destination
):

    if source not in graph:
        return None

    if destination not in graph:
        return None

    distances = {
        node: float("inf")
        for node in graph
    }

    distances[source] = 0

    parent = {}

    heap = [(0, source)]

    while heap:

        current_distance, node = heapq.heappop(
            heap
        )

        if current_distance > distances[node]:
            continue

        if node == destination:
            break

        for neighbor, latency in graph[node]:

            new_distance = (
                current_distance +
                latency
            )

            if new_distance < distances[neighbor]:

                distances[neighbor] = new_distance

                parent[neighbor] = node

                heapq.heappush(
                    heap,
                    (
                        new_distance,
                        neighbor
                    )
                )

    if distances[destination] == float("inf"):
        return None

    path = []

    current = destination

    while current != source:

        if current not in parent:
            return None

        path.append(current)

        current = parent[current]

    path.append(source)

    path.reverse()

    return {
        "total_latency": distances[destination],
        "path": path
    }