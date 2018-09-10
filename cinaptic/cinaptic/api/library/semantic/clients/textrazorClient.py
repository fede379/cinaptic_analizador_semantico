import textrazor
from consts import *
class TextRazorClient:

    def get_entities_from_url(self, url):
        try:
            textrazor.api_key = TEXT_RAZOR_API_KEY_1
            client = textrazor.TextRazor(extractors=[ENTITES, RELATIONS, TOPICS])
            response = client.analyze_url(url)
            return response
        except Exception, e:
            print("ERROR For URL: {0} - {1}".format(url, str(e)))
            raise Exception()

    def get_entities_from_text(self, text):
        try:
            textrazor.api_key = TEXT_RAZOR_API_KEY_1
            client = textrazor.TextRazor(extractors=[ENTITES, RELATIONS, TOPICS])
            response = client.analyze(text)
            return response
        except Exception, e:
            print(str(e))
            raise Exception(str(e))
