# -*- coding: utf-8 -*-
''' 1. LIBRARY IMPORT '''
import regex as re
from bs4 import BeautifulSoup
import requests
import pandas as pd
from time import gmtime, strftime

def main():
    def headline_collector(news_url, tag):
        user_agent = {'user-agent': 'University of Colorado at Boulder, natalie.castro@colorado.edu'}
        response = requests.get(news_url, headers=user_agent)
        if response.status_code == 200:
            news_text = BeautifulSoup(response.text, 'html.parser')
            tags = news_text.find_all(tag)
            return tags
        else:
            return []

    def headline_cleaner(headline):
        string_headline = str(headline)
        match_pattern = '(?<=>).+(?=<)'
        match_result = re.findall(match_pattern, string_headline)

        if len(match_result) > 0:
            return match_result[0]
        else:
            return None

    ''' 3. NEWS VARIABLE CREATION '''
    websites_and_tags = {"https://www.nytimes.com/":"p",
    "https://www.nytimes.com/section/climate":"a",
    "https://www.cnn.com/":"span",
    "https://www.cnn.com/climate":"span",
    "https://www.foxnews.com/":"a",
    "https://www.foxnews.com/category/science/planet-earth":"a",
    "https://www.bbc.com/":"h2",
    "https://www.bbc.com/future-planet":"h2",
    "https://abcnews.go.com/":"h2",
    "https://www.cbsnews.com/":"h4",
    "https://www.msnbc.com/":"a",
    "https://www.nbcnews.com/":"a",
    "https://www.usatoday.com/":"span",
    "https://www.usatoday.com/":"a",
    "https://www.usatoday.com/":"div",
    "https://www.usatoday.com/climate-change/":'a',
    "https://www.wsj.com/":"div",
    "https://www.politico.com/":"a",
    "https://www.politico.com/energy-climate-news-updates-analysis":"a",
    "https://www.politico.com/energy-climate-news-updates-analysis":"span",
    "https://www.bloomberg.com/green":"span",
    'https://www.huffpost.com/':"a",
    "https://www.huffpost.com/":"h3",
    "https://www.huffpost.com/impact/green":"h3",
    "https://www.euronews.com/":"a",
    "https://www.euronews.com/green":"a",
    "https://www.cgtn.com/":"a",
    "https://ddnews.gov.in/en/":"h2",
    "https://ddnews.gov.in/en/category/environment/":"a",
    "https://www.dw.com/en/top-stories/s-9097":"a",
    "https://www.dw.com/en/environment/s-11798":"a",
    "https://www.france24.com/en/":"h2",
    "https://www.france24.com/en/environment/":"h2",
    "https://www.rt.com/":"span",
    "https://www.i24news.tv/en":"h3",
    "https://www.aljazeera.com/":"span",
    "https://www.aljazeera.com/":"a",
    "https://www.aljazeera.com/climate-crisis":"a",
    "https://news.sky.com/":"a",
    "https://news.sky.com/science-climate-tech":"a",
    "https://english.alarabiya.net/":"span",
    "https://www3.nhk.or.jp/nhkworld/en/news/":"a",
    "https://www.africanews.com/":"a",
    "https://www.africanews.com/tag/climate-crisis/#home":"a",
    "https://www.africa-confidential.com/news":"a"
    }

    websites = list(websites_and_tags.keys())

    ''' 4. DATA COLLECTIONS '''
    ## Creating a storage container for the website data with the headlines, tag, and source
    website_data = []

    ## Iterating through each news source and collecting the URL information
    for url in websites:
        ## Setting the tag and the progress statement
        current_tag = websites_and_tags[url]

        ## Collecting the headlines from the respective website
        headlines = headline_collector(url, current_tag)

        ## Structuring the data to a list of dictionaries
        scraped_data = {"source": url, "tag": current_tag, "headlines": headlines}
        website_data.append(scraped_data)

    ''' 5. STRUCTURING THE DATA '''
    data = pd.DataFrame(website_data)
    headlines_full = data.explode('headlines')
    headlines_full.reset_index(inplace=True)
    headlines_full['headline clean'] = headlines_full['headlines'].apply(lambda x: headline_cleaner(x))

    curr_date = strftime("%Y-%m-%d-%H", gmtime())
    print(curr_date)

    headlines_full.to_csv(f'{curr_date}-headline_collection.csv')

if __name__ == "__main__":
    main()
