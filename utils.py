import re
from constant import *


def create_search_url(query, start=1, site=GOOGLE_STORE_DETAIL_URL):
    base_url = "https://customsearch.googleapis.com/customsearch/v1"
    cx = SEARCH_ENGINE_ID
    key = API_KEY
    url = f"{base_url}?cx={cx}&q={query}&siteSearch={site}&key={key}&start={start}"
    return url


def get_id_from_detail_url(url):
    try:
        return re.findall(ID_PATTERN, f"{url}&")[0]
    except:
        return None
