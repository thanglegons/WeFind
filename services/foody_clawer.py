import json
import uuid

import requests
from tqdm import tqdm

from database.eswh import es, ES_INDEX, ES_DOC


class Crawler:
    IDS = [(218, 64939)]  # Hanoi only
    SIZE_PER_TIME = 10

    def crawl(self):
        for city_id, count in self.IDS:
            headers = {
                'Pragma': 'no-cache',
                'DNT': '1',
                'Accept-Encoding': 'gzip, deflate, br',
                'Accept-Language': 'en-US,en;q=0.9,vi;q=0.8,ja;q=0.7',
                'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36',
                'Accept': 'application/json, text/plain, */*',
                'Cache-Control': 'no-cache',
                'X-Requested-With': 'XMLHttpRequest',
                'Cookie': 'flg=vn; __ondemand_sessionid=z3s1lfqdsyds3c1yhkx5jpug; gcat=food; xfci=UFEFTVQQYQSMYBZ; floc={}'.format(
                    city_id),
                'Connection': 'keep-alive'
            }

            for i in tqdm(range(self.SIZE_PER_TIME), desc='City: {}'.format(city_id)):
                url = 'https://www.foody.vn/__get/Place/HomeListPlace?t=1562771365533&page={}&lat=15.121387&lon=108.804415&count={}&districtId=&cateId=&cuisineId=&isReputation=&type=1'.format(
                    i, 3)
                r = requests.get(url, headers=headers)
                p = json.loads(r.text)
                items = p['Items']
                for item in items:
                    name = item['Name']
                    address = item['Address']
                    lat = item['Latitude']
                    long = item['Longitude']
                    print(name, address, lat, long)
                    es.index(
                        index=ES_INDEX,
                        doc_type=ES_DOC,
                        id=uuid.uuid4(),
                        body={
                            'name': name,
                            'address': address,
                            'lat': lat,
                            'long': long
                        }
                    )
