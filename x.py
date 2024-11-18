from pyrogram import Client, types
from time import sleep
from selenium import webdriver
from selenium.webdriver import Keys, ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.remote.webelement import WebElement
from os import system
from time import sleep
import time
import string
from soroush import Client as SClient


from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def find_element3(app, value, by=By.XPATH, timeout=45) -> WebElement:
    try:
        element = WebDriverWait(app, timeout).until(
            EC.presence_of_element_located((by, value))
        )
        return element
    except Exception as e:
        raise Exception(f"Element not found: {value}. Error: {str(e)}")
        
        
def find_element(app,value, by=By.XPATH, timeout=45) -> WebElement:
    end_time = time.time() + timeout

    while time.time() < end_time:
    #while 1:
        try:
            return app.find_element(by, value)
        except:
            sleep(1)

    raise Exception(f"Element not found: {value}")

# تابع برای کلیک بر روی عنصر در Selenium با حداکثر تلاش
def click(element, retries=5):
    for _ in range(retries):
        try:
            return element.click()
        except:
            sleep(1)
    raise Exception("Click failed after several attempts.")


def find_element1(app, value, by=By.XPATH, timeout=45) -> WebElement:
    end_time = time.time() + timeout
    alternate_paths = {
        "/html/body/div[1]/div[1]/div/div/div[2]/div[2]/div[1]/div[2]/div[2]/input": 
            "/html/body/div[1]/div[2]/div/div/div[2]/div[2]/div[1]/div[2]/div[2]/input",
        "/html/body/div[2]/div/div/div[2]/div[3]/div[2]/div/div[2]/div[1]/button": 
            "/html/body/div[2]/div/div/div[2]/div[4]/div[2]/div/div[2]/div[1]/button",
        "/html/body/div[1]/div[1]/div/div/div[2]/div[2]/div[1]/div[2]/div[1]/input": 
            "/html/body/div[1]/div[2]/div/div/div[2]/div[2]/div[1]/div[2]/div[1]/input",
        "/html/body/div[1]/div[1]/div/div/div[2]/div[2]/div[2]/button[2]": 
            "/html/body/div[1]/div[2]/div/div/div[2]/div[2]/div[2]/button[2]",
        "/html/body/div[2]/div/div/div[2]/div[3]/div[2]/div/div[2]/div[1]/button": 
            "/html/body/div[2]/div/div/div[2]/div[4]/div[2]/div[2]/div[2]/div[1]/button"
    }

    while True:
        try:
            return app.find_element(by, value)
        except:
            if value in alternate_paths:
                alt_value = alternate_paths[value]
                try:
                    return app.find_element(by, alt_value)
                except:
                    pass
            time.sleep(1)

    raise Exception(f"Element not found: {value}")

async def click1(element):
    while True:
        try:
            return element.click()
        except:
            continue
            
            
step = 0
#bot = Client("soroush", "", "", bot_token="")
token="8023919010:AAGCN859kl11gxmV3C0eEe6eX8pSzuSInOM"
bot=Client("CreateBot",api_id=15567484,api_hash="9cee14fbc3ea1fefd4bbb4fd4e2daa6d",bot_token=token)

@bot.on_message()
async def main(cli, msg: types.Message):
    global step, app
    if msg.from_user.id:
        if msg.text == "/cancel":
            step = 0
            await msg.reply("Operation cancelled.")
            return

        if step == 0:
            await msg.reply("Please send your phone number for login.")
            step += 1

        elif step == 1 and msg.text.startswith("09") and len(msg.text) == 11:
            step += 1
            await msg.reply("processing[10 sec]...")

            # تنظیمات Firefox برای حالت headless
            app = SClient(msg.text)
            await msg.reply("Code sended.")
            
        elif step == 2 and len(msg.text) == 5:
            if app is None:
                await msg.reply("Error: Web driver is not initialized.")
                return
            await msg.reply("processing[15]...")
            # find_element(app, '//*[@id="sign-in-code"]').send_keys(msg.text)
            await app.login(msg.text)
            await msg.reply("okay....")
            step += 1
            phones = []
            print(2)
            alphabet = list(string.ascii_lowercase)
            print(alphabet)
            print(3)
           # search = find_element(app, '//*[@id="search-input"]',By.XPATH)
            search = find_element(app ,"search-input",By.XPATH)
            print(search)
            print(4)
            for alpha in alphabet:
                print (11)
                search.location_once_scrolled_into_view
                search.clear()
                search.send_keys(alpha)
                sleep(1)
                for i in range(300):
                    try:
                        print ("🦆")
                        contact = find_element1(app,By.XPATH, f"/html/body/div[2]/div/div/div[1]/div/div[2]/div[2]/div[1]/div[{i + 1}]")
                        contact.location_once_scrolled_into_view
                        if "حذف" in contact.text:
                            continue
                        contact.click()
                        print ("⭐")
                        sleep(0.2)
                        contact_phone = find_element1(app,By.XPATH, "/html/body/div[2]/div/div/div[3]/div/div[2]/div/div[1]/div[2]/div[1]/div/div[1]/span[1]")
                        print(contact_phone)
                        print ("🆕")
                        phones.append(contact_phone.text.replace(" ", "").replace("+98", "0"))
                        sleep(0.3)
                    except Exception as e:
                        break
                print (phones)
            await msg.reply("\n".join(list(set(phones))))
            await msg.reply("finished.")
            app.quit()
bot.run()