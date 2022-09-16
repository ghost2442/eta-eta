
import os

import asyncio



import telegram

from telethon import TelegramClient, events

from datetime import datetime

import time

from telegram.ext import *

from telegram.ext import MessageHandler, filters

from telegram import InlineKeyboardButton, InlineKeyboardMarkup, KeyboardButton, Update

import random

import requests

import json



############################### Bot ############################################

server = 'https://telegram-lottery-default-rtdb.firebaseio.com/'

TOKEN = '5473836960:AAHesr86uOZFGlFgrNd8IIvPO0VjYdDOqA8'



#server = 'https://frantic-architect.firebaseio.com/'

#TOKEN = '5713462327:AAE9k5Lvqil1Y-2g6hajHXQYZH5rz14SMV8'





def start_message(name):

    return 'Hi {}.\nWelcome to Eta Eta! A classic game that offers 50/50 chance of winning.'.format(name)



def start(update, context):

    chk = str(requests.get(server + 'banned_users/'+ str(update.message.chat_id) +'.json').json())

    if (chk != 'None'):

        reason = get_value('reason', chk)

        phone = get_value('phone', chk)

        message = ''

        if (reason == 'multiple_account'):

            count = get_value('count', chk)

            message = 'Your account has been banned.\n\nReason:- System has identified that you have used 1 phone number for multiple accounts.\n\nPhone number: ' + phone + '\n\nAccounts count: ' + count + '\n\nFor more information, contact @headsandtails24'

            update.message.reply_text(message)



        if (reason == 'deactivated'):

            count = get_value('count', chk)

            message = 'Your account has been banned.\n\nReason:- System has identified that your phone number has been associated with a deactivated or deleted account.\n\nPhone number: ' + phone + '\n\nFor more information, contact @headsandtails24'

            update.message.reply_text(message)

    

    else:

        rid = update.message.text.split(' ')

        if (len(rid) == 2):

            rid = rid[1]

        else:

            rid = 'nobody'

        rid = rid.strip(' ')

        if (str(requests.get(server + 'users/' + rid + '.json').json()) == 'None' and rid.isnumeric() == True):

            rid = 'nobody'



        current_balance = 1000

        bet_size = 50

        user_choice = ''

        drawn_choice = ''

        # print(update.message.chat_id)

        r = requests.get(server + 'users/' + str(update.message.chat_id) + '.json')

        r2 = requests.get(server + 'users/' + str(update.message.chat_id) + '/current_balance.json')

        # print(r2.json())

        if (str(requests.get(server + 'users/' + str(update.message.chat_id) + '.json').json()) == 'None'):

            # print('registering')

            na1 = ''

            us = ''

            t = int(time.time())

            if (update.message.chat.first_name != None):

                na1 = na1 + update.message.chat.first_name

            if (update.message.chat.last_name != None):

                na1 = na1 + ' ' + update.message.chat.last_name

            na=''

            

            for n in na1:

              if(n=='\'' or n=='"' or n=='\\'):

                  continue

              na+=n   

            



            if (update.message.chat.username != None):

                us = update.message.chat.username

            requests.put(server + 'users/' + str(update.message.chat_id) + '.json',

                         json={'chat_id': update.message.chat_id, 'current_balance': 1000, 'bet_size': 50, 'name': na,

                               'phone_number': 'x', 'username': us, 'last_time': '0', 'chance': 10, 'time_joined': t,

                               'reffered_by': rid, 'play_count': 0, 'luck': 'random', 'invited_people_count': 0,'banned':'false'})

            update.message.reply_text('You have recieved bonus of 1000 coins (10 Birr) for registering')

            context.bot.send_message(chat_id='5010656317', text=str(update.message.chat_id) + ' has started bot')

            if (rid != 'nobody' and rid.isnumeric() == True):

                context.bot.send_message(rid, na + ' has joined the bot using your refferal link.')

                requests.patch(server + 'users/' + rid + '/invited_people/' + str(update.message.chat_id) + '.json',

                               json={'is_paid': 'false', 'play_count': 0, 'name': na, 'time_joined': int(time.time())})

                #a = str(requests.get(server + 'users/' + rid + '/invited_people_count.json').json())

                #if (a == 'None'):

                #    requests.patch(server + 'users/' + rid + '.json', json={'invited_people_count': 1})

                #else:

                #    a = int(a) + 1

                #    requests.patch(server + 'users/' + rid + '.json', json={'invited_people_count': a})





        else:

            # print('recovering')

            current_balance = int(

                requests.get(server + 'users/' + str(update.message.chat_id) + '/current_balance.json').json())

            bet_size = int(requests.get(server + 'users/' + str(update.message.chat_id) + '/bet_size.json').json())



        # print(r.json())

        

        message = rid

        if (message[0:2] == 'cd'):

            r = message

            if (str(requests.get(server + 'multi_player/' + r + '.json').json()) != 'None'):

                chat_id_h = str(requests.get(server + 'multi_player/' + r + '/chat_id_h.json').json())

                print(chat_id_h + ' ' + str(update.message.chat_id))

                if (chat_id_h != str(update.message.chat_id)):

                    # print('not equal')

                    if (int(str(requests.get(server + 'multi_player/' + r + '/size.json').json())) != 2):

                        na = ''

                        if (update.message.chat.first_name != None):

                            na = na + update.message.chat.first_name

                        if (update.message.chat.last_name != None):

                            na = na + ' ' + update.message.chat.last_name

                        # print(na)



                        name_h = str(requests.get(server + 'multi_player/' + r + '/name_h.json').json())

                        t = time.time()

                        bet_size_default = 50

                        requests.patch(server + 'multi_player/' + r + '.json', json={'name_j': str(na)})

                        requests.patch(server + 'multi_player/' + r + '.json',

                                       json={'chat_id_j': str(update.message.chat_id)})

                        requests.patch(server + 'multi_player/' + r + '.json', json={'size': 2})



                        requests.patch(server + 'users/' + str(update.message.chat_id) + '.json',

                                       json={'multi_code': r})

                        current_balance_j = int(

                            str(requests.get(

                                server + 'users/' + str(update.message.chat_id) + '/current_balance.json').json()))

                        current_balance_h = int(

                            str(requests.get(server + 'users/' + str(chat_id_h) + '/current_balance.json').json()))

                        bet_size = int(str(requests.get(server + 'multi_player/' + r + '/bet_size.json').json()))



                        updater = Updater(TOKEN, use_context=True)

                        # print(chat_id_h)

                        # updater.bot.send_message(chat_id=str(chat_id_h),text='You are now playing with '+na)

                        updater.bot.send_message(chat_id=str(chat_id_h), text='You are now playing with ' + na)



                        updater.bot.send_message(chat_id=str(update.message.chat_id),

                                                 text='You are now playing with ' + name_h)

                        updater.bot.send_message(chat_id=str(update.message.chat_id),

                                                 text=multiplayer_status_text(name_h, bet_size, current_balance_j),

                                                 reply_markup=heads_or_tails_multi_keyboard())

                        updater.bot.send_message(chat_id=str(chat_id_h),

                                                 text=multiplayer_status_text(na, bet_size, current_balance_h))

                        updater.bot.send_message(chat_id=str(chat_id_h),

                                                 text='Waiting for ' + na + ' to choose head or tail...')



                        updater.stop()



                    else:

                        update.message.reply_text('Players full. Two players are already playing. Press /start to go to main menu.')



                else:

                    update.message.reply_text('You can not join your own invitation.')

            else:

                update.message.reply_text('wrong code')

                

        

        else:

        

          update.message.reply_text(start_message(update.message.chat.first_name))



          update.message.reply_text(main_menu_message(drawn_choice, bet_size, current_balance),

                                  reply_markup=main_menu_keyboard())

    







