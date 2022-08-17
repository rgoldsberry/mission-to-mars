# dependencies
from splinter import Browser
from bs4 import BeautifulSoup as soup
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd

# set up executable path and start a browser
executable_path = {'executable_path': ChromeDriverManager().install()}
browser = Browser('chrome', **executable_path, headless = False)

# Mars News Site Scraping
url = 'https://redplanetscience.com'
browser.visit(url)

# Optional delay for loading the page
browser.is_element_present_by_css('div.list_text', wait_time=1)

html = browser.html

#convert browser to soup, extract elements
news_soup = soup(html, 'html.parser')
slide_elem = news_soup.select_one('div.list_text')
news_title = slide_elem.find('div', class_='content_title').get_text()
news_p = slide_elem.find('div', class_='article_teaser_body').get_text()

# print(news_title)
# print(news_p)

# Jet Propulsion Lab Site Scraping
# visit url

url = 'https://spaceimages-mars.com'
browser.visit(url)

# Find and click the full image button
full_image_elem = browser.find_by_tag('button')[1]
full_image_elem.click()

# Parse the resulting html with soup
html = browser.html
img_soup = soup(html, 'html.parser')

# Find the relative image url
img_url_rel = img_soup.find('img', class_='fancybox-image').get('src')
img_url_rel

img_url = f'{url}{img_url_rel}'

print(img_url)

#  Getting Mars Facts Table
df = pd.read_html('https://galaxyfacts-mars.com')[0]
df.columns=['description', 'Mars', 'Earth']
df.set_index('description', inplace=True)

#send it to html
df.to_html()

print(df)

# Ending Session
browser.quit()