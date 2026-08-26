import requests
import bs4 
from fake_headers import Headers
from datetime import datetime
from urllib.parse import urljoin


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

        #article_link = 'https://habr.com' + article_tag.find('a')['href']
        article_link = urljoin('https://habr.com', article_tag.find('a')['href'])
        if not article_link.startswith('https://habr.com/'):
            continue
        #print(article_link)

        article_prewiew_tag = soup_article.find('div', class_='lead')
        article_prewiew_text = article_prewiew_tag.text.strip()
        if any(word.lower() in article_prewiew_text.lower() for word in KEYWORDS):
            print(f"{article_date_str} - {article_title} - {article_link}")

        #--Дополнительное (необязательное) задание -----------------------------
        response_full_article = requests.get(article_link, headers=headers)
        soup_full_article = bs4.BeautifulSoup(response_full_article.text, features='lxml')
        full_article_text = soup_full_article.find('div', class_='tm-article-presenter__body').text.strip()

        #if any(word.lower() in article_title.lower() for word in KEYWORDS):
        if any(word.lower() in full_article_text.lower() for word in KEYWORDS):
            print(f"{article_date_str} - {article_title} - {article_link}")


if __name__ == '__main__':
    main()