from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

# List of WhatsApp group names
group_choice = "SN"
group_names = []
group_names = ['NewsWave English SuperGrp', "NewsWaveLK English Test"]

if group_choice == "EN":
    group_names = ['NewsWave English SuperGrp', 'NewsWave LK English - 01', 'NewsWave LK English - 23', 'NewsWave LK English - 32',
               'NewsWave LK English - 33', 'NewsWave LK English - 45', 'NewsWave LK English - 46', 'NewsWave LK English - 47']

elif group_choice == "SN":
    group_names = ['NewsWave Sinhala SuperGrp', 'NewsWave LK - 01', 'NewsWave LK - 02', 'NewsWave LK - 06', 'NewsWave LK - 21',
                'NewsWaveLK - 25', 'NewsWave LK - 31', 'NewsWave LK - 35', 'NewsWave LK - 39', 'NewsWave LK - 40', 'NewsWave LK - 43']


# Message to send
message_1 = "*අපි තාම තීරණය කරලා නෑ* - https://newswave.lk/63364/"
message_2 = "*රේගුවේ වාහන පෙන්වා ජනපති ආරක්ෂක අංශයේ හිටපු කොස්තාපල් ගහපු ගේම* - https://newswave.lk/63349/"
message_3 = "*ලෝකෙත් නැති ව්‍යාපාර පෙන්වා මුදල් ගරමින් සිටි නයිජීරියානුවා මෙරට පෙම්වතිය සමඟ කොටු* - https://newswave.lk/63348/"
message_4 = "*උසස් පෙළ කෘෂි විද්‍යා ප්‍රශ්න පත්‍රයේ ප්‍රශ්න පිටකල ගුරා රක්ෂිතයට - ප්‍රශ්න පිටවුණු අයුරු තාමත් ප්‍රශ්නයක්* - https://newswave.lk/63345/"
message_5 = "*සිසුවියන් දෙදෙනෙක් සහ සිසුවෙක් කළු ගං පතුලේ සැඟවෙති* - https://newswave.lk/63344/"

messages = [message_1, message_2, message_3, message_4, message_5]

# Replace with the path to your Chrome profile
chrome_profile_path = 'C:/Users/malit/AppData/Local/Google/Chrome/User Data/Default'

# Set Chrome options to use the existing profile
options = Options()
options.add_argument(f'user-data-dir={chrome_profile_path}')

# Initialize WebDriver with the specified profile
driver = webdriver.Chrome(options=options)

# Open WhatsApp Web
driver.get('https://web.whatsapp.com')
wait = WebDriverWait(driver, 300)

# Function to send message to a group
def send_message_to_group(group_name, message, count):
    # Search for the group
    wait.until(EC.presence_of_element_located((By.XPATH, '//div[@contenteditable="true"][@data-tab="3"]')))
    search_box = driver.find_element(By.XPATH, '//div[@contenteditable="true"][@data-tab="3"]')
    search_box.clear()
    search_box.click()
    search_box.send_keys(group_name)
    time.sleep(2)  # Time for search results to appear
    search_box.send_keys(Keys.ENTER)

    # Enter the message
    wait.until(EC.presence_of_element_located((By.CLASS_NAME, '_3Uu1_')))
    message_box = driver.find_element(By.CLASS_NAME, '_3Uu1_')
    message_box.send_keys(message)
    if count == 0 or count == 1:
        time.sleep(15)
        message_box.send_keys(Keys.ENTER)
    else:
        time.sleep(3)
        message_box.send_keys(Keys.ENTER)

# Iterate over each group and send the message
count = 0

for group in group_names:
        for message in messages:
            send_message_to_group(group, message, count)
            time.sleep(1)
        count += 1
        time.sleep(2)

# while True:
#     count = 0
#     heading = input("Enter Heading: ")
#     link = input("Enter Link: ")

#     message_1 = "*"+heading+"* - "+link

#     messages = [message_1]

#     for group in group_names:
#         for message in messages:
#             send_message_to_group(group, message, count)
#             time.sleep(1)
#         count += 1
#         time.sleep(2)

time.sleep(10)
driver.quit()