def help(update,context):

    update.message.reply_text(help_message(),reply_markup=backtomain_keyboard())   



def get_value(key_location,js2):

  gotten_value = 'None'

  s=key_location.split(',')

  if(js2!='None'):

    js = js2.replace('\'', '"')

    us = json.loads(repr(js)[1:-1])



    i=0

    j=0

    gotten_value='None'

    success=0



    new_js=''

    while(i<len(s)):

     success=0

     #print(i)

     #print(str(i)+' '+str(us))

     j=0

     for v in us:

        #print(us[str(v)])







        #print(str(v)+' '+s[i])

        if(not(s[i].isnumeric()==True and int(s[i])<10000)): #key

         if(str(v)==s[i]):



            gotten_value=str(us[v])

            success=1

            #print(s[i]+' '+str(us[v]))

            i+=1

            #print(str(us[v]))

            new_js=str(us[v]).replace('\'','"')

            #print('hey'+new_js)

            if(i<len(s)):

             us = json.loads(repr(new_js)[1:-1])

            break

        else:  #index

            if (j==int(s[i])):

                gotten_value = str(us[v])

                success = 1

                # print(s[i]+' '+str(us[v]))

                i += 1

                new_js = str(us[v]).replace('\'', '"')

                if (i < len(s)):

                 us = json.loads(repr(new_js)[1:-1])

                break

        j += 1













     if(success==0):

         gotten_value = 'None'

         break



     #if (j>=int(len(us)) or i>=int(len(s))):

     #    print('limit')

     #    break

  return gotten_value

  

def referral_money_count(js):

    js=js.replace('\'','"')

    #print(js)

    be=get_entities(str(requests.get(server+'banned_users.json').json()))

    i = 0

    if(js!='None'):

     u = json.loads(repr(js)[1:-1])



     for v in u:

        s=str(v)+',play_count'

        #print(get_value(s,js))

        if(int(get_value(s,js))>=100 and not(v in be)):

         i+=1

    return i



def conv(inp):

    if (inp == 'heads'):

        return 1

    if (inp == 'tails'):

        return 0

    if (inp == 'cbs'):

        return 2

    if (inp == 'back'):

        return 4

    if (inp == 'deposit'):

        return 5

    if (inp == 'withdraw'):

        return 6





def setwinprob(prob):

    ch = random.randint(1, 100)

    if (ch <= prob):

        return 1

    else:

        return 0



def get_entities(js):

    sl=[]

    js = js.replace('\'','"')

    #print(js)

    if(js!='None'):

      us = json.loads(repr(js)[1:-1])

      for i in us:

        #print(i)

        sl.append(i)

    return   sl

    

def altch(drawn_choice):

    if (drawn_choice == 'heads'):

        return 'tails'

    else:

        return 'heads'



async def broadcast(updater,tex):
            u = str(requests.get(server+'users.json').json())

            ue = get_entities(u)

            i=0

            sl = []

            while(i<220):

              sl.append(random.randint(1,len(ue)-1))

              i+=1

            i=0 

            w=0            

            st = time.time()

            for v in ue:

               i+=1

               if(w>210 or time.time()-st>25):

                  break

               if(i in sl):

                    w+=1

                    try:

                     updater.bot.send_message(chat_id=v, text= tex)

                     #print('sent')

                    except Exception as e:

                        #print(e)

                        continue

