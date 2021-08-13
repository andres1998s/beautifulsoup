import requests
import lxml.html as html
import datetime
import os 

XPATH_LINKS = '//text-fill/a/@href'
JOURNALIST_LINK = 'https://www.larepublica.co/'
XPATH_TITLE =   '//div[@class="row OpeningPostNormal"]/div/div/text-fill/span/text()'
XPATH_SUMMARY = '//div[@class="row article-wrapper"]//div[@class="lead"]/p/text()'
XPATH_BODY = '//div[@class="html-content"]/p/text()'


def parse_notice(link, today):
    try:
        response = requests.get(link)
        if response.status_code != 200:
            raise ValueError(f'Error   {response.status_code}')
        
        notice = response.content.decode('utf-8')
        parse_notice = html.fromstring(notice)
        
        try:
            title = parse_notice.xpath(XPATH_TITLE)[0]
            title = title.replace('\"' , '')
            summary = parse_notice.xpath(XPATH_SUMMARY)[0]
            body = parse_notice.xpath(XPATH_BODY) 
            #print(f'{title} \n {link} \n \n ')

        except IndexError:
            return
        
        with open(f'{today}/{title}.txt' , 'w' , encoding='utf-8') as f:
            f.write(f'{title}  \n \n \n ')
            f.write(f'{summary} \n \n \n ')
            for i in body:
                f.write(f'{i} \n \n ')
                     
    except ValueError as ve:
        print(ve)
        



def parse_home():
    try:
        response = requests.get(JOURNALIST_LINK)
        if response.status_code == 200:
            content = response.content.decode('utf-8')
            parsed_home = html.fromstring(content)

            links_to_notice = parsed_home.xpath(XPATH_LINKS)
            #for a,b in enumerate(links_to_notice):
            #   print(f'{a}   {b}')
            
            today = datetime.date.today().strftime('%d-%m-%Y')
            if not os.path.isdir(today):
                os.mkdir(today)
            
            for link in  links_to_notice:
                  parse_notice(link , today)
              
              
        else:
            raise ValueError(f'Erros:   {response.status_code}')
    except ValueError as ve:
        print(ve)
        
        
if __name__ == '__main__':
    parse_home()