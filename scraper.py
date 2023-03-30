import requests
from bs4 import BeautifulSoup
from googleapiclient.discovery import build
from google.oauth2 import service_account
import time
import lxml
import re


SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]
SERVICE_ACCOUNT_FILE = 'ReadSheet/keys.json'

creds = None
creds = service_account.Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE, scopes=SCOPES)


SAMPLE_SPREADSHEET_ID = '1ooD0it1sR5UIArNTFSoDgFzcARthXZqT5ZC0qqQoVf4'
service = build('sheets', 'v4', credentials=creds)

# Call the Sheets API
sheet = service.spreadsheets()
j_dict = dict()
job_dict = j_dict.copy()
url = 'https://academicpositions.harvard.edu/postings/search'
home_url = 'https://academicpositions.harvard.edu'
new_url = 'https://academicpositions.harvard.edu/postings/search'
requests_session = requests.Session()
API_KEY = '63afa3012c69707ef49c9033'
headers = {
  'Cookie': 'incap_ses_1469_2811896=UgQrGRVM5A6pjhgZF/BiFEnQs2MAAAAAzBvDIdQXGrmmNNC7iEOXnQ==; nlbi_2811896=71zVZUopl1JqGotFqEaqIwAAAACEBB7y/9tihVYsesba9idT; visid_incap_2811896=JA28wsntRJeKGhMyhFxuFEjQs2MAAAAAQUIPAAAAAACty+L27mIBMY46qJUczs86; AWSALB=8vMYtnW6FkkTKfUKea5EayEKTIkhhq34z+OXsidEiulFm5JWx46VwMG+/wWwIvVJxp5o85+QkmDDaKIZ43lSsfvw087PbyJcokf3Pz07K5qFXdc5WW5Sz7jagYUy; AWSALBCORS=8vMYtnW6FkkTKfUKea5EayEKTIkhhq34z+OXsidEiulFm5JWx46VwMG+/wWwIvVJxp5o85+QkmDDaKIZ43lSsfvw087PbyJcokf3Pz07K5qFXdc5WW5Sz7jagYUy; _hr_suite_session_1=OWI3dGg0Q2xwK2VOMmo5dm0zTjFqZFI4U3UvNVFrV0Z5SnF0NFdGVjhZeUd2TzdzMEYvRTR2bk4vM1NEWlNGNE1NTE1TaUFReFRuMWQ5ZGtaN2pCdEQxaGxkVGlFbVVHS054bEpLRllQSVBPTGdoTmF2MTNsNmZPSzluU2Z6YXprU3JKR2FnZFdrditzRUo1aWRoYUw2NlYzMzhTdVNwMzN4clRkSHFONVJlbUFCRWRVelBJUXBkZ0dSQjh3QldJLS0xYVpMMU9DaUo1eGVZVGgxcEwrRmxBPT0%3D--9d3cd064acebe2e5af9c00fede277b9e7e2f0308'
}
tag_list = []
def make_requests(url):
    # Make a request to the website
    # response = requests_session.get(url)
    response = requests_session.get(url, headers=headers)
    # Parse the HTML content
    soup = BeautifulSoup(response.text, 'lxml')
    return soup

def crawl_next(url):
    next_btn = make_requests(url).find(class_='next_page').get("href")
    if next_btn == None:
        return False
    return True



def crawl_page(url):
    all_anchor_tags = make_requests(url).find_all(name='a', class_='btn primary_button_color')
    index = len(job_dict) + 1
    for tag in all_anchor_tags:
        id = tag.get("href")
        if re.search('postings\/[0-9]', tag.get("href")):
            id = id.strip('/postings/')
            job_dict[index] = {}
            job_dict[index]["id"] = id
            a = home_url + '/postings/' + job_dict[index]["id"]
            tag_list.append(a)
            index+=1
            
def crawl():
    for url in range(len(tag_list)):
        res =  make_requests(tag_list[url])
        data = res.find_all('td')
        myKeys = ["Title", "School", "Department", "Description", "Qualifications", 
        "Additional Qualifications", "Special Instructions", "Contact Information", 
        "Contact Email", "Equal Opportunity", "Minimum References","Maximum References", "Keywords"]
        myValues = []
        
        for i in data:
            myValues.append(i.text)
        print(f"######Job {url+1} has been added into the database#####")
        job_dict[url+1].update(zip(myKeys, myValues))
        


# def crawl_page(url):
#     all_anchor_tags = make_requests(url).find_all(name='a', class_='btn primary_button_color')

#     index = len(job_dict) + 1
#     for tag in all_anchor_tags:
#         id = tag.get("href")
#         if re.search('postings\/[0-9]', tag.get("href")):
#             id = id.strip('/postings/')
#             job_dict[index] = {}
#             job_dict[index]["id"] = id
#             a = home_url + '/postings/' + job_dict[index]["id"]

#             res = requests_session.get(a, headers=headers, verify=False)
#             # Parse the HTML content
#             s = BeautifulSoup(res.text, 'lxml')
#             data = s.find_all('td')

#             myKeys = ["Title", "School", "Department", "Description", "Qualifications", 
#             "Additional Qualifications", "Special Instructions", "Contact Information", 
#             "Contact Email", "Equal Opportunity", "Minimum References","Maximum References", "Keywords"]
#             myValues = []
            
#             for i in data:
#                 myValues.append(i.text)

#             job_dict[index].update(zip(myKeys, myValues))
#             index+=1
    


def write_data():
    data = [[] for _ in range(len(job_dict))]
    count = 1

    for index in range(len(job_dict)):
        for value in job_dict[count].values():
            data[index].append(value)
        count+=1

    # dict_size = len(job_dict) + 1
    # request = sheet.values().update(spreadsheetId=SAMPLE_SPREADSHEET_ID, 
    #                                         range=f"Sheet1!A2", valueInputOption="USER_ENTERED", 
    #                                         body={"values":data})
    # request.execute()
    print("Data has been added into the sheet!")

isTrue = True
if __name__ == "__main__":
    start_time = time.time()
    while isTrue:
        crawl_page(new_url)

        if crawl_next(new_url):
            new_url = home_url + make_requests(new_url).find(class_='next_page').get("href")
            print("##########Crawling Next Page##########", new_url[-1])
        else:
            isTrue = False
            print("########Crawling Webpages###########")
            crawl()
            write_data()

    print("Process finished --- %s seconds ---" % (time.time() - start_time))
