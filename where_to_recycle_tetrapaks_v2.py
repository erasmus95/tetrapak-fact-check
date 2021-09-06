# -*- coding: utf-8 -*-
"""
Created on Thu May 20 17:58:26 2021

@author: Gregory Robben
"""

"""
This program is designed to test all known US zipcodes against www.recylcecartons.com
and find out where in the US you can actually recycle your tetrapak cartons.

The claim made by tetrapak is 60% of US households can recycle their cartons at the curb.
To test this claim we will need both the valid zipcodes from www.recyclecartons.com,
as well as the distribution of the US population within these zipcodes.

Inputs: None
Outputs: 
    + csv file of zipcodes and True or False values for if a carton can be recylced
    + Print the percent of the US population that can recycle cartons at the curb

"""
import selenium
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import chromedriver_binary #adds chromedriver binary to path
import time
import csv
counter = 0
yes_freq = 0
no_freq = 0

##############################################################################
#Open Chrome and our target site
driver = webdriver.Chrome()
driver.get("https://www.recyclecartons.com/find/state/?n=usa")
#print(driver.title) #State - Carton Council
#assert "Carton" in driver.title #assert can be used as a sanity check. Catch errors with try
##############################################################################
#Open our source file in read mode to get the zipcodes and other columns
with open("zip_code_database_p4.csv", newline='',mode= 'r') as zip_source:
    #Open/create an output file in write mode
    with open("zip_results_p4.csv",newline='',mode='w') as zip_output:
        #reader object, only reads in the zips from source
        zip_reader = csv.reader(zip_source,dialect='excel') 
        #Define the column names for the output file
        fieldnames = ['zip','state','irs_estimated_population_2015','carton_recycling']
        #Writer object just for the output
        zip_writer = csv.DictWriter(zip_output, fieldnames= fieldnames, dialect='excel')
        zip_writer.writeheader()
        next(zip_reader) #skips the first row
       
        try:
            #Now we loop through the zipcodes and see what we get
            for row in zip_reader:
                #grabbing an element: ID > NAME > CLASS > TAG
                #We are looking for the name "zip" 
                if row[14]=="0": 
                    continue #skip row if no population
                zip_enter = driver.find_element_by_name("zip")
                #type in and send our zipcode into the search box
                zip_enter.send_keys(row[0].zfill(5))
                zip_enter.send_keys(Keys.RETURN)
                #wait an arbitrary amount of time
                time.sleep(0.25)#could replace to wait for certain elements to appear
            
                result = driver.find_element_by_xpath("/html/body/div[3]/div/h2[1]") #title found AKA Yes
                result_short = 1
                
                #since both results were visible regardless of input check which result is true
                if len(result.text) == 0:
                    result = driver.find_element_by_xpath("/html/body/div[3]/div/h2[3]") #title AKA No
                    result_short = 0
                    no_freq +=1
                else:
                    yes_freq += 1 
                counter += 1
                print(f"{counter}: {row[0]}: {result.text} - {result_short}")
                
        
                zip_writer.writerow({'zip': row[0],'state':row[6],'irs_estimated_population_2015':row[14],'carton_recycling':result_short})
                #time.sleep(0)
                if counter == 250: 
                    time.sleep(60) 
                    counter = 0
        except:
            driver.close() #closes current tab
            driver.quit() #closes browser   
coverage = yes_freq/counter *100
print(f"Of the zip codes searched: {yes_freq}/{counter} or {coverage}% had curbside recycling available")            
driver.close() #closes current tab
driver.quit() #closes browser