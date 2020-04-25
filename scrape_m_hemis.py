######################################
############ scrape data! ############
# import dependencies
from bs4 import BeautifulSoup
import requests
import pandas as pd

# -- import spliter & set path
from splinter import Browser

def init_browser():
    executable_path = {'executable_path': 'chromedriver.exe'}
    return Browser('chrome', **executable_path, headless=False)

def hemi_scrapes():
    
    # start splinter
    browser = init_browser()

    ##############################
    ### mars hemisphere images ###
    #----------------------------#

    usgs_url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'

    # use requests...
    #usgs_response = requests.get(usgs_url)

    # ... splinter, & soup
    browser.visit(usgs_url)
    usgs_html = browser.html
    usgs_soup = BeautifulSoup(usgs_html, 'lxml')

    # get the data for the four hemispheres from the page in a list
    hsphere_data = usgs_soup.find_all('div', class_='item')

    # set variables for holding the hemisphere data and the main url for usgs astro
    hspheres_img_urls = []
    usgs_astro_url = 'https://astrogeology.usgs.gov'

    # make a loop to parse through the list, pull out the headers & links...
    # ... store and append the data to the hsphere's list...
    # ... into a dictionary format...
    
    for h in hsphere_data:
        # getting header for the hemisphere
        title = h.find('h3').text
        
        # get the link ends for visiting the page
        link_end = h.find('a', class_='itemLink product-item')['href']
        
        # visit the particular hemisphere page
        browser.visit(usgs_astro_url + link_end)
        
        # set a new HTML object for the particular page
        link_end = browser.html
        
        # use soup to pull the data
        soup = BeautifulSoup(link_end, 'lxml')
        
        # use the home url and soup to concat the full image url
        h_img_url = usgs_astro_url + soup.find('img', class_='wide-image')['src']
        
        # append the full img url to the list
        hspheres_img_urls.append({'Title': title, 'Image_URL': h_img_url})
    
    # end splinter session
    browser.quit()


    ####################################
    ############ load data! ############

    # import dependecies
    #####from flask import Flask, render_template
    import pymongo

    # create an instance of Flask
    #####app = Flask(__name__)

    # create connection variable
    conn = 'mongodb://localhost:27017'

    # pass connection to the pymongo instance
    client = pymongo.MongoClient(conn)

    # Connect to a database. Will create one if not already available.
    db = client.mars_db

    # drops collections if they exist to remove duplicates
    db.hemispheres.drop()

    # update the collection variable
    #####collection = db.hemispheres

    # re-insert data
    db.hemispheres.insert_many(hspheres_img_urls) 