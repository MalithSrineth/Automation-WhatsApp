from flask import Flask, request
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import ElementClickInterceptedException
from selenium.common.exceptions import ElementNotInteractableException
import pyperclip
import time

app = Flask(__name__)

# This variable will store the last processed post_id
last_processed_post_ids = []

# List of WhatsApp group names
group_choice = "EN"
group_names = []
group_names = ['NewsWave English SuperGrp', "NewsWaveLK English Test"]

if group_choice == "EN":
    group_names = ['NewsWave English SuperGrp', 'NewsWave LK English - 01', 'NewsWave LK English - 23', 'NewsWave LK English - 32',
               'NewsWave LK English - 33', 'NewsWave LK English - 45', 'NewsWave LK English - 46', 'NewsWave LK English - 47']

elif group_choice == "SN":
    group_names = ['NewsWave Sinhala SuperGrp', 'NewsWave LK - 01', 'NewsWave LK - 02', 'NewsWave LK - 06', 'NewsWave LK - 21',
                'NewsWaveLK - 25', 'NewsWave LK - 31', 'NewsWave LK - 35', 'NewsWave LK - 39', 'NewsWave LK - 40', 'NewsWave LK - 43']

# Replace with the path to your Chrome profile
chrome_profile_path = 'C:/Users/malit/AppData/Local/Google/Chrome/User Data/Default'

# Set Chrome options to use the existing profile
options = Options()
options.add_argument(f'user-data-dir={chrome_profile_path}')


# Initialize WebDriver with the specified profile
driver = webdriver.Chrome(options=options)

# Open WhatsApp Web
driver.get('https://web.whatsapp.com')
wait = WebDriverWait(driver, 30)

def wait_for_element(xpath, search_box, search_box_text, group_name, timeout=10, attempts=10):
    for attempt in range(attempts):
        try:
            print(xpath)
            return WebDriverWait(driver, timeout).until(EC.presence_of_element_located((By.XPATH, xpath)))
        except TimeoutException or ElementClickInterceptedException or ElementNotInteractableException:
            print("Exception Occured: "+xpath)
            print(f"Attempt {attempt+1} failed, retrying...")
            search_box_text.send_keys(Keys.CONTROL + "a")
            search_box_text.send_keys(Keys.DELETE)
            search_box.send_keys(Keys.ENTER)
            search_box.send_keys(group_name)
            time.sleep(2)
            if attempt == attempts - 1:
                raise

def send_message_to_group(group_name, message, count):
    # Search for the group
    wait.until(EC.presence_of_element_located((By.XPATH, '//div[@contenteditable="true"][@data-tab="3"]')))
    search_box = driver.find_element(By.XPATH, '//div[@contenteditable="true"][@data-tab="3"]')
    search_box_text = driver.find_element(By.XPATH, '//*[@id="side"]/div[1]/div/div[2]/div[2]/div/div[1]/p')
    # search_box.clear()
    # search_box.click()
    # search_box.send_keys(group_name)
    # time.sleep(2)  # Time for search results to appear
    while search_box.text != group_name:
        # search_box_text.clear()
        search_box.send_keys(Keys.ENTER)
        search_box.send_keys(group_name)
        time.sleep(2)

    if search_box.text == group_name:
        group_xpath = f'//span[@title="{group_name}"]'
        group_element = wait_for_element(group_xpath, search_box, search_box_text, group_name, timeout=10, attempts=10)
        if search_box.text == group_name:
            search_box.send_keys(Keys.ENTER)
        else:
            search_box.send_keys(Keys.ENTER)
            search_box.send_keys(group_name)
            time.sleep(2)
            search_box.send_keys(Keys.ENTER)

        # wait.until(EC.presence_of_element_located((By.XPATH, f'//span[@title="{group_name}"]'))).click()
        # search_box.send_keys(Keys.ENTER)
    

    # Enter the message
    wait.until(EC.presence_of_element_located((By.CLASS_NAME, '_ak1l')))
    message_box = driver.find_element(By.CLASS_NAME, '_ak1l')
    time.sleep(2)
    message_box.send_keys(message)
    if count == 0 or count == 1:
        time.sleep(10)
        message_box.send_keys(Keys.ENTER)
    else:
        time.sleep(3)
        message_box.send_keys(Keys.ENTER)






