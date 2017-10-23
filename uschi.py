#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import telepot
import time
import os
import pyinotify as pyno
from pprint import pprint
from subprocess import call
from telepot.namedtuple import InlineKeyboardMarkup, InlineKeyboardButton

telegram_token = os.environ['USCHI_TELEGRAM_TOKEN']
authorized_ids = os.environ['USCHI_TELEGRAM_AUTHORIZED_IDS']

bot = telepot.Bot(telegram_token)
bot.setWebhook() # unset webhook with out parameters

wm = pyno.WatchManager()
watching = 0

class EventHandler(pyno.ProcessEvent):
    def process_IN_CREATE(self, event):
        if watching:
            print("new Picture detected")
            time.sleep(2)
            for id in authorized_ids:
                bot.sendPhoto(id, photo=open(event.pathname, 'rb'))
        else:
            notifier.stop()

handler = EventHandler()
notifier = pyno.Notifier(wm, handler)
wdd = wm.add_watch('/root/BigUschi/pics', pyno.IN_CREATE)



def takePicture(query_id, from_id):
    bot.answerCallbackQuery(query_id, text='Uschi hält die Augen offen.')
    picName = "/root/BigUschi/pics/test.jpg"
    #call(["fswebcam", "--no-banner", "-q", "-S", "20", picName])
    bot.sendPhoto(from_id, photo=open(picName, 'rb'))


def on_chat_message(msg):
    content_type, chat_type, chat_id = telepot.glance(msg)
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
                   [InlineKeyboardButton(text='Mach ein Foto!', callback_data='takePicture')],
                   [InlineKeyboardButton(text='Stopp!', callback_data='stopWatching')],
                   [InlineKeyboardButton(text='Wache!', callback_data='watchdog')]
               ])

    bot.sendMessage(chat_id, 'Was soll Uschi für dich tun?', reply_markup=keyboard)

def on_callback_query(msg):
    query_id, from_id, query_data = telepot.glance(msg, flavor='callback_query')
    print('Anfrage an Uschi: ', from_id, query_data, time.asctime(time.localtime(time.time())))
    if from_id not in authorized_ids:
        bot.answerCallbackQuery(query_id, text='Du hast leider keine Berechtigung dafür.')
        return
    if query_data == 'takePicture':
        takePicture(query_id, from_id)
    elif query_data == 'watchdog':
        print("start watching")
        watching = 1 
        notifier.loop()
    elif query_data == 'stopWatching':
        watching = 0
        print("stop watching")

bot.message_loop({'chat': on_chat_message,
                  'callback_query': on_callback_query})
print("Listening...")
while 1:
    time.sleep(10)
