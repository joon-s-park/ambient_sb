#!/usr/bin/env python3
import traceback
import itertools
import requests
import json
import time

def decode(r):
    if r.status_code != 200:
        try:
            if r.status_code == 400 and r.json()["error"] == "# premium feature":
                print("Warning, this API call failed because user is not a RescueTime Premium User")
                print(traceback.format_exc())
                return None
        except:
            None
        print("ERROR API returned status code: " + str(r.status_code))
        print(r.text)
        print(traceback.format_exc())
        return None
    try:
        return r.json()
    except Exception as e:
        print("\nError Decoding JSON:\n" + r.text + "\n\n")
        print(traceback.format_exc())
        return None


def _analytics_api(api_key):

    location = "https://www.rescuetime.com/anapi/data"
    payload={"format" : "json", "key": api_key}

    r = requests.get(location, params=payload)

    return decode(r)


def _detail_summary_feed_api(api_key):

    location = "https://www.rescuetime.com/anapi/daily_summary_feed"
    payload={"key": api_key}

    r = requests.get(location, params=payload)

    return decode(r)

def _alerts_feed_api(api_key):

    location = "https://www.rescuetime.com/anapi/alerts_feed"
    payload={"key": api_key, "op": "list"}

    r = requests.get(location, params=payload)

    return decode(r)


def _highlights_feed_api(api_key):

    location = "https://www.rescuetime.com/anapi/highlights_feed"
    payload={"key": api_key}

    r = requests.get(location, params=payload)

    return decode(r)

# Premium Feature
def _highlights_post_api(api_key, description, source):

    location = "https://www.rescuetime.com/anapi/highlights_post"
    payload={"key": api_key, "highlight_date": str(int(time.time())), "description": description, "source" : source}

    r = requests.post(location, params=payload)

    return decode(r)
    
# Not Private
def get_productivity_today(api_key):
    analytics = _analytics_api(api_key)

    row_headers = analytics["row_headers"]
    #print(row_headers)
    rows = analytics["rows"]
    rows.sort()
    rows = list(rows for rows,_ in itertools.groupby(rows))

    productivity = {}
    total_time = 0
    for row in rows:
        total_time += row[1]
        if not row[5] in productivity:
            productivity[row[5]] = row[1]
        else:
            productivity[row[5]] += row[1]

    productivity["TotalTimeSeconds"] = total_time
    return productivity


def get_yesterday_report(api_key):
    daily_reports = _detail_summary_feed_api(api_key)
    #TODO not sure whether this gives the first or last
    return daily_reports[-1]

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# Run unit tests if this file is run alone
#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
if __name__ == "__main__":

    print("Running RescueAPI unit test...")

    api_key = input("Please input a valid API key followed by an endline: ")

    if api_key == "":
        # api_key = "YOU CAN TEMPORARILY PUT AN API KEY HERE, BUT DONT COMMIT IT"
        api_key = "B63ooE5FEezS1kdXD4kAwVCTuPEqBWFoUjHuJ_Yf"

    print("Working with key \"" + api_key +  "\"")

    # Get Analytics
    analytics = _analytics_api(api_key)
    assert type(analytics) is dict
    print("+ Analytics Endpoint - PASS")

    # Get Details
    detail_summary = _detail_summary_feed_api(api_key)
    assert type(detail_summary) is list
    #print(detail_summary)
    print("+ Details Endpoint - PASS")

    user = get_productivity_today(api_key)
    assert type(user) is dict
    print(user)

    yesterday = get_yesterday_report(api_key)
    assert type(yesterday) is dict
    print(yesterday)

    '''We currently don't have plans to use alerts'''
    # Get User Set Alerts
    alerts = _alerts_feed_api(api_key)
    #print("Number of alerts set on this account: " + str(len(alerts)))


    '''Highlights are behind a paywall. We do.'''
    # Get Highlights
    #highlights = _highlights_feed_api(api_key)
    #print(highlights)
    #
    # Try Adding a Highlight
    #_highlights_post_api(api_key, "Integration TEST", "Test")
    #highlights = _highlights_feed_api(api_key)
    #print(highlights)
    

    print("\n\n***PASS***\n\n")

