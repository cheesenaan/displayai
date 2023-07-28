import datetime
from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse
import gspread
from google.oauth2.service_account import Credentials
from django.shortcuts import redirect


# Global variable placeholders
NAME = None
EMAIL = None
PHONE = None
CITY = None
STATE = None
LINK = None
UNIVERSITY = None
DEGREE_TYPE = None
UNIVERSITY_START_DATE = None
UNIVERSITY_END_DATE = None
MAJOR = None
MINOR = None
GPA = None
EXPERIENCE1 = None
EXPERIENCE1_START_DATE = None
EXPERIENCE1_END_DATE = None
TITLE1 = None
EXPERIENCE1_LOCATION = None
EXPERIENCE1_BULLET1 = None
EXPERIENCE1_BULLET2 = None
EXPERIENCE1_BULLET3 = None
EXPERIENCE2 = None
EXPERIENCE2_START_DATE = None
EXPERIENCE2_END_DATE = None
TITLE2 = None
EXPERIENCE2_LOCATION = None
EXPERIENCE2_BULLET1 = None
EXPERIENCE2_BULLET2 = None
EXPERIENCE2_BULLET3 = None
EXPERIENCE3 = None
EXPERIENCE3_START_DATE = None
EXPERIENCE3_END_DATE = None
TITLE3 = None
EXPERIENCE3_LOCATION = None
EXPERIENCE3_BULLET1 = None
EXPERIENCE3_BULLET2 = None
EXPERIENCE3_BULLET3 = None
EXPERIENCE4 = None
EXPERIENCE4_START_DATE = None
EXPERIENCE4_END_DATE = None
TITLE4 = None
EXPERIENCE4_LOCATION = None
EXPERIENCE4_BULLET1 = None
EXPERIENCE4_BULLET2 = None
EXPERIENCE4_BULLET3 = None
EXPERIENCE5 = None
EXPERIENCE5_START_DATE = None
EXPERIENCE5_END_DATE = None
TITLE5 = None
EXPERIENCE5_LOCATION = None
EXPERIENCE5_BULLET1 = None
EXPERIENCE5_BULLET2 = None
EXPERIENCE5_BULLET3 = None
PROJECT1 = None
PROJECT1_BULLET1 = None
PROJECT1_BULLET2 = None
PROJECT2 = None
PROJECT2_BULLET1 = None
PROJECT2_BULLET2 = None
PROJECT3 = None
PROJECT3_BULLET1 = None
PROJECT3_BULLET2 = None
PROJECT4 = None
PROJECT4_BULLET1 = None
PROJECT4_BULLET2 = None
PROJECT5 = None
PROJECT5_BULLET1 = None
PROJECT5_BULLET2 = None
LANGUAGES = None
TECHNOLOGIES = None
LEADERSHIP = None



def home(request):
    return render(request,'home.html')

