#from selenium.webdriver import Keys, ActionChains
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.remote.webelement import WebElement
from bs4 import BeautifulSoup
#from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
import time
import time

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

    while 1:
        try:
            return app.find_element(by, value)
        except:
            # Attempt to use an alternative path if one is defined
            if value in alternate_paths:
                alt_value = alternate_paths[value]
                try:
                    return app.find_element(by, alt_value)
                except:
                    pass
            time.sleep(1)

    raise Exception(f"Element not found: {value}")

# تابع برای کلیک بر روی عنصر در Selenium با حداکثر تلاش
def click(element):
    while 1:
        try:
            return element.click()
        except:
            continue

class Client:
    
    def __init__(self, phone):
        # Set up Firefox options
        options = Options()
        options.add_argument("--headless")  # Run in headless mode
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-gpu")
        options.add_argument("--window-size=1920,1080")

        # Initialize the WebDriver
        self.app = webdriver.Firefox(options=options)
        
        try:
            # Open the target website
            self.app.get("https://web.splus.ir")
            time.sleep(2)  # Wait for the page to load

            # Perform actions
            action = ActionChains(self.app)
            action.send_keys(phone[1:])  # Send phone number without the first character
            action.pause(1)  # Pause for 1 second
            action.send_keys(Keys.ENTER)  # Press Enter
            action.perform()
            
            time.sleep(10)  # Wait to observe the result (optional)
        
        except Exception as e:
            print(f"An error occurred: {e}")
        
        finally:
            self.app.quit()  # Ensure 

    def login(self, code: int):
        action = ActionChains(self.app)
        action.send_keys(code)
        action.perform()
        time.sleep(5)
        click(find_element(self.app, '/html/body/div[2]/div/div/div[1]/div/div[4]/div[4]'))
        
    
    def check(self, phone):
        click(find_element(self.app, '/html/body/div[2]/div/div/div[1]/div/div[2]/div[2]/div[2]/button'))
        time.sleep(1)
        find_element(self.app, '/html/body/div[1]/div[1]/div/div/div[2]/div[2]/div[1]/div[2]/div[1]/input').send_keys(phone[1:])
        time.sleep(0.2)
        click(find_element(self.app, '/html/body/div[1]/div[1]/div/div/div[2]/div[2]/div[1]/div[2]/div[2]/input'))
        time.sleep(0.2)
        find_element(self.app, '/html/body/div[1]/div[1]/div/div/div[2]/div[2]/div[1]/div[2]/div[2]/input').send_keys(phone)
        time.sleep(0.2)
        click(find_element(self.app, '/html/body/div[1]/div[1]/div/div/div[2]/div[2]/div[2]/button[2]'))
        time.sleep(0.2)
        name = BeautifulSoup(self.app.page_source, "html.parser").find_all("div", {"class":"info"})[-1].find("h3").text
        if phone == name:
            return True
        return False
    
    def send(self, text):
        time.sleep(0.5)
        action = ActionChains(self.app)
        action.send_keys(text)
        action.pause(0.2)
        action.send_keys(Keys.ENTER)
        action.perform()
        
s1 = Client(input("phone = "))
s1.login(input("code = "))
s1.check("09144084093")
s1.send(input("msg = "))
