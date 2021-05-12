from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


PATH = r"C:\Users\Ricem\Documents\Code\PokernowInfo\chromedriver.exe"
driver = webdriver.Chrome(PATH)


driver.get("https://www.pokernow.club/games/AMJ_4Z-jUwxPFwFJaJm2OFMv0")

#Click the log/ledger menu
try:
    logLedger = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "show-log-button")))
except: 
    driver.quit
logLedger.click()

#click the button to display the session ledger 
try:
    logControls = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, "log-modal-controls"))
        )
    buttons = logControls.find_elements_by_class_name("green-2")
    buttons[1].click()
except: 
    driver.quit