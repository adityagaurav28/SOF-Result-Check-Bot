#Selenium Version - 3.141.0
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.select import Select

import pandas as pd

#ChromeDriver Version - 89.0.4389.23
#Chrome Version - 89.0.4389.90
driver = webdriver.Chrome("C:\\Software\\chromedriver.exe")     #Replace it with your location of browser driver
driver.get("http://results.sofworld.org/results")   #Opening the browser

#For summarising the result
Names = []
Marks = []
Rank = []
Award_Won = []

#Olympiad for which you want to check
#Should exactly match the dropdown menu option
olympiad = 'SOF NSO 2020-21' 

schoolCode = "GJ0637"   #Replace the school code for which you want to check
standard = '08'     #Replace the standard for which you want to check
rollNo = ['001','002','003','004','005','006','007','008','009','010']  #Replace the roll numbers of the students as a list 

for number in rollNo:   #Iterating through all the roll numbers
    startUrl = driver.current_url
    
    #Filling out the input fields
    Select(driver.find_element_by_id('edit-olympiad-selected')).select_by_visible_text(olympiad)
    driver.find_element_by_id('edit-rollid1').send_keys(schoolCode)
    driver.find_element_by_id('edit-rollid2').send_keys(standard)
    driver.find_element_by_id('edit-rollid4').send_keys(number)
    
    #Getting the captcha question
    mathsQuestion = driver.find_element_by_class_name('field-prefix').text
    space = mathsQuestion.find(' ')
    num1 = int(mathsQuestion[0:space])
    num2 = int(mathsQuestion[space+3:-1])
    ans = num1 + num2
    
    #Providing answer
    driver.find_element_by_id('edit-captcha-response').send_keys(str(ans) + Keys.ENTER)
    endUrl = driver.current_url
    if endUrl == startUrl:  #To check if the roll number exist or not
        Names.append('NA')
        Marks.append('NA')
        Rank.append('NA')
        Award_Won.append('NA')
        continue 

    #Getting the info
    name = driver.find_element_by_css_selector('#block-system-main .content .result-cards-no-border tbody tr:nth-child(1) td:nth-child(2)').text    
    marks = driver.find_element_by_css_selector('#block-system-main .content .result-cards-no-border tbody tr:nth-child(5) td:nth-child(2)').text    
    rank = driver.find_element_by_css_selector('#block-system-main .content .result-cards-no-border tbody tr:nth-child(11) td:nth-child(2)').text    
    award = driver.find_element_by_css_selector('#block-system-main .content .result-cards-no-border tbody tr:nth-child(12) td:nth-child(2)').text    
    
    Names.append(name)
    Marks.append(marks)
    Rank.append(rank)
    Award_Won.append(award)

    #Going back to home page
    driver.back()
    driver.refresh()

driver.close()  #Closing the browser

#Storing the result as a pandas table
Result = pd.DataFrame()
Result['Roll No.'] = rollNo
Result['Name'] = Names
Result['Marks'] = Marks
Result['Rank'] = Rank
Result['Award Won'] = Award_Won

print("\n")
print(Result.to_string(index=False))
#:)
