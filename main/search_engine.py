"""
Manticora search engine
By @djangoner
"""
import os
import dotenv
import logging
import manticoresearch
from manticoresearch.rest import ApiException
from pprint import pprint

from . import models

dotenv.load_dotenv()

logger = logging.getLogger("SearchEngine")

# Defining the host is optional and defaults to http://127.0.0.1:9308
# See configuration.py for a list of all supported configuration parameters.
MANTICORA_URL = os.environ.get("MANTICORA_URL")
if not MANTICORA_URL:
    logging.critical("MANTICORA_URL in environ not configured! Search engine probably not working!!!")
    MANTICORA_URL = "localhost:9308"
HOST = "http://{}".format(MANTICORA_URL)

configuration = manticoresearch.Configuration(
    host = HOST
)

def search(query, per_page=10, page=1, max_pages=10):
    """"Search in Manticora"""
    # # Enter a context with an instance of the API client
    with manticoresearch.ApiClient(configuration) as api_client:
        # Create an instance of the API class
        api_instance = manticoresearch.SearchApi(api_client)
        body = {
            "index":"docs",
            "query":{
                "match":{
                    "title,annotation": {
                        "query": query,
                        "operator": "or"
                    },
                },
            },
            "sort": [{'_score':'desc'}],
            "max_matches": per_page * max_pages,
            "limit": per_page,
            "offset": per_page * (page - 1)
        }

        try:
            # Performs a search
            api_response = api_instance.search(body)
        except ApiException as e:
            logging.exception("Exception when calling SearchApi->search: ", exc_info=e)
            return False
        else:
            # pprint(api_response)
            return api_response

def search_queryset(query, *args, **kwargs):
    "Create django queryset from search results"
    results = search(query, *args, **kwargs)
    if not results:
        return results
    #
    id_list = [int(i['_id']) for i in results.hits.hits]
    # print(id_list)
    qs = models.Document.objects.filter(pk__in=id_list).order_by()
    docs_ids = {doc.id: doc for doc in qs}
    results = []
    print(id_list, docs_ids, qs.count())
    for id in id_list:
        doc = docs_ids.get(id)
        if not doc:
            continue
        results.append(doc)
    #-- Add not sorted
    for doc in qs:
        if not doc in results:
            results.append(doc)
    return results
