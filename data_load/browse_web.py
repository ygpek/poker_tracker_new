from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import TimeoutException
import os

# Streamlit app URL from environment variable (or default)
STREAMLIT_URLS = [
    "https://kartydengidvatuza.streamlit.app/",
    "https://matchenginehackathon-i3jgbmutzakg3gntslaohx.streamlit.app/",
]


def check_app(driver, url):
    try:
        driver.get(url)
        print(f"Opened {url}")

        wait = WebDriverWait(driver, 15)

        try:
            button = wait.until(
                EC.element_to_be_clickable((By.XPATH, "//button[contains(text(),'Yes, get this app back up')]"))
            )

            print("Wake-up button found. Clicking...")
            button.click()

            try:
                wait.until(
                    EC.invisibility_of_element_located(
                        (By.XPATH, "//button[contains(text(),'Yes, get this app back up')]")
                    )
                )
                print(f"App waking up successfully: {url} ✅")

            except TimeoutException:
                print(f"Wake-up button did not disappear: {url} ❌")
                return False

        except TimeoutException:
            print(f"App already awake: {url} ✅")

        return True

    except Exception as e:
        print(f"Error checking {url}: {e}")
        return False


def main():
    options = Options()
    options.add_argument("--headless=new")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-gpu")
    options.add_argument("--window-size=1920,1080")

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

    try:
        results = {}

        for url in STREAMLIT_URLS:
            print(f"\nChecking app: {url}")
            results[url] = check_app(driver, url)

        print("\n--- Summary ---")
        for url, success in results.items():
            print(f"{'✅' if success else '❌'} {url}")

        if not all(results.values()):
            raise SystemExit(1)

    finally:
        driver.quit()
        print("Script finished.")


if __name__ == "__main__":
    main()
