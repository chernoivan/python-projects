import undetected_chromedriver
import time


def main(driver):
    try:
        for i in range(0, 1000, 24):
            driver.get(f"https://onlyfinder.com/best-onlyfans/top/{i}")
            if i == 0:
                time.sleep(30)

            time.sleep(7)

            with open(f"/Users/alex/Documents/repos/parsing/onlyfinder/data/index_{i}.html", "w") as file:
                file.write(driver.page_source)

    except Exception as ex:
        print(ex)
    finally:
        driver.close()
        driver.quit()
        time.sleep(5)


if __name__ == '__main__':
    try:
        driver = undetected_chromedriver.Chrome()
        main(driver)
    except Exception as ex:
        print(ex)
