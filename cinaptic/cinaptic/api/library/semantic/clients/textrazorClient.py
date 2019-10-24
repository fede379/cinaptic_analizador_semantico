import textrazor
from .consts import *
import json
class TextRazorClient:

    def get_entities_from_url(self, url):
        try:
            textrazor.api_key = TEXT_RAZOR_API_KEY_1
            client = textrazor.TextRazor(extractors=[ENTITIES, RELATIONS, TOPICS])
            client.set_cleanup_mode("cleanHTML")
            response = client.analyze_url(url)
            return response
        except Exception as e:
            print("ERROR For URL: {0} - {1}".format(url, str(e)))
            raise Exception()

    def get_entities_from_text(self, text):
        try:
            textrazor.api_key = TEXT_RAZOR_API_KEY_1
            client = textrazor.TextRazor(extractors=[ENTITIES, RELATIONS, TOPICS])
            response = client.analyze(text)
            return response
        except Exception as e:
            print(str(e))
            raise Exception(str(e))


# textrazorc = TextRazorClient()
# response = textrazorc.get_entities_from_text("water quality satellite monitoring algae image processing")

# for entity in response.entities():
# # print(list(response.matching_rules()))
#     print("Entity ID : "+str(entity.id), " - RelevanceScore : "+str(entity.relevance_score), " - ConfidenceScore : "+str(entity.confidence_score))