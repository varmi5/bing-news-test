# bing-news-test

### Recommends top articles from each news website based on user profile

### Packages to be Downloaded

Install latest OpenAI API library ( openai 1.10.0 ) - this code may not work with the older openai libraries | also requests & os libraries |

### What you can modify:

#### For news_articles_output() 

- count - can increase so there is more articles but will make the gpt process for longer
- freshness - choice between day, week or month on api doc
- TextDecorations and TextFormat - enabled this to maybe make it easier for gpt to try to see keypoints to make it analyse articles quicker

#### For gpt_response():
- can change model depending on openai docs
- in messages you can modify {content} for both system and user. For system, I have given it an explanation on what to output. For prompt it takes in both article and profile and chooses best articles within these parameters. There are also other roles within messages like assistant but do not need them in this case
- can change temperature but i kept it at 0.2 as 0 is better for consistency and conciseness
- can have json_format for output response but decided to use normal

#### for get_top_articles_with_gpt()
- can change prompt to specify it


