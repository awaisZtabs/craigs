from django.shortcuts import render
import requests
from bs4 import BeautifulSoup
from . import models 
from requests.compat import quote_plus
BASE_CRAIGLIST_URL = 'https://newyork.craigslist.org/d/for-sale/search/sss?query={}'
BASE_IMAGE_URL = 'https://images.craigslist.org/{}_300x300.jpg'
# Create your views here.
def home(request):
    return render(request, 'base.html')
    

def new_search(request):
    search = request.POST.get('search')
    # models.Search.objects.create(search=search)
    final_url = BASE_CRAIGLIST_URL.format(quote_plus(search))
    response = requests.get(final_url)
    data = response.text
    soup = BeautifulSoup(data, features='html.parser')

    post_listings = soup.findAll('li', {'class': 'result-row'})

    final_posting = []

    for post in post_listings:
        # get the title of post
        post_title = post.find(class_='result-title').text   
        # get the title of url from a tag
        post_url = post.find('a').get('href')

        if post.find(class_='result-price'):
            post_price = post.find(class_='result-price').text 
            post_url = post.find('a').get('href')
        else:
            post_price = 'N/A'

        if post.find(class_='result-image').get('data-ids'):
            post_image_id = post.find(
                class_='result-image').get('data-ids').split(',')[0].split(':')[1]
            post_image_url = BASE_IMAGE_URL.format(post_image_id)
            # print(post_image_url)
        else:
            post_image_url = 'https://craigslist.org/images/peace.jpg'

        final_posting.append((post_title, post_url, post_price, post_image_url))
        


    stuff_for_front_end = {
        'search' : search,
        'final_posting': final_posting
    }
    print(final_posting[0])

    return render(request, 'my_app/new_search.html', stuff_for_front_end)
    

    # post_titles.text
    # post_titles.get('href')  for scraping link out of a-tag
    # post_titles = soup.findAll('a', {'class': 'result-title'})    # print(final_url)
