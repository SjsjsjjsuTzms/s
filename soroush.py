from selenium.webdriver import Keys, ActionChains
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.remote.webelement import WebElement
from bs4 import BeautifulSoup
import time

async def find_element(app, value, by=By.XPATH, timeout=45) -> WebElement:
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

    while 1:
        try:
            return app.await find_element(by, value)
        except:
            # Attempt to use an alternative path if one is defined
            if value in alternate_paths:
                alt_value = alternate_paths[value]
                try:
                    return app.await find_element(by, alt_value)
                except:
                    pass
            time.sleep(1)

    raise Exception(f"Element not found: {value}")

# تابع برای کلیک بر روی عنصر در Selenium با حداکثر تلاش
async def click(element):
    while 1:
        try:
            return element.click()
        except:
            continue

class Client:
    
    async def __init__(self, phone):
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

    async def login(self, code: int):
        action = ActionChains(self.app)
        action.send_keys(Keys.BACKSPACE, Keys.BACKSPACE, Keys.BACKSPACE, Keys.BACKSPACE, Keys.BACKSPACE)
        action.send_keys(code)
        action.perform()
        time.sleep(5)
        await click(await find_element(self.app, '/html/body/div[2]/div/div/div[1]/div/div[4]/div[4]'))
    
    async def check(self, phone):
        await click(await find_element(self.app, '/html/body/div[2]/div/div/div[1]/div/div[2]/div[2]/div[2]/button'))
        time.sleep(1)
        await find_element(self.app, '/html/body/div[1]/div[1]/div/div/div[2]/div[2]/div[1]/div[2]/div[1]/input').send_keys(phone[1:])
        time.sleep(0.2)
        await click(await find_element(self.app, '/html/body/div[1]/div[1]/div/div/div[2]/div[2]/div[1]/div[2]/div[2]/input'))
        time.sleep(0.2)
        await find_element(self.app, '/html/body/div[1]/div[1]/div/div/div[2]/div[2]/div[1]/div[2]/div[2]/input').send_keys(phone)
        time.sleep(0.2)
        await click(await find_element(self.app, '/html/body/div[1]/div[1]/div/div/div[2]/div[2]/div[2]/button[2]'))
        time.sleep(0.2)
        name = BeautifulSoup(self.app.page_source, "html.parser").find_all("div", {"class":"info"})[-1].find("h3").text
        if phone == name:
            return True
        return False
    
    async def send(self, text):
        time.sleep(0.5)
        action = ActionChains(self.app)
        action.send_keys(text)
        action.pause(0.2)
        action.send_keys(Keys.ENTER)
        action.perform()

    async def exit(self):
        self.app.close()
        self.app.quit()
