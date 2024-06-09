import csv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException, ElementNotInteractableException

username = "Username"
password = "Password"
target_user = "Targated Username"  


driver = webdriver.Chrome()


driver.get("https://github.com/login")


def wait_for_element_interactable(by, value, timeout=10):
    try:
        element = WebDriverWait(driver, timeout).until(
            EC.element_to_be_clickable((by, value))
        )
        return element
    except TimeoutException:
        print(f"Element {value} not interactable within {timeout} seconds.")
        return None


username_field = wait_for_element_interactable(By.ID, "login_field")
if username_field:
    username_field.send_keys(username)


password_field = wait_for_element_interactable(By.ID, "password")
if password_field:
    password_field.send_keys(password)


login_button = wait_for_element_interactable(By.NAME, "commit")
if login_button:
    login_button.click()


try:
    error_message = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "div.flash.flash-full.flash-error"))
    )
    print("Login failed: Incorrect username or password.")
    driver.quit()
except TimeoutException:
    
    print("Login successful!")


    driver.get(f"https://github.com/{target_user}?tab=repositories")

    repositories = []
    try:
        repo_elements = WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, "div#user-repositories-list li"))
        )
        for repo in repo_elements:
            repo_name = repo.find_element(By.CSS_SELECTOR, "a[itemprop='name codeRepository']").text
            repo_url = repo.find_element(By.CSS_SELECTOR, "a[itemprop='name codeRepository']").get_attribute("href")
            repositories.append({"name": repo_name, "url": repo_url})
    except TimeoutException:
        print("Failed to load repository elements.")

    
    with open("repositories.csv", mode="w", newline='') as file:
        writer = csv.DictWriter(file, fieldnames=["name", "url"])
        writer.writeheader()
        for repo in repositories:
            writer.writerow(repo)

    print("Data extraction complete. Check repositories.csv for the extracted data.")

 
    driver.quit()
