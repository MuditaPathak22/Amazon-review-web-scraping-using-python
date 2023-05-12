import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
import requests
from bs4 import BeautifulSoup
import pandas as pd

reviewlist = []

def get_soup(url):
    r = requests.get('http://localhost:8050/render.html', params={'url': url, 'wait': 2})
    soup = BeautifulSoup(r.text, 'html.parser')
    return soup


def get_reviews(soup):
    reviews = soup.find_all('div', {'data-hook': 'review'})
    try:
        for item in reviews:
            review = {
            'product': soup.title.text.replace('Amazon.in:Customer reviews:', '').strip(),
            'title': item.find('a', {'data-hook': 'review-title'}).text.strip(),
            'rating':  float(item.find('i', {'data-hook': 'review-star-rating'}).text.replace('out of 5 stars', '').strip()),
            'body': item.find('span', {'data-hook': 'review-body'}).text.strip(),
            }
            reviewlist.append(review)
    except:
        pass

for x in range(5):
    soup = get_soup(f'https://www.amazon.co.uk/product-reviews/B07WD58H6R/ref=cm_cr_arp_d_paging_btm_next_2?ie=UTF8&reviewerType=all_reviews&pageNumber=%7Bx%7D={x}')
    print(f'Getting page: {x}')
    get_reviews(soup)
    print(len(reviewlist))
    if not soup.find('li', {'class': 'a-disabled a-last'}):
        pass
    else:
        break

df = pd.DataFrame(reviewlist)
df.to_excel('new.xlsx', index=False)
print('Fin.')

df = pd.read_excel('new.xlsx')
print(df.head()) # print the first 5 rows of the data
print(df.info()) # print information about the data
print(df.describe()) # print summary statistics for the data
plt.bar(df['title'], df['rating'], color='red')
plt.title('My Bar Chart')
plt.xlabel('title')
plt.ylabel('rating')
plt.show()

