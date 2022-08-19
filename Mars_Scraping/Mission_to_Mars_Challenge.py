# %%
# dependencies
from splinter import Browser
from bs4 import BeautifulSoup as soup
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd

# %%
# set up executable path and start a browser
executable_path = {'executable_path': ChromeDriverManager().install()}
browser = Browser('chrome', **executable_path, headless = False)

# %% [markdown]
# ## Mars News Site Scraping

# %%
# visit the mars nasa news site
url = 'https://redplanetscience.com'
browser.visit(url)

# Optional delay for loading the page
browser.is_element_present_by_css('div.list_text', wait_time=1)

# %%
html = browser.html

news_soup = soup(html, 'html.parser')

slide_elem = news_soup.select_one('div.list_text')

news_title = slide_elem.find('div', class_='content_title').get_text()
news_p = slide_elem.find('div', class_='article_teaser_body').get_text()

# %%
news_title

# %% [markdown]
# ## Jet Propulsion Lab Site Scraping

# %% [markdown]
# ### Featured Images

# %%
# visit url

url = 'https://spaceimages-mars.com/'
browser.visit(url)

# %%
# Find and click the full image button
full_image_elem = browser.find_by_tag('button')[1]
full_image_elem.click()

# %%
# Parse the resulting html with soup
html = browser.html
img_soup = soup(html, 'html.parser')

# Find the relative image url
img_url_rel = img_soup.find('img', class_='fancybox-image').get('src')
img_url_rel

img_url = f'{url}{img_url_rel}'

img_url

# %% [markdown]
# ## Getting Mars Facts Table

# %%
# get the table
df = pd.read_html('https://galaxyfacts-mars.com')[0]
df.columns=['description', 'Mars', 'Earth']
df.set_index('description', inplace=True)

#send it to html
df.to_html()

# %% [markdown]
# # Challenge Deliverable 1
# ## Hemisphere Images and Titles

# %%
# 1. Use browser to visit the URL 
url = 'https://marshemispheres.com/'

browser.visit(url)


# %%
# get the html elements
html = browser.html
hemi_soup = soup(html, 'html.parser')

# %%
# 2. Create a list to hold the images and titles.
hemisphere_details_urls = []

hemis_containers = hemi_soup.find_all('div', class_='description')

# build list of hemisphere links to visit
for hemi in hemis_containers:
    rel_link = hemi.a.get('href')
    hemi_url = f'{url}{rel_link}'
    hemisphere_details_urls.append(hemi_url)

# 3. Write code to retrieve the image urls and titles for each hemisphere.
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

# %%
# 4. Print the list that holds the dictionary of each image url and title.
hemisphere_image_urls

# %% [markdown]
# ## Ending Session

# %%
# line to quit browser
browser.quit()


