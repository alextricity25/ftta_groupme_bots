from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

from .models import Greeting

import time
import requests
import re
import random
import os
import logging
import json


# Create your views here.
def index(request):
    # return HttpResponse('Hello from Python!')
    return render(request, 'index.html')


def ride(request):

    some_ride_data = "The time is: {}".format(time.ctime())
    return render(request, 'ride.html', {'time': some_ride_data})


def _upload_groupme_image(access_token, filename):
    url = 'https://image.groupme.com/pictures'
    headers = {
        'X-Access-Token': access_token,
        'Content-Type': 'image/png'
    }
    r = requests.post(
        url,
        data=open("{}.png".format(filename), 'rb').read(),
        headers=headers
    )
    return r


@csrf_exempt
def pick_a_song(request):
    logger = logging.getLogger(__name__)
    if request.method == 'POST':
        BOT_ID = os.environ['GROUPME_BOT_ID']
        ACCESS_TOKEN = os.environ['GROUPME_ACCESS_TOKEN']
        # URL of bot post
        url = "https://api.groupme.com/v3/bots/post"
        # Get the text from the message
        r_dict = json.loads(request.body)

        if 'hello' in r_dict['text'].lower():
            data = {
                'text': 'HI THERE',
                'bot_id': BOT_ID
            }
            r = requests.post(url, json=data)

        if ('#sendsong' in r_dict['text'].lower() or
           '#hymn' in r_dict['text'].lower()):
            from wand.image import Image
            import PyPDF2

            # The user can either get a random song from
            # the uk yp songbook, or requests a specific
            # hymn number from the guitar hymnal
            if '#hymn' in r_dict['text'].lower():
                songbook_name = "guitar_hymnal.pdf"
                hymn_rt = re.search(r"#hymn ([0-9]+)", r_dict['text'])
                if hymn_rt:
                    page_number = int(hymn_rt.group(1))
                else:
                    # If page number is not recognized by the regexp above,
                    # then always return page number 1
                    page_number = 1
            elif '#sendsong' in r_dict['text'].lower():
                songbook_name = "uk_songbook.pdf"
            # Getting random page from the UK songbook...
            pdf_file_obj = open(
                               "/app/data/{}".format(songbook_name),
                               'rb')
            pdf_reader = PyPDF2.PdfFileReader(pdf_file_obj, strict=False)
            pdf_writer = PyPDF2.PdfFileWriter()
            number_of_pages = pdf_reader.numPages
            # If a song from the uk yp songbook is requested, then pick a
            # random page.
            if '#sendsong' in r_dict['text'].lower():
                page_number = random.randint(0, number_of_pages - 1)

            page_obj = pdf_reader.getPage(page_number)
            pdf_writer.addPage(page_obj)

            # Save random page as seperate file
            filename = "/tmp/songbook_{}".format(page_number)
            pdf_output = open(filename, 'wb')
            pdf_writer.write(pdf_output)
            pdf_output.close()

            # Convert pdf document to PNG
            with Image(filename=filename, resolution=200) as img:
                img.negate(grayscale=True)
                img.save(filename="{}.png".format(filename))

            # Send to GroupMe Image Service
            r = _upload_groupme_image(ACCESS_TOKEN, filename)
            logger.info("ALEX - Image service response: {}".format(r.text))
            response_dict = json.loads(r.text)
            image_url = response_dict['payload']['picture_url']

            # Post the image to the group
            data = {
                'bot_id': BOT_ID,
                'attachments': [
                    {
                        "type": "image",
                        "url": image_url
                    }
                 ]
            }
            requests.post(url, json=data)
            os.remove(filename)
            os.remove("{}.png".format(filename))

    return render(request, 'pick_a_song.html', {'request': request})


def db(request):

    greeting = Greeting()
    greeting.save()

    greetings = Greeting.objects.all()

    return render(request, 'db.html', {'greetings': greetings})


def memory_verse(request):
    return render(request, 'memory_verses.html')
