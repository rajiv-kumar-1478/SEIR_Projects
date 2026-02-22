import sys
import requests as re
import bs4 as bs


def crawl(url):
    header={
        'User-Agent': 'Mozilla/5.0',
    }
    try:
        response = re.get(url,timeout=(5,20),headers=header)
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

    
    body=soup.find('body')
    if body:
        body=body.get_text(separator=" ",strip=True)
        body=" ".join(body.split())
        # print(type(body))
        print(body)

    anchors=soup.find_all('a')
    links=[]
    for anchor in anchors:
        href=anchor.get('href')
        if href and (href.startswith('http') or href.startswith('https')):
            links.append(href)
        if href and href.startswith('/'):
            links.append(url+href)
    print(" ".join(links))
    
        
if __name__=="__main__":
    if (len(sys.argv))<2:
        print("Usage python crawler.py <url>")
        sys.exit(1)
        
    url=sys.argv[1]
    html=crawl(url)
    if html:
        parse(html,url)