def data(request):
    if request.method == 'POST':

        # get personal details
        first_name = request.POST.get('firstName', '')
        last_name = request.POST.get('lastName', '')
        NAME = first_name +  ' ' + last_name
        #print("this is the name ", NAME)
        PHONE = request.POST.get('phone', '')
        EMAIL = request.POST.get('email', '')
        CITY = request.POST.get('city', '')
        STATE = request.POST.get('stateCountry', '')
        LINK = request.POST.get('link', '')

        # get education details
        UNIVERSITY = request.POST.get('university', '') 
        city_edu = request.POST.get('city-education', '')
        UNIVERSITY = UNIVERSITY + ' - ' + city_edu
        DEGREE_TYPE = request.POST.get('degreeType', '')
        GPA = request.POST.get('gpa', '')
        MAJOR = request.POST.get('major', '')
        MINOR = request.POST.get('minor', '')
        UNIVERSITY_START_DATE = request.POST.get('university-start-date', '')
        UNIVERSITY_END_DATE = request.POST.get('university-end-date', '')

        #coursework = request.POST.get('coursework', '')

        # get work experience details
        work_experience_fields = ['work-description']
        count = 0
        for key in request.POST.keys():
            for field in work_experience_fields:
                if field in key:
                    count += 1
        #print("Number of work experiences:", count)
        experiences = []
        experience_count = int(request.POST.get('experience_count', count))
        for i in range(1, experience_count + 1):
            company = request.POST.get(f'company{i}', '')
            title = request.POST.get(f'title{i}', '')
            start_date = request.POST.get(f'experience{i}-start-date', '')
            end_date = request.POST.get(f'experience{i}-end-date', '')
            work_description = request.POST.get(f'work-description{i}', '')
            city = request.POST.get(f'city{i}', '')  # Retrieve the city value
            state = request.POST.get(f'state{i}', '')  # Retrieve the state value
            location = city + ', ' + state
            experience = {
                'company': company,
                'title': title,
                'start_date': start_date,
                'end_date': end_date,
                'work_description': work_description,
                'location': location,  
            }
            experiences.append(experience)

            # Set individual variables for each experience
            # locals()[f"EXPERIENCE{i}"] = experiences[i-1]['company']
            # locals()[f"EXPERIENCE{i}_START_DATE"] = experiences[i-1]['start_date']
            # locals()[f"EXPERIENCE{i}_END_DATE"] = experiences[i-1]['end_date']
            # locals()[f"TITLE{i}"] = experiences[i-1]['title']
            # locals()[f"EXPERIENCE{i}_LOCATION"] = ''  # Set the appropriate location value
            # locals()[f"EXPERIENCE{i}_BULLET1"] = experiences[i-1]['work_description']
            # locals()[f"EXPERIENCE{i}_BULLET2"] = ''
            # locals()[f"EXPERIENCE{i}_BULLET3"] = ''


        if (len(experiences)) >= 1:
            EXPERIENCE1 = experiences[0]['company']
            EXPERIENCE1_START_DATE = experiences[0]['start_date']
            EXPERIENCE1_END_DATE = experiences[0]['end_date']
            TITLE1 = experiences[0]['title']
            EXPERIENCE1_LOCATION = experiences[0]['location']
            EXPERIENCE1_BULLET1 = experiences[0]['work_description']
            EXPERIENCE1_BULLET2 = 'TBT OPENAI'
            EXPERIENCE1_BULLET3 = 'TBT OPENAI'

        if len(experiences) >= 2:
            EXPERIENCE2 = experiences[1]['company']
            EXPERIENCE2_START_DATE = experiences[1]['start_date']
            EXPERIENCE2_END_DATE = experiences[1]['end_date']
            TITLE2 = experiences[1]['title']
            EXPERIENCE2_LOCATION = experiences[1]['location']
            EXPERIENCE2_BULLET1 = experiences[1]['work_description']
            EXPERIENCE2_BULLET2 = 'TBT OPENAI'
            EXPERIENCE2_BULLET3 = 'TBT OPENAI'
        else:
            EXPERIENCE2 = ""
            EXPERIENCE2_START_DATE = ""
            EXPERIENCE2_END_DATE = ""
            TITLE2 = ""
            EXPERIENCE2_LOCATION = ""
            EXPERIENCE2_BULLET1 = ""
            EXPERIENCE2_BULLET2 = ""
            EXPERIENCE2_BULLET3 = ""

        
        if len(experiences) >= 3:
            EXPERIENCE3 = experiences[2]['company']
            EXPERIENCE3_START_DATE = experiences[2]['start_date']
            EXPERIENCE3_END_DATE = experiences[2]['end_date']
            TITLE3 = experiences[2]['title']
            EXPERIENCE3_LOCATION = experiences[2]['location']
            EXPERIENCE3_BULLET1 = experiences[2]['work_description']
            EXPERIENCE3_BULLET2 = 'TBT OPENAI'
            EXPERIENCE3_BULLET3 = 'TBT OPENAI'
        else:
            EXPERIENCE3 = ""
            EXPERIENCE3_START_DATE = ""
            EXPERIENCE3_END_DATE = ""
            TITLE3 = ""
            EXPERIENCE3_LOCATION = ""
            EXPERIENCE3_BULLET1 = ""
            EXPERIENCE3_BULLET2 = ""
            EXPERIENCE3_BULLET3 = ""

        if len(experiences) >= 4:
            EXPERIENCE4 = experiences[3]['company']
            EXPERIENCE4_START_DATE = experiences[3]['start_date']
            EXPERIENCE4_END_DATE = experiences[3]['end_date']
            TITLE4 = experiences[3]['title']
            EXPERIENCE4_LOCATION = experiences[3]['location']
            EXPERIENCE4_BULLET1 = experiences[3]['work_description']
            EXPERIENCE4_BULLET2 = 'TBT OPENAI'
            EXPERIENCE4_BULLET3 = 'TBT OPENAI'
        else:
            EXPERIENCE4 = ""
            EXPERIENCE4_START_DATE = ""
            EXPERIENCE4_END_DATE = ""
            TITLE4 = ""
            EXPERIENCE4_LOCATION = ""
            EXPERIENCE4_BULLET1 = ""
            EXPERIENCE4_BULLET2 = ""
            EXPERIENCE4_BULLET3 = ""

        if len(experiences) >= 5:
            EXPERIENCE5 = experiences[4]['company']
            EXPERIENCE5_START_DATE = experiences[4]['start_date']
            EXPERIENCE5_END_DATE = experiences[4]['end_date']
            TITLE5 = experiences[4]['title']
            EXPERIENCE5_LOCATION = experiences[4]['location']
            EXPERIENCE5_BULLET1 = experiences[4]['work_description']
            EXPERIENCE5_BULLET2 = 'TBT OPENAI'
            EXPERIENCE5_BULLET3 = 'TBT OPENAI'
        else:
            EXPERIENCE5 = ""
            EXPERIENCE5_START_DATE = ""
            EXPERIENCE5_END_DATE = ""
            TITLE5 = ""
            EXPERIENCE5_LOCATION = ""
            EXPERIENCE5_BULLET1 = ""
            EXPERIENCE5_BULLET2 = ""
            EXPERIENCE5_BULLET3 = ""


        # get project details
        project_fields = ['project{}-description']
        count = 0
        for key in request.POST.keys():
            for field in project_fields:
                for i in range(1, 10):
                    if field.format(i) in key:
                        count += 1
        print("Number of projects:", count)
        projects = []
        project_count = int(request.POST.get('project_count', count))
        for i in range(1, project_count + 1):
            project_title = request.POST.get(f'project{i}-title', '')
            project_description = request.POST.get(f'project{i}-description', '')
            project = {
                'title': project_title,
                'description': project_description
            }
            projects.append(project)

        if len(projects) >= 1:
            PROJECT1 = projects[0]['title']
            PROJECT1_BULLET1 = projects[0]['description']
            PROJECT1_BULLET2 = 'TBT OPENAI'
        else:
            PROJECT1 = ""
            PROJECT1_BULLET1 = ""
            PROJECT1_BULLET2 = ""

        if len(projects) >= 2:
            PROJECT2 = projects[1]['title']
            PROJECT2_BULLET1 = projects[1]['description']
            PROJECT2_BULLET2 = 'TBT OPENAI'
        else:
            PROJECT2 = ""
            PROJECT2_BULLET1 = ""
            PROJECT2_BULLET2 = ""

        if len(projects) >= 3:
            PROJECT3 = projects[2]['title']
            PROJECT3_BULLET1 = projects[2]['description']
            PROJECT3_BULLET2 = 'TBT OPENAI'
        else:
            PROJECT3 = ""
            PROJECT3_BULLET1 = ""
            PROJECT3_BULLET2 = ""

        if len(projects) >= 4:
            PROJECT4 = projects[3]['title']
            PROJECT4_BULLET1 = projects[3]['description']
            PROJECT4_BULLET2 = 'TBT OPENAI'
        else:
            PROJECT4 = ""
            PROJECT4_BULLET1 = ""
            PROJECT4_BULLET2 = ""

        if len(projects) >= 5:
            PROJECT5 = projects[4]['title']
            PROJECT5_BULLET1 = projects[4]['description']
            PROJECT5_BULLET2 = 'TBT OPENAI'
        else:
            PROJECT5 = ""
            PROJECT5_BULLET1 = ""
            PROJECT5_BULLET2 = ""


        # get skills details
        LANGUAGES = request.POST.get('languages', '')
        TECHNOLOGIES = request.POST.get('technologies', '')
        LEADERSHIP = request.POST.get('leadership', '')

        def convert_date(date_str):
                months = {
                "01": "Jan", "02": "Feb", "03": "Mar", "04": "Apr",
                "05": "May", "06": "Jun", "07": "Jul", "08": "Aug",
                "09": "Sep", "10": "Oct", "11": "Nov", "12": "Dec"
            }
                year, month, _ = date_str.split("-")
                return f"{months[month]} {year}"

        if UNIVERSITY_START_DATE:
            UNIVERSITY_START_DATE = convert_date(UNIVERSITY_START_DATE)

        if UNIVERSITY_END_DATE:
            UNIVERSITY_END_DATE = convert_date(UNIVERSITY_END_DATE)

        if EXPERIENCE1_START_DATE:
            EXPERIENCE1_START_DATE = convert_date(EXPERIENCE1_START_DATE)

        if EXPERIENCE1_END_DATE:
            EXPERIENCE1_END_DATE = convert_date(EXPERIENCE1_END_DATE)

        if EXPERIENCE2_START_DATE:
            EXPERIENCE2_START_DATE = convert_date(EXPERIENCE2_START_DATE)

        if EXPERIENCE2_END_DATE :
            EXPERIENCE2_END_DATE = convert_date(EXPERIENCE2_END_DATE)

        if EXPERIENCE3_START_DATE :
            EXPERIENCE3_START_DATE = convert_date(EXPERIENCE3_START_DATE)

        if EXPERIENCE3_END_DATE :
            EXPERIENCE3_END_DATE = convert_date(EXPERIENCE3_END_DATE)

        if EXPERIENCE4_START_DATE :
            EXPERIENCE4_START_DATE = convert_date(EXPERIENCE4_START_DATE)

        if EXPERIENCE4_END_DATE :
            EXPERIENCE4_END_DATE = convert_date(EXPERIENCE4_END_DATE)

        if EXPERIENCE5_START_DATE :
            EXPERIENCE5_START_DATE = convert_date(EXPERIENCE5_START_DATE)

        if EXPERIENCE5_END_DATE :
            EXPERIENCE5_END_DATE = convert_date(EXPERIENCE5_END_DATE)

       



        def print_values(): 
            print()
            print()
            print()
            print()
            print()

            print()
            print()
            print()
            print()
            print()

            print("Name:", NAME or "")
            print("Email:", EMAIL or "")
            print("Phone:", PHONE or "")
            print("City:", CITY or "")
            print("State:", STATE or "")
            print("Link:", LINK or "")
            print("University:", UNIVERSITY or "")
            print("Degree Type:", DEGREE_TYPE or "")
            print("University Start Date:", UNIVERSITY_START_DATE or "")
            print("University End Date:", UNIVERSITY_END_DATE or "")
            print("Major:", MAJOR or "")
            print("Minor:", MINOR or "")
            print("GPA:", GPA or "")

            print()
            print()
            print()

            print("  Company1:", EXPERIENCE1 or "")
            print("  Start Date:", EXPERIENCE1_START_DATE or "")
            print("  End Date:", EXPERIENCE1_END_DATE or "")
            print("  Title:", TITLE1 or "")
            print("  Location:", EXPERIENCE1_LOCATION or "")
            print("  Bullet 1:", EXPERIENCE1_BULLET1 or "")
            print("  Bullet 2:", EXPERIENCE1_BULLET2 or "")
            print("  Bullet 3:", EXPERIENCE1_BULLET3 or "")
            print()

            print("  Company2:", EXPERIENCE2 or "")
            print("  Start Date:", EXPERIENCE2_START_DATE or "")
            print("  End Date:", EXPERIENCE2_END_DATE or "")
            print("  Title:", TITLE2 or "")
            print("  Location:", EXPERIENCE2_LOCATION or "")
            print("  Bullet 1:", EXPERIENCE2_BULLET1 or "")
            print("  Bullet 2:", EXPERIENCE2_BULLET2 or "")
            print("  Bullet 3:", EXPERIENCE2_BULLET3 or "")
            print()

            print("  Company3:", EXPERIENCE3 or "")
            print("  Start Date:", EXPERIENCE3_START_DATE or "")
            print("  End Date:", EXPERIENCE3_END_DATE or "")
            print("  Title:", TITLE3 or "")
            print("  Location:", EXPERIENCE3_LOCATION or "")
            print("  Bullet 1:", EXPERIENCE3_BULLET1 or "")
            print("  Bullet 2:", EXPERIENCE3_BULLET2 or "")
            print("  Bullet 3:", EXPERIENCE3_BULLET3 or "")
            print()
            
            print("  Company4:", EXPERIENCE4 or "")
            print("  Start Date:", EXPERIENCE4_START_DATE or "")
            print("  End Date:", EXPERIENCE4_END_DATE or "")
            print("  Title:", TITLE4 or "")
            print("  Location:", EXPERIENCE4_LOCATION or "")
            print("  Bullet 1:", EXPERIENCE4_BULLET1 or "")
            print("  Bullet 2:", EXPERIENCE4_BULLET2 or "")
            print("  Bullet 3:", EXPERIENCE4_BULLET3 or "")
            print()

            print("  Company5:", EXPERIENCE5 or "")
            print("  Start Date:", EXPERIENCE5_START_DATE or "")
            print("  End Date:", EXPERIENCE5_END_DATE or "")
            print("  Title:", TITLE5 or "")
            print("  Location:", EXPERIENCE5_LOCATION or "")
            print("  Bullet 1:", EXPERIENCE5_BULLET1 or "")
            print("  Bullet 2:", EXPERIENCE5_BULLET2 or "")
            print("  Bullet 3:", EXPERIENCE5_BULLET3 or "")
            print()


            print()
            print()
            print()

            
            print("  Project:", PROJECT1 or "")
            print("  Bullet 1:", PROJECT1_BULLET1 or "")
            print("  Bullet 2:", PROJECT1_BULLET2 or "")
            print()

            
            print("  Project:", PROJECT2 or "")
            print("  Bullet 1:", PROJECT2_BULLET1 or "")
            print("  Bullet 2:", PROJECT2_BULLET2 or "")
            print()

            
            print("  Project:", PROJECT3 or "")
            print("  Bullet 1:", PROJECT3_BULLET1 or "")
            print("  Bullet 2:", PROJECT3_BULLET2 or "")
            print()
            
            print("  Project:", PROJECT4 or "")
            print("  Bullet 1:", PROJECT4_BULLET1 or "")
            print("  Bullet 2:", PROJECT4_BULLET2 or "")
            print()
            
            print("  Project:", PROJECT5 or "")
            print("  Bullet 1:", PROJECT5_BULLET1 or "")
            print("  Bullet 2:", PROJECT5_BULLET2 or "")
            print()

            print()
            print()
            print()
            
            print("Languages:", LANGUAGES or "")
            print("Technologies:", TECHNOLOGIES or "")
            print("Leadership:", LEADERSHIP or "")

        print_values()

        

        print()

        def create_resume():
            from googleapiclient.discovery import build
            from google.oauth2 import service_account
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
            #SERVICE_ACCOUNT_FILE = '/Users/cheesenaan/Documents/projects/resume_app/project/.ipynb_checkpoints/resume_App/resume_app/resume_app/doc.json'
            SERVICE_ACCOUNT_FILE = '/home/resumeai/resume_app/resume_app/doc.json'

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
            return resume_link

        # resume_link = create_resume()
        
        # return redirect('resume' , user_id , NAME, resume_link)
        resume_link = create_resume()


        def save_to_user_resume_data():
            from resume_app.models import user_resume_data
            resume_data = user_resume_data(
            NAME=NAME or None,
            EMAIL=EMAIL or None,
            PHONE=PHONE or None,
            CITY=CITY or None,
            STATE=STATE or None,
            LINK=LINK or None,
            RESUME_LINK = resume_link or None,
            UNIVERSITY=UNIVERSITY or None,
            DEGREE_TYPE=DEGREE_TYPE or None,
            UNIVERSITY_START_DATE=UNIVERSITY_START_DATE or None,
            UNIVERSITY_END_DATE=UNIVERSITY_END_DATE or None,
            MAJOR=MAJOR or None,
            MINOR=MINOR or None,
            GPA=GPA or None,
            EXPERIENCE1=EXPERIENCE1 or None,
            EXPERIENCE1_START_DATE=EXPERIENCE1_START_DATE or None,
            EXPERIENCE1_END_DATE=EXPERIENCE1_END_DATE or None,
            TITLE1=TITLE1 or None,
            EXPERIENCE1_LOCATION=EXPERIENCE1_LOCATION or None,
            EXPERIENCE1_BULLET1=EXPERIENCE1_BULLET1 or None,
            EXPERIENCE1_BULLET2=EXPERIENCE1_BULLET2 or None,
            EXPERIENCE1_BULLET3=EXPERIENCE1_BULLET3 or None,
            EXPERIENCE2=EXPERIENCE2 or None,
            EXPERIENCE2_START_DATE=EXPERIENCE2_START_DATE or None,
            EXPERIENCE2_END_DATE=EXPERIENCE2_END_DATE or None,
            TITLE2=TITLE2 or None,
            EXPERIENCE2_LOCATION=EXPERIENCE2_LOCATION or None,
            EXPERIENCE2_BULLET1=EXPERIENCE2_BULLET1 or None,
            EXPERIENCE2_BULLET2=EXPERIENCE2_BULLET2 or None,
            EXPERIENCE2_BULLET3=EXPERIENCE2_BULLET3 or None,
            EXPERIENCE3=EXPERIENCE3 or None,
            EXPERIENCE3_START_DATE=EXPERIENCE3_START_DATE or None,
            EXPERIENCE3_END_DATE=EXPERIENCE3_END_DATE or None,
            TITLE3=TITLE3 or None,
            EXPERIENCE3_LOCATION=EXPERIENCE3_LOCATION or None,
            EXPERIENCE3_BULLET1=EXPERIENCE3_BULLET1 or None,
            EXPERIENCE3_BULLET2=EXPERIENCE3_BULLET2 or None,
            EXPERIENCE3_BULLET3=EXPERIENCE3_BULLET3 or None,
            EXPERIENCE4=EXPERIENCE4 or None,
            EXPERIENCE4_START_DATE=EXPERIENCE4_START_DATE or None,
            EXPERIENCE4_END_DATE=EXPERIENCE4_END_DATE or None,
            TITLE4=TITLE4 or None,
            EXPERIENCE4_LOCATION=EXPERIENCE4_LOCATION or None,
            EXPERIENCE4_BULLET1=EXPERIENCE4_BULLET1 or None,
            EXPERIENCE4_BULLET2=EXPERIENCE4_BULLET2 or None,
            EXPERIENCE4_BULLET3=EXPERIENCE4_BULLET3 or None,
            EXPERIENCE5=EXPERIENCE5 or None,
            EXPERIENCE5_START_DATE=EXPERIENCE5_START_DATE or None,
            EXPERIENCE5_END_DATE=EXPERIENCE5_END_DATE or None,
            TITLE5=TITLE5 or None,
            EXPERIENCE5_LOCATION=EXPERIENCE5_LOCATION or None,
            EXPERIENCE5_BULLET1=EXPERIENCE5_BULLET1 or None,
            EXPERIENCE5_BULLET2=EXPERIENCE5_BULLET2 or None,
            EXPERIENCE5_BULLET3=EXPERIENCE5_BULLET3 or None,
            PROJECT1=PROJECT1 or None,
            PROJECT1_BULLET1=PROJECT1_BULLET1 or None,
            PROJECT1_BULLET2=PROJECT1_BULLET2 or None,
            PROJECT2=PROJECT2 or None,
            PROJECT2_BULLET1=PROJECT2_BULLET1 or None,
            PROJECT2_BULLET2=PROJECT2_BULLET2 or None,
            PROJECT3=PROJECT3 or None,
            PROJECT3_BULLET1=PROJECT3_BULLET1 or None,
            PROJECT3_BULLET2=PROJECT3_BULLET2 or None,
            PROJECT4=PROJECT4 or None,
            PROJECT4_BULLET1=PROJECT4_BULLET1 or None,
            PROJECT4_BULLET2=PROJECT4_BULLET2 or None,
            PROJECT5=PROJECT5 or None,
            PROJECT5_BULLET1=PROJECT5_BULLET1 or None,
            PROJECT5_BULLET2=PROJECT5_BULLET2 or None,
            LANGUAGES=LANGUAGES or None,
            TECHNOLOGIES=TECHNOLOGIES or None,
            LEADERSHIP=LEADERSHIP or None
    )
            resume_data.save()
            return resume_data.ID

        user_id = save_to_user_resume_data()

        return redirect('resume', user_id, first_name)
        

    return render(request, 'data.html')


 ## printing


