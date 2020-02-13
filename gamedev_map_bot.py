import sys
import csv
import unicodedata

from selenium import webdriver
from time import sleep
from datetime import datetime

class bot():
    def logMessage(self, message, toConsole=True):
        timeNow = datetime.now().strftime("%d.%m.%Y %H:%M:%S:%f")
        logLine = timeNow + " | " + message
        if toConsole:
            print logLine
        self.log.append(logLine)

    def __init__(self):
        self.driver = webdriver.Chrome()
        self.driver.get("https://www.gamedevmap.com/")

        self.companyRows = []
        self.header = []
        self.log = []
        self.logMessage("Bot initialized")
        companySelect = self.driver.find_element_by_id('typeDropdown').find_elements_by_tag_name("option")
        companyTypes = [elem for elem in companySelect if elem.get_attribute("value") != ""]
        
        self.typeNames = [t.get_attribute("value") for t in companyTypes]
        self.logMessage("Company types: " + ','.join(self.typeNames))
    
    def selectType(self, name):
        companySelect = self.driver.find_element_by_id('typeDropdown').find_elements_by_tag_name("option")
        companyTypes = [elem for elem in companySelect if elem.get_attribute("value") == name]
        companyTypes[0].click()
        
    def selectCountry(self, name):
        countriesSelect = self.driver.find_element_by_id('countryDropdown').find_elements_by_tag_name("option")
        countries = [elem for elem in countriesSelect if elem.get_attribute("value") != ""]
        for country in countries:
            tmpName = country.get_attribute("value")
            if name == tmpName:
                self.logMessage("Selected country - " + tmpName)
                country.click()
            
    def parseHeader(self, headerRow):
        cells = headerRow.find_elements_by_tag_name('td')
        formatted = [st.text.encode('ascii','ignore') for st in cells]
        return formatted
            
    def parseCompany(self, companyRow):
        cells = companyRow.find_elements_by_tag_name('td')
        formatted = [st.text.encode('ascii','ignore') for st in cells]
        return formatted

    def parseTable(self):
        table = self.driver.find_element_by_xpath('/html/body/table/tbody/tr/td/div[3]/table[3]')
        rows = table.find_elements_by_tag_name('tr')
        
        self.header = self.parseHeader(rows[3])
        self.header = ','.join(self.header)
        self.logMessage("-------" + self.header + "--------")
        i = 1
        for row in rows[4:-1]: # from 4th row to second last (included)
            companyRow = self.parseCompany(row)
            companyRow = ','.join(companyRow)
            self.companyRows.append(companyRow)
            self.logMessage(str(i) + " - " + companyRow)
            i += 1
        self.logMessage("-----------------------------")

    def getNext(self):
        try:
            nextPageBtn = self.driver.find_element_by_link_text(">>")
            return nextPageBtn
        except:
            # print("Next page button not found: ", sys.exc_info()[0])
            return None

    def allCompByType(self):
        # for each company type [in reverse order]
        for t in reversed(self.typeNames):
            self.selectType(t) # select dropdown item
            sleep(0.1) # wait for page to load
            self.logMessage("- " + t + "- parsing...")
            pageN = 1
            
            while True:
                self.logMessage("- page " + str(pageN))
                self.parseTable()
                # return # uncomment to parse first page
                nextPageBtn = self.getNext()
                if nextPageBtn:
                    nextPageBtn.click()
                    pageN += 1
                    sleep(0.1)
                else:
                    self.logMessage(str("- " + t + "- completed."))
                    # return # uncomment to parse first company type only
                    break
            
    def dump(self):
        with open('gamedevmap.csv','wb') as file:
            
            file.write(self.header)
            file.write("\n")
            
            for row in self.companyRows:
                file.write(row)
                file.write('\n')
            
    def dumpLog(self):
        with open('log.txt','wb') as file:
            for line in self.log:
                file.write(line)
                file.write('\n')

b = bot()
sleep(0.2)
b.allCompByType()
b.dump()
b.dumpLog()