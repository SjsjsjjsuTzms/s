from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup , InlineQueryResultArticle, InputTextMessageContent , CallbackQuery
from pyrogram.types.bots_and_keyboards import force_reply 
from pyrogram import Client,types,filters
from pyromod import listen
import random, string
from asyncio import sleep
import time
import json
import re
import os
from soroush import Client as SClient






START=InlineKeyboardMarkup([
[InlineKeyboardButton("✅ اضافه کردن اکانت ✅" , "Addaccount")],
[ InlineKeyboardButton("⚙ تنظیم بنر یک ⚙" , "banner1")],
])

cancell=ReplyKeyboardMarkup([['/cancell']],resize_keyboard =True)
wait=ReplyKeyboardMarkup([['منتظر باش دلقک']],resize_keyboard =True)

proxy = None
Owner=[390353852,5394456754] # ایدی عددی بزار
token="8023919010:AAGCN859kl11gxmV3C0eEe6eX8pSzuSInOM"
Bot=Client("CreateBot",api_id=15567484,api_hash="9cee14fbc3ea1fefd4bbb4fd4e2daa6d",bot_token=token)

      

@Bot.on_message(filters.user(Owner) & filters.command("start") )
async def start(_:Bot,Event:types.Message):
    B = open(f'./banner.txt', 'r')
    banner = B.read()
    await Event.reply(f"""

Banner : {banner}

Channel : @PyUnknown""",reply_markup=START)



@Bot.on_callback_query(filters.user(Owner) & filters.regex("Addaccount"))
async def logins(Event:types.Message,Call:CallbackQuery):
    phone=await Bot.ask(chat_id=Call.message.chat.id,text="شماره خود را برای ورود ارسال کنید\nمثال:\n09957619252\n یا /cancell",reply_markup=cancell)
    if phone.text=="/cancell":
        await Call.message.reply("cancell Ok",reply_markup=START)
    else:       
        if len(phone.text) == 11:  
            await Call.message.reply("درحال اتصال به سروش [ 10 ثانیه صبر کن ]...")
            app = SClient(Final)     
        else:
            await Call.message.reply("احمق گفتم شماره رو درست بفرست",reply_markup=START)
            
            return
        
        
        result=await Bot.ask(chat_id=Call.message.chat.id,text="کد را وارد کنید یا /cancell",reply_markup=cancell)        
        if result.text=="/cancell":
            await Call.message.reply("cancell Ok",reply_markup=START)
        else:
            if len(result.text) == 5:  
                print ("ok")
            else:
                await Call.message.reply("احمق گفتم کد رو درست بفرست",reply_markup=START)
                return
            try:            
                await Call.message.reply("درحال وارد کردن کد [ 20 ثانیه صبر کن, سپس ارسال شروع میشه]...")                
                x = await app.login(result.text)
            except:
                pass
            await app.exit()                       
            await Call.message.reply(f"""❕هشدار:\n- اکانت {Final} با موفقیت از دیتابیس حذف شد ✅\n تعداد پیام های ارسال شده : {x}""",reply_markup=START)
       
            
           
@Bot.on_callback_query(filters.user(Owner) & filters.regex("banner1"))
async def banner1(Event:types.Message,Call:CallbackQuery):
    time=await Bot.ask(chat_id=Call.message.chat.id,text="""بنرت رو ارسال کن یا برای لغو عملیات /cancell""",reply_markup=cancell)
    if time.text=="/cancell":
        await Call.message.reply("cancell Ok",reply_markup=START)
    else:      
        os.remove('banner.txt')
        t = time.text
        with open('banner.txt', 'a') as f:
            f.write(t) 
        await Call.message.reply(f"با موفقیت تنظیم شد , \nBanner :\n {time.text}",reply_markup=START)    
print("Run")
Bot.run()