def work(request):
    return render(request, 'work.html')


def resume(request , user_id, first_name):
    from resume_app.models import user_resume_data
    # Retrieve the user_resume_data instance with the provided user_id
    resume_instance = get_object_or_404(user_resume_data, ID=user_id)

    # Access the RESUME_LINK attribute of the retrieved instance
    resume_link = resume_instance.RESUME_LINK

    # Pass the resume_link to the template and render the response
    context = {'link': resume_link, 'first_name': first_name}
    return render(request, 'resume.html', context)



# def enter_personal_data(request):
#     if request.method == 'POST':

#         # get personal detials
#         first_name = request.POST.get('firstName', '')
#         last_name = request.POST.get('lastName', '')
#         phone = request.POST.get('phone', '')
#         email = request.POST.get('email', '')
#         city = request.POST.get('city', '')
#         state = request.POST.get('stateCountry', '')
#         link = request.POST.get('link', '')

#         #get education details
#         university = request.POST.get('university', '')
#         degree_type = request.POST.get('degreeType', '')
#         city = request.POST.get('city', '')
#         gpa = request.POST.get('gpa', '')
#         major = request.POST.get('major', '')
#         minor = request.POST.get('minor', '')
#         university_start_date = request.POST.get('university-start-date', '')
#         university_end_date = request.POST.get('university-end-date', '')
#         coursework = request.POST.get('coursework', '')

