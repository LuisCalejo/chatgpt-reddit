import os
import json
import datetime
from time import sleep
import praw

LIMIT = 250  # Limit per request
TIMER = 2  # Waiting time in seconds between each request to avoid being blocked by server
SUBREDDITS = ['all', 'ChatGPT', 'chatgpt_prompts_', 'chatgpt_promptDesign', 'OpenAI', 'singularity', 'chatgpt_newtech',
              'ChatgptStories', 'technology', 'GPT3', 'chatgpt_de', 'chatgpt_brasil', 'ChatGPTCoding', 'ChatGPTPro',
              'ChatGPT_Prompts', 'ChatGPTGoneWild', 'ProgrammerHumor', 'ArtificialInteligence', 'ChatGPTPromptGenius',
              'ChatGPTJailbreak', 'Futurology', 'artificial', 'ChatGPT_FR', 'ChatGptDAN', 'StableDiffusion',
              'midjourney', 'ChatGPTforWork', 'ChatGPTforall', 'AnarchyChess', 'conspiracy', 'ChatGPTjailbreaks',
              'ChatGPT_Sims', 'MachineLearning', 'copypasta', 'ChatGPTMemes', 'ChatGPTSucks', 'SideProject', 'antiwork',
              'crackGPT', 'ChatGPT4Global', 'Professors', 'chatGPT4userRs', 'ChatGPT_LegalAdviceUS', 'tech',
              'wallstreetbets', 'ChatGPT_Ideas_', 'ChatGPT_Tips', 'technews', 'shitposting', 'ChatGPT_RPG',
              'chatgptcirclejerk', 'aipromptprogramming', 'developersIndia', 'chatGPTprogramming', 'ChatGPTAdventures',
              'bing', 'programming', 'ChatGPTSpanish', 'ChatGPTalk', 'exmormon', 'memes', 'ChatGPTPrompts',
              'ChatGPTBrasil', 'brasil', 'france', 'ChatGPTGuild', 'ChatGPTes', 'Teachers', 'brasilivre',
              'chatgptoutofcontext', 'ChatGPTLibertas', 'PoliticalCompassMemes', 'learnmachinelearning',
              'chatgptprompteng', 'ChatGPTdeutsch', 'exjw', 'CryptoCurrency', 'southpark', 'redscarepod',
              'ChatGPTRoleplay', 'brdev', 'Superstonk', 'ChatGPTology', 'chatGPTism', 'KGBTR', 'shortcuts',
              'ChatGPTSymposium', 'ChatGPTWrongAnswers', 'LinkedInLunatics', 'ApplyingToCollege', 'ChatGPTSerious',
              'chatgptwritingprompts', 'okbuddychicanery', 'GoogleBard', 'Google_Bard_Chatbot']


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


def get_reddit_posts(subreddits):
    print('Fetching Reddit posts...')
    start_time = datetime.datetime.now()

    for sub in subreddits:
        print(sub)
        sleep(TIMER)
        subreddit = reddit.subreddit(sub)
        # post_dict_list = []

        posts = subreddit.search('chatgpt', sort='relevance', limit=LIMIT)
        post_list = list(posts)
        print(f'Found {len(list(post_list))} posts.')

        post_dict_list = [
            {
                'title': post.title,
                'subreddit': post.subreddit.display_name,
                'created_utc': post.created_utc,
                'url': post.url,
                'is_self': post.is_self,
                'content': post.selftext if post.is_self else '',
                'comment_count': post.num_comments
            }
            for post in post_list
        ]

        with open(f'../data/posts/posts_{datetime.datetime.now()}_{sub}.json', 'w') as f:
            json.dump(post_dict_list, f)

    elapsed_time = datetime.datetime.now() - start_time
    print('Finished fetching Reddit posts.')
    print(f"Time elapsed: {elapsed_time}")


if __name__ == '__main__':
    get_reddit_posts(SUBREDDITS)
