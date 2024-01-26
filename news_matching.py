import requests
from openai import OpenAI

bing_api_key = '2f205aa286254e00a0dee2b4de582869'

open_ai_api_key = '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'

# requests
#This endpoint returns news articles based on the user's search query. If the search query is empty, the call returns the top news articles.
bing_endpoint = 'https://api.bing.microsoft.com/v7.0/news/search	'

def matched_stories(newsite_url, profile):
    
    def news_articles_input(url):
        headers = {'Ocp-Apim-Subscription-Key' : bing_api_key}
        params = {"q": url, "textDecorations": True, "textFormat": "HTML", 'count': 20}
        response = requests.get(bing_endpoint, headers=headers, params=params)
        response.raise_for_status()
        search_results = response.json()['value']
        return print(search_results)
    
profile1 = {
    "Name": "Titus Sharpe",
    "Job Role": "Founder & NED",
    "Company URL": "mvfglobal.com",
    "Sector": "Customer Generation and Digital Media",
    "Company Postcode": "N1 6QL"
}

url1 = 'techcrunch.com'

print(matched_stories(url1,profile1))