#         # get work experience details
#         work_experience_fields = ['work-description']
#         count = 0
#         for key in request.POST.keys():
#             for field in work_experience_fields:
#                 if field in key:
#                     count += 1
#         print("number of work experiences is" , count)
#         experiences = []
#         experience_count = int(request.POST.get('experience_count', count))
#         for i in range(1, experience_count + 1):
#             company = request.POST.get(f'company{i}', '')
#             title = request.POST.get(f'title{i}', '')
#             start_date = request.POST.get(f'experience{i}-start-date', '')
#             end_date = request.POST.get(f'experience{i}-end-date', '')
#             work_description = request.POST.get(f'work-description{i}', '')
#             experience = {
#                 'company': company,
#                 'title': title,
#                 'start_date': start_date,
#                 'end_date': end_date,
#                 'work_description': work_description
#             }
#             experiences.append(experience)

#         # get project details
#         project_fields = ['project{}-description']
#         count = 0
#         for key in request.POST.keys():
#             for field in project_fields:
#                 for i in range(1, 10):
#                     if field.format(i) in key:
#                         count += 1
#         print("Number of projects:", count)
#         projects = []
#         project_count = int(request.POST.get('project_count', count))
#         for i in range(1, project_count + 1):
#             project_title = request.POST.get(f'project{i}-title', '')
#             project_description = request.POST.get(f'project{i}-description', '')
#             project = {
#                 'title': project_title,
#                 'description': project_description
#             }
#             projects.append(project)

