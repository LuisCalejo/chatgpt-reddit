import requests
import praw
import datetime
import json
import math
import time
from time import sleep
import os

LIMIT = 250 # Limit per request
TIMER = 2 # waiting time in seconds between each request to avoid being blocked by server
# SUBREDDITS = [
#     'all'
# ]
SUBREDDITS = ['technology', 'ChatGPT', 'Futurology', 'ProgrammerHumor', 'facepalm', 'MapPorn', 'nextfuckinglevel', 'gaming', 'technews', 'comics', 'Showerthoughts', 'Piracy', 'WorkReform', 'antiwork', 'thatHappened', 'OpenAI', 'HolUp', 'tech', 'anime_titties', 'news', 'IllegalLifeProTips', 'Teachers', 'gadgets', 'LifeProTips', 'CryptoCurrency', 'books', 'self', 'sweden', 'Superstonk', 'falloutnewvegas', 'webdev', 'wallstreetbets', '2westerneurope4u', 'singularity', 'stocks', 'memes', 'PoliticalCompassMemes', 'AnarchyChess', 'MachineLearning', 'italy', 'france', 'Genshin_Impact', 'Entrepreneur', 'marketing', 'de', 'coolguides', 'RocketLeague', 'crochet', 'skyrimvr', 'xqcow', 'Meditation', 'Professors', 'overemployed', 'privacy', 'newzealand', 'artificial', 'conspiracy', 'usajobs', 'ArtificialInteligence', 'osugame', 'radiohead', 'singapore', 'cybersecurity', 'Romania', 'homeassistant', 'soccercirclejerk', 'chatgpt_promptDesign', 'chatgpt_prompts_', 'chatgpt_newtech', 'ChatgptStories', 'GPT3', 'chatgpt_de', 'chatgpt_brasil', 'ChatGPTCoding', 'ChatGPTPro', 'ChatGPT_Prompts', 'ChatGPTGoneWild', 'ChatGPTJailbreak', 'ChatGPTPromptGenius', 'ChatGptDAN', 'ChatGPT_FR', 'StableDiffusion', 'midjourney', 'ChatGPTforWork', 'ChatGPTjailbreaks', 'ChatGPT4SearchEngines', 'ChatGPTforall', 'SideProject', 'ChatGPT_Sims', 'ChatGPT_LegalAdviceUS', 'ChatGPT_RPG', 'ChatGPTSucks', 'ChatGPTMemes', 'ChatGPTAdventures', 'crackGPT', 'ChatGPT4_AI_Talks', 'shitposting', 'developersIndia', 'chatGPT4userRs', 'ChatGPT4Global', 'bing', 'aipromptprogramming', 'ChatGPT_Tips', 'ChatGPT_Ideas_', 'copypasta', 'chatgptcirclejerk', 'chatGPTprogramming', 'programming', 'exmormon', 'ChatGPTLibertas', 'ChatGPTSpanish', 'brasil', 'chatgptplus', 'ChatGPTology', 'chatGPTism', 'ChatGPTWrongAnswers', 'brasilivre', 'learnmachinelearning', 'ChatGPTalk', 'ChatGPTPrompts', 'southpark', 'exjw', 'chatgptoutofcontext', 'chatgptprompteng', 'redscarepod', 'ChatGPTdeutsch', 'ChatGPTRoleplay', 'brdev', 'ChatGPTBrasil', 'ChatGPTtextart', 'shortcuts', 'ChatGPTGuild', 'ChatGPTModels', 'ApplyingToCollege', 'slatestarcodex', 'ChatGPTes', 'ChatGPTSymposium', 'LinkedInLunatics', 'ChatGPTSerious', 'chatgptwritingprompts', 'GoogleBard', 'Google_Bard_Chatbot', 'ReallyShittyCopper', 'BoJackHorseman', 'okbuddyretard', 'gme_meltdown', 'martialarts', 'UWMadison', 'RTGameCrowd', 'cellbits', 'AskMiddleEast', 'Hacking_Tutorials', 'geometrydash', 'trump', 'FilthyFrank', 'ihadastroke', 'China_irl', 'mlb', 'sustainability', '691', 'Ni_Bondha', 'radioheadcirclejerk', 'Zillennials', 'NationalConservative', 'bangladesh', 'theydidthemonstermath', 'virtualreality', 'Pikabu', 'CosmicSkeptic', 'Drizzy', 'LawStudentsPH', 'AIAssisted', 'flashlight', 'FreeNotionTemplates', 'PeepShowQuotes', 'NotionSoApp', 'HQMC', 'SuperMegaBaseball', 'lostgeneration', 'CHERUB', 'real_China_irl', 'NormMacdonald', 'INDYCAR', 'okbuddychicanery', 'teenagers', '90s', 'ARK', 'GodofWar', 'TedNivison', 'VisitingIceland', 'tacobell', 'rpg_brasil', 'IndiaAntiSocial', 'baseballcirclejerk', 'SoulmateAI', 'TechStartups', 'BatmanArkham', 'IndiaSpeaks', 'Geico', 'seranking_official', 'notionlayouts', 'yolowirecom', 'helpdesk', 'Numerama', 'SmorgasbordBizarre', 'MotionDesign', 'somnivexillology', 'UdemyCouponsMe', 'deeplearning', 'initaliano', 'chatgpt_deutschland', 'newtimes', 'RightWingUK', 'Emailmarketing', 'Connecticut', 'jollyyou', 'Udemies', 'enespanol', 'CommunityManager', 'StockMarket', 'CABarExam', 'ios_france', 'h3h3productions', 'CPTSDFreeze', 'actuallynot', 'bartenders', 'BooksAndFilms', 'AHELP_reviews', 'ContagiousLaughter', 'lost', 'mexico', 'novosti_kriptovalyut', 'perplexity_ai', 'nufiofficial', 'chrome_extensions', 'ProductHunters', 'Paradot', 'Millennials', 'iTalki', 'TheDecoder', 'Cyberpunk', 'AITechTips']
# scopes = ['identity', 'read', 'history']
# state = 'unique_state_string'
# duration = 'permanent'
# auth_url = reddit.auth.url(scopes=scopes, state=state, duration=duration)

