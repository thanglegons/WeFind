from cache.redis_cache import RedisCache
from services.distance_getter import DistanceGetter
from services.location_searcher import LocationSearcher
from services.routing import Routing


def main():
    # loc_sea = LocationSearcher()
    # dis_get = DistanceGetter()
    # str_a = 'GHTK Building'
    # str_b = '216 trần quốc hoàn, cầu giấy, hà nội'
    # cor_a = loc_sea.get_coordinate(str_a)
    # cor_b = loc_sea.get_coordinate(str_b)
    # dis_ab = dis_get.get_distance(cor_a, cor_b)

    # locations = ['GHTK Building', '216 trần quốc hoàn, cầu giấy, hà nội', 'đại học công nghệ, đại học quốc gia hà nội, cầu giấy, hà nội',
    #              '1 Đ. Thanh Niên, Trúc Bạch, Ba Đình, Hà Nội, Vietnam']
    # routing = Routing()
    # res = routing.get_route(locations)
    # print(res)

    redis = RedisCache()

    redis.set('123', '123')
    print(redis.get('123').decode('utf-8'))
    print(redis.get('333'))


if __name__ == '__main__':
    main()