@app.route('/webhook', methods=['POST'])
def webhook():
    global last_processed_post_ids
    data = request.json
    current_post_id = data.get('post_id')  # Extract the post_id from the incoming data
    post = data.get('post')
    post_status = post.get('post_status')

    count = 0

    # Check the post status and the last processed post_id
    if post_status == "auto-draft":
        print(f"Auto Draft request for post_id: {current_post_id} skipped.")
        return 'Auto Draft request skipped', 200
    
    elif post_status == "draft":
        print(f"Draft request for post_id: {current_post_id} skipped.")
        return 'Draft request skipped', 200
    
    elif post_status == "publish" and current_post_id in last_processed_post_ids:
        print(f"Update request for post_id: {current_post_id} skipped.")
        return 'Update request skipped', 200
    
    elif post_status == "publish" and current_post_id not in last_processed_post_ids:
        last_processed_post_ids.append(current_post_id)

        print(f"Publish request for post_id: {current_post_id} processed.")
        post_title = post.get('post_title')
        post_url = data.get('post_permalink')
        message = (f"*{post_title}* - {post_url}")

        facebook_message = (f"{post_title}\n{post_url}\n\nJoin our WhatsApp Group.\nhttps://get.newswave.lk/ENAlert")
        print(f"https://www.facebook.com/sharer.php?u={post_url}")
        print(facebook_message)

        for group in group_names:
            if count == 0:
                time.sleep(20)
            time.sleep(1)
            send_message_to_group(group, message, count)
            time.sleep(3)
            count += 1
            
        time.sleep(5)
        driver.execute_script("window.open(arguments[0], '_blank');", f"https://www.facebook.com/sharer.php?u={post_url}")
        time.sleep(5)
        pyperclip.copy(facebook_message)

        # driver.switch_to.window(driver.window_handles[1])

        # # Now, locate the textarea in the new tab
        # textarea = driver.find_element(By.CSS_SELECTOR, 'textarea[title="Say something about this..."]')
        # textarea.send_keys(facebook_message)
        # textarea.send_keys(Keys.BACKSPACE)
        # textarea.send_keys('h')
        # time.sleep(1)
        # textarea.send_keys(Keys.ENTER)

        # post_button = driver.find_element(By.XPATH, '//*[@class="_42ft _4jy0 layerConfirm _1flv _51_n autofocus _4jy3 _4jy1 selected _51sy"]')
        # post_button.click()
        # driver.switch_to.window(driver.window_handles[0])

        
        # driver.get(f"https://www.facebook.com/sharer.php?u={post_url}")
        # time.sleep(5)
        # typeBox = driver.find_element(By.CLASS_NAME, 'uiTextareaNoResize uiTextareaAutogrow input mentionsTextarea textInput')
        
        
        # pyperclip.paste()

        # typeBox.click()
        # typeBox.send_keys('facebook_message')
        # time.sleep(2)
        # postButton = driver.find_element(By.XPATH, '//*[@id="u_0_22_bQ"]')
        # postButton.click()
        
        # WebDriverWait(driver, 10).until(
        #     EC.presence_of_element_located((By.XPATH, "//textarea[@name='xhpc_message_text']"))
        # )

        # # Find the input area and enter the message
        # input_area = driver.find_element(By.XPATH, "//textarea[@name='xhpc_message_text']")
        # input_area.send_keys(facebook_message)

        # # Find the 'Post to Facebook' button and click it
        # post_button = driver.find_element(By.XPATH, "//button[contains(text(),'Post to Facebook')]")
        # post_button.click()
        return 'Publish request processed', 200
    
    elif post_status == "trash":
        print(f"Trash request for post_id: {current_post_id} skipped.")
        return 'Trash request skipped', 200
    
    else:
        print(f"{post_status} for post_id: {current_post_id} skipped.")
        return 'Unknown request skipped', 200

if __name__ == '__main__':
    app.run(debug=False, port=5000)  