import logging

from io import BytesIO

from flask import Flask
from flask import send_file

from requests_html import HTMLSession

from PIL import Image, ImageDraw, ImageFont

import time
import atexit

from appschduler.schedulers.background import BackgroundScheduler

app = Flask(__name__)

output = BytesIO()

generate_image()

scheduler = BackgroundScheduler(timezone=utc)
scheduler.add_job(func=generate_image, trigger='cron', hour=0, minute=5)

def generate_image():
	session = HTMLSession()
	r = session.get('https://en.wikiquote.org/wiki/Wikiquote:Quote_of_the_day?action=render')
    wikitext = r.html.find('div > center > table', first=True).text
    img = Image.new('RGB', (800,150), color='white')
    fnt = ImageFont.truetype('Montserrat-Regular.ttf', 14)
    d = ImageDraw.Draw(img)
    d.multiline_text((10,10), wikitext, font=fnt, fill='black', spacing=6)
    img.save(output, format='PNG')
    output.seek(0)

@app.route('/')
def hello():
    return send_file(output, mimetype='image/png')

@app.errorhandler(500)
def server_error(e):
    # Log the error and stacktrace.
    logging.exception('An error occurred during a request.')
    return 'An internal error occurred.', 500
# [END app]
