from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup , InlineQueryResultArticle, InputTextMessageContent , CallbackQuery
from pyrogram.types.bots_and_keyboards import force_reply 
from pyrogram import Client,types,filters
from pyromod import listen
import random, string
from asyncio import sleep
import time
import json
import re
from soroush import Client as SClient





database= {'SLEEPTIME': 1, 'banner1' : None, 'banner2' : None, 'name' : None}
groupText=str(database['banner1'])
START=InlineKeyboardMarkup([
[InlineKeyboardButton("✅ اضافه کردن اکانت ✅" , "Addaccount")],
[ InlineKeyboardButton("⚙ تنظیم بنر یک ⚙" , "banner1")],
])

cancell=ReplyKeyboardMarkup([['/cancell']],resize_keyboard =True)
wait=ReplyKeyboardMarkup([['منتظر باش دلقک']],resize_keyboard =True)
yesno=ReplyKeyboardMarkup([
['Yes','No'],
],resize_keyboard =True)

def randomword(length=5):
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(length))
    
    
def lichNumber(num):
    return "\n".join([num + str(random.randint(1000000, 9999999)) for i in range(10000)])
  
proxy = None
Owner=[390353852,5394456754] # ایدی عددی بزار
token="8023919010:AAFtivUU-IGSpfUYmTnEWWrOZ7LsRkxoQKM"
Bot=Client("CreateBot",api_id=15567484,api_hash="9cee14fbc3ea1fefd4bbb4fd4e2daa6d",bot_token=token)

      

@Bot.on_message(filters.user(Owner) & filters.command("start") )
async def start(_:Bot,Event:types.Message):

    await Event.reply(f"""

Banner (1) : {database['banner1']}

Channel : @PyUnknown""",reply_markup=START)



@Bot.on_callback_query(filters.user(Owner) & filters.regex("Addaccount"))
async def getphone(Event:types.Message,Call:CallbackQuery):
    phone=await Bot.ask(chat_id=Call.message.chat.id,text="Enter Phone Number or /cancell",reply_markup=cancell)
    if phone.text=="/cancell":
        await Call.message.reply("cancell Ok",reply_markup=START)
    else:       
        Final = phone.text
        Final = phone.text.translate(str.maketrans('۰۱۲۳۴۵۶۷۸۹', '0123456789'))        
        Final = Final.replace("+98", "09")      
        app = SClient(Final)                  
        
        
        result=await Bot.ask(chat_id=Call.message.chat.id,text="Enter code or /cancell",reply_markup=cancell)        
        if result.text=="/cancell":
            await Call.message.reply("cancell Ok",reply_markup=START)
        try:            
            await app.login(result.text)
        except:pass
        response = True
        if response:
            await Call.message.reply(f"Login to {Final} was successful",reply_markup=wait)            
            num=await Bot.ask(chat_id=Call.message.chat.id,text="لیست شماره هاتو بفرست \n 09128610029 \n09126184872 \n09128097882\n یا /cancell",reply_markup=cancell)
            if num.text=="/cancell":
                await Call.message.reply("cancell Ok",reply_markup=START)
                return
            x = 0
            for number in num.text.split('\n'):                                
                try:
                    T= await app.check(number)
                    if T == "ok":
                        await app.send(str(database['banner1']))        
                        x +=1        
                except Exception as e:
                    await Call.message.reply(e)
            await app.exit()                       
            await Call.message.reply(f"""❕هشدار:\n- اکانت {Final} با موفقیت از دیتابیس حذف شد ✅\n تعداد پیوی های ارسا شده : {x}""",reply_markup=START)
        else:
            if result.text == "/cancell":
                print ("55")
            else:
                await Call.message.reply("ERROR",reply_markup=START)
                
            
           

@Bot.on_callback_query(filters.user(Owner) & filters.regex("banner1"))
async def getpjdjdhohhntse(Event:types.Message,Call:CallbackQuery):
    time=await Bot.ask(chat_id=Call.message.chat.id,text="""بنرت رو ارسال کن یا برای لغو عملیات /cancell""",reply_markup=cancell)
    if time.text=="/cancell":
        await Call.message.reply("cancell Ok",reply_markup=START)
    else:      
        database['banner1'] = time.text
        await Call.message.reply(f"با موفقیت تنظیم شد , \nBanner :\n {time.text}",reply_markup=START)    
print("Run")
Bot.run()