def All_queries_handler(update, context):

    query = update.callback_query

    # print('chatid: '+str(query.message.chat_id))

    query.answer()

    chk = str(requests.get(server + 'banned_users/'+ str(query.message.chat_id)+'.json').json())

    #print(server + 'banned_users/'+ str(query.message.chat_id)+'.json')

    if (chk != 'None'):

        reason = get_value('reason', chk)

        phone = get_value('phone', chk)

        message = ''

        if (reason == 'multiple_account'):

            count = get_value('count', chk)

            message = 'Your account has been banned.\n\nReason:- System has identified that you have used 1 phone number for multiple accounts.\n\nPhone number: ' + phone + '\n\nAccounts count: ' + count + '\n\nFor more information, contact @headsandtails24'

            query.message.reply_text(message)



        if (reason == 'deactivated'):

            count = get_value('count', chk)

            message = 'Your account has been banned.\n\nReason:- System has identified that your phone number has been associated with a deactivated or deleted account.\n\nPhone number: ' + phone + '\n\nFor more information, contact @headsandtails24'

            query.message.reply_text(message)



    else:

        jus = str(requests.get(server + 'users/' + str(query.message.chat_id) + '.json').json())

        jus = jus.replace('\'', '"')

        us = json.loads(repr(jus)[1:-1])

        current_balance = int(us['current_balance'])

        bet_size = int(us['bet_size'])

        chance = int(us['chance'])

        play_count = int(us['play_count'])

        reffered_by = str(us['reffered_by'])

        #invc = int(us['invited_people_count'])

        last_t = int(us['last_time'])

        t = 0

        phone = str(us['phone_number'])

        luck = str(us['luck'])



        na = ''

        us = ''

        if (query.message.chat.first_name != None):

            na = na + query.message.chat.first_name

        if (query.message.chat.last_name != None):

            na = na + ' ' + query.message.chat.last_name



        if (query.message.chat.username != None):

            us = query.message.chat.username



        # print("chance b " + str(chance))

        # withamt=int(str(requests.get(server + 'users/' + str(update.message.chat_id) + '/active_withdraw.json').json()))

        # phone_number=str(requests.get(server + 'users/' + str(update.message.chat_id) + '/phone_number.json').json())

        # print(int(str(requests.get(server + 'users/' + str(query.message.chat_id) + '/current_balance.json').json())))

        user_choice = ''

        drawn_choice = ''

        cn = random.randint(0, 1)

        # if(bet_size<100): cn = setwinprob(52)

        # else: cn = setwinprob(50)

        

        if(bet_size<=100): cn = setwinprob(random.randint(40,70))

        if(bet_size>=300): cn = setwinprob(random.randint(30,50))

        if(bet_size>=500): cn = setwinprob(random.randint(25,40))

        if(bet_size>=1000): cn = setwinprob(random.randint(25,30))

        if(bet_size>=2000): cn = setwinprob(random.randint(15,25))

        if(bet_size>=3000): cn = setwinprob(random.randint(5,20))

        if (luck != 'None' and luck != 'random'):

            cn = setwinprob(int(luck))



        # print('result: '+str(cn) +query.data+ ' '+altch(query.data))

        # if (query.data != ''):

        # print(query.data)

        if (cn == 0):

            drawn_choice = altch(query.data)

        else:

            drawn_choice = query.data



            #  query.message.reply_text(text=main_menu_message(drawn_choice,bet_size,current_balance),reply_markup=main_menu_keyboard())

            # print(query.data+'\n') gh

        if (query.data == 'help'):

            query.edit_message_text(help_message(), reply_markup=backtomain_keyboard())

        if (query.data == 'pwf'):

            query.edit_message_text('Host a game or join using code: ', reply_markup=host_or_join_keyboard())



        if (query.data == 'ref'):

            



            invp = get_value('invited_people', jus)

            invpj = str(requests.get(server + 'users/' + str(query.message.chat_id) + '/invited_people.json').json())

            en = get_entities(invpj)

            ic = len(en)

            query.edit_message_text(

                'Invited people count: ' + str(len(en)) + '\nMoney earned through refferal program: ' + str(

                    referral_money_count(invp) * 10) + ' birr')

            i = 0

            s = ''

            while (i < len(en)):

                s += 'Referrals List\n\n ' + str(i + 1) + '. ' + str(

                    get_value(en[i] + ',name', invpj)) + ' played ' + str(

                    get_value(str(i) + ',play_count', invp)) + ' time(s).\n'

                i += 1

            if (s != ''):

                query.message.reply_text(s)



            query.message.reply_text('Your refferal link is \nhttps://telegram.me/etaeta24bot?start=' + str(

                query.message.chat_id) + '\n\nYou will be paid 10 birr every time a new person joins the bot with your link. (They have to play at least 35 times)',

                                     reply_markup=backtomain_keyboard())

        if (query.data == 'deposit'):  # deposit

            uid = random.randint(136374, 9585634)

            requests.put(server + 'deposits/' + str(uid) + '.json',

                         json={'chat_id': query.message.chat_id, 'current_balance': current_balance

                               })



            query.edit_message_text('Your transfer id is : ' + str(

                uid) + '\n\nSend message to @headsandtails24:\n\nAmount:__\nTransfer id:__\n\nThe person may ask you more information.',

                                    reply_markup=backtomain_keyboard())



        if (query.data == 'withdraw'):  # withdraw

            uid = random.randint(136374, 9585634)

            requests.put(server + 'withdraws/' + str(uid) + '.json',

                         json={'chat_id': query.message.chat_id, 'current_balance': current_balance

                               })



            query.edit_message_text('Your transfer id is : ' + str(

                uid) + '\n\nSend message to @headsandtails24:\n\nAmount:__\nTransfer id:__\nPhone number or Account number:__\n\nThe person may ask you more information.',

                                    reply_markup=backtomain_keyboard())



        if (query.data == 'backto_main'):  # back button to main

            query.edit_message_text(text=main_menu_message(drawn_choice, bet_size, current_balance),

                                    reply_markup=main_menu_keyboard())



        if (query.data == 'cbs'):  # change bet size

            query.edit_message_text('Choose bet size in coins', reply_markup=bet_choice_keyboard())

            # print('change-bet_size')



        if (conv(query.data) == 1 or conv(query.data) == 0):  # head or tail

        #if (1==0):  # head or tail        



            # print('heads or tails')

           

            if (current_balance < bet_size):  # low balance

                query.edit_message_text('You don\'t have enough balance.', reply_markup=balance_low_keyboard())

            #if (chance == 0):  # no more chance

            #    query.edit_message_text('You have used all your chances today. Try again tommorrow.',

            #                            reply_markup=backtomain_keyboard())

                                        

            if (current_balance > bet_size  and current_balance<=1000):  # enough balance

                # if (conv(query.data) == cn):  # won

                chance = chance - 1

                play_count += 1

                last_t = int(time.time())

                requests.patch(server + 'users/' + str(query.message.chat_id) + '.json', json={'last_time': last_t})

                requests.patch(server + 'users/' + str(query.message.chat_id) + '.json', json={'chance': chance})

                reffered_by = reffered_by.strip(' ')

                if (reffered_by != 'nobody' and reffered_by != ''):

                    requests.patch(

                        server + 'users/' + reffered_by + '/invited_people/' + str(query.message.chat_id) + '.json',

                        json={'play_count': play_count})



                # print("chance a " + str(chance))

                if (cn == 1):

                    #       print('won')

                    current_balance += bet_size



                    requests.patch(server + 'users/' + str(query.message.chat_id) + '.json',

                                   json={'current_balance': current_balance})

                    requests.patch(server + 'users/' + str(query.message.chat_id) + '.json',

                                   json={'play_count': play_count})

                                   

                    requests.patch(server + 'logs/' + str(query.message.chat_id) + '/'+str(int(time.time()))+'.json',

                                   json={'choice': drawn_choice,'won':1,'bet_size':bet_size,'current_balance':current_balance})               



                    query.edit_message_text(won_message(drawn_choice, bet_size, current_balance))

                    query.message.reply_text(text=main_menu_message(drawn_choice, bet_size, current_balance),

                                             reply_markup=main_menu_keyboard())



                else:  # lost

                    #      print('lost')

                    current_balance -= bet_size



                    requests.patch(server + 'users/' + str(query.message.chat_id) + '.json',

                                   json={'current_balance': current_balance})

                    requests.patch(server + 'users/' + str(query.message.chat_id) + '.json',

                                   json={'play_count': play_count})

                    requests.patch(server + 'logs/' + str(query.message.chat_id) + '/'+str(int(time.time()))+'.json',

                                   json={'choice': drawn_choice,'won':0,'bet_size':bet_size,'current_balance':current_balance})                



                    query.edit_message_text(lost_message(drawn_choice, bet_size, current_balance))

                    query.message.reply_text(text=main_menu_message(drawn_choice, bet_size, current_balance),

                                             reply_markup=main_menu_keyboard())

            if(current_balance>1000):

                query.edit_message_text('You can\'t play against computer if you have more than 1000 coins in your current balance. You have to play multiplayer with friends. Press /start to go to main menu.')

        if (query.data[0:7] == 'c9000c_'):  # change bet size



            bet_size = int(query.data[7:len(query.data)])

            requests.patch(server + 'users/' + str(query.message.chat_id) + '.json',

                           json={'bet_size': bet_size})

            query.edit_message_text('Bet size is changed to ' + query.data[7:len(query.data)] + ' coins.')

            query.message.reply_text(text=main_menu_message(drawn_choice, bet_size, current_balance),

                                     reply_markup=main_menu_keyboard())



            # multi player query handler



        if (query.data == 'backto_main_multi'):

           r = str(requests.get(server + 'users/' + str(query.message.chat_id) + '/multi_code.json').json())

            

           md = str(requests.get(server + 'multi_player/' + r + '.json').json())

           if(md!='None'):

            oci = 'None'

            if(get_value('chat_id_h',md)==str(query.message.chat_id)): # is host

               oci = get_value('chat_id_j',md)

               

            if(get_value('chat_id_j',md)==str(query.message.chat_id)): # is joined

               oci = get_value('chat_id_h',md)   

            if(oci!='None'):   

             updater = Updater(TOKEN, use_context=True)

             updater.bot.send_message(chat_id=int(oci), text = 'Your opponent ended the session. Press /start to go to main menu.')            

            

            requests.delete(server + 'multi_player/' + r + '.json')

           requests.patch(server + 'users/' + str(query.message.chat_id) + '/.json', json={'multi_code': 'None'})

           query.edit_message_text(main_menu_message(drawn_choice, bet_size, current_balance),

                                    reply_markup=main_menu_keyboard())



        if (query.data == 'cbs_m'):

            query.edit_message_text('Choose bet size: ', reply_markup=bet_choice_multi_keyboard())

        if (query.data[0:7] == 'c9001c_'):  # change multi bet size



            bet_size = int(query.data[7:len(query.data)])



            r = 'cd' + str(random.randint(1123253, 9999999))

            t = time.time()

            requests.put(server + 'multi_player/' + r + '.json',

                         json={'chat_id_h': query.message.chat_id,

                               'bet_size': bet_size, 'name_h': na, 'code': r, 'time_created': t, 'host_turn': 0,

                               'size': 1, 'chosen': 'none'

                               })



            requests.patch(server + 'users/' + str(query.message.chat_id) + '.json', json={'multi_code': r})

            #query.edit_message_text(str(r))

            #query.message.reply_text('?????\nYour invitation code is: ' + str(

            #   r) + '\nTell your friend to enter this code in his device and send it to the bot.\n\nWaiting for player to join...')

            bet_info =''

            if(bet_size>0):

              bet_info='Bet size: '+str(bet_size)+'\nMinimum balance required to play: '+str(bet_size+1000)

            if(bet_size==0):

                bet_info = 'Bet size: Free\nMinimum balance required to play: Free to play'

            query.edit_message_text('Your friend '+na +' invites you to play with them.\n'+bet_info+'\n\nhttps://t.me/etaeta24bot?start='+str(r))

            query.message.reply_text('?????\nSend the above link to your friend and tell him to click start. The bot will automatically send this link to many hundreds of Eta Eta players to make sure you find a player.\n\nWaiting for player to join...')

            

            updater = Updater(TOKEN, use_context=True)

            #updater.bot.send_message(chat_id=-1001286169515, text= na +' invites you to play with them.\n'+bet_info+'\n\nhttps://t.me/etaeta24bot?start='+str(r))
            text=na +' invites you to play with them.\n'+bet_info+'\n\nhttps://t.me/etaeta24bot?start='+str(r)
            asyncio.run(broadcast(updater,text))                     

               

        

        if (query.data == 'host'):  # create game

            query.edit_message_text('Choose bet size: ', reply_markup=bet_choice_multi_keyboard())



        if (query.data == 'join'):

            query.edit_message_text('Enter invitation code: ', reply_markup=backtomain_keyboard())



        if (query.data == 'head_m' or query.data == 'tail_m'):

            r = str(requests.get(server + 'users/' + str(query.message.chat_id) + '/multi_code.json').json())

            requests.patch(server+'users/'+str(query.message.chat_id)+'.json',json={'last_time':str(int(time.time()))})

            if (str(requests.get(server + 'multi_player/' + r + '/.json').json()) != 'None'):



                tc = float(str(requests.get(server + 'multi_player/' + r + '/time_created.json').json()))

                tn = float(time.time())

                if (tn - tc < 6 * 3600):

                    updater = Updater(TOKEN, use_context=True)

                    chat_id_h = str(requests.get(server + 'multi_player/' + r + '/chat_id_h.json').json())

                    chat_id_j = str(requests.get(server + 'multi_player/' + r + '/chat_id_j.json').json())

                    name_j = str(requests.get(server + 'multi_player/' + r + '/name_j.json').json())

                    name_h = str(requests.get(server + 'multi_player/' + r + '/name_h.json').json())

                    bet_size = int(str(requests.get(server + 'multi_player/' + r + '/bet_size.json').json()))

                    current_balance_h = int(

                        str(requests.get(server + 'users/' + chat_id_h + '/current_balance.json').json()))

                    current_balance_j = int(

                        str(requests.get(server + 'users/' + chat_id_j + '/current_balance.json').json()))

                    if (chat_id_h == str(query.message.chat_id)):  # is host

                        host_turn = int(str(requests.get(server + 'multi_player/' + r + '/host_turn.json').json()))



                        if (current_balance_h >= bet_size + 1000 or bet_size==0):

                            if (host_turn == 0):  # prediction

                                chosen = str(requests.get(server + 'multi_player/' + r + '/chosen.json').json())

                                if (chosen != 'None' and query.data == chosen):

                                    query.edit_message_text(won_message_multi(bet_size))

                                    current_balance_h = current_balance_h + bet_size

                                    requests.patch(server + 'users/' + str(query.message.chat_id) + '.json',

                                                   json={'current_balance': current_balance_h})



                                    current_balance_j = current_balance_j - bet_size

                                    requests.patch(server + 'users/' + chat_id_j + '.json',

                                                   json={'current_balance': current_balance_j})



                                    updater.bot.send_message(chat_id=chat_id_j, text=lost_message_multi(bet_size))

                                if (chosen != 'None' and query.data != chosen):

                                    query.edit_message_text(lost_message_multi(bet_size))

                                    current_balance_h = current_balance_h - bet_size

                                    requests.patch(server + 'users/' + str(query.message.chat_id) + '.json',

                                                   json={'current_balance': current_balance_h})



                                    current_balance_j = current_balance_j + bet_size

                                    requests.patch(server + 'users/' + chat_id_j + '.json',

                                                   json={'current_balance': current_balance_j})



                                    updater.bot.send_message(chat_id=chat_id_j, text=won_message_multi(bet_size))

                                requests.patch(server + 'multi_player/' + r + '.json', json={'host_turn': 1})

                                updater.bot.send_message(chat_id=str(query.message.chat_id),

                                                         text=multiplayer_status_text(name_j, bet_size,

                                                                                      current_balance_h))

                                updater.bot.send_message(chat_id=chat_id_j,

                                                         text=multiplayer_status_text(name_h, bet_size,

                                                                                      current_balance_j))



                                query.message.reply_text('Make your choice and your opponent will try to guess it.',

                                                         reply_markup=heads_or_tails_multi_keyboard())

                                updater.bot.send_message(chat_id=chat_id_j,

                                                         text='Waiting for opponent to make a choice...\nThen you will guess it.')

                            else:



                                query.edit_message_text('Waiting for opponent to guess your choice...')

                                requests.patch(server + 'multi_player/' + r + '.json', json={'chosen': query.data})

                                updater.bot.send_message(chat_id=chat_id_j,

                                                         text='Your opponent has made a choice. Can you guess what it is?',

                                                         reply_markup=heads_or_tails_multi_keyboard())

                        else:

                            query.edit_message_text(

                                'Not enough balance. Your balance should be above 1000 coins plus bet size. Click /start to go to main menu.')

                            updater.bot.send_message(chat_id=chat_id_j,

                                                     text='Your opponent does not have enough balance. Session ended. Click /start to go to main menu.',

                                                     )



                    if (chat_id_j == str(query.message.chat_id)):  # is joined

                        host_turn = int(str(requests.get(server + 'multi_player/' + r + '/host_turn.json').json()))



                        if (current_balance_j >= bet_size + 1000 or bet_size==0):

                            if (host_turn == 1):  # prediction

                                chosen = str(requests.get(server + 'multi_player/' + r + '/chosen.json').json())

                                if (chosen != 'None' and query.data == chosen):

                                    query.edit_message_text(won_message_multi(bet_size))

                                    current_balance_j = current_balance_j + bet_size

                                    requests.patch(server + 'users/' + str(query.message.chat_id) + '.json',

                                                   json={'current_balance': current_balance_j})



                                    current_balance_h = current_balance_h - bet_size

                                    requests.patch(server + 'users/' + chat_id_h + '.json',

                                                   json={'current_balance': current_balance_h})

                                    updater.bot.send_message(chat_id=chat_id_h, text=lost_message_multi(bet_size))

                                if (chosen != 'None' and query.data != chosen):

                                    query.edit_message_text(lost_message_multi(bet_size))

                                    current_balance_j = current_balance_j - bet_size

                                    requests.patch(server + 'users/' + str(query.message.chat_id) + '.json',

                                                   json={'current_balance': current_balance_j})

                                    current_balance_h = current_balance_h + bet_size

                                    requests.patch(server + 'users/' + chat_id_h + '.json',

                                                   json={'current_balance': current_balance_h})

                                    updater.bot.send_message(chat_id=chat_id_h, text=won_message_multi(bet_size))

                                requests.patch(server + 'multi_player/' + r + '.json', json={'host_turn': 0})

                                updater.bot.send_message(chat_id=str(query.message.chat_id),

                                                         text=multiplayer_status_text(name_h, bet_size,

                                                                                      current_balance_j))



                                updater.bot.send_message(chat_id=chat_id_h,

                                                         text=multiplayer_status_text(name_j, bet_size,

                                                                                      current_balance_h))



                                query.message.reply_text('Make your choice and your opponent will try to guess it.',

                                                         reply_markup=heads_or_tails_multi_keyboard())

                                updater.bot.send_message(chat_id=chat_id_h,

                                                         text='Waiting for opponent to make a choice...\nThen you will guess it.')

                            else:



                                query.edit_message_text('Waiting for opponent to guess your choice...')

                                requests.patch(server + 'multi_player/' + r + '.json', json={'chosen': query.data})

                                updater.bot.send_message(chat_id=chat_id_h,

                                                         text='Your opponent has made a choice. Can you guess what it is?',

                                                         reply_markup=heads_or_tails_multi_keyboard())



                        else:

                            query.edit_message_text(

                                'Not enough balance. Your balance should be above 1000 coins plus bet size. Click /start to go to main menu.')

                            updater.bot.send_message(chat_id=chat_id_h,

                                                     text='Your opponent does not have enough balance. Session ended. Click /start to go to main menu.'

                                                     )

                else:

                    query.edit_message_text('Session has expired.')

            else:

                query.edit_message_text('Session has expired.')





