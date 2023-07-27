from googleapiclient.discovery import build
from google.oauth2 import service_account



NAME = "Sulemaan Farooq"
EMAIL = "shf46@rutgers.edu"
PHONE = "(917) 4565697"
CITY = "Edison"
STATE = "NJ"
LINK = "sulemaanfarooq.com"
UNIVERSITY = "Rutgers University - New Brunswick"
DEGREE_TYPE = "Science"
UNIVERSITY_START_DATE = "Jan 2021"
UNIVERSITY_END_DATE = "May 2024"
MAJOR = "Computer Science"
MINOR = "Data Science"
GPA = "4.0"
EXPERIENCE1 = "Verizon"
EXPERIENCE1_START_DATE = "Aug 2023"
EXPERIENCE1_END_DATE = "Dec 2023"
TITLE1 = "Data Engineer Intern"
EXPERIENCE1_LOCATION = "Bedminster, NJ"
EXPERIENCE1_BULLET1 = "Software development and data science for 5G activation pipeline"
EXPERIENCE1_BULLET2 = "Predicted fire possibility is cell towers using cocktail unsupervised machine learning algorithm leading to 95% more safety"
EXPERIENCE1_BULLET3 = "empty"
EXPERIENCE2 = "Ford Motor"
EXPERIENCE2_START_DATE = "May 2023"
EXPERIENCE2_END_DATE = "Aug 2023"
TITLE2 = "Software Engineer Intern"
EXPERIENCE2_LOCATION = "Dearborn, MI"
EXPERIENCE2_BULLET1 = "Engineered Java spring boot API’s to get and save Ford dealership credit data leading to 90% effective Ford decisions"
EXPERIENCE2_BULLET2 = "Aided in Ford app deployment on Google cloud platform with Tekton pipeline and terraform reducing cyber attacks by 80%"
EXPERIENCE2_BULLET3 = "Utilized agile test-driven development, unit testing, and pair programming leading to 95% more efficient code"
EXPERIENCE3 = "AlphaROC"
EXPERIENCE3_START_DATE = "May 2022"
EXPERIENCE3_END_DATE = "Aug 2022"
TITLE3 = "Software Engineer Intern"
EXPERIENCE3_LOCATION = "Summit, NJ"
EXPERIENCE3_BULLET1 = "Lead a team in the development of AlphaROC website https://alpharoc.ai/ using agile methodologies allowing customers to view the firm's data science services leading to a 100% increase in website leads and sales"
EXPERIENCE3_BULLET2 = "Connected MySQL to Amazon S3 with a Python script. Coached by a senior developer on Amazon S3 permissions"
EXPERIENCE3_BULLET3 = "Engineered a data science model that predicts 8000 emails in 5 minutes with 95% accuracy in the CRM of 50,000 rows which boosted Hubspot email marketing campaign efficiency by 120%"
EXPERIENCE4 = "Answering Service Care"
EXPERIENCE4_START_DATE = "Sep 2022"
EXPERIENCE4_END_DATE = "Dec 2022"
TITLE4 = "Software Engineer Intern"
EXPERIENCE4_LOCATION = "Margate, FL"
EXPERIENCE4_BULLET1 = "Directed a team of five interns to fix a bug that determines if a credit card is Amex, Visa or Master based on the number of digits, leading to 100% more successful PayPal payments"
EXPERIENCE4_BULLET2 = "Spearheaded a software model that predicts the reasons for abrupt spikes in CPU utilization of containers and virtual machines within clusters, reducing cloud computing costs by 25%"
EXPERIENCE4_BULLET3 = "Accelerated DevOps with Datadog monitors that send alerts to the team slack channel if Amazon EC2 hosts count exceeds 12, and if cluster CPU utilization exceeds 70%, saving $4000 per month"
EXPERIENCE5 = "Contracting"
EXPERIENCE5_START_DATE = "Aug 2022"
EXPERIENCE5_END_DATE = "Dec 2022"
TITLE5 = "web app contracting"
EXPERIENCE5_LOCATION = "Edison, NJ"
EXPERIENCE5_BULLET1 = "Architected a Django full-stack web app with PayPal integration that finds personality type from a survey of 60 questions"
EXPERIENCE5_BULLET2 = "Incorporated Python PDF libraries such as PyMuPdf to construct custom free and paid personality reports"
EXPERIENCE5_BULLET3 = "Revamped the web app from AWS to PythonAnywhere resulting in the client saving $22 per month in cloud hosting costs"
PROJECT1 = "Machine learning - Handwritten digits"
PROJECT1_BULLET1 = "Unsupervised k-means clustering to convert 100000 handwritten numbers to text digits with 0.1 error"
PROJECT1_BULLET2 = "Algorithmized k-means with: random centers; k-means plus centers; and matrix forms with loss function for evaluation"
PROJECT2 = "Algorithmic Trading Bot"
PROJECT2_BULLET1 = "Launched Flask trading web app using IEX API and SQL backend that saves traders hundreds of hours per week"
PROJECT2_BULLET2 = "empty"
PROJECT3 = "Image Regeneration"
PROJECT3_BULLET1 = "Pioneered low-level C program that recovers JPEGs from corrupted memory cards preventing data loss"
PROJECT3_BULLET2 = "empty"
PROJECT4 = "Computer Vision Filter Algorithms"
PROJECT4_BULLET1 = "Designed Greyscale, Sepia, Reflection, and Blur algorithms in C which are 45 times faster than Python library OpenCV"
PROJECT4_BULLET2 = "empty"
PROJECT5 = "Audio signal amplification"
PROJECT5_BULLET1 = "Amplified an audio file based on user input in C in less than 5 seconds saving 55% time compared to Python"
PROJECT5_BULLET2 = "empty"
LANGUAGES = "R, Java, Python, C, HTML, CSS, JavaScript, React, Ruby"
TECHNOLOGIES = "Linux, Git, MySQL, SQLite, NoSQL, AWS, Django, Flask, Spring Boot, PythonAnywhere, Heroku, GCP"
LEADERSHIP = "Rutgers orientation leader, Data Science E-board"



