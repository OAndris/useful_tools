"""
Idea based on "Complete Python Developer in 2020: Zero to Mastery" from Andrei Neagoie.
"""


import json
import pandas as pd
import requests
from bs4 import BeautifulSoup


def scrape_hackernews(url='https://news.ycombinator.com/news'):
    # Request URL, parse HTML, and select what we need.
    res = requests.get(url)
    soup = BeautifulSoup(res.text, 'html.parser')
    links = soup.select('.storylink')
    subtext = soup.select('.subtext')
    return links, subtext


def scrape_multiple_pages(num_of_pages=3):
    # Collect the data from multiple HTML pages.
    all_links = []
    all_subtext = []
    for i in range(num_of_pages):
        url = f'https://news.ycombinator.com/news?p={i+1}'
        links, subtext = scrape_hackernews(url)
        all_links += links
        all_subtext += subtext
    return all_links, all_subtext


def customize_hackernews(links, subtext, min_votes=100):
    # Process the collected data (output: list of dicts)
    stories = []
    for idx, _ in enumerate(links):
        title = links[idx].getText()
        href = links[idx].get('href', None)
        vote = subtext[idx].select('.score')
        if len(vote):
            points = int(vote[0].getText().replace(' points', ''))
            if points >= min_votes:
                stories.append({'title': title, 'link': href, 'votes': points})
    stories = sorted(stories, key=lambda d: d['votes'], reverse=True)
    return stories


def postprocess_hackernews(stories):
    # Post-process data - some of the HackerNews links are just links to another HackerNews pages; in these cases, the URL has to be adjusted.
    return [{k: (v if not (k=='link' and v.startswith('item?id=')) else 'https://news.ycombinator.com/'+v) for k, v in story.items()} for story in stories]


def main(display='html', num_of_pages=2, min_votes=100):
    """Collect the articles from multiple HackerNews pages, filter and order them based on the number of votes, and output to a HTML page or to the console."""
    links, subtext = scrape_multiple_pages(num_of_pages)
    stories = customize_hackernews(links, subtext, min_votes)
    stories = postprocess_hackernews(stories)
    if display == 'console':
        print(json.dumps(stories, indent=2))
    elif display == 'html':
        df = pd.DataFrame(stories)
        df.to_html('table.html', render_links=True, justify='center')


if __name__ == "__main__":
    main(display='html', num_of_pages=2, min_votes=100)
