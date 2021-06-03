import json
import time

import requests
import config
from database import redis_cache

from common.coordinates import Coordinates
from database.eswh import es, ES_INDEX


class Strategy:

    def get_result(self, text):
        pass


class RedisCacheStrategy(Strategy):

    def get_result(self, text):
        return redis_cache.get_cache(text)


class ESStrategy(Strategy):

    def get_result(self, text):
        res = es.search(index=ES_INDEX, body={
            'query': {
                'multi_match': {
                    'query': text,
                    'fields': ["name", "address"],
                    "minimum_should_match": "90%"
                }
            }
        })
        if res is None:
            return None
        hits = res['hits']['hits']
        if len(hits) == 0:
            return None
        top_hit = hits[0]
        lat = top_hit['_source']['lat']
        log = top_hit['_source']['long']
        respond = {
            'features': [
                {
                    'geometry': {
                        'coordinates': [
                            log,
                            lat
                        ]
                    }
                }
            ]
        }
        return json.dumps(respond)


class APIStrategy(Strategy):
    API_URL = 'https://apis.wemap.asia/geocode-1/search'

    def get_result(self, text):
        result = requests.get(self.API_URL, params={'text': text, 'key': config.API_KEY})
        if result.status_code != 200:
            return None
        return result.content


class LocationSearcher:

    strategies = [RedisCacheStrategy(), ESStrategy(), APIStrategy()]

    def get_coordinate(self, text):
        result = None
        start_time = time.time()
        for strategy in self.strategies:
            result = strategy.get_result(text)
            if result is not None:
                end_time = time.time()
                print('Got', text, 'by', strategy.__class__, 'took', end_time - start_time)
                break
        if result is None:
            return None
        json_result = json.loads(result)
        if 'features' not in json_result or len(json_result['features']) == 0:
            return None

        top_feature = json_result['features'][0]
        raw_coordinates = top_feature['geometry']['coordinates']

        redis_cache.set_cache(text, result)

        return Coordinates(raw_coordinates[1], raw_coordinates[0])
