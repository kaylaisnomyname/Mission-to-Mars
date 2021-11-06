#!/usr/bin/env python
# coding: utf-8


# Import Splinter, BeautifulSoup and pandas
from splinter import Browser
from bs4 import BeautifulSoup as soup
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd 
import datetime as dt


# initialize the browser, create a data dictionary, end the WebDriver and return the scraped data
def scrape_all():
    # initiate headless driver for deployment # set up splinter:
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=True)  # headless=True : scraping is running in background

    # # set up splinter:
    # # executable_path = {'executable_path': ChromeDriverManager().install()}
    # browser = Browser('chrome', **executable_path, headless=False)  # headless=False to check scraping in action

    # set return variables:
    news_title, news_paragraph = mars_news(browser)

    # create data dictionary: run all scraping functions and store results in dictionary:
    data = {
        "news_title": news_title,
        "news_paragraph": news_paragraph,
        "feature_image": featured_image(browser),
        "facts": mars_facts(),
        "last_modified": dt.datetime.now()
    }

    # stop webdriver and return data
    browser.quit()
    return data

# refactor the scraping code into a function to scrape news titles and paragraph
def mars_news(browser):
    # # Visit the mars nasa news site
    #url = 'https://redplanetscience.com/'
    url = 'https://data-class-mars.s3.amazonaws.com/Mars/index.html'
    browser.visit(url)
    # Optional delay for loading the page
    browser.is_element_present_by_css('div.list_text', wait_time=1)

    # set up HTML parser: convert the browser to a soup object and then quit the browser
    html = browser.html
    news_soup = soup(html, 'html.parser')
   
    # add try/except for error handling
    try:
        slide_elem = news_soup.select_one('div.list_text')

        # assign the title and summary text to variables
        # news_title = slide_elem.find('div', class_='content_title').get_text()

        # Use the parent element to find the first `a` tag and save it as `news_title`
        news_title = slide_elem.find('div', class_='content_title').get_text()
        #news_title

        # Use the parent element to find the paragraph text
        news_p = slide_elem.find('div', class_='article_teaser_body').get_text()
        #news_p
    except AttributeError:
        return None, None
    return news_title, news_p


# ### Featured Images :  JPL Space Images
def featured_image(browser):
    # Visit URL
    #url = 'https://spaceimages-mars.com'
    url = 'https://data-class-jpl-space.s3.amazonaws.com/JPL_Space/index.html'
    browser.visit(url)

    # Find and click the full image button
    full_image_elem = browser.find_by_tag('button')[1]
    full_image_elem.click()


    # Parse the resulting html with soup
    html = browser.html
    img_soup = soup(html, 'html.parser')

    try:
        # Find the relative image url
        img_url_rel = img_soup.find('img', class_='fancybox-image').get('src')
        #img_url_rel
    except AttributeError:
        return None
    # Use the base URL to create an absolute URL
    #img_url = f'https://spaceimages-mars.com/{img_url_rel}'
    img_url = f'https://data-class-jpl-space.s3.amazonaws.com/JPL_Space/{img_url_rel}'
    #img_url

    return img_url

def mars_facts():
    # try/except error handling during extraction
    try:
        # scraping data from 'Mars Facts' into a dataframe
        df = pd.read_html('https://data-class-mars-facts.s3.amazonaws.com/Mars_Facts/index.html')[0]
    except BaseException:
        return None

    df.columns=['description', 'Mars', 'Earth']
    df.set_index('description', inplace=True)

    # convert df into HTML format, add bootstrap
    return df.to_html(classes="table table-striped")

# at the buttom: tell Flask that this script is complete and ready for action
if __name__ == "__main__":
    # if runnning as script, print scraped data
    print(scrape_all())
