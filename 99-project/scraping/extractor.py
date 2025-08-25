from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from urllib.parse import urlparse

from utils import normalize_email
import time
import re
def get_start_date(driver, wait): 
    Start_Date = ""
    #Get begin date
    try:
        start_date_elem = wait.until(
            EC.presence_of_element_located((By.ID, "detail-kopfbereich-eintrittsdatum-mit-datum"))
        )
        print("Found date! ")
        print("Text:", start_date_elem.text)
        Start_Date = start_date_elem.text
    except:
        print("Không tìm thấy date_element ")
    
    return Start_Date
def get_application_link(driver, wait):
    Application_link = ""
    try:
        application_link_elem = wait.until(
            EC.presence_of_element_located((By.ID, "detail-bewerbung-url"))
        )
        ActionChains(driver).move_to_element(application_link_elem).perform()
        print("Found application link! ")
        print("Text:", application_link_elem.get_attribute("href"))
        Application_link = application_link_elem.get_attribute("href")
    except:
        print("Không tìm thấy application_link_element ")

    return Application_link

def get_reference_number(driver, wait):
    Ref_No = ""
    try:
        Ref_No_element = wait.until(
            EC.presence_of_element_located((By.ID, "detail-footer-referenznummer"))
        )
        print("Found Ref_No element")
        print("Text:", Ref_No_element.text)
        Ref_No = Ref_No_element.text
    except:
        print("Không tìm thấy Ref_No_element ")
    return Ref_No

def get_location(driver, wait):
    Location = ""
    try:
        Location_element = wait.until(
            EC.presence_of_element_located((By.ID, "detail-arbeitsorte-arbeitsort-0"))
        )
        print("Found Location element")
        print("Text:", Location_element.text)
        Location = Location_element.text
    except:
        print("Không tìm thấy Location_element ")
    return Location

def get_profession(driver, wait): 
    Profession = ""
    try:
        Profession_element = wait.until(
            EC.presence_of_element_located((By.ID, "detail-kopfbereich-ausbildungsberuf"))
        )
        print("Found Profesion element")
        print("Text:", Profession_element.text)
        Profession = Profession_element.text
    except:
        print("Không tìm thấy Profesion_element ")
    return Profession

def get_job_description(driver, wait):
    Job_description = ""
    try:
        Description_element = wait.until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="detail-beschreibung-beschreibung"]'))
        )
        print("Found Description element")
        Job_description = Description_element.text
    except:
        print("Không tìm thấy Description_element ")
    return Job_description
def get_external_link(driver, wait):
    External_link = ""
    try:
        External_link_element = wait.until(
            EC.presence_of_element_located((By.ID, "detail-beschreibung-externe-url-btn"))
        )
        print("Found External_link element")
        print("Text:", External_link_element.get_attribute("href"))
        External_link = External_link_element.get_attribute("href")
    except:
        print("Không tìm thấy External_link button")
        try:
            Homepage_link_element = wait.until(
                EC.presence_of_element_located((By.ID, "detail-agdarstellung-link-0"))
            )
            print("Found Homepage element")
            print("Text:", Homepage_link_element.get_attribute("href"))
            External_link = Homepage_link_element.get_attribute("href")
        except:
            print("Không tìm thấy Homepage_link")
    return External_link

def get_company_name(driver, wait):
    Company_Name = ""
    try:
        Company_Name_element = wait.until(
            EC.presence_of_element_located((By.ID, "detail-kopfbereich-firma"))
        )
        print("Found Description element")
        Company_Name = Company_Name_element.text
    except:
        print("Không tìm thấy Company_Name_element ")
    return Company_Name

def get_contact_details(driver, wait): 
    # Get Telephone and Email
    email_pattern = r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}"
    phone_pattern = r"(?:\+49|0049|49)[ -]?(?:\(?0?\d{2,5}\)?)[ -]?\d{3,}"
    Telephone = []
    Email = []
    contact_detail = ""
    try:
        addiontal_element = wait.until(
            EC.presence_of_element_located((By.CLASS_NAME, "angebotskontakt-bewerbungsdetails-wrapper"))
        )
        print("Found contact_detail element")
        contact_detail = addiontal_element.text
        #contact_detail_lines = contact_detail.split("\n")
        Email = re.findall(email_pattern, contact_detail.strip())
        print("Email:", Email)
        Telephone = re.findall(phone_pattern, contact_detail.strip())
        print("Telephone:", Telephone)
    except: 
        print("Không tìm thấy contact_detail element")
    
    return Email,Telephone

