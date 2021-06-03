import json

import requests

import config
from database import redis_cache
from common.coordinates import Coordinates
from common.distance import Distance


class Strategy:

    def get_result(self, point_start: Coordinates, point_end: Coordinates):
        pass


class RedisCacheStrategy(Strategy):

    @staticmethod
    def encode_key(point_start: Coordinates, point_end: Coordinates):
        return str(point_start) + '|' + str(point_end)

    def get_result(self, point_start: Coordinates, point_end: Coordinates):
        encoded_key = RedisCacheStrategy.encode_key(point_start, point_end)
        return redis_cache.get_cache(encoded_key)


class APIStrategy(Strategy):
    API_URL = 'https://apis.wemap.asia/route-api/route?point={point_start}&point={point_end}&type=json&locale=en-US&vehicle=car&weighting=fastest&elevation=false&key={api_key}'

    def get_result(self, point_start: Coordinates, point_end: Coordinates):
        result = requests.get(self.API_URL.format(point_start=str(point_start),
                                                  point_end=str(point_end),
                                                  api_key=config.API_KEY))
        if result.status_code != 200:
            return None
        return result.content


class DistanceGetter:
    strategies = [RedisCacheStrategy(), APIStrategy()]

    def get_distance(self, point_start: Coordinates, point_end: Coordinates):
        result = None
        for strategy in self.strategies:
            result = strategy.get_result(point_start, point_end)
            if result is not None:
                print('Got', RedisCacheStrategy.encode_key(point_start, point_end), 'by', strategy.__class__)
                break
        if result is None:
            return None
        json_result = json.loads(result)
        if 'paths' not in json_result or len(json_result['paths']) == 0:
            return None

        top_path = json_result['paths'][0]

        redis_cache.set_cache(RedisCacheStrategy.encode_key(point_start, point_end), result)

        return Distance(top_path['distance'], top_path['time'])
