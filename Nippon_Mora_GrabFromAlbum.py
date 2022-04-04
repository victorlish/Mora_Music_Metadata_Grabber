from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import mutagen, glob, requests, os.path

# The page of the album or the single
site = "https://mora.jp/package/43000087/SECL02421B00Z/"

# The location of the FLACs located
files = r"D:\tidal-dl\Album\Aimer\M_109966454_2019_Penny Rain"

try:
    
    # See if the input of location and site is empty
    if not files or not site:
        raise RuntimeError("No input.")
    LISTFILES = glob.glob(os.path.join(files, "*.flac"))
    
    # See if the directory is empty or not
    if not LISTFILES:
        raise RuntimeError("No File.")
    
    # See if the link inputtede is from Mora.jp or not
    if not site.startswith("https://mora.jp/package/"):
        raise RuntimeError("Invaild URL.")
    
    # See if the link inputted is reachable or not
    response = requests.get(site, timeout = 5)
    if response.status_code != requests.codes.ok:
        raise RuntimeError("Unreachable URL.")
    
    # Set and run ChromeDriver in headless
    print("Seting up Chromedriver.")
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_experimental_option('excludeSwitches', ['enable-logging'])
    driver = webdriver.Chrome(options=chrome_options)
    driver.get(site)
    
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
    driver.quit()
    
    # Check if the information and FLACs has the same amount or not (Will edit)
    if not len(TRACKNUM) == len(TRACKTTL) == len(LISTFILES):
        raise RuntimeError("Files and retrieved information mismatch.")
    
    print("{} - {} - {} - {} - {}".format(ALBUMINFO[1], ALBUMINFO[0], ALBUMINFO[2], \
                                          ALBUMINFO[4], ALBUMINFO[3]))
    
    # Open each FLACs and apply the information as tags
    for f in range(len(LISTFILES)):
        audio = mutagen.File(LISTFILES[f])
        print(">>>>>>>>>>>>>>>>>")
        for i in range(len(TRACKNUM)):
            tracknum = TRACKNUM[f]
            if i != f:
                continue
            for j in range(len(TRACKTTL)):
                tracktitle = TRACKTTL[f]
                if j != f:
                    continue
                print(tracknum + "_" + tracktitle)
                audio["artist"] = ALBUMINFO[1]
                audio["album"] = ALBUMINFO[0]
                audio["title"] = tracktitle
                audio["track"] = str(tracknum)
                audio["tracktotal"] = str(len(LISTFILES))
                audio["date"] = ALBUMINFO[3]
                audio["lyrics"] = ""
                audio.save()
                print(audio.pprint())

except RuntimeError as err:
    print(err)

# =============================================================================
# Search artist
# driver.get("https://mora.jp")
# driver.find_element_by_id("search").send_keys("Aimer")
# elements = driver.find_elements_by_class_name("searchBtn")
# for e in elements:
#     e.click()
# driver.quit()
# =============================================================================