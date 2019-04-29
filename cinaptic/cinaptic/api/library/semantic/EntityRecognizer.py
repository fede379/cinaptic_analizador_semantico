from clients.textrazorClient import TextRazorClient
TEXT_RAZOR_API_KEY_1 = "a6ccb809d4fe98c43b3492548298edf0b7d4ceb67aea9c58930eacc9"
TEXT_RAZOR_API_KEY_2 = "8cdcb70d8ae86e21ac318e3d8cd6fb2b456f6e9f984d39267fa78d32"
TEXT_RAZOR_API_KEY_3 = "9ef66800304909b23755c07c8cffda50a1f4bfc2462327c32d3b65d7"
ENTITES = "entities"
TOPICS = "topics"
RELATIONS = "relations"
ENTITY = "entity"
RELEVANCE = "relevance"
LONG_NAME = "long_name"
WIKI = "wiki"
WIKI_DATA_ID = "wikidataid"
WIKI_REGEX = "/wiki/"


class EntityRecognizer:
    """

    """
    def recognize_from_url(self, url = "", umbral = 0, limit = 1):
        """

        :param url:
        :param umbral:
        :param limit:
        :return:
        """
        try:
            text_razor_client = TextRazorClient()
            text_razor_entities = text_razor_client.get_entities_from_url(url=url)
            entities_recognized = self.recognize(tr_entities=text_razor_entities, umbral=umbral)
            return self.order_entities_by_relevance(entities_recognized, limit=limit)
        except Exception as e:
            print(str(e))

        return []

    def recognize_from_text(self, text = "", umbral = 0, limit = 1):
        """

        :param text:
        :param umbral:
        :param limit:
        :return:
        """
        try:
            text_razor_client = TextRazorClient()
            text_razor_entities = text_razor_client.get_entities_from_text(text=text)
            
            entities_recognized = self.recognize(tr_entities=text_razor_entities, umbral=umbral)
            return self.order_entities_by_relevance(entities_recognized, limit=limit)
        except Exception as e:
            print(str(e))
            raise Exception(str(e))

    def order_entities_by_relevance(self, entities = [], limit = 1):
        """

        :param entities:
        :param limit:
        :return:
        """
        newlist = sorted(entities, key=lambda k: k[RELEVANCE], reverse=False)
        distinct_list = {x[ENTITY]: x for x in newlist}.values()
        distinct_list = sorted(distinct_list, key=lambda k: k[RELEVANCE], reverse=True)

        return distinct_list[:limit]

    def recognize(self, tr_entities = [], umbral = 0):
        """

        :param tr_entities:
        :param umbral:
        :return:
        """
        entities = []
        for i, entity in enumerate(tr_entities.entities()):
            #if entity.relevance_score >= umbral:
            # print(self.parse_entity(entity))
            entities.append(self.parse_entity(entity))

        return entities

    def parse_entity(self, entity = {}):
        """

        :param entity:
        :return:
        """
        aux = entity.wikipedia_link.split(WIKI_REGEX)
        return {
                # ENTITY: entity.wikipedia_link.split(WIKI_REGEX)[1],
                ENTITY: aux[len(aux) - 1] if len(aux) != 1 else entity.id,
                RELEVANCE: entity.relevance_score,
                LONG_NAME: entity.id,
                WIKI: entity.wikipedia_link,
                WIKI_DATA_ID: entity.wikidata_id
            }


er = EntityRecognizer()
# tests = er.recognize_from_text("machine learning python algorithms", 0, 5)
# print(tests)
t2 = er.recognize_from_url('http://en.wikipedia.org/wiki/Machine_learning', 0.75, 10)
print(t2)
print(len(t2))