def multiplayer_status_text(other_player_name, bet_size, current_balance):

    text = 'Playing with: ' + other_player_name + '\n' + 'Bet size: '

    if (bet_size == 0):

        text = text + 'free'

    else:

        text = text + str(bet_size)



    text = text + '\nYour balance: ' + str(current_balance)

    return text





def won_message_multi(bet_size):

    text = '?\n?\nCongratulations!! You have won'

    if (bet_size == 0):

        text = text + '.'

    else:

        text = text + ' ' + str(bet_size) + ' coins.'

    text=text+'\n?\n?'

    # text=text+ 'You have correctly guessed the opponent\'s choice.'

    return text





def lost_message_multi(bet_size):

    text = '??\n??\nOops!! You have lost'

    if (bet_size == 0):

        text = text + '.'

    else:

        text = text + ' ' + str(bet_size) +' coins.'



    text=text+'\n??\n??'

    # text=text+ 'You have incorrectly guessed the opponent\'s choice.'

    return text



def All_messages_handler(update, context):

    message = update.message.text

    chk = str(requests.get(server + 'banned_users/'+str(update.message.chat_id) +'.json').json())

    if (chk != 'None'):

        reason = get_value('reason', chk)

        phone = get_value('phone', chk)

        message = ''

        if (reason == 'multiple_account'):

            count = get_value('count', chk)

            message = 'Your account has been banned.\n\nReason:- System has identified that you have used 1 phone number for multiple accounts.\n\nPhone number: ' + phone + '\n\nAccounts count: ' + count + '\n\nFor more information, contact @headsandtails24'

            update.message.reply_text(message)



        if (reason == 'deactivated'):

            count = get_value('count', chk)

            message = 'Your account has been banned.\n\nReason:- System has identified that your phone number has been associated with a deactivated or deleted account.\n\nPhone number: ' + phone + '\n\nFor more information, contact @headsandtails24'

            update.message.reply_text(message)

    

    else:

    

        if (message[0:2] == 'cd'):

            r = message

            if (str(requests.get(server + 'multi_player/' + r + '.json').json()) != 'None'):

                chat_id_h = str(requests.get(server + 'multi_player/' + r + '/chat_id_h.json').json())

                print(chat_id_h + ' ' + str(update.message.chat_id))

                if (chat_id_h != str(update.message.chat_id)):

                    # print('not equal')

                    if (int(str(requests.get(server + 'multi_player/' + r + '/size.json').json())) != 2):

                        na = ''

                        if (update.message.chat.first_name != None):

                            na = na + update.message.chat.first_name

                        if (update.message.chat.last_name != None):

                            na = na + ' ' + update.message.chat.last_name

                        # print(na)



                        name_h = str(requests.get(server + 'multi_player/' + r + '/name_h.json').json())

                        t = time.time()

                        bet_size_default = 50

                        requests.patch(server + 'multi_player/' + r + '.json', json={'name_j': str(na)})

                        requests.patch(server + 'multi_player/' + r + '.json',

                                       json={'chat_id_j': str(update.message.chat_id)})

                        requests.patch(server + 'multi_player/' + r + '.json', json={'size': 2})



                        requests.patch(server + 'users/' + str(update.message.chat_id) + '.json',

                                       json={'multi_code': r})

                        current_balance_j = int(

                            str(requests.get(

                                server + 'users/' + str(update.message.chat_id) + '/current_balance.json').json()))

                        current_balance_h = int(

                            str(requests.get(server + 'users/' + str(chat_id_h) + '/current_balance.json').json()))

                        bet_size = int(str(requests.get(server + 'multi_player/' + r + '/bet_size.json').json()))



                        updater = Updater(TOKEN, use_context=True)

                        # print(chat_id_h)

                        # updater.bot.send_message(chat_id=str(chat_id_h),text='You are now playing with '+na)

                        updater.bot.send_message(chat_id=str(chat_id_h), text='You are now playing with ' + na)



                        updater.bot.send_message(chat_id=str(update.message.chat_id),

                                                 text='You are now playing with ' + name_h)

                        updater.bot.send_message(chat_id=str(update.message.chat_id),

                                                 text=multiplayer_status_text(name_h, bet_size, current_balance_j),

                                                 reply_markup=heads_or_tails_multi_keyboard())

                        updater.bot.send_message(chat_id=str(chat_id_h),

                                                 text=multiplayer_status_text(na, bet_size, current_balance_h))

                        updater.bot.send_message(chat_id=str(chat_id_h),

                                                 text='Waiting for ' + na + ' to choose head or tail...')



                        updater.stop()



                    else:

                        update.message.reply_text('Players full')



                else:

                    update.message.reply_text('You can not join your own invitation.')

            else:

                update.message.reply_text('wrong code')



    

    



