from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import os


def _init_folder():
    folder = "screenshots"
    if not os.path.exists(folder):
        os.mkdir(folder)
    return folder


def _init_driver(show=True):
    options = Options()
    options.add_argument("--start-maximized")
    options.add_argument("--disable-notifications")
    options.add_argument("--incognito")
    if not show:
        options.add_argument("--headless")
    driver = webdriver.Chrome(options=options, executable_path="./chromedriver.exe")
    return driver


def save_screenshots_from_url(name, url):
    """Visit 'url' (str) and scroll through it, while taking screenshots of the entire page and
    saving them to files with names starting with 'name' (str).
    """
    folder = _init_folder()
    driver = _init_driver()
    driver.get(url)
    js_is_bottom_reached = (
        "return Math.abs(document.documentElement.scrollHeight"
        "- document.documentElement.scrollTop"
        "- document.documentElement.clientHeight) <= 3.0;"
    )
    count = 1
    while True:
        is_bottom_reached = driver.execute_script(js_is_bottom_reached)
        print("Continue..." if not is_bottom_reached else "Last one.")
        driver.save_screenshot(os.path.join(folder, f"{name}_{count}.png"))
        driver.execute_script(f"window.scrollTo(0, {count}*window.innerHeight);")
        count += 1
        if is_bottom_reached:
            driver.quit()
            break


def main(urls):
    """Record and save the entire page from multiple URLs to screenshots.
    The input 'urls' is a dictionary of custom names and URLs.
    Requires 'chromedriver.exe' to be placed in the same folder as this file.
    """
    for name, url in urls.items():
        print(f"\n** Working on '{name}' ** ")
        save_screenshots_from_url(name, url)



if __name__ == "__main__":
    main({
        "python": "https://www.python.org/",
        "selenium": "https://www.seleniumeasy.com/",
    })
