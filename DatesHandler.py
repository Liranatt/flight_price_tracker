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

    def pick_day_from_month(self, month_str: str, day: int):
        self.wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, "rdrMonth")))
        month_blocks = self.driver.find_elements(By.CLASS_NAME, "rdrMonth")

        for month in month_blocks:
            try:
                label = month.find_element(By.CLASS_NAME, "rdrMonthName")
                if month_str in label.text:
                    print(f"✅ Found month {month_str}")

                    # Search only in visible buttons (days)
                    buttons = month.find_elements(By.CLASS_NAME, "rdrDay")
                    for btn in buttons:
                        try:
                            text = btn.text.strip().split('\n')[0]  # Get just the number
                            if text == str(day):
                                print(f"🟢 Clicking on day {day} in {month_str}")
                                btn.click()
                                return
                        except Exception as e:
                            continue
                    raise Exception(f"❌ Could not find day {day} in {month_str}")
            except Exception as e:
                continue

        raise Exception(f"❌ Month block with {month_str} not found")

    def press_search_button(self):
        import re

        # Step 1: Open the passenger tab
        passengers_tab = self.wait.until(EC.element_to_be_clickable(
            (By.XPATH, "//div[contains(text(),'הרכב')]")))
        passengers_tab.click()
        print("👤 Opened passenger selection")
        time.sleep(1)

        # Step 2: Reduce adult passengers to 1
        while True:
            value_element = self.driver.find_element(By.CLASS_NAME, "_value_1w76n_65")
            num_passengers = int(value_element.text.strip())
            if num_passengers <= 1:
                print("✅ Passenger count is already 1")
                break
            minus_button = self.driver.find_element(By.XPATH,
                                                    "//div[contains(@class,'_button-group')]/button[contains(text(),'-')]")
            minus_button.click()
            print(f"➖ Reduced to {num_passengers - 1}")
            time.sleep(0.5)

        # Step 3: Press the "חפש" or "המשך" button
        search_button = self.wait.until(EC.element_to_be_clickable((
            By.XPATH, "//button[contains(text(),'חפש') or contains(text(),'המשך')]"
        )))
        search_button.click()
        print("🔍 Search button clicked")