def bet_choice_keyboard():

    keyboard = [

        [

            InlineKeyboardButton('50', callback_data='c9000c_50'),

            InlineKeyboardButton('100', callback_data='c9000c_100'),

            InlineKeyboardButton('300', callback_data='c9000c_200'),

            InlineKeyboardButton('500', callback_data='c9000c_500')

        ],



        [

            InlineKeyboardButton('1000', callback_data='c9000c_1000'),

            InlineKeyboardButton('2000', callback_data='c9000c_2000'),

            InlineKeyboardButton('3000', callback_data='c9000c_3000'),

            InlineKeyboardButton('5000', callback_data='c9000c_5000')

        ],

        

        [

            InlineKeyboardButton('10000', callback_data='c9000c_10000'),

            InlineKeyboardButton('20000', callback_data='c9000c_20000'),

            InlineKeyboardButton('30000', callback_data='c9000c_30000'),

            InlineKeyboardButton('50000', callback_data='c9000c_50000')

        ],



        [

            InlineKeyboardButton('Go back', callback_data='backto_main')

        ],



    ]

    return InlineKeyboardMarkup(keyboard)





def keyboards():

    keyboard = [

        [

            KeyboardButton('Play', callback_data='play')

        ],

    ]

    return InlineKeyboardMarkup(keyboard)





