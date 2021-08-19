# This is to have a clean version of scrape.py.

import requests
from bs4 import BeautifulSoup
import pprint

res = requests.get('https://news.ycombinator.com/news')
soup = BeautifulSoup(res.text, 'html.parser')

links = soup.select('.storylink')
subtext = soup.select('.subtext')


def sort_stories_by_votes(hnlist):
    return sorted(hnlist, key=lambda k: k['votes'], reverse=True)


def create_custom_hn(links, subtext):
    hn = []
    print("\n\nHERE ARE THE ARTICLES WITH MORE THAN 100 VOTES IN CHRONOLOGICAL ORDER:")
    for idx, item in enumerate(links):
        title = links[idx].getText()
        href = links[idx].get('href', None)
        vote = subtext[idx].select('.score')
        if len(vote):
            points = int(vote[0].getText().replace(' points', ''))
            if points >= 100:
                hn.append({'title': title, 'link': href, 'votes': points})
                print(f"\n{points} votes for \"{title}\" ({href})")
    print("\n\nHERE IS A PRETTY PRINT VERSION IN LIST AND DICT FORM, IN ORDER OF MOST VOTES:\n")
    return sort_stories_by_votes(hn)


pprint.pprint(create_custom_hn(links, subtext))
