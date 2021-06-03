from typing import List

from external_lib.pyxfind import XFind

from common.coordinates import Coordinates


class Routing:

    @staticmethod
    def get_route(coordinates: List[Coordinates], distances):
        num = len(coordinates)
        flatten_distances = distances.flatten()
        router = XFind(num, list(flatten_distances))
        route = router.get_route()
        return [int(x) for x in route.split()]


