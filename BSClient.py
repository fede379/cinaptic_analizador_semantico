from bs4 import BeautifulSoup
import urllib.request

class BSClient:
    def getTextFromUrl(self, uri=None):
        text = ''
        if uri is not None:
            html_doc = urllib.request.urlopen(uri)
            soup = BeautifulSoup(html_doc, 'html.parser')
            wiki_content = soup.find('div', class_='mw-content-ltr', id='mw-content-text')
            content = wiki_content.find_all('p')
            for i in content:
                print(i.prettify())
            return text.join(list(map(lambda x: x.find(text=True), content)))
        return text


bs = BSClient()
uri = 'https://es.wikipedia.org/wiki/Minecraft'
ctext = bs.getTextFromUrl(uri)

print(ctext)