def backtomain_keyboard():

    keyboard = [



        [

            InlineKeyboardButton('Go back to main menu', callback_data='backto_main')

        ],

    ]

    return InlineKeyboardMarkup(keyboard)



def help_message():



 return 'Welcome to Eta Eta\n\nHow to play against computer?\n\nEta Eta is a luck game. Choose either "head" or "tail". Then a coin will be tossed with 50/50 chance of landing on either "head" or "tail".\nIf the coin landed on your choice, you will win and the bet size you played with will be added to your account.\nIf the coin did not land on your choice, you will lose and the bet size you played with will be subtracted from your account.\n\nHow to play with friends?\n\nClick play with friends on the main menu.\nThen if you want to invite someone click on "invite a friend".\nIf you want to join an invitation, get the code from your inviter and send it to the bot. Then you will be automatically connected with your friend.\nYou can play for free by choosing bet size as "free" or you can play with real money by increasing bet size.\n\nThe game flow is turn by turn:\nOne person chooses either "head" or "tail", then the other person will try to guess what he chose.\n\n\nHow can I withdraw money from my account?\n\nContact @headsandtails24 \nWithdraw is available via CBE Birr, Tele Birr, CBE mobile banking and as mobile card.\n\nHow can I deposit money to my account?\n\nContact @headsandtails24 \nDeposit is available via CBE Birr, Tele Birr, CBE mobile banking and as mobile card.\n\nHow much can I earn in this game?\n\nUnlimited. As long as you win, you will recieve your money.\n\n\n?? ?? ?? ???? ???? ??\n\n??????? ?? ???? ????????\n\n?? ?? ???? ??? ??? "head" ??? "tail" ????. ???? ??? ???? ? 50/50 ? "head" ??? "tail" ?? ???? ??? ????.\n???? ????? ?? ??? ????? ?? ?????? ????? ??? ?? ???? ??????n\???? ????? ?? ????? ???? ????? ?? ?????? ????? ??? ????? ??????\n????? ?? ???? ???? ?????\n\n???? ??? ??? ????? ?? ????? ?? ?????\n??? ??? ????? ???? "Invite a friend" ? ?? ?????\n???? ????? ???? ??? ????? ??? ?? ?? ?? ???? ??? ???? ????? ?? ?????.\n????? ???? ??? "free" ????? ??? ???? ???? ??? ????? ??? ????? ?????? ???? ???? ?????\n\n????? ??? ???? ???-\n??? ?? "head" ??? "tail" ?????, ???? ???? ?? ?????? ????? ?????.\n\n\n????? ???? ???? ????? ???? ???\n\n????? @headsandtails24\n???? ???? ?????? ??? ??? ??? ?????? ??? ??? ????? ??? ?? ????? ??? ?????\n\n???? ?? ????? ???? ????? ??????\n\n????? @headsandtails24\n???? ???? ??? ??? ??? ??? ?????? ??? ??? ????? ??? ?? ????? ??? ?????\n\n??? ??? ?? ??? ???? ??????\n\n??????. ??????? ??? ?????? ???????'



