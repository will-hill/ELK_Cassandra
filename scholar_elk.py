import scholarly
proxies = {'http' : 'socks5://127.0.0.1:9050', 'https': 'socks5://127.0.0.1:9050'}
scholarly.scholarly.use_proxy(**proxies)
raw_results = scholarly.search_pubs_query('china virus')
first_result = next(raw_results)

print(first_result.bib)
##


from elasticsearch import Elasticsearch
import scholarly
import time
from spacy import displacy
import en_core_web_sm
nlp = en_core_web_sm.load()
from wordcloud import WordCloud

##
# SCRAPE
results = []
for index, result in enumerate(scholarly.search_pubs_query('china virus')):
    results.append(result.bib)
    if index > 3: break
clob = '. '.join(['.  '.join(r.values()) for r in results])

##
wordcloud = WordCloud(background_color="white", max_words=5000, contour_width=3, contour_color='steelblue')
wordcloud.generate(clob)
img = wordcloud.to_image()
##
displacy.render(nlp(big_clob), style='ent', jupyter=False)
##
# Connect to the elastic cluster
es = Elasticsearch([{'host': 'localhost', 'port': 9200}])
print(es)

##
def print_process(search_terms, limit=3, wait_time=30):
    # .search_author .search_keyword
    n = 0
    search = scholarly.search_pubs_query(search_terms)
    for result in search:
        n += 1
        result = result.bib
        abstract = result['abstract']
        tokens = nltk.word_tokenize(result)
        tagl = nltk.pos_tag(tokens)
        # NER the abstract
        # Topic Model the abstract


        res = es.index(index='scholar_scrape', doc_type='scholar_search', id=result['url'], body=result)
        print(result)
        if n >= limit:
            break

    time.sleep(wait_time)


print_process('virus china', limit=100, wait_time=10)

# Retrieve the author's data, fill-in, and print
search_query = scholarly.search_author('Steven A Cholewiak')
author = next(search_query).fill()
print(author)

# Print the titles of the author's publications
print([pub.bib['title'] for pub in author.publications])

# Take a closer look at the first publication
pub = author.publications[0].fill()
print(pub)

# Which papers cited that publication?
print([citation.bib['title'] for citation in pub.get_citedby()])
