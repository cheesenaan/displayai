# resume_app

## About Us

At ResumeAI, we help you create a professional resume in just 5 minutes. Our platform leverages the Google Cloud Platform (GCP) Google Doc API and advanced artificial intelligence and data science models to ensure your resume stands out. With a resume score of 95+/100, you can confidently apply for internships and kickstart your career.

## Features

- **Quick Resume Creation**: Input your basic information, and we'll generate a polished resume for you.

- **High Resume Score**: Our AI and data science models optimize your resume for ATS scanners, ensuring a score of 95+/100.

- **Designed for Internships**: Specifically tailored for internship applications, increasing your chances of getting noticed by employers.

## Getting Started

Follow these steps to set up the ResumeAI web app locally:

### Prerequisites

- Django
- gspread
- GCP Service Account Credentials

### Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/cheesenaan/resume_app.git
   ```

2. Navigate to the project directory:

   ```bash
   cd resume_app
   ```

3. Create a virtual environment and activate it:

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
   ```

4. Install Python dependencies:

   ```bash
   pip install -r requirements.txt
   ```

5. Migrate the database:

   ```bash
   python manage.py migrate
   ```

6. Create a GCP Service Account and configure the credentials.

   - Go to the Google Cloud Console and create a new Service Account.

   - Download the JSON key file for the Service Account.

   - Save the JSON key file as `gcp-credentials.json` in the project directory.

7. Collect static files:

   ```bash
   python manage.py collectstatic
   ```

8. Run the development server:

   ```bash
   python manage.py runserver
   ```

9. Access the web app at `http://localhost:8000/`.

## Pushing Code to GitHub

To push your code to GitHub, follow these steps:

1. Add all changes:

   ```bash
   git add .
   ```

2. Commit the changes with a meaningful message:

   ```bash
   git commit -m 'Add feature/fix/whatever'
   ```

3. Add your GitHub repository as the remote origin:

   ```bash
   git remote add origin https://github.com/cheesenaan/resume_app.git
   ```

4. Push your code to the `main` branch:

   ```bash
   git push -u origin main
   ```

## Pulling Code from GitHub to PythonAnywhere

To pull code from GitHub to PythonAnywhere, follow these steps:

1. Log in to your PythonAnywhere account.

2. Open a terminal within PythonAnywhere.

3. Create a virtual environment and activate it:

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
   ```

4. Install the project requirements:

   ```bash
   pip install -r requirements.txt
   ```

5. Commit any local changes:

   ```bash
   git commit -m 'Committing local changes'
   ```

6. Pull the latest code from GitHub:

   ```bash
   git pull origin main
   ```

---