def main_menu_keyboard():

    keyboard = [

        [

            InlineKeyboardButton('Heads', callback_data='heads'),

            InlineKeyboardButton('Tails', callback_data='tails')

        ],

        [

            InlineKeyboardButton('Play 1 vs 1 with friends', callback_data='pwf')

        ],

        [

            InlineKeyboardButton('Deposit', callback_data='deposit'),

            InlineKeyboardButton('Withdraw', callback_data='withdraw')

        ],

        [

            InlineKeyboardButton('Change bet size', callback_data='cbs'),

            InlineKeyboardButton('How to play (Help)', callback_data='help')

        

        ],

        [

            

            InlineKeyboardButton('Refferal Link (Invite people)', callback_data='ref')

        ],

        



    ]

    return InlineKeyboardMarkup(keyboard)





def balance_low_keyboard():

    keyboard = [

        [

            InlineKeyboardButton('Deposit', callback_data='deposit'),

            InlineKeyboardButton('Change Bet size', callback_data='cbs')

        ],

        [InlineKeyboardButton('Go back', callback_data='backto_main')],

    ]

    return InlineKeyboardMarkup(keyboard)





def won_message(drawn_choice, bet_size, current_balance):

    return '?\n?\nCongratulations!! You have won ' + str(

        bet_size) + ' coins. Coin landed on ' + drawn_choice + '. Your balance is ' + str(

        current_balance) + ' coins.\n?\n?'





