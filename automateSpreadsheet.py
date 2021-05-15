from __future__ import print_function
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google.oauth2 import service_account
import webScrape
from datetime import date as dt
from datetime import datetime 
import tkinter as tk

SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
SERVICE_ACCOUNT_FILE = "creds.json"

creds = None
creds = service_account.Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPES)


# The ID and range of a sample spreadsheet.
SAMPLE_SPREADSHEET_ID = '1Hn0_WByKg_TylDZoQWb2-mUWzj6UkRb5FBvPQASKJN8'


service = build('sheets', 'v4', credentials=creds)
sheet = service.spreadsheets()


def main():

    link = "https://www.pokernow.club/games/AMJ_4Z-jUwxPFwFJaJm2OFMv0"


    namesRange = "Copy of May W3!b4:b27"
    netRange = "Copy of May W3!c4:u27"
    datesRange = "Copy of May W3!c1:u1"
    players = sheet.values().get(spreadsheetId=SAMPLE_SPREADSHEET_ID,
                                range=namesRange).execute()
    netGainsLosses = sheet.values().get(spreadsheetId=SAMPLE_SPREADSHEET_ID,
                                range=netRange).execute()
    dates = sheet.values().get(spreadsheetId=SAMPLE_SPREADSHEET_ID,
                                range=datesRange).execute()

    values = dates.get('values', [])
    playerNames = players.get("values", [])

    #get results from the csv file
    playerDicts = webScrape.getPlayerData(str(link))

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
    resultLink = [[link]]
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



if __name__ == "__main__":
    main()