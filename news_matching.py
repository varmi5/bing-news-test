import requests
from openai import OpenAI
import os
from openai.types.chat.completion_create_params import ResponseFormat

# these two are my own keys , alter to your keys if you prefer

bing_api_key = '2f205aa286254e00a0dee2b4de582869'

open_ai_api_key = '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'

#This endpoint returns news articles based on the user's search query. If the search query is empty, the call returns the top news articles.
bing_endpoint = 'https://api.bing.microsoft.com/v7.0/news/search'

# Function to call news articles from api 

def news_articles_output(url):
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
    
 # function for the sytem prompt      
def gpt_response(prompt):
    client = OpenAI(api_key = os.environ.get('OPENAI_API_KEY', open_ai_api_key))
    response = client.chat.completions.create(
        model = 'gpt-3.5-turbo',
        messages = [
        {'role': 'system', 
        'content': 'You are an assistant that will help me rank articles based on a user profile. If the user profile is the most similar to the article put it first. The format of the output for the 5 articles should look like this <title> Title </title> , <summary> summary of description goes here </summary>, <link> link goes here </link>'},
        {'role': 'user', 'content': prompt} ],
        
        temperature = 0.2
    )
    output = response.choices[0].message.content
    
    return output

def get_top_articles_with_gpt(url, profile):
    articles = news_articles_output(url)
    # Generate a prompt for GPT-3.5 to select the top 5 articles based on the user's profile
    gpt_prompt = f"Select the top 5 articles from the following list based on the user's profile:\n {articles} \n Profile: {profile}"
    
    gpt_output = gpt_response(gpt_prompt)
    
    print(gpt_output)


site_url1 = 'techcrunch.com'

profile1 = {
    "Name": "Titus Sharpe",
    "Job Role": "Founder & NED",
    "Company URL": "mvfglobal.com",
    "Sector": "Custom Generation and Digital Media",
    "Company Postcode": "N1 6QL"
}


print(get_top_articles_with_gpt(site_url1,profile1))