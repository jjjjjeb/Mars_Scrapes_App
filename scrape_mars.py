######################################
############ scrape data! ############

# import dependencies
from bs4 import BeautifulSoup
import requests
import pandas as pd

# -- import spliter & set path
from splinter import Browser

#####from flask import Flask, render_template
import pymongo


def init_browser():
    executable_path = {'executable_path': 'chromedriver.exe'}
    return Browser('chrome', **executable_path, headless=False)


def all_the_mars_scrapes():
    browser = init_browser()

    #################
    ### mars news ###
    #---------------#

    url_news = 'https://mars.nasa.gov/news'

    # using requests module to retrieve page
    response = requests.get(url_news)

    # creating beautifulSoup object & parsing w html.parser
    soup = BeautifulSoup(response.text, 'html.parser')

    # get header, subheader & link
    marsNews_head = soup.find('div', class_='content_title').find('a').text.strip()
    marsNews_subhead = soup.find('div', class_='slide').\
        find('div', class_='image_and_description_container').\
        find('a').find('div', class_='rollover_description').text.strip()
    marsNews_link = soup.find('div', class_='slide').\
        find('div', class_='image_and_description_container').\
        find('a')['href']
    marsNews_link = marsNews_link.replace('/news', '')
    marsNews_link = url_news + marsNews_link

    print(marsNews_head)
    print('--------------')
    print(marsNews_subhead)
    print(marsNews_link)


    ###########################
    ### mars featured image ###
    #-------------------------#

    url_jpl_mars = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'

    # use splinter to visit site
    browser.visit(url_jpl_mars)

    # pull in beautiful soup to parse through the HTML
    html_jpl = browser.html
    soup = BeautifulSoup(html_jpl, 'html.parser')

    # get the background image for featured image
    # ...& clean the string w replace to isolate the url end
    featured_img = soup.find('article')['style'].replace('background-image: url(','')
    featured_img = featured_img.replace("'", "").replace(");", "")

    # set the main url
    url_jpl = 'https://www.jpl.nasa.gov'

    # concat the two urls to get the final image url
    featured_img_url = url_jpl + featured_img

    # check
    print(featured_img)

    #########################
    ### mars weather data ###
    #-----------------------#

    mars_tweets = 'https://twitter.com/marswxreport'

    # use requests and soup
    response = requests.get(mars_tweets)
    soup = BeautifulSoup(response.text, 'html.parser')

    # ...to pull the most recent weather data
    mars_weather = soup.find('div', 'js-tweet-text-container').p.text

    # use replace and split to clean the required string
    mars_weather = mars_weather.replace('\n', '').split('pic')
    mars_weather = mars_weather[0]
    print(mars_weather)


    ########################
    ### mars facts table ###
    #----------------------#

    space_facts_url = 'https://space-facts.com/mars/'

    # use pandas to read the html table from the page
    tables = pd.read_html(space_facts_url)

    # choose the table w indexing
    mars_df = tables[0]

    # clean up the columns
    mars_df.columns = ['', 'Mars Planet Facts']

    # transform it into an html string
    facts_table = mars_df.to_html(header=True)

    # clean up the string
    facts_table = facts_table.replace('\n', '')
    print(facts_table)
    
    # end splinter session
    browser.quit()

    ####################################
    ############ load data! ############

    # create an instance of Flask
    #####app = Flask(__name__)

    # create connection variable
    conn = 'mongodb://localhost:27017'

    # pass connection to the pymongo instance
    client = pymongo.MongoClient(conn)

    # Connect to a database. Will create one if not already available.
    db = client.mars_db

    # drops collections if they exist to remove duplicates
    db.updates.drop()

    # set the collection variable
    #####collection = db.updates

    # insert scraped & updated data into the update collection
    db.updates.insert(
        {
            'news_title': marsNews_head,
            'news_description': marsNews_subhead,
            'news_link': marsNews_link,
            'featured_img': featured_img_url,
            'weather': mars_weather,
            'facts_table': facts_table,
        }
    )
    # quite splinter
    browser.quit()