#         # get skills details
#         languages = request.POST.get('languages', '')
#         technologies = request.POST.get('technologies', '')
#         leadership = request.POST.get('leadership', '')

#         # Print statements
#         print('First Name:', first_name)
#         print('Last Name:', last_name)
#         print('Phone:', phone)
#         print('Email:', email)
#         print('City:', city)
#         print('State:', state)
#         print('Link:', link)
#         print('University:', university)
#         print('Degree Type:', degree_type)
#         print('GPA:', gpa)
#         print('Major:', major)
#         print('Minor:', minor)
#         print('University Start Date:', university_start_date)
#         print('University End Date:', university_end_date)
#         print('Coursework:', coursework)

#         print(experiences)

#         print('Experiences:')
#         for i, experience in enumerate(experiences):
#             print('Experience', i+1)
#             print('Company:', experience['company'])
#             print('Title:', experience['title'])
#             print('Start Date:', experience['start_date'])
#             print('End Date:', experience['end_date'])
#             print('Work Description:', experience['work_description'])


#         print('Projects:')
#         for i, project in enumerate(projects):
#             print('Project', i+1)
#             print('Title:', project['title'])
#             print('Description:', project['description'])

#         print('Languages:', languages)
#         print('Technologies:', technologies)
#         print('Leadership:', leadership)

        
        
