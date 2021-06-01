from selenium import webdriver

options = webdriver.ChromeOptions()
options.headless = True
options.add_argument("--window-size=800,800")
browser = webdriver.Chrome(executable_path='chromedriver', options=self.options)
#browser = webdriver.Chrome(executable_path='/Users/william.cecil/Desktop/Scripts/Briefgen/chromedriver-mac', options=options)
browser.get("https://www.uswitch.com")

print(browser.page_source)