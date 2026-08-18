import requests
import bs4 
from fake_headers import Headers
from datetime import datetime


## Определяем список ключевых слов:
KEYWORDS = ['дизайн', 'фото', 'web', 'python']

url = 'https://habr.com/ru/articles/'
headers = Headers(browser='chrome', os='windows').generate()
response = requests.get(url, headers=headers)


soup = bs4.BeautifulSoup(response.text, features='lxml')
soup_articles = soup.find_all('div', class_='article-snippet')

def main():

    for soup_article in soup_articles:

        article_time = soup_article.find('time')['datetime']
        article_time_date = datetime.strptime(
            article_time,
            '%Y-%m-%dT%H:%M:%S.%fZ'
        )
        article_date_str = article_time_date.strftime('%d.%m.%Y')
        #print(article_date_str)

        article_tag = soup_article.find('h2', class_='tm-title tm-title_h2')

        article_title = article_tag.text.strip()
        #print(article_title)

        article_link = 'https://habr.com' + article_tag.find('a')['href']
        #print(article_link)

        response_full_article = requests.get(article_link, headers=headers)
        soup_full_article = bs4.BeautifulSoup(response_full_article.text, features='lxml')
        full_article_text = soup_full_article.find('div', class_='tm-article-presenter__body').text.strip()

        #if any(word.lower() in article_title.lower() for word in KEYWORDS):
        if any(word.lower() in full_article_text.lower() for word in KEYWORDS):
            print(f"{article_date_str} - {article_title} - {article_link}")


if __name__ == '__main__':
    main()