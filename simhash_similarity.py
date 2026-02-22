import sys
import requests as re
import bs4 as bs

def getResponseBody(url):
    header={"User-Agent": "Mozilla/5.0"}
    try:
        response=re.get(url,headers=header)
        if response.status_code==200:
            soup=bs.BeautifulSoup(response.text,'html.parser') 
            body=soup.find('body')
            if body:
                body=body.get_text(separator=" ",strip=True)
                body=" ".join(body.split())
            return body
        else:
            print("response code:",response.status_code)
            return None
        
    except Exception as e:
        print(e)
        return None
    
def countWordFreq(response):
    freqDict={}
    words=response.lower().split()
    for word in words:
        if word in freqDict:
            freqDict[word]+=1
        else:
            freqDict[word]=1
    return freqDict



def polynomialrollingHash(word,p=53,m=2**64):
    hash_value=0
    #hash_value += ASCII * current_power
    curren_power=0
    power_value=1
    for char in word:
        hash_value+=ord(char)*(power_value)
        curren_power+=1
        power_value*=p
    return hash_value&((1<<64)-1)

def getSimHash(freqDict):
    listOfsimhash=[0]*64 
    for word,freq in freqDict.items():
        hash_value=polynomialrollingHash(word)
        for i in range(64):
            if hash_value&(1<<i):
                listOfsimhash[i]+=freq
            else:
                listOfsimhash[i]-=freq
    simhash=0
    for i in range(64):
        if listOfsimhash[i]>0:
            simhash|=(1<<i)
    return simhash


def commonBit(simhash1,simhash2):
    x=simhash1^simhash2
    distance=0
    for i in range(64):
        if x&(1<<i):
            distance+=1
    return 64-distance

if __name__=="__main__":
    if(len(sys.argv) != 3):
        print("Usage: python crawler.py <url1> <url2>")
        sys.exit(1)
    url1=sys.argv[1]
    url2=sys.argv[2]
    response1=getResponseBody(url1)
    response2=getResponseBody(url2)
    if response1 and response2:
        freqDict1=countWordFreq(response1)
        freqDict2=countWordFreq(response2)
        simhash1=getSimHash(freqDict1)
        simhash2=getSimHash(freqDict2)
        common_bits=commonBit(simhash1,simhash2)
        print(f"Common bits: {common_bits}")
    else:
        print("Failed to fetch data")