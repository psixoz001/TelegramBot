import sqlite3
import telebot
from config import *
from telebot import types
from create_db import *
from markups import *
from functions_db import *
import requests

bot = telebot.TeleBot(bot_token)

@bot.message_handler(commands=['start'])
def start(message):
        user = findUser(message.from_user.id)
        if user is None:
                registration(message.from_user.id)
                connect.commit()
        bot.send_message(message.chat.id, f'Здравствуйте, {message.from_user.username}', reply_markup=anyButtons(["Мои подписки","Подписаться","Отписаться","Новости"]))        

@bot.message_handler(content_types=['text'])
def func(message):
        if(message.text == "Мои подписки"):
                mySubs = findSubs(message.from_user.id)
                if(len(mySubs)>0):
                        mySubsText=' '.join(''.join(tup) for tup in mySubs)
                        bot.send_message(message.chat.id,' '.join(''.join(tup) for tup in mySubs))

                else:
                        bot.send_message(message.chat.id, 'У вас нет подписок')

        elif(message.text == "Подписаться"):
                btns=[]
                for key in category:
                        btns.append(f'sub_{key}')
                bot.send_message(message.chat.id,'Выберите категорию, на которую хотите подписаться: ', reply_markup=anyButtons(btns))       
                
        elif(message.text == "Отписаться"):

                mySubs = findSubs(message.from_user.id)

                if(len(mySubs)>0):
                        btns=[]
                        for item in mySubs:
                                btns.append(f'unsub_{item[0]}')
                        bot.send_message(message.chat.id,'Выберите категорию, от которой хотите отписаться: ', reply_markup=anyButtons(btns))
                
                else:
                        bot.send_message(message.chat.id, 'У вас нет подписок')
        elif(message.text in ['sub_business', 'sub_entertainment','sub_general','sub_health','sub_science','sub_sport','sub_technology']):
                category_name = message.text.split('_')[1]
                category_id=gimmeIdCategory(str(category_name))[0]
                if(findSubsAll(message.from_user.id,category_id)) is None:
                        subscribe(message.from_user.id, category_id)
                        bot.send_message(message.chat.id,f'Вы подписались на категорию {category_name}',reply_markup=anyButtons(["Мои подписки","Подписаться","Отписаться","Новости"]))
                else:
                        bot.send_message(message.chat.id,'Вы уже подпипсаны на эту категорию',reply_markup=anyButtons(["Мои подписки","Подписаться","Отписаться","Новости"]))
        elif(message.text in ['unsub_business', 'unsub_entertainment','unsub_general','unsub_health','unsub_science','unsub_sport','unsub_technology']):
                category_name = message.text.split('_')[1]
                category_id=gimmeIdCategory(str(category_name))[0]
                unsubscribe(message.from_user.id, category_id)
                bot.send_message(message.chat.id,f'Вы отписались от категории {category_name}',reply_markup=anyButtons(["Мои подписки","Подписаться","Отписаться","Новости"]))
        elif(message.text == "Новости"):
                mySubs = findSubs(message.from_user.id)

                if(len(mySubs)>0):
                        btns=[]
                        for item in mySubs:
                                btns.append(f'{item[0]}')
                        bot.send_message(message.chat.id,'Выберите категорию, по которой хотите увидеть новости: ', reply_markup=anyButtons(btns))
        elif(message.text in ['business', 'entertainment','general','health','science','sport','technology']):
                response=requests.get(f'https://newsapi.org/v2/top-headlines?apiKey={news_token}&category={message.text}&pageSize=10&country=ru')
                for i in response.json()['articles']:
                        bot.send_message(message.chat.id,f"{i['title']},\n{i['publishedAt']},\n{i['url']}")
                bot.send_message(message.chat.id,'Выберите следующее действие',reply_markup=anyButtons(["Мои подписки","Подписаться","Отписаться","Новости"]))
createDB()
bot.polling()