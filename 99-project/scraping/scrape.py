from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from time import sleep
from selenium.webdriver.common.by import By
import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver import ActionChains
import random
import pandas as pd
from extractor import get_salarylist, search_for_email,get_application_link, get_company_name, get_contact_details, get_external_link, get_job_description,get_location, get_profession, get_reference_number, get_start_date
import undetected_chromedriver as uc

def get_detailed_by_sections(driver, wait, link):
    driver.get(link)
    for _ in range(2):
        if "This site can’t be reached" in driver.page_source:
            print("Trang lỗi: This site can’t be reached")
            time.sleep(3)
            driver.get(link)

        else: 
            #Input captcha for the first time
            try:
                input_box = driver.find_element(By.CSS_SELECTOR, "input[id='kontaktdaten-captcha-input']")
                ActionChains(driver).move_to_element(input_box).perform()
                print("Đã tìm thấy captcha!, vui long nhap captchat: ")
                captcha_text = input()
                input_box.send_keys(captcha_text.strip())  
                submit_btn = driver.find_element(By.XPATH, "//button[contains(., 'Absenden')]")
                submit_btn.click()

            except: 
                print("Không tìm thấy captcha_element, hoặc đang có session")

            Start_Date = get_start_date(driver, wait)
            Application_link = get_application_link(driver, wait)
            Ref_No = get_reference_number(driver, wait)
            Location = get_location(driver, wait)
            Profession = get_profession(driver, wait)
            Job_description = get_job_description(driver, wait)
            External_link = get_external_link(driver, wait)
            Company_Name = get_company_name(driver, wait)
            Email, Telephone = get_contact_details(driver, wait)

            # Handle Missing Email ->
            # Nếu Email rỗng thì fallback sang Application_link hoặc External_link
            if len(Email) == 0:
                print("Không tìm thấy email trong contact_detail. Thử tìm ở Application_link...")
    
            # --- Kiểm tra Application_link ---
            Email = search_for_email(driver, wait, Application_link, External_link)
            return  Profession,Company_Name,Location,Start_Date, Telephone, Email,Job_description,Ref_No,External_link,Application_link

            



def crawler():  

    options = uc.ChromeOptions()
    # Giả lập user-agent của Chrome thật
    options.add_argument(
        "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/127.0.0.0 Safari/537.36"
    )

    # Một số flag để giảm khả năng bị detect
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument("--disable-dev-shm-usage")

    # Khởi tạo driver stealth
    driver = uc.Chrome(options=options)

    url = "https://www.arbeitsagentur.de/jobsuche/suche?angebotsart=4&ausbildungsart=0&arbeitszeit=vz&branche=22;1;2;9;3;5;7;10;11;16;12;21;26;15;17;19;20;8;23;29&veroeffentlichtseit=7&sort=veroeffdatum"
    driver.get(url)

    wait = WebDriverWait(driver, timeout=3)

    for _ in range(3): 
        try:
            cookie_btn = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(., 'Alle Cookies akzeptieren')]")))
            cookie_btn.click()
            print("Cookies accepted")
            break
        except Exception as e:
            print(f"Button not ready, retrying... Error: {type(e).__name__} - {e}")
            driver.refresh()

            
    click_nb = 0
    # click for exanding button 
    while True:  
        if (click_nb > 0): break
        try:
            cookie_btn = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(., ' Weitere Ergebnisse ')]")))
            ActionChains(driver).move_to_element(cookie_btn).perform()
            cookie_btn.click()
            time.sleep(2)
            print("Weitere Ergebnisse accepted")
            click_nb += 1
        except:
            print("No Weitere Ergebnisse button found (maybe already accepted)")
            break
    
    #Get items links
    job_items = wait.until(
    EC.presence_of_all_elements_located((By.XPATH, "//*[contains(@id,'ergebnisliste-item-')]"))
    )

    job_links = [item.get_attribute("href") for item in job_items]

    #Get salary
    Salary_list = []
    Salary_list= get_salarylist(driver, wait,job_items)
    
    print(Salary_list)
    print(len(Salary_list))
    Profession_list = []
    Company_Name_list = []
    Location_list = []
    Start_Date_list = []
    Telephone_list = []
    Email_list = []
    Job_description_list = []
    Ref_No_list = []
    External_link_list = []
    Application_link_list = []
    for job_link in job_links:        
        Profession, Company_Name, Location, Start_Date, Telephone, Email, Job_description, Ref_No, External_link, Application_link = get_detailed_by_sections(driver, wait, job_link)
        Profession_list.append(Profession)
        Company_Name_list.append(Company_Name)
        Location_list.append(Location)
        Start_Date_list.append(Start_Date)
        Telephone_list.append(Telephone)
        Email_list.append(Email)
        Job_description_list.append(Job_description)
        Ref_No_list.append(Ref_No)
        External_link_list.append(External_link)
        Application_link_list.append(Application_link)
        time.sleep(random.uniform(1, 1.2))

    lists = {
        "Profession_list": Profession_list,
        "Company_Name_list": Company_Name_list,
        "Location_list": Location_list,
        "Start_Date_list": Start_Date_list,
        "Telephone_list": Telephone_list,
        "Email_list": Email_list,
        "Job_description_list": Job_description_list,
        "Ref_No_list": Ref_No_list,
        "External_link_list": External_link_list,
        "Application_link_list": Application_link_list,
        "Salary_list": Salary_list,
    }

    for name, lst in lists.items():
        print(f"{name}: {len(lst)}")
    # Gom dữ liệu vào dict
    data = {
        "Profession": Profession_list,
        "Salary": Salary_list,
        "Company Name": Company_Name_list,
        "Location": Location_list,
        "Start Date": Start_Date_list,
        "Telephone": Telephone_list,
        "Email": Email_list,
        "Job Description": Job_description_list,
        "Ref.-Nr.": Ref_No_list,
        "External Link": External_link_list,
        "Application Link": Application_link_list
    }

    # Tạo DataFrame
    df = pd.DataFrame(data)

    # Xuất ra CSV
    df.to_csv("jobs_data_1.csv", index=False, sep="|", encoding="utf-8-sig")
    driver.quit()

crawler()