import time, os
from pdf import pdf
from pathlib import Path
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.options import Options
import click


def capture():

    if( os.path.exists('current_link.txt')):
        if click.confirm('There is a current link. Do you want to use it?'):
            with open("current_link.txt", "r") as f:
                u = f.read()
        else:
            u = click.prompt('URL: ')
    else:
        u = click.prompt('URL: ')


    # Initial driver
    chrome_options = Options()
    chrome_options.headless = True
    driver = webdriver.Firefox(options=chrome_options)
    driver.set_window_size(450, 1000)
    driver.get(u)
    block(driver)

    # Make directory to save screen hot
    dir = u.split("/")[-3]
    try:
        os.mkdir(dir)
    except:
        pass

    # Previous URL
    pre_url = u

    # Save link to a file
    with  open("current_link.txt", "w") as f:
        f.write(u)

    # Find load more
    load_more_button = driver.find_element_by_css_selector("a.btn.btn-info.next")

    while load_more_button:

        take_screen_shot(driver, pre_url, dir)

        if load_more_button:
            print("Next page...")
            try:
                load_more_button.click()
            except:
                pass
            #driver.execute_script("arguments[0].click();", load_more_button)
            time.sleep(1)
            end = False
            # Try 5 times before end
            for i in range(1,6):
                current_url = driver.current_url
                if(current_url != pre_url):
                    driver.get(current_url)
                    pre_url = current_url
                    # Save link to a file
                    with  open("current_link.txt", "w") as f:
                        f.write(pre_url)
                    break
                elif i < 5:
                    time.sleep(1)
                else:
                    end = True
            if end:
                print("The end")
                break
            block(driver)
            load_more_button = driver.find_element_by_css_selector("a.btn.btn-info.next")
        else:
            print("load more fail")

    Path("./current_link.txt").rename("./"+dir+"/current_link.txt")
    driver.quit()
    return dir

def block(driver):
    driver.execute_script("document.getElementsByClassName('reading-control')[0].style.display='none';")
    driver.execute_script("document.getElementsByClassName('header')[0].style.display='none';")
    driver.execute_script("document.getElementsByClassName('row')[1].style.display='none';")
    driver.execute_script("document.getElementsByClassName('top')[0].style.display='none';")
    driver.execute_script("document.getElementsByClassName('comment')[0].style.display='none';")
    driver.execute_script("document.getElementById('taboola-below-article-thumbnails-1').style.display='none';")
    driver.execute_script("document.getElementsByClassName('reading')[0].style.zoom='200%'")

def block50(driver):
    for i in range(1,51):
        driver.execute_script("document.getElementById('page_"+str(i)+"').style.display='none';")

def scroll(driver):

    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

    SCROLL_PAUSE_TIME = 0.5

    # Get scroll height
    last_height = driver.execute_script("return document.body.scrollHeight")

    while True:
        # Scroll down to bottom
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

        # Wait to load page
        time.sleep(SCROLL_PAUSE_TIME)

        # Calculate new scroll height and compare with last scroll height
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height
    return new_height

def take_screen_shot(driver, pre_url, dir):
    name = pre_url.split("/")[-2]
    height = scroll(driver)
    driver.set_window_size(450, height)
    print("height "+str(height))
    driver.save_screenshot(name+".png")
    Path("./"+name+".png").rename("./"+dir+"/"+name+".png")
    print(name)
    try:
        if height > 34000:
            block50(driver)
            height = scroll(driver)
            driver.set_window_size(450, height)
            print("height extra "+str(height))
            START = START + 1
            driver.save_screenshot(name+"_1.png")
            Path("./"+name+"_1.png").rename("./"+dir+"/"+name+"_1.png")
            print(name+'_1')
    except:
        pass

if __name__ == '__main__':
    dir = capture()
    print("Done capture - Move to make pdf")
    # Default number of files is 50
    pdf(dir)
