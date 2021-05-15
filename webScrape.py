from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options




def getPlayerData(URL):

    PATH = r"C:\Users\Ricem\Documents\Code\PokernowInfo\chromedriver.exe"

    options = Options()
    options.add_argument('--headless')
    options.add_argument('--disable-gpu')
    driver = webdriver.Chrome(PATH, chrome_options=options)


    driver.get(str(URL))
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

    try:
        playerTables = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "/html/body/div/div/div[1]/div/div/div[2]/div/div[2]/div[1]/div"))
        )
        rows = playerTables.find_elements_by_class_name("player-ledger-table")
        playersList = []
        #get data for each player in the table 
        for row in rows:
            data = row.text
            username = data.split("@ ")[1]
            nickname = data.split(" @")[0]
            username = username.split("\nDETAILS")[0]
            net = data.split()[7]
            net = net.replace('+', '')
            player = {
                        "nickname" : nickname,
                        "net" : net
                    }
            playersList.append(player)


        

    except:
        driver.quit

    driver.quit
    return playersList

