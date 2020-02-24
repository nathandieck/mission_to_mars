def scrape():

    #import dependencies

    #beautiful soup
    from bs4 import BeautifulSoup as bs

    #requests
    import requests

    #splinter
    from splinter import Browser

    #pandas
    import pandas as pd

    #selenium
    from selenium import webdriver
    import time

    #define URLs for our various news sources

    url_news = "https://mars.nasa.gov/news/"
    url_image = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
    url_weather = "https://twitter.com/marswxreport?lang=en"
    url_facts = "https://space-facts.com/mars/"
    url_hemispheres = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    url_chicago = "https://forecast.weather.gov/MapClick.php?lat=42.012590000000046&lon=-87.68613999999997#.XlKRDShKiUl"

    #Pull the information for NASA's Mars News.
        #the div class for the headlines is "content_title"
        #the div class for the paragraph is "rollover_description_inner"

    response = requests.get(url_news)

    soup = bs(response.text, 'html.parser')

    #store the headline and text as a variable

    news_headline = soup.find('div', class_="content_title").text
    news_headline = news_headline.replace("\n","")

    news_headline

    news_byline = soup.find('div', class_="rollover_description_inner").text
    news_byline = news_byline.replace("\n","")

    news_byline

    #Pull the JPL Mars Image URL (using Splinter per directions in the ReadMe)

    executable_path = {'executable_path': 'chromedriver.exe'}
    browser = Browser('chrome', **executable_path, headless=False)

    browser.visit(url_image)

    html = browser.html
    soup = bs(html, 'html.parser')

    slide = soup.find('li', class_="slide")
    fancybox = slide.find('a')
    fimage_name = fancybox['data-title']
    fimage_desc = fancybox['data-description']
    fimage_purl = fancybox['data-fancybox-href']

    fimage_url = f"jpl.nasa.gov{fimage_purl}"

    browser.quit()

    print(fimage_name)
    print(fimage_desc)
    print(fimage_url)

    #pull the martian weather report from Twitter to find out whether Chicago is colder than mars right now
        #(it happens.)

    driver = webdriver.Chrome()  #https://stackoverflow.com/questions/59222947/retrieving-text-from-twitter-account-using-beautifulsoup-and-splinter
    driver.get(url_weather)

    time.sleep(15)

    html = driver.page_source

    driver.close()

    soup = bs(html, 'html.parser')

    weather = soup.find('div', class_='css-901oao r-hkyrab r-1qd0xha r-a023e6 r-16dba41 r-ad9z0x r-bcqeeo r-bnwqim r-qvutc0').text

    print(weather)

    #chicago weather - high temp is...

    response = requests.get(url_chicago)

    soup = bs(response.text, 'html.parser')

    chicago_weather = soup.find('p', class_="myforecast-current-lrg").text

    chiberia = chicago_weather.replace("°F","")

    chiberia = int(chiberia)

    print(chiberia)

    #mars weather - high temp is...

    mars_weather = weather.split(")")
    mars_weather = mars_weather[2]
    mars_weather_2 = mars_weather.split("(")
    mars_weather_3 = mars_weather_2[1].replace("ºF","")
    martian_temp = float(mars_weather_3)
    martian_temp = int(martian_temp)
    print(martian_temp)

    #is it actually colder on Mars today? 

    if martian_temp > chiberia:
        ismarscolder = False
    else:
        ismarscolder = True

    #pull the list of mars facts from the mars facts website

    facts = pd.read_html(url_facts)
    facts = facts[0]

    print(facts)

    facts_html = facts.to_html()

    #here come the four martian hemispheres

    executable_path = {'executable_path': 'chromedriver.exe'}
    browser = Browser('chrome', **executable_path, headless=False)
        
    hemisphere_urls = []
        
    browser.visit(url_hemispheres)

    html = browser.html
    soup = bs(html, 'html.parser')

    results = soup.find('div', class_='container').find_all('h3')

    for result in results:
        
        temp_dict = {}
        
        print(result)
        title = str(result)
        title = title.replace("<h3>","")
        title = title.replace("</h3>","")
        print(title)
        
        browser.click_link_by_partial_text(title)
    
        html = browser.html
        soup = bs(html, 'html.parser')

        spot = soup.find('div', class_='container')
        image = spot.find('img', class_='wide-image')
        url = image['src']
        url = f"astrogeology.usgs.gov{url}"
        print(url)
        
    #     key1 = "title"
    #     key2 = "img_url"
        
        temp_dict.update({title : url})
        
        hemisphere_urls.append(temp_dict)
        
        browser.back()
        
    browser.quit()
    print(hemisphere_urls)

    """
    To review:
    Mars News Headline: news_headline
    Mars News Byline: news_byline

    Mars Image Name: fimage_name
    Mars Image Description: fimage_desc
    Mars Image URL: fimage_url

    Mars Weather Report: weather
    Chicago High Temperature: chiberia
    Martian High Temperature: martian_temp
    Binary Temperature Variable: ismarscolder

    Facts List: facts
    Facts HTML Code: facts_html

    Hemispheres URL Dictionary: hemisphere_urls

    """

    go2mars = {}

    go2mars["headline"] = news_headline
    go2mars["byline"] = news_byline
    go2mars["image_name"] = fimage_name
    go2mars["image_desc"] = fimage_desc
    go2mars["image_url"] = fimage_url
    go2mars["weather"] = weather
    go2mars["ismarscolder"] = ismarscolder
    go2mars["facts"] = facts
    go2mars["hemispheres"] = hemisphere_urls

    return go2mars

