import sys
import csv
from selenium import webdriver
from time import sleep

class bot():
    def __init__(self):
        self.driver = webdriver.Chrome()
        self.driver.get("https://www.gamedevmap.com/")

        global header
        global companyRows
        companyRows = []
        header = []
        companySelect = self.driver.find_element_by_id('typeDropdown').find_elements_by_tag_name("option")
        companyTypes = [elem for elem in companySelect if elem.get_attribute("value") != ""]
        self.typeNames = [t.get_attribute("value") for t in companyTypes]
        print "Company types:"
        for element in self.typeNames:
            print "- " + element
        # print "Countries:"
        # for element in self.countries:
        #     print "- " + element.get_attribute("value")
        
    
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
                print "Selected country - " + tmpName
                country.click()
            
    def parseHeader(self, headerRow):
        cells = headerRow.find_elements_by_tag_name('td')
        formatted = [st.text for st in cells]
        return formatted
            
    def parseCompany(self, companyRow):
        cells = companyRow.find_elements_by_tag_name('td')
        formatted = [st.text for st in cells]
        return formatted

    def parseTable(self):
        table = b.driver.find_element_by_xpath('/html/body/table/tbody/tr/td/div[3]/table[3]')
        rows = table.find_elements_by_tag_name('tr')
        global header
        header = self.parseHeader(rows[3])
        header = ','.join(header)
        print "-------" + header + "--------"
        i = 1
        for row in rows[4:-1]: # from 4th row to second last (included)
            global companyRows
            companyRow = self.parseCompany(row)
            companyRow = ','.join(companyRow)
            companyRows.append(companyRow)
            print i, " - ", companyRow
            i += 1
        print "-----------------------------"

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
            print "- " + t + "- parsing..."
            pageN = 1
            
            while True:
                print "- page ", pageN
                self.parseTable()
                # return # uncomment to parse first page
                nextPageBtn = self.getNext()
                if nextPageBtn:
                    nextPageBtn.click()
                    pageN += 1
                    sleep(0.1)
                else:
                    print "- " + t + "- completed."
                    return # uncomment to parse first company type only
                    break
            
    def dump(self):
        with open('gamedevmap.csv','wb') as file:
            global header
            file.write(header)
            file.write("\n")
            global companyRows
            for row in companyRows:
                file.write(row)
                file.write('\n')

b = bot()
sleep(0.2)
b.allCompByType()
b.dump()