#         return HttpResponse('Personal data received successfully')

#     return render(request, 'enter_personal_data.html')


# def get_google_sheet():
#     scopes = ['https://www.googleapis.com/auth/spreadsheets', 'https://www.googleapis.com/auth/drive']
#     creds = Credentials.from_service_account_file('/Users/cheesenaan/Documents/projects/resume_app/project/.ipynb_checkpoints/resume_App/resume_app/resume_app/resume-app-392923-d8e95b50b335.json', scopes=scopes)
#     client = gspread.authorize(creds)
#     sheet = client.open('resume_app').sheet1  # Replace with your actual Google Sheet name
#     return sheet



## google sheet
# def google_sheet(request):
#     if request.method == 'POST':

#         # get personal details
#         first_name = request.POST.get('firstName', '')
#         last_name = request.POST.get('lastName', '')
#         phone = request.POST.get('phone', '')
#         email = request.POST.get('email', '')
#         city = request.POST.get('city', '')
#         state = request.POST.get('stateCountry', '')
#         link = request.POST.get('link', '')

#         # get education details
#         university = request.POST.get('university', '')
#         degree_type = request.POST.get('degreeType', '')
#         gpa = request.POST.get('gpa', '')
#         major = request.POST.get('major', '')
#         minor = request.POST.get('minor', '')
#         university_start_date = request.POST.get('university-start-date', '')
#         university_end_date = request.POST.get('university-end-date', '')
#         coursework = request.POST.get('coursework', '')

