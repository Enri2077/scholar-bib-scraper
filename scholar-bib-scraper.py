# simple script to get bibtex entris of saved article in Google Scholer
# requires login and reCAPTCHA

import time 
from selenium import webdriver
from selenium.webdriver.support import ui
import codecs


def get_entries_on_file(driver, log_file='links.txt', bib_file='refs.bib'):
    with codecs.open(log_file, 'a', 'utf-8') as f: # for logging the current page
        f.write(driver.current_url + '\n')
    # all these sleeps may not be really necessary
    time.sleep(0.1)
    select_all = wait.until(lambda driver: driver.find_element_by_id('gs_res_ab_xall'))
    time.sleep(0.1)
    select_all_clicked = False
    while not select_all_clicked:
        try:
            select_all.click()
            select_all_clicked = True
            time.sleep(0.1)
        except:
            print "could not click on select all. Expand the window to make the button visible"
            time.sleep(2.0)
    export = wait.until(lambda driver: driver.find_element_by_id('gs_res_ab_exp-b'))
    time.sleep(0.1)
    export.click()
    time.sleep(0.1)
    bibtex = wait.until(lambda driver: driver.find_element_by_partial_link_text('BibTeX'))
    time.sleep(0.1)
    bibtex.click()
    time.sleep(0.1)
    body = wait.until(lambda driver: driver.find_element_by_tag_name('body'))
    time.sleep(0.1)
    text = body.text 
    with codecs.open(bib_file, 'a', 'utf-8') as f: # keep appending the bibtex entries to file
        f.write(text + '\n\n')


if __name__ == '__main__':
    # initialize the browser -- requires chromedriver   
    driver = webdriver.Chrome(executable_path='/home/enrico/w/scholar-bib-scraper/chromedriver')
    # this waiting may not be necessary
    wait = ui.WebDriverWait(driver, 90) 
    driver.get('http://www.scholar.google.com/');
    
    raw_input("Select the English language (EN-EN) for the page, log in and press enter in this console...")

    library = wait.until(lambda driver: driver.find_element_by_partial_link_text('library'))
    time.sleep(1)
    library.click()
    time.sleep(1)
    get_entries_on_file(driver) # get the 10 entries at the first page
    time.sleep(1) # this is where I had to solve reCAPTCHA

    for i in range(1, 500): 
        # this loop breaks with some error after all done
        # after the loop there will be total%10 more articles left
        time.sleep(1)
        link = 'https://scholar.google.com/scholar?start={}&hl=en&as_sdt=0,5&scilib=1'.format(10*i)
        driver.get(link); # alt method: find and click NEXT until no longer can
        get_entries_on_file(driver)


