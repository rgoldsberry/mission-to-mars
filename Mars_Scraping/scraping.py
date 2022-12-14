# dependencies
from splinter import Browser
from bs4 import BeautifulSoup as soup
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import datetime as dt

def scrape_all():
    # set up executable path and start a browser
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=True)

    #call news function
    news_title, news_paragraph = mars_news(browser)
    
    # fill in data
    # calling other funtions within the data since they just return one value
    data = {
      "news_title": news_title,
      "news_paragraph": news_paragraph,
      "featured_image": featured_image(browser),
      "facts": mars_facts(),
      "last_modified": dt.datetime.now(),
      "hemispheres": hemisphere_scrape(browser)
        }
    
    # Ending Session
    browser.quit()

    return data

def mars_news(browser):
    # Mars News Site Scraping
    url = 'https://redplanetscience.com'
    browser.visit(url)

    # Optional delay for loading the page
    browser.is_element_present_by_css('div.list_text', wait_time=1)

    html = browser.html
    news_soup = soup(html, 'html.parser')

    try:
        #attempt to grab elements        
        slide_elem = news_soup.select_one('div.list_text')
        news_title = slide_elem.find('div', class_='content_title').get_text()
        news_p = slide_elem.find('div', class_='article_teaser_body').get_text()
    except AttributeError:
        return None, None

    return news_title, news_p


def featured_image(browser):
    # Jet Propulsion Lab Site Scraping
    url = 'https://spaceimages-mars.com/'
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
    except AttributeError:
        return None

    img_url = f'{url}{img_url_rel}'
    return img_url


def mars_facts():
    
    try:
        #  Getting Mars Facts Table
        df = pd.read_html('https://galaxyfacts-mars.com')[0]
    except BaseException:
        return None

    # assign columns and set index of df
    df.columns=['description', 'Mars', 'Earth']
    df.set_index('description', inplace=True)
    
    #send it to html
    return df.to_html(classes="table table-striped")


def hemisphere_scrape(browser):
    url = 'https://marshemispheres.com/'
    browser.visit(url)

    html = browser.html
    hemi_soup = soup(html, 'html.parser')

    hemisphere_details_urls = []

    try: 
        hemis_containers = hemi_soup.find_all('div', class_='description')
        # build list of hemisphere links to visit
        for hemi in hemis_containers:
            rel_link = hemi.a.get('href')
            hemi_url = f'{url}{rel_link}'
            hemisphere_details_urls.append(hemi_url)

        hemisphere_image_urls = []

        for link in hemisphere_details_urls:
            # visit site, get html
            browser.visit(link)
            html = browser.html
            hemi_soup = soup(html, 'html.parser')

            #extract title (discarding ' Enhanced') and image link
            hemi_title = hemi_soup.find('h2').text.split(' E')[0]
            hemi_img_link = f"{url}{hemi_soup.find('a', text='Sample').get('href')}"

            #add hemisphere details to dictionary
            hemi_dict = {
                'img_url' : hemi_img_link,
                'title' : hemi_title
            }

            hemisphere_image_urls.append(hemi_dict)
    
    except AttributeError:
        return None
    
    return(hemisphere_image_urls)


if __name__ == "__main__":
    # If running as script, print scraped data
    print(scrape_all())