def create_resume():
        # Dictionary to store the placeholder replacements
    placeholder_replacements = {
                'name': NAME,
                'email': EMAIL,
                'phone': PHONE,
                'city': CITY,
                'state': STATE,
                'link': LINK,
                'university': UNIVERSITY,
                'Science/Art': DEGREE_TYPE,
                'university start date': UNIVERSITY_START_DATE,
                'university end date': UNIVERSITY_END_DATE,
                'Major': MAJOR,
                'Minor': MINOR,
                'GPA': GPA,
                'experience1': EXPERIENCE1,
                'experience1 start date': EXPERIENCE1_START_DATE,
                'experience1 end date': EXPERIENCE1_END_DATE,
                'title 1': TITLE1,
                'experience1 location': EXPERIENCE1_LOCATION,
                'experience1 bullet1': EXPERIENCE1_BULLET1,
                'experience1 bullet2': EXPERIENCE1_BULLET2,
                'experience1 bullet3': EXPERIENCE1_BULLET3,
                'experience2': EXPERIENCE2,
                'experience2 start date': EXPERIENCE2_START_DATE,
                'experience2 end date': EXPERIENCE2_END_DATE,
                'title 2': TITLE2,
                'experience2 location': EXPERIENCE2_LOCATION,
                'experience2 bullet1': EXPERIENCE2_BULLET1,
                'experience2 bullet2': EXPERIENCE2_BULLET2,
                'experience2 bullet3': EXPERIENCE2_BULLET3,
                'experience3': EXPERIENCE3,
                'experience3 start date': EXPERIENCE3_START_DATE,
                'experience3 end date': EXPERIENCE3_END_DATE,
                'title 3': TITLE3,
                'experience3 location': EXPERIENCE3_LOCATION,
                'experience3 bullet1': EXPERIENCE3_BULLET1,
                'experience3 bullet2': EXPERIENCE3_BULLET2,
                'experience3 bullet3': EXPERIENCE3_BULLET3,
                'experience4': EXPERIENCE4,
                'experience4 start date': EXPERIENCE4_START_DATE,
                'experience4 end date': EXPERIENCE4_END_DATE,
                'title 4': TITLE4,
                'experience4 location': EXPERIENCE4_LOCATION,
                'experience4 bullet1': EXPERIENCE4_BULLET1,
                'experience4 bullet2': EXPERIENCE4_BULLET2,
                'experience4 bullet3': EXPERIENCE4_BULLET3,
                'experience5': EXPERIENCE5,
                'experience5 start date': EXPERIENCE5_START_DATE,
                'experience5 end date': EXPERIENCE5_END_DATE,
                'title 5': TITLE5,
                'experience5 location': EXPERIENCE5_LOCATION,
                'experience5 bullet1': EXPERIENCE5_BULLET1,
                'experience5 bullet2': EXPERIENCE5_BULLET2,
                'experience5 bullet3': EXPERIENCE5_BULLET3,
                'project1': PROJECT1,
                'project1 bullet1': PROJECT1_BULLET1,
                'project1 bullet2': PROJECT1_BULLET2,
                'project2': PROJECT2,
                'project2 bullet1': PROJECT2_BULLET1,
                'project2 bullet2': PROJECT2_BULLET2,
                'project3': PROJECT3,
                'project3 bullet1': PROJECT3_BULLET1,
                'project3 bullet2': PROJECT3_BULLET2,
                'project4': PROJECT4,
                'project4 bullet1': PROJECT4_BULLET1,
                'project4 bullet2': PROJECT4_BULLET2,
                'project5': PROJECT5,
                'project5 bullet1': PROJECT5_BULLET1,
                'project5 bullet2': PROJECT5_BULLET2,
                'languages': LANGUAGES,
                'technologies': TECHNOLOGIES,
                'leadership': LEADERSHIP
    }


    # Path to your service account credentials JSON file
    SERVICE_ACCOUNT_FILE = '/Users/cheesenaan/Documents/projects/resume_app/project/.ipynb_checkpoints/resume_App/resume_app/resume_app/doc.json'

    # ID of the Google Doc you want to modify
    DOCUMENT_ID = '1LlDs00ayatWBgsmHzyYSk0d-yeJVbt33bC4dP34NHXk'

    # Folder ID where the copy will be placed
    FOLDER_ID = '1aGcF78a65Nus-K9kCv8P7NzMBSZjJnNY'

    # Authenticate and create the Google Drive API service
    credentials = service_account.Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=['https://www.googleapis.com/auth/documents', 'https://www.googleapis.com/auth/drive'])
    service = build('drive', 'v3', credentials=credentials)

    # Create a copy of the document
    copy_metadata = {
        'name': NAME + ' - Resume',
        'parents': [FOLDER_ID]
    }
    copy_response = service.files().copy(fileId=DOCUMENT_ID, body=copy_metadata).execute()
    copy_id = copy_response['id']

    print(f"Copy created with ID: {copy_id}")

    DOCUMENT_ID = str(copy_id)


    # Authenticate and create the Google Docs API service
    credentials = service_account.Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=['https://www.googleapis.com/auth/documents'])
    service = build('docs', 'v1', credentials=credentials)




    # Get the content of the Google Doc
    doc = service.documents().get(documentId=DOCUMENT_ID).execute()

    # Process each content element and replace placeholders
    for content in doc['body']['content']:
        if 'paragraph' in content:
            elements = content['paragraph']['elements']
            for element in elements:
                if 'textRun' in element:
                    text_run = element['textRun']
                    if 'content' in text_run:
                        content_text = text_run['content']
                        for placeholder, replacement in placeholder_replacements.items():
                            if placeholder in content_text:
                                content_text = content_text.replace(placeholder, replacement)
                                text_run['content'] = content_text

    # Create the requests list for batch updating
    requests = []
    for placeholder, replacement in placeholder_replacements.items():
        requests.append({
            'replaceAllText': {
                'containsText': {
                    'text': '{{' + placeholder + '}}',
                    'matchCase': False
                },
                'replaceText': replacement
            }
        })

    # Execute the batch update requests
    result = service.documents().batchUpdate(documentId=DOCUMENT_ID, body={'requests': requests}).execute()

    print('Placeholders replaced successfully in the Google Doc')


    # Get the content of the Google Doc
    doc = service.documents().get(documentId=DOCUMENT_ID).execute()
    body_content = doc['body']['content']

    # Iterate over the paragraphs in reverse order
    for i in range(len(body_content) - 1, -1, -1):
        paragraph = body_content[i]
        if 'paragraph' in paragraph:
            elements = paragraph['paragraph']['elements']
            for element in elements:
                if 'textRun' in element:
                    content = element['textRun']['content']
                    if 'empty' in content:
                        # Remove the paragraph if it contains the string "empty"
                        requests = [
                            {
                                'deleteContentRange': {
                                    'range': {
                                        'startIndex': paragraph['startIndex'],
                                        'endIndex': paragraph['endIndex']
                                    }
                                }
                            }
                        ]
                        service.documents().batchUpdate(documentId=DOCUMENT_ID, body={'requests': requests}).execute()
                        break  # Skip to the next paragraph after deleting the current one

    print("Rows with 'empty' text removed successfully!")
    # Get the link of the Google Doc
    resume_link = f"https://docs.google.com/document/d/{DOCUMENT_ID}"
    print("Link to the Google Doc:", resume_link)


create_resume()