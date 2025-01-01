from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import csv
from datetime import datetime
import os

# Function to setup the Chrome WebDriver
def setupDriver():
    options = Options()
    options.binary_location = "chrome-win32/chrome.exe"
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--disable-gpu')
    driver = webdriver.Chrome(options=options)
    driver.maximize_window()
    return driver, WebDriverWait(driver, 20)


# Function to input quantities on the orderSummary page
def inputQuantities(driver, wait, row):
    driver.get('http://localhost/ForTesting/orderSummary.html')
    items = ['peach-tea', 'mineral-water', 'banana-fritters', 'abc', 
                'fried-chicken-wings', 'braised-beef-noodle', 
                'nasi-lemak-curry-chicken', 'mee-goreng-mamak']
    
    for item in items:
        qty_input = wait.until(EC.presence_of_element_located((By.NAME, f'{item}-qty')))
        qty_input.clear()
        qty_input.send_keys(row[item])

    button_name = "calculate-discount" if row['discount'].lower() == 'true' else "calculate"
    driver.find_element(By.NAME, button_name).click()
    wait.until(EC.url_contains('bill.html'))


# Function to get total values from the bill page
def getBillValues(driver, row):
    subtotal = float(driver.find_element(By.NAME, "subtotal").text.replace('RM ', ''))
    discount = float(driver.find_element(By.NAME, "discount").text.replace('-RM ', '')) if row['discount'].lower() == 'true' else 0.0
    tax = float(driver.find_element(By.NAME, "tax").text.replace('RM ', ''))
    total = float(driver.find_element(By.NAME, "total").text.replace('RM ', ''))
    return subtotal, discount, tax, total


# Function to validate the test case
def validateTestCase(row, actual_values):
    subtotal, discount, tax, total = actual_values
    assert subtotal == float(row['expected_subtotal']), f"Subtotal mismatch. Expected: RM {float(row['expected_subtotal']):.2f}, Actual: RM {subtotal:.2f}"
    assert discount == float(row['expected_discount']), f"Discount mismatch. Expected: RM {float(row['expected_discount']):.2f}, Actual: RM {discount:.2f}"
    assert tax == float(row['expected_tax']), f"Tax mismatch. Expected: RM {float(row['expected_tax']):.2f}, Actual: RM {tax:.2f}"
    assert total == float(row['expected_total']), f"Total mismatch. Expected: RM {float(row['expected_total']):.2f}, Actual: RM {total:.2f}"


# Function to format item names
def formatItemName(item_name):
    return ' '.join(word.capitalize() for word in item_name.split('-'))


# Function to print test case details
def printTestCaseDetails(row):
    print("Test Case Details:")
    print("-" * 30)
    print(f"Discount Applied: {row['discount']}")
    print("\nInput Values:")
    items = ['peach-tea', 'mineral-water', 'banana-fritters', 'abc', 
                'fried-chicken-wings', 'braised-beef-noodle', 
                'nasi-lemak-curry-chicken', 'mee-goreng-mamak']
    for item in items:
        if int(row[item]) > 0:
            print(f"  {formatItemName(item)}: {row[item]}")
    
    print("\nExpected Values:")
    print(f"  Subtotal: RM {float(row['expected_subtotal']):.2f}")
    print(f"  Discount: RM {float(row['expected_discount']):.2f}")
    print(f"  Tax: RM {float(row['expected_tax']):.2f}")
    print(f"  Total: RM {float(row['expected_total']):.2f}")
    print("-" * 30)

# Function to run the test cases
def runTestCases():
    driver, wait = setupDriver()
    test_counter = 1
    
    if not os.path.exists('screenshots'):
        os.makedirs('screenshots')
        
    try:
        with open('testcases.csv', newline='') as csvfile:
            for row in csv.DictReader(csvfile):
                try:
                    print("\n\n\n" + "=" * 100)
                    print(f"TC{test_counter}: {row['test-name']}")
                    printTestCaseDetails(row)
                    
                    inputQuantities(driver, wait, row)
                    actual_values = getBillValues(driver, row)
                    validateTestCase(row, actual_values)
                    
                    # Take screenshot after pass
                    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
                    screenshot_path = f"screenshots/TC{test_counter}_{timestamp}.png"
                    driver.save_screenshot(screenshot_path)
                    
                    print("✓ Test Case PASSED!")
                    print(f"Screenshot saved to: {screenshot_path}")
                    print("=" * 100)
                    
                except AssertionError as e:
                    # Take screenshot on failure
                    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
                    screenshot_path = f"screenshots/TC{test_counter}_FAILED_{timestamp}.png"
                    driver.save_screenshot(screenshot_path)
                    
                    print(f"❌ Test Case FAILED!")
                    print(f"Error: {str(e)}")
                    print(f"Failure screenshot saved to: {screenshot_path}")
                    print("=" * 100)
                    
                test_counter += 1
                
    finally:
        driver.quit()

# Main function
if __name__ == "__main__":
    runTestCases()
