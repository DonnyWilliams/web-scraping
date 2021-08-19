# This program is to scrape HackerNews.com and print the title, link and vote numbers
# for each story on the front page that has more than 100 votes, in order starting
# with the greatest number of votes, working down to 100.

# This allows us to make requests to websites for the data we're scraping.
# Specifically, requests allows us to download the HTML code from a website.
import requests
# This is the syntax for importing Beautiful Soup.
# I installed Beautiful Soup 4, the most recent version at this time.
# Beautiful Soup allows us to use the HTML from websites and grab data from it.
from bs4 import BeautifulSoup
# Pretty print (pprint) helps clean up the way something is displayed when printed.
import pprint

# res is short for "response", but we can name our variable anything.
# We'll put the URL we want to grab data from inside the ('').
# Using Hacker News here as an example
res = requests.get('https://news.ycombinator.com/news')
# print(res) will return <Response [200]>, which means it ran as planned.
# print(res.text) will return the text of the HTML file for the URL we input.

# res.text is the raw HTML string that is returned.
# 'html.parser' says the string is HTML and needs to be parsed.
# There are other parsers, but 99% of the time, we're going to use the HTML parser.
# soup is just the name of the variable for our soup object we've created here.
soup = BeautifulSoup(res.text, 'html.parser')
# print(soup) returns HTML file that is an object and no longer a string.
# This allows us to manipulate the code.
# print(soup.body) returns just the body of the HTML code.
# print(soup.body.contents) returns the contents in list form.
# print(soup.find_all('div')) finds all of the div objects in the code.
# print(soup.find_all('a')) finds all of the a tags (the links) in the code.
# print(soup.title) prints the title tag of the code.
# In this case, it returns <title>Hacker News</title>
# print(soup.a) returns the first a tag (link) that occurs.
# print(soup.find('a')) returns the first a tag it finds.
# .find_all() returns everything found.
# .find() returns just the first instance found.
# print(soup.find(id='score_27674413')) returns score info associated with this id.
# In this case: <span class="score" id="score_27674413">309 points</span>
# print(soup.select('a')) returns all of the a tags (links) in list form.
# print(soup.select('.score')) returns all of the info with class Score as a list.
# class="score" is represented as '.score'
# The period in this syntax means it's the name of a class.
# print(soup.select('#score_27674413')) returns the score class info for this ID.
# The hashtag symbol in this syntax means it's an ID.
# print(soup.select(id='score_27674413')) is another way to do the same thing.
# print(soup.select('.storylink')) grabs all the a tags bc they have class storylink.
# print(soup.select('.storylink')[0]) grabs only the first one.

# Creating new variables here to simplify the code.
# In this case, we know the first link corresponds to the virst vote, etc.
links = soup.select('.storylink')
# Using class Subtext here instead of class Score to get the votes bc all links
# have a class Subtext, but if someone just hasn't voted on a link yet, it won't
# have a class Score.
# This way, it insures we won't get IndexError: list index out of range bc the
# number of returns doesn't match up if there's a link with no votes.
subtext = soup.select('.subtext')
# print(votes[0].get('id)) returns the ID value of the first vote object.

# This function is to sort how the dict sets are returned in vote order.
# hnlist is undefined bc it's just a placeholder for a variable entered later.


def sort_stories_by_votes(hnlist):
    # This sorts by specifically the votes key.
    # Not sure why we need to use a lambda function here, but that's what the
    # instructor said.
    # I think it has to do with something wonky in the sorted() module.
    # And specifically bc we're sorting by a key in a dict.
    # reverse=True at the end sorts in reverse order, so the highest number will
    # be the first returned, etc.
    return sorted(hnlist, key=lambda k: k['votes'], reverse=True)

# Creating this function to get the actual results we're looking for.


def create_custom_hn(links, subtext):
    # Creates a new hacker news list that begins empty.
    hn = []
    # I only want to return the text, not the HTML, to make it easier to read.
    # idx is short for index.
    # enumerate() gives us an index.
    # The index is important because we want to use enumerate() on the links
    # variable, but not the subtext variable.
    # Writing it like this allows us to do this.
    # It's also why we need to include [0] when setting up each variable below.
    for idx, item in enumerate(links):
        # .getText() is a bs4 module that gets just the text in a span.
        title = links[idx].getText()
        # This is to grab the a href storylinks for each title (so we could actually
        # go to the story if we want, and it's not just a list of inaccessible titles).
        # Using .get() instead of .getText() bc we don't want the text. We want the
        # HTML code.
        # Set None as the default second arg. This way, it'll still grab an href
        # even if it doesn't use the word href.
        href = links[idx].get('href', None)
        # This is to use the subtext variable to get only the vote info we want.
        vote = subtext[idx].select('.score')
        # This is saying if anything is there as the vote, do the following.
        # This way, if there are no votes, nothing is returned and there's no error.
        # len(0) is False. len([any value greater than 0]) is True.
        if len(vote):
            # Using points as the variable name to distinguish from subtext variable.
            # Using .replace() to replace the parts of subtext text we don't want
            # with an empty string.
            # Using int() to turn the remaining number given into an int that can
            # then be worked as an int instead of a string that is a number.
            # Important to have an index position with vote bc it says we want to
            # start looping at the first result.
            # Otherwise, we'd get AttributeError: 'list' object has no attribute
            # 'getText'.
            points = int(vote[0].getText().replace(' points', ''))
            # print(points) here would show us we're getting the points data
            # displayed how we want: with just the vote numerals as integers.
            if points >= 100:
                # hn.append(title) fills out our new list with just the collected
                # titles.
                # Using a dict bc we want to link title and href.
                hn.append({'title': title, 'link': href, 'votes': points})
    # This is to return our hn list in a way that's sorted by votes.
    return sort_stories_by_votes(hn)


# Even though values are already set for links and subtext, I still need to pass
# these two as args here bc function expects two args.
# Using pprint.pprint() to print here prints each dict set on a new line so it's
# easier to read.
pprint.pprint(create_custom_hn(links, subtext))
