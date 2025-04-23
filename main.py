import time
import os
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
from DatesHandler import DatesHandler


def create_driver():
    options = uc.ChromeOptions()
    driver = uc.Chrome(options = options)
    return driver

def go_to_results_page(driver):
    print("opening travelist")
    driver.get("https://www.travelist.co.il")
    wait = WebDriverWait(driver,20)
    print("clicking form where")
    from_buttuom = wait.until(EC.element_to_be_clickable((By.XPATH, "//div[contains(text(),'מאיפה')]")))
    from_buttuom.click()
    print("filling in tel aviv")
    from_input = wait.until((EC.presence_of_element_located((By.XPATH, "//input[@placeholder='מאיפה טסים?']"))))
    from_input.send_keys("תל אביב")
    from_input.send_keys(Keys.ENTER)
    print("done")

    print("clicking destination")
    to_buttuom = wait.until(EC.element_to_be_clickable((By.XPATH, "//div[contains(text(),'לאן טסים?')]")))
    to_buttuom.click()

    print("pausing to let input render...")
    time.sleep(2)  # sometimes needed after animation

    # Debug: Print all input fields
    inputs = driver.find_elements(By.TAG_NAME, "input")
    for i, field in enumerate(inputs):
        print(f"Input {i}: placeholder = {field.get_attribute('placeholder')}, id = {field.get_attribute('id')}")

    print("waiting for destination input")
    to_input = wait.until(EC.visibility_of_element_located((By.XPATH, "//input[@placeholder='הקלד יעד…']")))
    print("typing Bangkok")
    to_input.send_keys("בנגקוק")
    to_input.send_keys(Keys.ENTER)
    print("typed bangkok succesfully")

def main():
    driver = create_driver()
    wait = WebDriverWait(driver, 20)
    go_to_results_page(driver)
    dates = DatesHandler(driver, wait)
    dates.open_calender()
    dates.move_to_month("אוג׳ 2025")

    dates.pick_day(20, side="right")
    dates.move_to_month("אוק׳ 2025")
    dates.pick_day(28, side="left")

    time.sleep(30)
if __name__== "__main__":
    main()

