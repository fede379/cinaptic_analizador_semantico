import os
import sys; sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))
import bs4 as bs
# import urllib2
import importlib

from consts import *
from pattern.web import Bing, SEARCH

# END_POINT_BING = "https://www.bing.com/search?q={0}&qs=n&form=QBLH&sp=-1&pq={0}&sc=2-0&sk=&cvid=105FD159528E4D039AEB0EA503BE825E&first={1}"

class BingClient:

    def get_urls(self, q = "", n = 1, limit = 1):
        url = []
        importlib.reload(sys)
        # sys.setdefaultencoding(GOOGLE_API_ENCODING)
        engine_google = Bing(license=None, throttle=0.5, language=None)
        for i in range(1, (n + 1)):
            for result in engine_google.search(q, start=i, count=10, type=SEARCH, cached=False):
                url.append(result.url)

        return url[:limit]