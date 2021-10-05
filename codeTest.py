import os
import errno
from os.path import abspath
import validators
import urllib.request
from urllib.parse import urlparse
from bs4 import BeautifulSoup
from collections import Counter
from datetime import datetime
import requests
import re

# define base directory
BASE = os.path.dirname(abspath(__file__))


def get_metadata(fetch_file):
    with open(fetch_file, encoding="utf8") as fp:
        soup = BeautifulSoup(fp, 'html.parser')

    found_links = Counter(
        [link["href"] for link in soup.find_all("a", href=lambda href: href and not href.startswith("#"))])
    print("num_links: " + str(len(found_links)))
    images = soup.findAll('img')
    print("images: " + str(len(images)))


def download_assets(fetch_url, save_file, save_dir):
    with open(save_file, encoding="utf8") as fp:
        soup = BeautifulSoup(fp, 'html.parser')
    img_tags = soup.find_all('img')
    urls = []
    for img in img_tags:
        if img.has_attr('src'):
            urls.append(img['src'])
        elif img.has_attr('data-src'):
            urls.append(img['data-src'])
    # urls = [img['attrs']['src'] for img in img_tags]

    for url in urls:
        filename = os.path.basename(urlparse(url).path)
        if not filename:
            # print("Regex didn't match with the url: {}".format(url))
            continue
        with open(os.path.join(save_dir,filename), 'wb') as f:
            if 'http' not in url:
                # sometimes an image source can be relative
                # if it is provide the base url which also happens
                # to be the site variable atm.
                url = '{}{}'.format(fetch_url, url)
            response = requests.get(url)
            f.write(response.content)

def main():
    try:
        # get save directory name
        save_folder = input("please input save directory name : ")
        # make save directory path
        save_dir = os.path.join(BASE, save_folder)

        # check exists directory and make
        try:
            os.makedirs(save_dir)
        except OSError as e:
            if e.errno == errno.EEXIST:
                print("directory exists!")
                pass
            else:
                print(str(e))
                return
        # get fetch urls
        urls = input("please input fetch urls (Separate urls with spaces): ")
        url_list = urls.split(" ")
        # loop fetch urls
        for fetch_url in url_list:
            # fetch url validation
            if validators.url(fetch_url):
                # get domain and make save name
                domain = urlparse(fetch_url).netloc
                save_file = os.path.join(save_dir, domain + ".html")
                save_asset_dir = os.path.join(save_dir, domain)
                # check exists directory and make
                try:
                    os.makedirs(save_asset_dir)
                except OSError as e:
                    if e.errno == errno.EEXIST:
                        print("assets download directory exists!")
                        pass
                    else:
                        print(str(e))
                        pass
                # get fetch page to save html
                urllib.request.urlretrieve(fetch_url, save_file)
                # get fetch time
                fetch_time = datetime.utcnow()
                # print meta data
                print("site: " + domain)
                # get meta data function
                get_metadata(save_file)
                print("last_fetch: " + fetch_time.strftime("%A %B %d %Y %H:%M"))

                # download all assets
                download_assets(fetch_url, save_file, save_asset_dir)

            else:
                print(fetch_url + "is not url")

    except Exception as e:
        print(str(e))
        return


if __name__ == "__main__":
    main()
