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
    driver = uc.Chrome(options=options)
    return driver


def go_to_results_page(driver):
    print("opening travelist")
    driver.get("https://www.travelist.co.il")
    wait = WebDriverWait(driver, 20)

    # Step 1: Select "מאיפה" and enter "תל אביב"
    print("clicking form where")
    from_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//div[contains(text(),'מאיפה')]")))
    from_button.click()

    print("filling in tel aviv")
    from_input = wait.until(EC.presence_of_element_located((By.XPATH, "//input[@placeholder='מאיפה טסים?']")))
    from_input.send_keys("תל אביב")
    from_input.send_keys(Keys.ENTER)
    print("done")

    # Step 2: Select "לאן טסים?" and enter "בנגקוק"
    print("clicking destination")
    to_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//div[contains(text(),'לאן טסים?')]")))
    to_button.click()

    print("pausing to let input render...")
    time.sleep(2)  # allow UI animation/render

    print("waiting for destination input")
    to_input = wait.until(EC.visibility_of_element_located((By.XPATH, "//input[@placeholder='הקלד יעד…']")))
    print("typing Bangkok")
    to_input.send_keys("בנגקוק")
    print("typed bangkok, waiting for suggestion...")

    time.sleep(1.5)  # let dropdown suggestions load

    # Step 3: Click on the dropdown suggestion for Bangkok
    wait.until(EC.presence_of_element_located((By.CLASS_NAME, "_results_1cpnn_255")))
    print("suggestions box appeared, waiting for Bangkok suggestion...")

    suggestion = wait.until(EC.element_to_be_clickable((By.CLASS_NAME, "_resultItem_1cpnn_119")))
    suggestion.click()
    print("✅ Clicked suggestion for Bangkok, Thailand")


def main():
    driver = create_driver()
    wait = WebDriverWait(driver, 20)
    go_to_results_page(driver)
    dates = DatesHandler(driver, wait)
    dates.open_calender()
    dates.move_to_month("אוג׳ 2025")

    dates.pick_day_from_month("אוג׳ 2025", 20)
    dates.move_to_month("אוק׳ 2025")
    dates.pick_day_from_month("אוק׳ 2025", 28)
    time.sleep(5)
    dates.press_search_button()
    time.sleep(20)


if __name__ == "__main__":
    main()
