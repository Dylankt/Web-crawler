import os
import re
from urllib.parse import urlparse
from utils import get_logger
from tokenizer import tokenize, compute_word_frequencies
from bs4 import BeautifulSoup
from UniqueTester import *
from blacklist import blacklist


# process file to get report data
valid_domains = set([".ics.uci.edu/", ".cs.uci.edu/", ".informatics.uci.edu/",
                    ".stat.uci.edu/", "today.uci.edu/department/information_computer_sciences/"])
logger = get_logger("scraper_logger")
# creates output file if output file doesnt exist
if not os.path.exists("output.txt"):
    open("output.txt", "w+").close()

# soup.get_text() and tokenize this and save website and number to file
# logger.info #saves string to file
# logger.error #says string is an error
# status code 200 = success get this from resp.status and log anything that isn't status 200 (like 600-699 which is wrong websites)
# if code 200 use resp.raw_response.text for actual text from website

def scraper(url, resp):
    # defragging of URL
    url = url.split("#")[0]
    # status code 200 = success get this from resp.status and log anything that isn't status 200 (like 600-699 which is wrong websites)
    if resp.status != 200:
        logger.error("URL: " + url +
                     " returned a status code of " + resp.status)
        blacklist.add(url)
        return list()
    if is_valid(url):
        links = extract_next_links(url, resp)
        # use beautifulSoup to get tokens and URLs from websites and append to file
        soup = BeautifulSoup(resp.raw_response.text, "html.parser")
        words_in_file = soup.get_text()
        file_tokens = tokenize(words_in_file)
        # don't crawl websites with less than 250 words or if less than 20% of website is words
        if len(file_tokens) < 250 or len(words_in_file) < 0.2*len(resp.raw_response.text) or len(words_in_file) > 100000:
            blacklist.add(url)
            return list()
        with open("output.txt", "a+") as output:
            # store frequencies of each word and number of words for each page
            output.write(url + "\n" + str(len(file_tokens)) + "\n" +
                         str(compute_word_frequencies(file_tokens)) + "\n")
    return [link for link in links if is_valid(link)]

def extract_next_links(url, resp):
    if resp.status == 200:
        # use beautifulSoup to get URLs from websites and append to file
        soup = BeautifulSoup(resp.raw_response.text, "html.parser")
        links = set()
        for link in soup.find_all('a', href=True):
            links.add(link.get('href').split("#")[0])
    return links




def is_valid(url):
    with open("output.txt", "r+") as output:
        # defragging of URL
        url = url.split("#")[0]
        try:
            parsed = urlparse(url)
            output.seek(0)
            # check if its an href url
            if parsed.scheme not in set(["http", "https"]):
                logger.error(parsed + " is not a href url")
                return False
            # check if previously crawled
            elif parsed in output:
                logger.error("URL: " + url + " has already been crawled")
                return False
            # check if in blacklist
            elif parsed.netloc in blacklist:
                logger.error("URL: " + url + " is in my blacklist")
            # check if in valid domains
            valid = False
            for domain in valid_domains:
                if domain in parsed.netloc:
                    valid = True
            if valid == False:
                logger.error("URL: " + url +
                             " is not in the correct domain")
                return valid
            return not re.match(
                r".*\.(css|js|bmp|gif|jpe?g|ico"
                + r"|png|tiff?|mid|mp2|mp3|mp4"
                + r"|wav|avi|mov|mpeg|ram|m4v|mkv|ogg|ogv|pdf"
                + r"|ps|eps|tex|ppt|pptx|doc|docx|xls|xlsx|names"
                + r"|data|dat|exe|bz2|tar|msi|bin|7z|psd|dmg|iso"
                + r"|epub|dll|cnf|tgz|sha1"
                + r"|thmx|mso|arff|rtf|jar|csv"
                + r"|rm|smil|wmv|swf|wma|zip|rar|gz)$", parsed.path.lower())
            # blacklist urls (avoid WICS.ics.uci.edu)
        except TypeError:
            print("TypeError for ", url)
            raise
