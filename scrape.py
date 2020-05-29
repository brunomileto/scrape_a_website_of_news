import requests
from bs4 import BeautifulSoup
import pprint

num_pages_wanted = int(input('How many pages do you want to check?: '))

hacker_news_standard_url = 'https://news.ycombinator.com/news'
hacker_news_url_list = []

# This for loop, create a list with all hacker news standard url, adding the pages that the user want
for i in range(num_pages_wanted + 1):
    if i <= 1:
        if hacker_news_url_list.count(hacker_news_standard_url) == 0:
            hacker_news_url_list.append(hacker_news_standard_url)
    else:
        hacker_news_url_list.append(f'{hacker_news_standard_url}?p={i}')

# This is the list that will contain our data
hacker_news_list = []


def main(url_list):
    """
    This function will get from our url list, the links of the pages, make the requests, create the soup object and
    select the values of the given html parameters. Then this function calls another function to actually get the
    values of the html parameters and, in the end this function will call another function to sort the result.
    :param url_list: hacker_news_url_list: List of the containing the link of all pages the user want
    :return: hacker_news_list: A print with a list that contain all data, from the web pages, filtered and sorted.
    """
    global hacker_news_list     # Getting the global version of the variable
    for item in url_list:
        response = requests.get(item)   # Make the request on the website and storing it in the response variable
        soup_object = BeautifulSoup(response.text, 'html.parser')   # Creating the soup object, parsing the data
        # to html format
        list_of_links = soup_object.select('.storylink')    # Get all values from 'storylink' html class
        list_of_subtext = soup_object.select('.subtext')    # Get all values from 'subtext' html class
        custom_hacker_news(list_of_links, list_of_subtext)  # Calling the function, passing the parameters
    hacker_news_list = sort_stories(hacker_news_list)   # Calling the function, passing the parameters
    return pprint.pprint(hacker_news_list)


def custom_hacker_news(links, subtext):
    """
    The principal function. It will get the parameters and find all the respective values. The main value is the vote.
    On hacker news, each news can be voted by the user. This function will select only the ones that has more than 100
    votes. With that, this function will get the titles of each news and its respective link. With all that, this
    function create a dictionary, with the these 3 datas of each news and append it on the hacker_news_list
    :param links: list_of_links: get the all values of the html class 'storylink' that has the title and link of a news
    :param subtext: list_of_subtext: html class that contain, among other things, another class 'score'. This 'score'
    contain the values of the votes that we want.
    :return: hacker_news_list: A complete list with a dict for each row (news), containing the title, vote and link
    """
    global hacker_news_list     # Get the global version of the variable
    for index in range(len(links)):
        title_link = links[index].getText()     # Get the text of the given class, provide by 'links'
        href = links[index].get('href', None)   # Get the value of the 'href' class
        if href[0:4] == 'item':     # Some href, does not have the full link to the same website. Providing the link
            href = 'https://news.ycombinator.com/' + href
        vote = subtext[index].select('.score')  # Get the value of the votes, stored on the 'score' class
        if len(vote):   # Some news does not have votes, so it causes an error. This check if it have a vote
            points = int(vote[0].getText().replace(' points', ''))
            if points >= 100:   # If the vote is more than 100, create a dict with all values and append it in the list
                hacker_news_list.append({'title': title_link, 'link': href, 'votes': points})


def sort_stories(list_for_sorting):
    """
    A simple sort function for dictionaries, since they does not have a method for that
    :param list_for_sorting: hacker_news_list: The final list of data filtered, that we got from previous function
    :return: hacker_news_list: the same list but sorted. The news that has more votes are shown first
    """
    return sorted(list_for_sorting, key=lambda key: key['votes'], reverse=True)     # Simple code to sort dict


main(hacker_news_url_list)
