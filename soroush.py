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
        t =BeautifulSoup(self.app.page_source, "html.parser")
        with open(f'./1.txt', 'a') as f:
            f.write(str(t))
            

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
    async def check2(self):
        try:
            phones = []
            alphabet = list(string.ascii_lowercase)
            search = self.app.find_element(By.XPATH, '//*[@id="search-input"]')
            
            for alpha in alphabet:
                search.location_once_scrolled_into_view
                search.clear()
                search.send_keys(alpha)
                await asyncio.sleep(1)  # استفاده از sleep غیرهمزمان
                
                for i in range(1000):
                    try:
                        contact = self.app.find_element(By.XPATH, f"/html/body/div[2]/div/div/div[1]/div/div[2]/div[2]/div[1]/div[{i + 1}]")
                        contact.location_once_scrolled_into_view
                        
                        if "حذف" in contact.text:
                            continue
                        
                        contact.click()
                        await asyncio.sleep(0.2)  # استفاده از sleep غیرهمزمان
                        
                        contact_phone = self.app.find_element(By.XPATH, "/html/body/div[2]/div/div/div[3]/div/div[2]/div/div[1]/div[2]/div[1]/div/div[1]/span[1]")
                        phones.append(contact_phone.text.replace(" ", "").replace("+98", "0"))
                        await asyncio.sleep(0.3)  # استفاده از sleep غیرهمزمان
                        
                    except Exception as e:
                        print(e)
                        break
                return phones
        except Exception as e:
            print(e)

        
    
   
    async def send(self, text):
        await asyncio.sleep(0.5)  # استفاده از sleep غیرهمزمان
        action = ActionChains(self.app)
        action.send_keys(text)
        action.pause(0.2)        
        action.send_keys(Keys.ENTER)        
        action.perform()        
        print("⭐⭐")

    async def exit(self):
    # اگر app.close() و app.quit() همزمان هستند، می‌توانید مستقیماً آنها را فراخوانی کنید.
        self.app.close()
        self.app.quit()