#         # get work experience details
#         work_experience_fields = ['work-description']
#         count = 0
#         for key in request.POST.keys():
#             for field in work_experience_fields:
#                 if field in key:
#                     count += 1
#         print("Number of work experiences:", count)
#         experiences = []
#         experience_count = int(request.POST.get('experience_count', count))
#         for i in range(1, experience_count + 1):
#             company = request.POST.get(f'company{i}', '')
#             title = request.POST.get(f'title{i}', '')
#             start_date = request.POST.get(f'experience{i}-start-date', '')
#             end_date = request.POST.get(f'experience{i}-end-date', '')
#             work_description = request.POST.get(f'work-description{i}', '')
#             experience = {
#                 'company': company,
#                 'title': title,
#                 'start_date': start_date,
#                 'end_date': end_date,
#                 'work_description': work_description
#             }
#             experiences.append(experience)

#         # get project details
#         project_fields = ['project{}-description']
#         count = 0
#         for key in request.POST.keys():
#             for field in project_fields:
#                 for i in range(1, 10):
#                     if field.format(i) in key:
#                         count += 1
#         print("Number of projects:", count)
#         projects = []
#         project_count = int(request.POST.get('project_count', count))
#         for i in range(1, project_count + 1):
#             project_title = request.POST.get(f'project{i}-title', '')
#             project_description = request.POST.get(f'project{i}-description', '')
#             project = {
#                 'title': project_title,
#                 'description': project_description
#             }
#             projects.append(project)

