import json
from typing import List

from flask import Flask, request

from common.coordinates import Coordinates
from common.edge import Edge
from common.node import Node
from common.respond import Respond
from services.distance_getter import DistanceGetter
from services.location_searcher import LocationSearcher

import numpy as np

from services.routing import Routing

app = Flask(__name__)

LOC_SEARCHER = LocationSearcher()
DISTANCE_GETTER = DistanceGetter()


@app.route('/routing')
def routing():
    points = request.args.getlist("point")
    coordinates: List[Coordinates] = [LOC_SEARCHER.get_coordinate(point) for point in points]
    if None in coordinates:
        return {'status: 400'}
    distances = get_distance(coordinates)
    routes = Routing.get_route(coordinates, distances)
    if routes is None:
        return {'status: 400'}
    respond = transform(points, coordinates, distances, routes)
    print(to_dict(respond))
    return to_dict(respond)


def to_dict(obj):
    return json.loads(json.dumps(obj, default=lambda o: o.__dict__))


def get_distance(coordinates):
    num = len(coordinates)
    distances = np.zeros([num, num], dtype=int)
    for start_ind in range(num):
        for end_ind in range(num):
            if start_ind == end_ind:
                continue
            start_coordinates = coordinates[start_ind]
            end_coordinates = coordinates[end_ind]
            distance = DISTANCE_GETTER.get_distance(start_coordinates, end_coordinates)
            if distance is None:
                distances[start_ind][end_ind] = 1000000007
            else:
                distances[start_ind][end_ind] = distance.time
    return distances


def transform(points, coordinates, distances, routes):
    nodes = []
    edges = []
    total_time = 0
    for node_ind in routes:
        nodes.append(Node(points[node_ind], coordinates[node_ind]))
    for i in range(len(routes) - 1):
        start_node_ind = routes[i]
        end_node_ind = routes[i + 1]
        start_node = nodes[i]
        end_node = nodes[i + 1]
        time = int(distances[start_node_ind][end_node_ind])
        edges.append(Edge(start_node, end_node, time))
        total_time += time
    return Respond(total_time=int(total_time), nodes=nodes, edges=edges)


if __name__ == '__main__':
    app.run()
