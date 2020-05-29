import requests
from bs4 import BeautifulSoup
import pprint


num_pages_wanted = int(input('How many pages do you want to check?: '))

hacker_news_standard_url = 'https://news.ycombinator.com/news'
hacker_news_url_list = []

for i in range(num_pages_wanted+1):
    if i <= 1:
        if hacker_news_url_list.count(hacker_news_standard_url) == 0:
            hacker_news_url_list.append(hacker_news_standard_url)
    else:
        hacker_news_url_list.append(f'{hacker_news_standard_url}?p={i}')


hacker_news_list = []


def main(url_list):
    global hacker_news_list
    for item in url_list:
        response = requests.get(item)
        soup_object = BeautifulSoup(response.text, 'html.parser')
        list_of_links = soup_object.select('.storylink')
        list_of_subtext = soup_object.select('.subtext')
        custom_hacker_news(list_of_links, list_of_subtext)
    hacker_news_list = sort_stories(hacker_news_list)
    return hacker_news_list


def sort_stories(list_for_sorting):
    return sorted(list_for_sorting, key=lambda key: key['votes'], reverse=True)


def custom_hacker_news(links, subtext):
    global hacker_news_list
    for index in range(len(links)):
        title_link = links[index].getText()
        href = links[index].get('href', None)
        if href[0:4] == 'item':
            href = 'https://news.ycombinator.com/' + href
        vote = subtext[index].select('.score')
        if len(vote):
            points = int(vote[0].getText().replace(' points', ''))
            if points >= 100:
                hacker_news_list.append({'title': title_link, 'link': href, 'votes': points})


main(hacker_news_url_list)
pprint.pprint(hacker_news_list)
