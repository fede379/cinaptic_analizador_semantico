# To change this license header, choose License Headers in Project Properties.
# To change this template file, choose Tools | Templates
# and open the template in the editor.

import os, sys; sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))
from pattern.web import Google, SEARCH
from consts import *

class GoogleClient:
    def get_urls(self, q = "", n = 1, limit = 1):
        url = []
        reload(sys)
        sys.setdefaultencoding(GOOGLE_API_ENCODING)
        engine_google = Google(license=GOOGLE_API_KEY, language=GOOGLE_API_LANG)
        for i in range(1, (n + 1)):
            for result in engine_google.search(q, start=i, count=10, type=SEARCH, cached=False):
                url.append(result.url)

        return url[:limit]
