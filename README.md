# Web Application with Automated Testing
This project is a web-based restaurant billing system that allows users to manage orders, calculate bills with tax and optional discounts, and test the system using Selenium automation.

## Features

- **Order Summary Page:** Add items to an order, adjust quantities, and calculate the bill.
- **Bill Summary Page:** View the detailed breakdown of the bill, including subtotal, discount, tax, and total.
- **Selenium Test Automation:** Automatically test various order scenarios to ensure accuracy.

## Project Structure

### HTML Files

1. **`orderSummary.html`**
   - Page to create and manage an order.
   - Features item selection, quantity adjustment, and options for calculating bills (with or without discounts).

2. **`bill.html`**
   - Displays the detailed bill summary, including tax and discount calculations.

### CSS

- **`style.css`**
  - Defines the look of the project, providing a consistent theme and responsive design.

### Python

- **`seleniumTest.py`**
  - Automated test script using Selenium to validate the system's functionality.
  - Tests different orders by pulling test cases from a CSV file.
  - Calculates totals and verifies the results against expected outputs.

## Usage

### Setting Up the System

1. Place all files in a web server directory (e.g., `htdocs` for XAMPP).
2. Access the `orderSummary.html` page in your browser.

### Running Tests

1. Install dependencies:
   ```bash
   pip install selenium
   ```
2. Ensure you have the Chrome WebDriver installed and accessible.
3. Prepare a `testcases.csv` file containing the test scenarios in the same directory as the Python script.
4. Run the Selenium script:
   ```bash
   python seleniumTest.py
   ```
5. View results in the console. Screenshots of each test are saved in the `screenshots` directory.

## Disclaimer
This project was originally completed as an assignment and has been uploaded to GitHub at a later date due to limited OneDrive storage. As a result, the commit history may not accurately reflect the development process, and there may be only a few commits for the project.