client_id = os.environ.get('REDDIT_CLIENT_ID')
client_secret = os.environ.get('REDDIT_CLIENT_SECRET')
redirect_uri = os.environ.get('REDDIT_REDIRECT_URI')
user_agent = os.environ.get('REDDIT_USER_AGENT')

reddit = praw.Reddit(
    client_id=client_id,
    client_secret=client_secret,
    redirect_uri=redirect_uri,
    user_agent=user_agent
)




print('Fetching Reddit posts...')
start_time = datetime.datetime.now()
after = None
for sub in SUBREDDITS:
    print(sub)
    sleep(TIMER)
    subreddit = reddit.subreddit(sub)
    post_dict_list = []
    # posts = subreddit.new(limit=limit, params={"after": after})
    posts = subreddit.search('chatgpt', sort='relevance', limit=LIMIT)
    print('Found ' + str(len(list(posts))) + ' posts.')
    for post in posts:
        if post.is_self:
            post_content = post.selftext
        else:
            post_content = ''
        post_dict = {
            'title': post.title,
            'subreddit': post.subreddit.display_name,
            'created_utc': post.created_utc,
            'url': post.url,
            'is_self': post.is_self,
            'content': post_content,
            'comment_count': len(post.comments)
        }
        post_dict_list.append(post_dict)
    with open('../data/posts/posts_' + sub + '_' + str(start_time) + '.json', 'w') as f:
        json.dump(post_dict_list, f)
elapsed_time = datetime.datetime.now() - start_time
print('Finished fetching Reddit posts.')
print("Time elapsed: {:.2f} seconds".format(elapsed_time))

