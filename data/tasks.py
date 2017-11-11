from celery import task
import os
import requests
import logging
import random
import re
from bs4 import BeautifulSoup


def fetch_verse():
    """
    Fetch a verse from online.recoveryversion
    """
    BIBLE = {
        "Genesis": {
            "chapters": 50
        },
        "Exodus": {
            "chapters": 40
        },
        "Leviticus": {
            "chapters": 27
        },
        "Numbers": {
            "chapters": 36
        },
        "Deuteronomy": {
            "chapters": 34
        },
        "Joshua": {
            "chapters": 24
        },
        "Judges": {
            "chapters": 21
        },
        "Ruth": {
            "chapters": 4
        },
        "1 Samuel": {
            "chapters": 31
        },
        "2 Samuel": {
            "chapters": 24
        },
        "1 Kings": {
            "chapters": 22
        },
        "2 Kings": {
            "chapters": 25
        },
        "1 Chronicles": {
            "chapters": 29
        },
        "2 Chronicles": {
            "chapters": 36
        },
        "Ezra": {
            "chapters": 10
        },
        "Nehemiah": {
            "chapters": 13
        },
        "Esther": {
            "chapters": 10
        },
        "Job": {
            "chapters": 42
        },
        "Psalms": {
            "chapters": 150
        },
        "Proverbs": {
            "chapters": 31
        },
        "Ecclesiastes": {
            "chapters": 12
        },
        "Song of Songs": {
            "chapters": 8
        },
        "Isaiah": {
            "chapters": 66
        },
        "Jeremiah": {
            "chapters": 52
        },
        "Lamentations": {
            "chapters": 5
        },
        "Ezekiel": {
            "chapters": 48
        },
        "Daniel": {
            "chapters": 12
        },
        "Hosea": {
            "chapters": 14
        },
        "Joel": {
            "chapters": 3
        },
        "Amos": {
            "chapters": 9
        },
        "Obadiah": {
            "chapters": 1
        },
        "Jonah": {
            "chapters": 4
        },
        "Micah": {
            "chapters": 7
        },
        "Nahum": {
            "chapters": 3
        },
        "Habakkuk": {
            "chapters": 3
        },
        "Zephaniah": {
            "chapters": 3
        },
        "Haggai": {
            "chapters": 2
        },
        "Zechariah": {
            "chapters": 14
        },
        "Malachi": {
            "chapters": 4
        },
        "Matthew": {
            "chapters": 28
        },
        "Mark": {
            "chapters": 16
        },
        "Luke": {
            "chapters": 24
        },
        "John": {
            "chapters": 21
        },
        "Acts": {
            "chapters": 28
        },
        "Romans": {
            "chapters": 16
        },
        "1 Corinthians": {
            "chapters": 16
        },
        "2 Corinthians": {
            "chapters": 13
        },
        "Galatians": {
            "chapters": 6
        },
        "Ephesians": {
            "chapters": 6
        },
        "Philippians": {
            "chapters": 4
        },
        "Colossians": {
            "chapters": 4
        },
        "1 Thessalonians": {
            "chapters": 5
        },
        "2 Thessalonians": {
            "chapters": 3
        },
        "1 Timothy": {
            "chapters": 6
        },
        "2 Timothy": {
            "chapters": 4
        },
        "Titus": {
            "chapters": 3
        },
        "Philemon": {
            "chapters": 1
        },
        "Hebrews": {
            "chapters": 13
        },
        "James": {
            "chapters": 5
        },
        "1 Peter": {
            "chapters": 5
        },
        "2 Peter": {
            "chapters": 3
        },
        "1 John": {
            "chapters": 5
        },
        "2 John": {
            "chapters": 1
        },
        "3 John": {
            "chapters": 1
        },
        "Jude": {
            "chapters": 1
        },
        "Revelation": {
            "chapters": 22
        }
    }
    # Logger
    logger = logging.getLogger(__name__)

    retries = 0
    status_code = 0
    while status_code != 200 and retries < 5:

        # Randomize the book
        # Take note of the one-off number due to
        # indicies starting at zero
        book_number = random.randint(1, len(BIBLE.keys()))
        book_name = list(BIBLE.keys())[book_number]
        chapter_number = random.randint(1, int(BIBLE[book_name]['chapters']))
        
        #print("http://online.recoveryversion.bible/txo/{}_{}{}.htm".format(book_number + 1, book_name.replace(" ", ""), chapter_number))
        url = "http://online.recoveryversion.bible/txo/{}_{}{}.htm".format(book_number + 1, book_name.replace(" ", ""), chapter_number)
        
        r = requests.get(url)
        status_code = r.status_code

        # If status code is not 201, there is no need
        # to continue with this iteration. Istead, we
        # Are going to rety the request
        if status_code != 200:
            retries += 1
            logger.info("ALEX the status code is: {}".format(status_code))
            logger.info("ALEX - Could not successfully send request this time. Retrying..")
            continue
    
        chapter_html = r.text
        soup = BeautifulSoup(chapter_html, 'html.parser')
        verses_list_soup = soup.get_text().split('\n')
        # Clean up verses_list
        verses_list = []
        for verse in verses_list_soup:
            if re.search(r'[0-9]+:[0-9]+', verse):
                verses_list.append(verse)
        
        random_verse_index = random.randint(1, len(verses_list) - 1)
        logger.info("ALEX - Sending Verse: {}".format(verses_list[random_verse_index]))


    if retries >= 5:
        logger.info("ALEX - Number of retries exceeded. Nothing returned..")
        return " "

    return "{} {}".format(book_name, verses_list[random_verse_index])
    

@task()
def add(x, y):
    return x + y

@task()
def groupme_verse(message="", groupme_id=os.environ["TEST_GROUPID"]):
    GROUP_ID = groupme_id
    ACCESS_TOKEN = os.environ["GROUPME_ACCESS_TOKEN"]

    headers = {'X-Access-Token': ACCESS_TOKEN}
    verse = fetch_verse()
    data = {
        'message': {
            'source_guid': "GUID",
            'text': "{}\n Random verse of the day: \n{}".format(message, verse)
        }
    }
    url = "https://api.groupme.com/v3/groups/{}/messages".format(
        GROUP_ID
    )
    logger = logging.getLogger(__name__)
    r = requests.post(url, json=data, headers=headers)
    if r.status_code != 201:
        data['text'] = "Failed to send verse..."
        r2 = requests.post(url, json=data, headers=headers)
    logger.info("ALEX - sending request to URL: {}".format(url))
    logger.info("ALEX - response is:".format(r.text))
    logger.info("ALEX - status code: {}".format(r.status_code))

@task()
def hit_myself():
    logger = logging.getLogger(__name__)
    logger.info("ALEX - Sending a request to our selves...")
    r = requests.get('https://thawing-savannah-68245.herokuapp.com/')