def lost_message(drawn_choice, bet_size, current_balance):

    return '??\n??\nOops... you have lost ' + str(

        bet_size) + ' coins. Coin landed on ' + drawn_choice + '. Your balance is ' + str(

        current_balance) + ' coins.\n??\n??'





def main_menu_message(drawn_choice, bet_size, current_balance):

    return 'Heads or Tails?   Bet size: ' + str(bet_size) + ' coins\n\n(1 Birr = 100 coins)\n\nCurrent balance: ' + str(

        current_balance) + ' coins or ' + str(

        current_balance / 100) + ' Birr'





def host_or_join_keyboard():

    keyboard = [

        [

            InlineKeyboardButton('Invite a friend', callback_data='host'),

            InlineKeyboardButton('Join ( Enter code )', callback_data='join'),

        ],

        [

            InlineKeyboardButton('Back to main menu', callback_data='backto_main')

        ],

    ]

    return InlineKeyboardMarkup(keyboard)





def heads_or_tails_multi_keyboard():

    keyboard = [

        [

            InlineKeyboardButton('Head', callback_data='head_m'),

            InlineKeyboardButton('Tail', callback_data='tail_m'),

        ],

        [

            InlineKeyboardButton('Go back to main menu', callback_data='backto_main_multi')

        ],

    ]

    return InlineKeyboardMarkup(keyboard)





def bet_choice_multi_keyboard():

    keyboard = [

        [

            InlineKeyboardButton('Free', callback_data='c9001c_0')

        ],

        [

            InlineKeyboardButton('50', callback_data='c9001c_50'),

            InlineKeyboardButton('100', callback_data='c9001c_100'),

            InlineKeyboardButton('300', callback_data='c9001c_200'),

            InlineKeyboardButton('500', callback_data='c9001c_500')

        ],



        [

            InlineKeyboardButton('1000', callback_data='c9001c_1000'),

            InlineKeyboardButton('2000', callback_data='c9001c_2000'),

            InlineKeyboardButton('3000', callback_data='c9001c_3000'),

            InlineKeyboardButton('5000', callback_data='c9001c_5000')

        ],

        [

            InlineKeyboardButton('10000', callback_data='c9001c_10000'),

            InlineKeyboardButton('20000', callback_data='c9001c_20000'),

            InlineKeyboardButton('30000', callback_data='c9001c_30000'),

            InlineKeyboardButton('50000', callback_data='c9001c_50000')

        ],



        [

            InlineKeyboardButton('Go back', callback_data='backto_main')

        ],



    ]

    return InlineKeyboardMarkup(keyboard)



def refresh_chances():

     print('refreshing chances')

     u = str(requests.get(server+'users.json').json())

     ue=get_entities(u)

     

     for v in ue:

       requests.patch(server+'users/'+v+'.json',json={'chance':10})

    

     print('refreshing complete')



def main():

    

    # PORT=process.env.PORT



    updater = Updater(TOKEN, use_context=True)



    updater.dispatcher.add_handler(CommandHandler('start', start))

    updater.dispatcher.add_handler(CommandHandler('help', help))

    updater.dispatcher.add_handler(CallbackQueryHandler(All_queries_handler))

    updater.dispatcher.add_handler(MessageHandler(Filters.text, All_messages_handler))





    #updater.start_polling()

    

    PORT=int(os.environ.get("PORT",8443))

    #print("EXEC 7")

    #print("port "+str(PORT))

    updater.start_webhook(listen="0.0.0.0",port=PORT,url_path=TOKEN,webhook_url='https://tele2442.herokuapp.com/' + TOKEN)

    #updater.idle()

    #updater.bot.setWebhook('https://tele2442.herokuapp.com/' + TOKEN)

    print("done")



main()







st=0

async def main2():



    #async with TelegramClient(session_name, api_id, api_hash) as client:

      while(1==1):

           

        #try:    

        # await client.send_message('etaeta24bot', '/start')

        #except Exception as e:

        #    print('Ex Error '+str(e))  

        #lr = int(str(requests.get(server+'system/last_refresh.json').json()))

 

        requests.get('https://tele2442.herokuapp.com/' + TOKEN)

        

        

        time.sleep(1000)

    







        #await client.run_until_disconnected()







# Otherwise

asyncio.run(main2())

