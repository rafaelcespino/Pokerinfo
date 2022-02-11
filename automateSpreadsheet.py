from __future__ import print_function
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google.oauth2 import service_account
from datetime import date as dt
from datetime import datetime 
import tkinter as tk
from selenium import webdriver
import selenium
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options

SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
SERVICE_ACCOUNT_FILE = "./creds.json"

creds = None
creds = service_account.Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPES)


# The ID and range of a sample spreadsheet.
SAMPLE_SPREADSHEET_ID = '1Hn0_WByKg_TylDZoQWb2-mUWzj6UkRb5FBvPQASKJN8'


service = build('sheets', 'v4', credentials=creds)
sheet = service.spreadsheets()



def getPlayerData():
    
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

def on_open():
    global driver 

    if not driver:
        options = Options()
        options.add_argument('--headless')
        options.add_argument('--disable-gpu')
        PATH = "./driver/chromedriver.exe"
        driver = webdriver.Chrome(PATH, chrome_options=options)
        link = e.get()
        if "https" not in link:
            url = "https://www.{}".format(link)
        else:
            url = link
        driver.get(url)

    namesRange = "Copy of May W3!b4:b27"
    netRange = "Copy of May W3!c4:u27"
    datesRange = "Copy of May W3!c1:u1"
    players = sheet.values().get(spreadsheetId=SAMPLE_SPREADSHEET_ID,
                                range=namesRange).execute()
    dates = sheet.values().get(spreadsheetId=SAMPLE_SPREADSHEET_ID,
                                range=datesRange).execute()

    values = dates.get('values', [])
    playerNames = players.get("values", [])

    #get results from the csv file
    playerDicts = getPlayerData()

    #get the leftmost unused column to work with 
    dateCounter = 0
    dateCol = None
    for date in values[0]:
        if "Date of Match" in date:
            dateCol = dateCounter + 3
            break
        dateCounter += 1

    dateCol = chr(ord('`')+dateCol)

    #Fill in the date 
    today = dt.today()
    d1 = today.strftime("%d/%m/%Y")
    currentDate = [[d1]]
    result = service.spreadsheets().values().update(
        spreadsheetId=SAMPLE_SPREADSHEET_ID, range="Copy of May W3!{}1".format(dateCol),
        valueInputOption="USER_ENTERED", body={"values":currentDate}).execute()

    #Fill in the time
    now = datetime.now().time()
    current_time = now.strftime("%H:%M:%S")
    currentTime = [[current_time]]
    result = service.spreadsheets().values().update(
        spreadsheetId=SAMPLE_SPREADSHEET_ID, range="Copy of May W3!{}2".format(dateCol),
        valueInputOption="USER_ENTERED", body={"values":currentTime}).execute()

    #Fill in the link to the game 
    resultLink = [[url]]
    result = service.spreadsheets().values().update(
        spreadsheetId=SAMPLE_SPREADSHEET_ID, range="Copy of May W3!{}3".format(dateCol),
        valueInputOption="USER_ENTERED", body={"values":resultLink}).execute()


    for playerDict in playerDicts:
        write = [[playerDict["net"]]]
        rowCounter = 0
        for player in playerNames:
            #search for the right row 

            if player[0] == playerDict["nickname"]:
                rowNum = rowCounter +4
            rowCounter += 1
        #print("Row for {} is {}".format(playerDict["nickname"], rowNum))
        
        result = service.spreadsheets().values().update(
        spreadsheetId=SAMPLE_SPREADSHEET_ID, range="Copy of May W3!{}{}".format(dateCol, rowNum),
        valueInputOption="USER_ENTERED", body={"values":write}).execute()

    #close the driver after use 
    on_close()

def on_close():
    global driver

    if driver:
        driver.close()
        driver = None


# -- GUI -- #
driver = None

root = tk.Tk()
e = tk.Entry(root, width=50)
e.pack()

b = tk.Button(root, text = "Open", command=on_open)
b.pack()



root.mainloop()