import re

API_KEY = "AIzaSyD6rJt9J0ZeV_OCANSbsuCPskwkAA1mJbk"
SEARCH_ENGINE_ID = "9128acdb3f4e14bf8"
GOOGLE_STORE_DETAIL_URL = "play.google.com/store/apps/details"

LIST_LANGUAGES = ["vi", "en"]
LIST_COUNTRY = ["vn", "us"]

# https://play.google.com/store/apps/details?id=me.gira.widget.countdown&hl=en_US

ID_PATTERN = re.compile(r"id=(.*?)&")

COLUMNS = ["title", "url", "appId", "developer", "developerEmail",
           "developerWebsite", "released", "developerAddress", "realInstalls", ]

INVALID_EMAILS_LIST = []