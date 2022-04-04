import requests
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

# sample artist
# Aimer:    57498
# Ado:      1310625
# Claris:   11236
# LiSA:     25868
# milet:    1103556
# Uru:      695242
# YOASOBI:  1223123
try:
    
    # The artist page on Mora.jp
    site = "https://mora.jp/artist/1310625/h#discArea"
    
    # Check if the link is reachable or not
    response = requests.get(site, timeout = 5)
    if response.status_code != requests.codes.ok:
        raise RuntimeError("Unreachable URL.")
    
    # Set and run ChromeDriver in headless
    print("Setup chromedriver...")
    chrome_options = Options()
    chrome_options.add_argument('--headless')
    chrome_options.add_experimental_option('excludeSwitches', ['enable-logging'])
    driver = webdriver.Chrome(options=chrome_options)
    driver.get(site)
    
    # Get each albums and singles
    print("Scanning...")
    article_link = driver.find_elements(By.XPATH, "//article/a[@href]")
    urls = []
    for article in article_link:
        temp = article.get_attribute("href")
        if temp.startswith("https://mora.jp/package"):
            urls.append(temp)
    
    # Remove replicated links with 'trackMaterialNo'
    urls = list(dict.fromkeys(urls))
    urls = [url for url in urls if "trackMaterialNo" not in url]
    
    for link in urls:
        
        # Go for the links retrieved in urls[]
        print("Loading %s"%link)
        driver.get(link)
        ALBUMINFO, TRACKNUM, TRACKTTL = [], [], []
        
        # Grab the information of the albums or singles 
        # Album title
        album_title = driver.find_elements(By.ID, "package_title")
        # Album artist
        album_artist = driver.find_elements(By.ID, "package_artist")
        # Album info
        album_info = driver.find_elements(By.CSS_SELECTOR, ".package_infoDataM")
        # Album tracks
        album_tracks = driver.find_elements(By.CSS_SELECTOR, ".package_td1")
        # Album titles
        album_titles = driver.find_elements(By.CSS_SELECTOR, ".package_title2")
        
        # See if all information records are the same (Should be all the same)
        if not all([album_title, album_artist, album_info, album_tracks, album_titles]):
            driver.quit()
            raise RuntimeError("Missing information from the site.")

        # Process the information retrieved by driver and save to each list
        for info in album_title:
            temp = info.text
            ALBUMINFO += temp.splitlines()
        
        for info in album_artist:
            temp = info.text
            ALBUMINFO += temp.splitlines()
        
        for line in album_info:
            temp = line.text
            ALBUMINFO += temp.splitlines()
        
        for info in album_tracks:
            temp = info.text
            track = temp.splitlines()[0]
            TRACKNUM.append(track)
        TRACKNUM.pop(0)
        
        for info in album_titles:
            temp = info.text
            title = temp.splitlines()[0]
            TRACKTTL.append(title)
        
        album_info = ALBUMINFO[1] + " - " + ALBUMINFO[0] + " - " + \
                     ALBUMINFO[2] + " - " + ALBUMINFO[3] + " - " + ALBUMINFO[4]
        
        # Print all the information
        print(album_info)
        for i in range(len(TRACKNUM)):
            track = TRACKNUM[i]
            for j in range(len(TRACKTTL)):
                title = TRACKTTL[i]
                if j != i:
                    continue
                print("%s - %s" %(track, title))
        print()
    driver.quit()

except RuntimeError as err:
    print(err)
