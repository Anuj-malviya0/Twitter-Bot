#imports
from pyunsplash import PyUnsplash
from PIL import Image ,ImageDraw,ImageFont
from datetime import date
import os , requests, random , textwrap, tweepy

#Twitter keys and setting up Api elements
CONSUMER_KEY = '''Twitter account tokens comes here'''
CONSUMER_SECRET ='''Twitter account tokens comes here'''
ACCESS_KEY = '''Twitter account tokens comes here'''
ACCESS_SECRET = '''Twitter account tokens comes here'''

auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_KEY, ACCESS_SECRET)
api = tweepy.API(auth)

#key for accessing the images
UNSPLASH_ACCESS_KEY ='''Unspalash developer account acces token'''
#using the api to get the random quote
def get_quote():
	url='https://programming-quotes-api.herokuapp.com/quotes/random'
	data=requests.get(url)
	quote=data.json()['en']
	return quote

#using the api to get a random image
def get_image():
	file='image.png'
	if os.path.exists(file):
		os.remove(file)
	pu = PyUnsplash(api_key=UNSPLASH_ACCESS_KEY)
	img_data = pu.photos(type_='random', count=1, featured=True, query="dark flower",orientation="portrait")
	[photo] = img_data.entries
	response = requests.get(photo.link_download)
	open('image.png', 'wb').write(response.content)#saving image with image.png name

#resizing the image for desired size
def resize_image(file,ratio=0.5):
    file=Image.open(file)
    w,h=file.size
    if w>3800:
        ratio=1/3
    new=file.resize((round(w*ratio),round(h*ratio)))
    new.save('image_s.jpeg')#saving resized image with image_s.png name

#randomizing the font the font
def font_random():
    font_list=[
    r"fonts\kodakku.ttf",
    r"fonts\Sports World-Regular.ttf",
    r"fonts\theboldfont.ttf",
    r"fonts\Viafont.ttf"]
    font = ImageFont.truetype(random.choice(font_list), fontsize)
    return font

def draw_multiple_line_text(image, text, font, text_color, text_start_height):
    '''
    From unutbu on python PIL draw multiline text on image
    '''
    draw = ImageDraw.Draw(image)
    image_width, image_height = image.size
    y_text = text_start_height
    lines = textwrap.wrap(text, width=20)#40
    for line in lines:
        line_width, line_height = font.getsize(line)
        line_height+=10
        draw.text(((image_width - line_width) / 2, y_text), 
                  line, font=font, fill=text_color)
        y_text += line_height


def Write():
    image=Image.open('image_s.jpeg')
    # Randomizing the font by using font_random function
    font = font_random()
    # Fetching the text with the get_quote function
    text1 = text_q
    # Getting the image dimesnions size
    w,h=image.size
    # Text color in RGB
    text_color = (255, 255, 255)
    # Hegiht at which the text starts
    text_start_height = h/3
    draw_multiple_line_text(image, text1, font, text_color, text_start_height)
    image.save('text_img.jpg')#saving image with text with text_img name
    os.remove('image_s.jpeg')
    os.remove('image.png')

#function that tweets things
def tweet(text):
    tweet =text
    media = api.media_upload("text_img.jpg")
    print("Tweeting the image and text")
    post_result = api.update_status(status=tweet, media_ids=[media.media_id])
    print("done")
#function that gives date in specific format
def date_():
    now=date.today()
    now=now.strftime("%b-%d-%y")
    return now
#globals
text_q=get_quote()
fontsize = 100     
prev='Apr-24-22'

def main():
    global prev 
    while True:
        if date_() != prev:
            get_image()
            resize_image(file='image.png')
            Write()
            tweet(text_q)
            prev=date_()

if __name__ == "__main__":





    main()
