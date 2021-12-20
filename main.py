import os
import telebot
import requests as req

APP_KEY = os.getenv('APP_KEY')
bot     = telebot.TeleBot(APP_KEY)
btw     = ' '*2
def namaKota(message):
    try:
        return req.get('https://api.pray.zone/v2/times/today.json?city={}'.format(message))
    except req.exceptions.RequestException as e:
        return e    

@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message,"Masukan Nama Kota yang ingin ditampilkan")

def city_request(message):
    txt = message.text
    if namaKota(txt).status_code != 200:
        bot.send_message(message.chat.id,"Kota tidak ditemukan")
        return False
    else:
        return True 
        
@bot.message_handler(func=city_request)
def jam(message):
    text = message.text.split()[0];
    a    = namaKota(text).json()
    kota = a['results']['location']['city']
    zona = a['results']['location']['timezone']
    for x in a['results']['datetime']:
        tgl     = x['date']['gregorian']
        Dhuhr   = x['times']['Dhuhr']
        Asr     = x['times']['Asr']
        Imsak   = x['times']['Imsak']
        Isha    = x['times']['Isha']
        Maghrib = x['times']['Maghrib']
    bot.send_message(message.chat.id,
    "Jam Sholat Kota {} \ntanggal{}: {}\nZona Waktu  : {}\n\nImsak{}: {} local time\nDhuhr{}: {} local time\nAsr{}: {} local time\nMaghrib{}: {} local time\nIsha{}: {} local time"
    .format(kota,btw*5,tgl,zona,btw*6,Imsak,btw*5,Dhuhr,btw*8,Asr,btw*3,Maghrib,btw*7,Isha))

bot.polling()