#         # get skills details
#         languages = request.POST.get('languages', '')
#         technologies = request.POST.get('technologies', '')
#         leadership = request.POST.get('leadership', '')

#         # Prepare the data as a list of lists
#         data = [
#             ['First Name', first_name],
#             ['Last Name', last_name],
#             ['Phone', phone],
#             ['Email', email],
#             ['City', city],
#             ['State', state],
#             ['Link', link],
#             ['University', university],
#             ['Degree Type', degree_type],
#             ['GPA', gpa],
#             ['Major', major],
#             ['Minor', minor],
#             ['University Start Date', university_start_date],
#             ['University End Date', university_end_date],
#             ['Coursework', coursework]
#         ]

#         for i, experience in enumerate(experiences):
#             data.append(['Experience', i+1])
#             data.append(['Company', experience['company']])
#             data.append(['Title', experience['title']])
#             data.append(['Start Date', experience['start_date']])
#             data.append(['End Date', experience['end_date']])
#             data.append(['Work Description', experience['work_description']])

#         for i, project in enumerate(projects):
#             data.append(['Project', i+1])
#             data.append(['Title', project['title']])
#             data.append(['Description', project['description']])

#         data.append(['Languages', languages])
#         data.append(['Technologies', technologies])
#         data.append(['Leadership', leadership])

#         # Update the Google Sheet
#         sheet = get_google_sheet()
#         sheet.append_rows(data)

#         return HttpResponse('Personal data received successfully')

#     return render(request, 'enter_personal_data.html')



##############

