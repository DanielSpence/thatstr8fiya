import urllib.request
import re

#creates the complete url for the top 50
def appendURL(list):
    count = 0;
    for a in list:
        list[count] = 'https://soundcloud.com' + list[count]
        count = count + 1;
    return list

def scrapeLink():
    html = urllib.request.urlopen("https://soundcloud.com/charts/top?genre=hiphoprap")
    htmlString = str(html.read())
    list = re.findall(r'<a itemprop="url" href=[\'"]?([^\'" >]+)', htmlString)
    return list

#scraps the top 50 of the week for hiphop and returns a list of the links
def createSoundCloudLinks():
    list = scrapeLink()
    return appendURL(list)
        
songList = createSoundCloudLinks()

