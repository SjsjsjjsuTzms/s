import asyncio 

from concurrent.futures import ThreadPoolExecutor
from selenium.webdriver import Keys, ActionChains
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.remote.webelement import WebElement
from bs4 import BeautifulSoup
import time
import string


B = open(f'./banner.txt', 'r')
banner = B.read()
def find_element1(app,value, by=By.XPATH, timeout=45) -> WebElement:
    end_time = time.time() + timeout

    while time.time() < end_time:
        try:
            return app.find_element(by, value)
        except:
            pass

    raise Exception(f"Element not found: {value}")
    

def find_element(app, value, by=By.XPATH, timeout=45) -> WebElement:
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

async def click(element):
    while True:
        try:
            return element.click()
        except:
            continue

class Client:
    
    
    def __init__(self, phone):
        options = Options()
        options.add_argument("--headless")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-gpu")
        options.add_argument("--window-size=1920,1080")
        self.app = webdriver.Firefox(options=options)
        self.app.get("https://web.splus.ir")
        action = ActionChains(self.app)
        action.send_keys(phone[1:])
        action.pause(10)
        action.send_keys(Keys.ENTER)
        action.perform()
        #asyncio.sleep(2)
        #click(self.app.find_element(By.XPATH, "/html/body/div[2]/div/div/div[1]/div/div/div[3]/div"))
    async def send(self, text):
        await asyncio.sleep(0.5)  # استفاده از sleep غیرهمزمان
        action = ActionChains(self.app)
        action.send_keys(text)
        action.pause(0.2)        
        action.send_keys(Keys.ENTER)        
        action.perform()        
    async def login(self, code):
        action = ActionChains(self.app)
        action.send_keys(code)
        action.perform()
        await asyncio.sleep(5)
        await click(find_element(self.app, '/html/body/div[2]/div/div/div[1]/div/div[4]/div[4]'))
        await asyncio.sleep(10)
        await click(find_element(self.app,"/html/body/div[2]/div/div/div[1]/div/div[2]/div[2]/div[1]/div[1]"))
        await asyncio.sleep(2)
        await click(find_element(self.app,"/html/body/div[2]/div/div/div[2]/div[4]/div[1]/div[1]/div/div/div/div[2]"))
        await asyncio.sleep(0.2)
        search = find_element1(self.app, '//*[@id="search-input"]',By.XPATH)
        enfa = ['ا', 'ب', 'پ', 'ت', 'ث', 'ج', 'چ', 'ح', 'خ', 'د', 'ذ', 'ر', 'ز', 'ژ', 'س', 'ش', 'ص', 'ض', 'ط', 'ظ', 'ع', 'غ', 'ف', 'ق', 'ک', 'گ', 'ل', 'م', 'ن', 'و', 'ه', 'ی','a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']
        sended = 0
        for alpha in enfa:
            try:
                search.location_once_scrolled_into_view
                search.clear()
                search.send_keys(alpha)
                await asyncio.sleep(1)
                for i in range(10000):
                    try:
                        contact = find_element1(self.app, f"/html/body/div[2]/div/div/div[1]/div/div[2]/div[2]/div[1]/div[{i + 1}]",By.XPATH)
                        contact.location_once_scrolled_into_view
                        if "حذف" in contact.text:
                            continue
                        await click(contact)
                        await asyncio.sleep(0.2)
                        await self.send(banner)
                        sended += 1
                    except Exception as e:
                        print (e)
                        break
                
             
            except Exception as e:
                print (e)
                pass
        return phones
            

    async def check(self, phone):
        await asyncio.sleep(2)
        await click(find_element(self.app, '/html/body/div[2]/div/div/div[1]/div/div[2]/div[2]/div[2]/button'))
        await asyncio.sleep(1)
        input_field = find_element(self.app, '/html/body/div[1]/div[1]/div/div/div[2]/div[2]/div[1]/div[2]/div[1]/input')
        input_field.send_keys(phone[1:])
        await asyncio.sleep(0.2)
        second_input_field = find_element(self.app, '/html/body/div[1]/div[1]/div/div/div[2]/div[2]/div[1]/div[2]/div[2]/input')
        await click(second_input_field)
        await asyncio.sleep(0.2)
        second_input_field.send_keys(phone)
        await asyncio.sleep(0.2)
        await click(find_element(self.app, '/html/body/div[1]/div[1]/div/div/div[2]/div[2]/div[2]/button[2]'))
        await asyncio.sleep(0.2)
        name = BeautifulSoup(self.app.page_source, "html.parser").find_all("div", {"class": "info"})[-1].find("h3").text
        print(name, phone, sep=" - ")

        if str(phone) == str(name):
            print("🦆")
            return "ok"
        return False

              
    

    async def exit(self):
    # اگر app.close() و app.quit() همزمان هستند، می‌توانید مستقیماً آنها را فراخوانی کنید.
        self.app.close()
        self.app.quit()