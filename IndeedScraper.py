from multiprocessing.connection import wait
from os import remove
import random
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
import pandas as pd
from selenium.common.exceptions import ElementClickInterceptedException
import yake

file_object = open('job reqs.txt', 'a')


driver = webdriver.Chrome('/Users/jamesmatherly/sample/indeed-scraper/chromedriver')
lastUrl = 'https://www.indeed.com/jobs?q=java+developer&l=remote&sc=0kf%3Aattr%28DSQF7%29attr%28EVPJU%29explvl%28MID_LEVEL%29jt%28fulltime%29%3B&start=90&pp=gQB4AAAAAAAAAAAAAAAB60l2owC1AQIBJGgHWp8K6uOp0r0DAmWezVNK7QjJrvGZlUiu9kmpBKVNdhbyZmcULuMnYRasrhfEoEm6BRTyFkn4-TYCZbHwaCLaB0HquCtcO1-H06uOsVjQqtKjTjqHeLqGSXaYzUuEfeEJD99Tqdpefgdt3cetpF_GNX2D-3kGA6-K4p0tyVyLkjC2gt9xvdpWs_hpkEPYaBB_zpb9lO0Ow4I4qA3cBWaH8zY4DPBYMWkXmgzQf-q9kQAA&vjk=a4cb394acb5f303a&advn=6821675637299254'
driver.get(lastUrl)


try:
    while len(driver.find_elements(By.XPATH, '//*/a[@aria-label="Next Page"]')) > 0:
        jobCards = driver.find_elements(By.CLASS_NAME, 'job_seen_beacon')
        for jobCard in jobCards:
            jobCard.click()
            if len(driver.window_handles) > 1:
                for i in range(1, len(driver.window_handles) - 1):
                    driver.switch_to.window(driver.window_handles[1])
                    if 'Checking if the site connection is secure' in driver.page_source or 'About Indeed\'s estimated salaries' in driver.page_source:
                        print('breakpoint')
                    if len(driver.find_elements(By.ID, 'jobDescriptionText')) > 0:
                        jd = driver.find_element(By.ID, 'jobDescriptionText')
                        file_object.write(jd.text)
                    else:
                        print('breakpoint')
                    driver.close()
                    driver.switch_to.window(driver.window_handles[0])
            else:
                if len(driver.find_elements(By.ID, 'jobDescriptionText')) > 0:
                    jd = driver.find_element(By.ID, 'jobDescriptionText')
                    file_object.write(jd.text)
                else:
                    print('breakpoint')
        time.sleep(random.randint(1, 3))                
        try:
            driver.find_element(By.XPATH, '//*/a[@aria-label="Next Page"]').click()
        except ElementClickInterceptedException:
            print('breakpoint')
        if 'Checking if the site connection is secure' in driver.page_source or 'About Indeed\'s estimated salaries' in driver.page_source:
            print('breakpoint')
finally:
    print('breakpoint')
    driver.switch_to.window(driver.window_handles[0])
    print (driver.current_url())


file_object.close()
file_object = open('job reqs.txt', 'r')
output_file = open('keyword output.txt', 'w')
fullText = file_object.read()
extractor = yake.KeywordExtractor(top=500)
keywords = extractor.extract_keywords(fullText)
for k, v in keywords:
    output_file.write(k + '\n')

for i in range(1, len(driver.window_handles) - 1):
    driver.switch_to.window(driver.window_handles[0])
    driver.close()

file_object.close()
output_file.close()


