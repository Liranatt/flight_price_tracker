from selenium.common.exceptions import NoSuchElementException
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
class DatesHandler:
    def __init__(self, driver, wait):
        self.driver = driver
        self.wait = wait

    def open_calender(self):
        dates_tab = self.wait.until(EC.element_to_be_clickable((By.XPATH, "//div[contains(text(),'תאריכים')]")))
        dates_tab.click()
        print("opened date tab")
        time.sleep(1)

    def move_to_month(self, month_str: str):
        while True:
            try:
                self.driver.find_element(By.XPATH, f"//*[contains(text(), \"{month_str}\")]")
                print(f"✅ Found {month_str}!")
                break
            except NoSuchElementException:
                print(f"🔄 Still looking for {month_str}, clicking left arrow...")
                left_arrow = self.wait.until(
                    EC.element_to_be_clickable((By.CLASS_NAME, "rdrNextButton"))
                )
                left_arrow.click()
                time.sleep(1)

    def pick_day(self, day: int, side: str = "left"):
        """
        Picks a specific day from the calendar side (left or right).
        """
        print(f"📅 Looking for day {day} on the {side} calendar")

        # Map side to calendar index: left = 0, right = 1
        side_index = 0 if side == "left" else 1

        # Find all calendars
        calendars = self.driver.find_elements(By.CLASS_NAME, "rdrMonth")
        if len(calendars) <= side_index:
            raise Exception(f"❌ Could not find {side} calendar (index {side_index})")

        calendar = calendars[side_index]
        cells = calendar.find_elements(By.XPATH,
                                       ".//td[contains(@class, '_cell__default') and not(contains(@class, 'outside'))]")

        for cell in cells:
            try:
                span = cell.find_element(By.TAG_NAME, "span")
                if span.text.strip() == str(day):
                    print(f"✅ Found and clicked day {day}")
                    span.click()
                    return
            except Exception as e:
                continue

        raise Exception(f"❌ Day {day} not found in {side} calendar")

