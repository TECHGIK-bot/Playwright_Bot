# import playwirght library touse....In this case we use sync_playwright 
from playwright.sync_api import sync_playwright
import time
import requests

# Replace with your bot token and chat ID
BOT_TOKEN = "7057194211:AAF_StFo_FwRn1AR_XOJQurXuYgh5ZvO2b4"
CHAT_ID = "6260151149"

def send_telegram_message(message):
    """Sends a message to your Telegram bot."""
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    data = {"chat_id": CHAT_ID, "text": message}
    
    try:
        response = requests.post(url, data=data)
        if response.status_code == 200:
            print("Telegram notification sent successfully!")
        else:
            print(f"Failed to send message: {response.text}")
    except Exception as e:
        print(f"Error sending Telegram message: {e}")

# A function that gets the hot numbers from the webpage and puts them in a list
def Hot_Numbers(Web_page):
   Hot_Numbers = Web_page.locator("xpath=//html/body/div[1]/div/div/div/main/div[1]/div[2]/div[2]/div[1]")
   First_Hot_Ball = Hot_Numbers.locator("xpath =.//div[1]/span").inner_text()
   Second_Hot_Ball = Hot_Numbers.locator("xpath =.//div[2]/span").inner_text()
   Third_Hot_Ball = Hot_Numbers.locator("xpath =.//div[3]/span").inner_text()
   
   # Convert strings to integers
   try:
      Balls = [int(First_Hot_Ball), int(Second_Hot_Ball), int(Third_Hot_Ball)]
      print(f'The Hot Balls are: {Balls}')
   except ValueError:
      print("One or more hot balls are not valid integers")
      Balls = []

   return Balls
   

def Container(Web_page):
   Ball_numbers = []
   for i in range(1, 7):   
      container_xpath = f'/html/body/div[1]/div/div/div/footer/div[2]/div[1]/div/div[1]/div[{i}]/div/div'
      container_numbers = Web_page.locator(f"xpath= {container_xpath}")
      Numbers = container_numbers.inner_text()

      # Convert to integer before appending
      try:
         Ball_numbers.append(int(Numbers))
         print(f"Container {i}, Ball-Number is: {int(Numbers)}")
         
      except ValueError:
         print(f"Container {i}, Ball-Number is not a valid integer: {Numbers}")

   return Ball_numbers

def checker(Web_page):
    failure_count = 0
    max_failure_count = 0
    waiting_for_container = True

    while True:
         try:
            if waiting_for_container:
                # Call the Hot_Numbers function
                Balls = Hot_Numbers(Web_page)
                print("Hot numbers updated.")
                waiting_for_container = False  # Now wait for the timer to reach 40
            else:
                # Wait for the timer element to be present
                Timer = Web_page.wait_for_selector("xpath=/html/body/div[1]/div/div/div/footer/div[2]/div[4]/div/div/div", timeout=5000)
                
                # Get the timer value
                Time = Timer.inner_text().strip()
                
                # Check if the timer equals 40
                if Time.isdigit() and int(Time) == 40:
                    print(f"Timer matched 40. Current time: {Time}")
                    
                    # Call the Container function
                    Ball_numbers = Container(Web_page)
                    print(f'The Hot Balls are: {Balls}')
                    
                    # Check if any of the hot numbers are in the container numbers
                    if any(ball in Ball_numbers for ball in Balls):
                        failure_count += 1  # Increment failure count when a match is found
                        print(f"Match found! Failure count incremented to {failure_count}")
                        
                        if failure_count >= 2:
                            message = (
                                f"The bot has failed {failure_count} times.\n"
                                f"Play {Balls} as ball zero in the next round.\n"
                                f"The highest failure count so far is {max_failure_count}."
                            )
                            send_telegram_message(message)
                    else:
                        failure_count = 0  # Reset failure count when no match is found
                        print(f"No match found. Failure count reset to {failure_count}")
                    
                    # Update the maximum failure count if the current one exceeds it
                    if failure_count > max_failure_count:
                        max_failure_count = failure_count
                        print(f"New highest failure count: {max_failure_count}")
                    
                    # Wait 10 seconds and prepare to call Hot_Numbers again
                    time.sleep(10)
                    waiting_for_container = True  # Switch back to update Hot_Numbers
         except Exception as e:
            print(f'an error occured: {e}')
        


#To create a function that opens the 49ja website
def Open_49ja():
   with sync_playwright() as p:

      url = 'https://logigames.bet9ja.com/Games/Launcher?gameId=11000&provider=0&pff=1&skin=201'
      # So firstly we create our browser
      chrome = p.chromium.launch(headless = False, executable_path=r'C:\Program Files\Google\Chrome\Application\chrome.exe')
      # Next we Open a new page to input our url
      Web_page  = chrome.new_page()
      # Next we tell the webpage to go to our url
      Web_page.goto(url)

      checker(Web_page)
      

Open_49ja()   