def search_for_email(driver, wait, Application_link,External_link):
    Email = []
    if Application_link:
        driver.get(Application_link)
        time.sleep(3)  # chờ load trang
        app_page = driver.page_source
        Email = normalize_email(app_page)
        if Email:
            print("Tìm thấy Email trong Application_link:", Email)
        else:
            print("Không tìm thấy Email trong Appilication_link")
        if not Email:
            contact_pattern = ["contact", "kontakt", "imprint", "impressum"]
            for contact in contact_pattern:
                try:
                    el = driver.find_element(f"xpath", f"//*[text()='{contact}']")
                    driver.get(el.get_attribute("href"))
                    time.sleep(2)
                    page_src = driver.page_source
                    Email = normalize_email(page_src)
                    link = el.get_attribute("href")
                    if Email:
                        print(f"Tìm thấy Email bằng contact_element {link}: {Email}")
                        return Email
                    else: 
                        print(f"Không tìm thấy Email bằng contact_element_link {link}")

                except Exception as e:
                    print(f"Lỗi khi tìm contact_element {contact}: Thử tìm email với suffix {contact}")

                try:       
                    parsed = urlparse(External_link)
                    domain = f"{parsed.scheme}://{parsed.netloc}" + "/" + contact
                    driver(domain)
                    time.sleep(2)
                    page_src = driver.page_source
                    Email = normalize_email(page_src)
                    if Email:
                        print(f"Tìm thấy Email bằng suffix trong {link}: {Email}")
                        return Email
                    else: 
                        print(f"Không tìm thấy Email bằng suffix trong {link}")
                except: 
                    print(f"Lỗi khi tìm Email bằng suffix trong  {domain}")


    if not Email and External_link:
        print("Không tìm thấy email trong Application_link. Thử tìm ở External_link...")
        try:
            # Trước tiên thử chính External_link
            driver.get(External_link)
            time.sleep(3)
            ext_page = driver.page_source
            Email = normalize_email(ext_page)
            if Email:
                print("Tìm thấy Email trong External_link:", Email)

            # Nếu vẫn không có, thử thêm các suffix phổ biến
            if not Email:
                contact_pattern = ["contact", "kontakt", "imprint", "impressum"]
                for contact in contact_pattern:
                    try:
                        el = driver.find_element(f"xpath", f"//*[text()='{contact}']")
                        driver.get(el.get_attribute("href"))
                        time.sleep(2)
                        page_src = driver.page_source
                        Email = normalize_email(page_src)
                        link = el.get_attribute("href")
                        if Email:
                            print(f"Tìm thấy Email thông qua contact_element trong {link}: {Email}")
                            break
                        else:
                            print(f"Không thấy Email thông qua contact_element trong {link}" )
                    except Exception as e:
                        print(f"Lỗi khi tìm contact_element với {contact}:", e)

                    try:       
                        parsed = urlparse(External_link)
                        domain = f"{parsed.scheme}://{parsed.netloc}" + "/" + contact
                        driver(domain)
                        time.sleep(2)
                        page_src = driver.page_source
                        Email = normalize_email(page_src)
                        if Email:
                            print(f"Tìm thấy Email trong {link}: {Email}")
                            return Email
                        else: 
                            print(f"Không tìm thấy Email trong {link}") 
                    except: 
                        print(f"Lỗi khi tìm Email bằng suffix trong {domain}")

        except Exception as e:
            print("Lỗi khi truy cập External_link:", e)
    return Email

def get_salarylist(driver, wait, job_items):
    Salary_list = []
    for i, item in enumerate(job_items):
        try:
            salary_element = wait.until(
                    EC.presence_of_element_located((By.ID, f"eintrag-{i}-ausbildungsverguetung"))
            )
            print("Salary:", salary_element.text)
            Salary_list.append(salary_element.text)
        except:
            print("No salary for job", i+1)
            Salary_list.append("")
    return Salary_list



