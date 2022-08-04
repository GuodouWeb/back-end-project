# -*- coding: utf-8 -*-

import requests

url = "http://192.168.52.212/api/v1/user/tixian"


def rq_rsult(url):
    r = requests.get(url)
    print(r.json())


from concurrent.futures import ThreadPoolExecutor

theard_pool = ThreadPoolExecutor(max_workers=1)

for i in range(1):
    theard_pool.submit(rq_rsult, url)
theard_pool.shutdown(wait=True)
