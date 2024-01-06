import streamlit as st
import requests

from google_play_scraper import search, app
import pandas as pd
# from Parallelizer import make_parallel
from utils import *
from constant import *
from sheet import Sheet


@st.cache_data
def get_search_result(query, n_hits=30, lang="en", country="us"):
    return search(query, n_hits=n_hits, lang=lang, country=country)


@st.cache_data
def get_app_detail(app_id):
    try:
        return app(app_id)
    except Exception as e:
        print(e)
        return None


# @make_parallel
def get_app_details(app_id):
    # return get_app_detail(app_id)
    list_app = [get_app_detail(x) for x in app_id]
    list_app = [x for x in list_app if x is not None]
    return list_app


@st.cache_data
def google_search(query, start=1):
    url = create_search_url(query, start=start)
    print(url)
    payload = {}
    headers = {
        'Accept': 'application/json'
    }

    response = requests.request("GET", url, headers=headers, data=payload)

    return response.json()


@st.cache_data
def get_app_id_from_search_result(query, start):
    results_list = google_search(query, start=start)
    items = results_list.get("items") or []
    links = [x.get("link") for x in items]
    app_ids = [get_id_from_detail_url(link) for link in links]
    app_ids = [x for x in app_ids if x is not None]
    print(f"Found {len(app_ids)} app ids")
    return app_ids


def main():
    st.title("Google Play Store Scraper")
    st.markdown(
        """
    This app retrieves the top search results for a given query on the Google Play Store.
    Guide to use:
     * Set up:
        - Create a google sheet and share it to `googlesheet@disco-freedom-410216.iam.gserviceaccount.com` with edit permission
        - Enter the name of the spreadsheet and worksheet in the sidebar
    * Enter your keyword in the sidebar
    * Select the number of results you want to retrieve
    * Select the language and country
    * Click on Search
    * Wait for the results to be displayed
    * If you want to save the results to a Google Sheet, check the checkbox and click on Search
    """
    )

    query = st.sidebar.text_input("Enter your keyword")
    list_url = st.sidebar.text_input("Enter your list url (leave blank if want to search from keyword)")
    n_hits = st.sidebar.slider("Number of results", 1, 500, 200, 50)
    # lang = st.sidebar.selectbox("Language", LIST_LANGUAGES)
    lang = "vi"
    country = st.sidebar.selectbox("Country", LIST_COUNTRY)
    min_realInstalls = st.sidebar.number_input("Min realInstalls", 0, 1000000, 50000,10000)
    
    is_save_to_sheet = st.sidebar.checkbox("Save to Google Sheet")
    spreadsheet_name = st.sidebar.text_input("Enter spreadsheet name", "Google Play Store Scraper")
    worksheet_name = st.sidebar.text_input("Enter worksheet name", "Sheet1")

    if st.sidebar.button("Search"):
        with st.spinner("Searching ..."):
            if not list_url:
                results_list = get_search_result(query, n_hits=n_hits, lang=lang, country=country)
                list_app_ids = [r["appId"] for r in results_list]
                set_app_ids = set(list_app_ids)
                original_len = len(set_app_ids)

                start = 1
                while len(set_app_ids) < n_hits and start < 100:
                    app_ids_search = get_app_id_from_search_result(
                        query, start=start)
                    if len(app_ids_search) == 0:
                        break
                    list_app_ids += app_ids_search
                    set_app_ids = set(list_app_ids)
                    start += 10
            else:
                list_app_ids = [get_id_from_detail_url(x) for x in list_url.split(" ") if get_id_from_detail_url(x) is not None]
                set_app_ids = set(list_app_ids)
                original_len = len(set_app_ids)

            st.markdown(f"Found {len(set_app_ids)} apps -> Trying to get details")

            results = get_app_details(list_app_ids)
            
            
            
        df = pd.DataFrame(results)
        df = df[COLUMNS]
        df = df.drop_duplicates(subset=["appId"]).reset_index(drop=True)
        df = df.drop_duplicates(subset=["developerEmail"]).reset_index(drop=True)
        df = df[df["realInstalls"] >= min_realInstalls]
        # Filter out invalid emails
        len_before = len(df)
        # df = df[~df["developerEmail"].str.contains("|".join(INVALID_EMAILS_LIST))]
        st.write(f"Filter out {len_before - len(df)} apps with invalid emails")
        st.markdown(f"# Top {len(df)} results")
        st.markdown(f"{original_len} apps founds in google store search")
        st.markdown(f"{len(df) - original_len} apps founds in extra search")
        
        if is_save_to_sheet:
            with st.spinner("Saving to Google Sheet ..."):
                sheet = Sheet(spreadsheet_name, worksheet_name)
                sheet.append_replace(df)
        st.dataframe(df)
        


if __name__ == "__main__":
    main()
