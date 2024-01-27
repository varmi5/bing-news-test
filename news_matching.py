import requests
from openai import OpenAI
import os


# these two are my own keys , alter to your keys if you prefer

bing_api_key = '2f205aa286254e00a0dee2b4de582869'

open_ai_api_key = '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'

#This endpoint returns news articles based on the user's search query. If the search query is empty, the call returns the top news articles.
bing_endpoint = 'https://api.bing.microsoft.com/v7.0/news/search'

# Function to call news articles from api 

def news_articles_output(url):
    '''
    connects to bing api and returns 20 articles from the link given based on our parameters 
    '''
    headers = {'Ocp-Apim-Subscription-Key' : bing_api_key}
    # i set count as 20 and freshness to get articles from the past week, use sortBy Date to get 20 recent results
    params = {"q": url, "textDecorations": True, "textFormat": "HTML", 'count': 20, 'freshness' : 'Week', 'sortBy' : 'Date'}
    response = requests.get(bing_endpoint, headers=headers, params=params)
    response.raise_for_status()
    
    articles = response.json()['value']
    parsed_articles = []
    
    for article in articles:
        # these are the main atributes of the api response i require
        parsed_article = {
            'name': article['name'],
            'url': article['url'],
            'description': article['description']
            
        }
        parsed_articles.append(parsed_article)
    
    return parsed_articles
 
 
    
 # function to connect to open ai gpt.    
def gpt_response(prompt):
    client = OpenAI(api_key = os.environ.get('OPENAI_API_KEY', open_ai_api_key))
    response = client.chat.completions.create(
        model = 'gpt-3.5-turbo',
        # gave the system a format to output the answer
        messages = [
        {'role': 'system', 
        'content': 'Completely Read all the Articles provided. You are an assistant that will help me rank these articles given to you based on a user profile. Make sure to read all aspects of the user profile and match the best articles to these. If the user profile is the most similar to the article put it first. The format of the output for the 5 articles should look like this <title> Title </title> , <summary> summary of description goes here </summary>, <link> link goes here </link> . Make sure you do not just simply give the top 5 results but actually read through all results'},
        {'role': 'user', 'content': prompt} ],
        
        temperature = 0.2
    )
    # we need to extract just the 'content' not everything else
    output = response.choices[0].message.content
    return output




# combine the 2 above so that the user prompt alongside articles data and profile goes into gpt response
def get_top_articles_with_gpt(url, profile):
    articles = news_articles_output(url)
    # Generate a prompt for GPT-3.5 to select the top 5 articles based on the user's profile
    gpt_prompt = f"Select the 5 articles that best match the user profile from the following articles based on the user's profile:\n {articles} \n Profile: {profile}"
    
    # put our user gpt_prompt into gpt_response(function) alongside the articles and profile
    gpt_output = gpt_response(gpt_prompt)
    
    print(gpt_output)




site_url1 = 'techcrunch.com'

profile1 = {
    "Name": "John Applebee",
    "Job Role": "Apple Inc Professor of Engineering ",
    "Company URL": "apple.com",
    "Sector": " Iphone Engineering",
    "Company Postcode": "WC1H 0EA"
}

site_url2 = 'techcrunch.com'

profile2 = {
    "Name": "John Doe",
    "Job Role": "Managing Director",
    "Company URL": "bankofengland.co.uk",
    "Sector": "Central Banks",
    "Company Postcode": "Threadneedle Street"
}

get_top_articles_with_gpt(site_url2, profile2)