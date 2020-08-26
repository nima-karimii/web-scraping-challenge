from splinter import Browser
import pandas as pd
from bs4 import BeautifulSoup as bs
import time
from webdriver_manager.chrome import ChromeDriverManager


def init_browser():
    # @NOTE: Replace the path with your actual path to the chromedriver
    executable_path = {'executable_path':ChromeDriverManager().install()}
    return Browser("chrome", **executable_path, headless=False)

def scrape_info():
    browser = init_browser()


    url = 'https://mars.nasa.gov/news'
    browser.visit(url)
    time.sleep(2)

    # Scrape page into Soup
    html = browser.html
    soup = bs(html, 'html.parser')

    Dates = soup.find_all('div', class_='list_date')
    titles = soup.find_all('div', class_='content_title')
    paragraphs = soup.find_all('div', class_='article_teaser_body')

    latest_date=Dates[0].text
    latest_title = titles[1].text
    latest_p = paragraphs[0].text

    url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(url)
    time.sleep(2)
    browser.click_link_by_partial_text("FULL IMAGE")
    time.sleep(2)
    browser.click_link_by_partial_text("more info")
    time.sleep(2)

    html = browser.html
    soup = bs(html, 'html.parser')

    Imgs = soup.find_all('figure', class_='lede')
    featured_image_url="https://www.jpl.nasa.gov/"+Imgs[0].a["href"]

    ########
    url = 'https://space-facts.com/mars/'
    browser.visit(url)
    time.sleep(2)
    tables = pd.read_html(url)
    df=tables[0]
    df.columns=['Descriptions' , 'Info']
    df=df.set_index('Descriptions')
    html_table = df.to_html()

    ########
    url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(url)
    html = browser.html
    soup = bs(html, 'html.parser')

    Hms = soup.find_all('h3')
    titles=[]
    for Hm in Hms:
        titles.append(Hm.text)

    # Image_urls=[]
    hemisphere_image_urls=[]
    for title in titles:
        url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
        browser.visit(url)
        time.sleep(3)
        browser.click_link_by_partial_text(title)
        html = browser.html
        soup = bs(html, 'html.parser')
        image_url=soup.find_all('li')[0].a["href"]
        # Image_urls.append(image_url)

    #Adding them in to a List
        Temp={}
        Temp['title']=title
        Temp['img_url']=image_url
        hemisphere_image_urls.append(Temp)

    Mars_data= {
    "news_date":latest_date,
    "news_title":latest_title,
    "news_p":latest_p,
    "features_img":featured_image_url,
    "mars_table":html_table,
    "hemispheres":hemisphere_image_urls
    }

    browser.quit()

    return Mars_data







