#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import telepot
import time
import tokenconfig as tk
import pyinotify as pyno
from pprint import pprint
from subprocess import call
from telepot.namedtuple import InlineKeyboardMarkup, InlineKeyboardButton

bot = telepot.Bot(tk.token)
bot.setWebhook() # unset webhook with out parameters

wm = pyno.WatchManager()

mask = pyno.IN_CREATE

class EventHandler(pyno.ProcessEvent):
    def process_IN_CREATE(self, event):
        print("new Picture detected")
        time.sleep(2)
        for id in tk.authorized_ids:
            bot.sendPhoto(id, photo=open(event.pathname, 'rb'))
            

handler = EventHandler()
notifier = pyno.Notifier(wm, handler)
wdd = wm.add_watch('/root/BigUschi/pics', mask)
notifier.loop()

def takePicture():
    picName = "/root/BigUschi/pics/test.jpg"
    call(["fswebcam", "--no-banner", "-q", "-S", "20", picName])
    return picName

def on_chat_message(msg):
    content_type, chat_type, chat_id = telepot.glance(msg)
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
                   [InlineKeyboardButton(text='Mach ein Foto!', callback_data='takePicture')],
               ])

    bot.sendMessage(chat_id, 'Was soll Uschi für dich tun?', reply_markup=keyboard)

def on_callback_query(msg):
    query_id, from_id, query_data = telepot.glance(msg, flavor='callback_query')
    print('Anfrage an Uschi: ', from_id, query_data, time.asctime(time.localtime(time.time())))
    if from_id in tk.authorized_ids:
        if query_data == 'takePicture':
            bot.answerCallbackQuery(query_id, text='Uschi hält die Augen offen.')
            pic = takePicture()
            #bot.sendPhoto(from_id, photo=open(pic, 'rb'))
    else:
        bot.answerCallbackQuery(query_id, text='Du hast leider keine Berechtigung dafür.')

bot.message_loop({'chat': on_chat_message,
                  'callback_query': on_callback_query})
print("Listening...")
while 1:
    time.sleep(10)
