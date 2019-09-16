from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import random
import json
import requests
import re
import logging

#A Simple Telegram Bot that fetches pictures of Cats/Dogs and Bible verses
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

def ranFindMsg(typ):
    if typ == "dog":
        comments = ["Finding you a puppy! :)", "Fetching you a puppy! :)","Fetching one!", "Here you go :)", "wooffff", "woof!", "woof"]
        i = random.randint(0,6)
    elif typ == "cat":
        comments = ["Okay... Fetching you a cat!", "Fetching you a cat! :)","Fetching one!", "Here you go :)", "wooffff", "woof!", "woof"]
        i = random.randint(0,6)
    return comments[i]

	
def get_jpgUrlDog():
    contents = requests.get('https://random.dog/woof.json').json()
    jpg = contents['url']
    return jpg

def get_jpgUrlCat():
    contents = requests.get('http://aws.random.cat/meow').json()    
    jpg = contents['file']
    return jpg

def get_bibleVerse():
    contents = requests.get('https://beta.ourmanna.com/api/v1/get/?format=json&order=random').json()
    verse = contents['verse']
    details = verse['details']
    text = details['text']
    reference = details['reference']
    version = details['version']
    rText = str(text+ " - "+reference+" ("+version+")")
    return rText
	
def get_image_url(typ):
    allowed_extension = ['jpg','jpeg','png']
    file_extension = ''
    while file_extension not in allowed_extension:
        if typ == "dog":
            url = get_jpgUrlDog()
        elif typ == "cat":
            url = get_jpgUrlCat()
        file_extension = re.search("([^.]*)$",url).group(1).lower()
    return url

def woof(update, context):
    url = get_image_url("dog")
    chat_id = update.message.chat_id
    context.bot.send_message(chat_id = chat_id, text = ranFindMsg("dog"), disable_notification = True)
    context.bot.send_photo(chat_id = chat_id, photo = url, disable_notification = True)
    context.bot.send_message(chat_id = chat_id, text = menuMsg, parse_mode ="HTML", disable_notification = True)
	
def meow(update, context):
    url = get_image_url("cat")
    chat_id = update.message.chat_id
    context.bot.send_message(chat_id = chat_id, text = ranFindMsg("cat"), disable_notification = True)
    context.bot.send_photo(chat_id = chat_id, photo = url, disable_notification = True)
    context.bot.send_message(chat_id = chat_id, text= menuMsg, parse_mode ="HTML", disable_notification = True)
	
def verse(update, context):
    chat_id = update.message.chat_id
    context.bot.send_message(chat_id = chat_id, text = get_bibleVerse(), disable_notification = True)
    context.bot.send_message(chat_id = chat_id, text = menuMsg, parse_mode ="HTML", disable_notification = True)
	
def hello(update, context):
    chat_id = update.message.chat_id
    context.bot.send_message(chat_id = chat_id, text = 'Hello! I was made by @danielninetyfour!',disable_notification = True)
	
def start(update, context):
	chat_id = update.message.chat_id
	context.bot.send_message(chat_id = chat_id, text = startMsg, disable_notification = True, disable_web_page_preview = True)

def help(update, context):
    chat_id = update.message.chat_id
    context.bot.send_message(chat_id = chat_id, text = helpMsg, parse_mode = "HTML", disable_notification = True)

def unknown(update, context):
    chat_id = update.message.chat_id
    context.bot.send_message(chat_id = chat_id, text = errorMsg, disable_notification = True)
	
def main():
    updater = Updater(botToken,use_context=True)
    dispatch = updater.dispatcher
    dispatch.add_handler(CommandHandler('start', start))
    dispatch.add_handler(CommandHandler('help', help))
    dispatch.add_handler(CommandHandler('woof',woof))
    dispatch.add_handler(CommandHandler('meow',meow))
    dispatch.add_handler(CommandHandler('verse',verse))
    dispatch.add_handler(CommandHandler('hello',hello))
    dispatch.add_handler(MessageHandler(Filters.command, unknown))
    updater.start_polling()
    updater.idle()
	
	
if __name__ == "__main__":
	#Global Variables
    botToken = "<token>" #Insert your Telegram Bot Token here
    errorMsg = "Sorry, I cannot identify this command :("
    startMsg = "Hello! Welcome to Puppy Bot! Here are some basic commands you can use to get me to fetch you stuffs :)\n/start - this command! Alternatively you can use /help :)\n/hello - say hello!\n/woof - fetch a random puppy\n/meow - fetch a random cat\n/verse - get a random Bible verse!\n\nLike my bot? Support my work/buy me a coffee @ https://www.patreon.com/Pupper_Bot ! Thank you!"
    helpMsg = "Hello! Welcome to Puppy Bot! Here are some basic commands you can use to get me to fetch you stuffs :)\n/help - this command!\n/hello - say hello!\n/woof - fetch a random puppy\n/meow - fetch a random cat\n/verse - get a random Bible verse!\n"
    menuMsg = "What can I fetch you next? :)\n/woof - fetch me a random puppy!\n/meow - fetch me a random cat!(But whyyy)\n/verse - fetch me a random Bible verse!!"
    main()