import requests,webbrowser
from bs4 import BeautifulSoup



def google():
    search_word = 'facebook'
    USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.129 Safari/537.36"
    link = f'https://www.google.com/search?q={search_word}'
    headers = {"user-agent" : USER_AGENT}
    response = requests.get(link, headers=headers)
    text = response.text
    soup = BeautifulSoup(text, "html.parser")
    search_result=soup.select('.r a')
    # a = soup.find_all('h3', {'class': 'LC20lb DKV0Md'})
    
    # search_headers=soup.find_all('h3',{'class':'LC20lb DKV0Md'})
    search_result=soup.find_all('div',{'class':'r'})
    # print(search_headers)
    # for i in range(6):
    
    res=''
    num=0
    for a in search_result:
        search_text=soup.find_all('h3',{'class':'LC20lb DKV0Md'})
        search_result_link=soup.select('.r a')
        or_headers=search_text[num].text
        for i in search_result_link:
            or_link=i.get('href')

        res+=or_headers+ '\n'+or_link+'\n'    
        num+=1
    
         
    # for link in search_result[:6]:
        
    #     res+=or_link+'\n'  
    return res  
            
            
        
        
google()