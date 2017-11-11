from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

from .models import Greeting

import time
import requests
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

@csrf_exempt
def pick_a_song(request):
    logger = logging.getLogger(__name__)
    if request.method == 'POST':
        # MemoryVerseBot bot_id
        ACCESS_TOKEN = 'INSERTTOKEN'
        # SingSongsToHim bot_id
        #ACCESS_TOKEN = 'INSERTOKEN'
        # URL of bot post
        url = "https://api.groupme.com/v3/bots/post"
        # Headers for the bot to post
        headers = {'X-Access-Token': ACCESS_TOKEN}
        # Get the text from the message
        r_dict = json.loads(request.body)

        if 'hello' in r_dict['text'].lower():
            data = {
                'text': 'HI THERE',
                'bot_id': ACCESS_TOKEN
            }
            r = requests.post(url, json=data)

        if '#sendsong' in r_dict['text'].lower():
            from wand.image import Image
            import PyPDF2
            # Getting random page from the UK songbook...
            pdf_file_obj = open('/app/hello/uk_songbook.pdf', 'rb')
            pdf_reader = PyPDF2.PdfFileReader(pdf_file_obj, strict=False)
            pdf_writer = PyPDF2.PdfFileWriter()
            number_of_pages = pdf_reader.numPages
            random_page = random.randint(0, number_of_pages -1)
            page_obj = pdf_reader.getPage(random_page)
            pdf_writer.addPage(page_obj)

            # Save random page as seperate file
            filename = "/tmp/uk_songbook_{}".format(random_page)
            pdf_output = open(filename, 'wb')
            pdf_writer.write(pdf_output)
            pdf_output.close()

            # Convert pdf document to PNG
            with Image(filename=filename, resolution=200) as img:
                img.negate(grayscale=True)
                img.save(filename="{}.png".format(filename))

            # Send to GroupMe Image Service
            ALEX_ACCESS_TOKEN = os.environ['GROUPME_ACCESS_TOKEN']
            image_api_url = 'https://image.groupme.com/pictures'
            image_api_headers = {
                'X-Access-Token': ALEX_ACCESS_TOKEN,
                'Content-Type': "image/png"
            }
            r = requests.post(image_api_url, data=open("{}.png".format(filename), 'rb').read(), headers=image_api_headers)
            logger.info("ALEX - Image service response: {}".format(r.text))
            response_dict = json.loads(r.text)
            image_url = response_dict['payload']['picture_url']

            # Post the image to the group
            data = {
                'bot_id': ACCESS_TOKEN,
                'attachments': [
                    {
                        "type": "image",
                        "url": image_url
                    }
                 ]
            }
            rg = requests.post(url, json=data)
            os.remove(filename)
            os.remove("{}.png".format(filename))

    return render(request, 'pick_a_song.html', {'request': request})

def db(request):

    greeting = Greeting()
    greeting.save()

    greetings = Greeting.objects.all()

    return render(request, 'db.html', {'greetings': greetings})

