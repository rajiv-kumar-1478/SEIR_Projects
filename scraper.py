import sys
import requests as re
import bs4 as bs
from urllib.parse import urljoin

def crawl(url):
    header={
        'User-Agent': 'Mozilla/5.0',
    }
    try:
        response = re.get(url,headers=header)
        if response.status_code==200:
            return response.text
        else:
             return None
    except Exception as e:
        print(e)
        return None 
    
def parse(html,url):
    soup=bs.BeautifulSoup(html,'html.parser') 
    
    title=soup.find('title')
    # title=title.strip()
    if title:
        title=title.text.strip()
        print(title)

    body = soup.find('body')
    if body:
        body=body.get_text(separator=" ", strip =True)
        # print(type(body))
        print(body)

    anchors=soup.find_all('a')
    
    for anchor in anchors:
        href=anchor.get('href')
        if href:
            full_url = urljoin(url, href)
            print(full_url)
    
        
if __name__=="__main__":
    if (len(sys.argv))<2:
        print("Usage: python scraper.py <url>")
        sys.exit(1)
        
    url = sys.argv[1]

    if not url.startswith("http://") and not url.startswith("https://"):
        url = "https://" + url
    html=crawl(url)
    if html:
        parse(html,url)





