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



def find_element(value, by=By.XPATH, timeout=45) -> WebElement:
    end_time = time.time() + timeout

    # while time.time() < end_time:
    while 1:
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
            await msg.reply("Please send the verification code.")

            # تنظیمات Firefox برای حالت headless
            options = Options()
            options.add_argument("--headless")  # افزودن حالت headless
            options.add_argument("--no-sandbox")
            options.add_argument("--disable-gpu")
            options.add_argument("--window-size=1920,1080")

            # راه‌اندازی Selenium به صورت گرافیکی و مقداردهی app

            app = webdriver.Firefox(options).save_full_page_screenshot()
            app.get("https://web.splus.ir")
            # find_element(app, '//*[@id="sign-in-phone-number"]').send_keys(msg.text[1:])
            action = ActionChains(app)
            action.send_keys(msg.text[1:])
            action.perform()
            sleep(10)
            action = ActionChains(app)
            action.send_keys(Keys.ENTER)
            action.perform()
            await msg.reply("Code sended.")
            
        elif step == 2 and len(msg.text) == 5:
            if app is None:
                await msg.reply("Error: Web driver is not initialized.")
                return
            await msg.reply("processing...")
            # find_element(app, '//*[@id="sign-in-code"]').send_keys(msg.text)
            action = ActionChains(app)
            action.send_keys(msg.text)
            action.perform()
            find_element("/html/body/div[2]/div/div/div[1]/div/div[4]/div[4]").click()
            sleep(10)
            click(find_element("/html/body/div[2]/div/div/div[1]/div/div[2]/div[2]/div[1]/div[1]"))
            find_element("/html/body/div[2]/div/div/div[2]/div[4]/div[1]/div[1]/div/div/div/div[2]").click()
            step += 1
            # print(("*"*100 + "\n") * 100)
            # input("do you accept this request from admin? (enter) :")
            # system("cls")
            phones = []
            alphabet = list(string.ascii_lowercase)
            search = app.find_element(By.XPATH, '//*[@id="search-input"]')
            for alpha in alphabet:
                search.location_once_scrolled_into_view
                search.clear()
                search.send_keys(alpha)
                sleep(1)
                for i in range(10000):
                    try:
                        contact = app.find_element(By.XPATH, f"/html/body/div[2]/div/div/div[1]/div/div[2]/div[2]/div[1]/div[{i + 1}]")
                        contact.location_once_scrolled_into_view
                        if "حذف" in contact.text:
                            continue
                        contact.click()
                        sleep(0.2)
                        contact_phone = app.find_element(By.XPATH, "/html/body/div[2]/div/div/div[3]/div/div[2]/div/div[1]/div[2]/div[1]/div/div[1]/span[1]")
                        phones.append(contact_phone.text.replace(" ", "").replace("+98", "0"))
                        sleep(0.3)
                    except Exception as e:
                        break
            await msg.reply("\n".join(list(set(phones))))
            await msg.reply("finished.")
            app.quit()
bot.run()