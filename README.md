
![Screenshot (144)](https://github.com/OgwuegbuMaxwell/django_automation_apps/assets/53094485/ec76ea00-36b7-40c3-a95c-2db76ce36c4f)


![Screenshot (145)](https://github.com/OgwuegbuMaxwell/django_automation_apps/assets/53094485/9bd48200-181a-4b9d-b694-ef0316eba646)


![Screenshot (147)](https://github.com/OgwuegbuMaxwell/django_automation_apps/assets/53094485/d4e98741-684e-4382-95a3-49f15271b1d3)


![Screenshot (146)](https://github.com/OgwuegbuMaxwell/django_automation_apps/assets/53094485/d035bac4-cf21-4c06-bb77-25b7ff196e23)


# Django Automation Apps

## Introduction

Django Automation Apps is a comprehensive suite of applications built with the Django framework, designed to automate tasks across multiple domains including student management, customer relations, and employee data handling. It also integrates functionalities for automated email communications and robust file management systems.

## Features

- **Data Entry**: Manage data for students, customers, and employees through a user-friendly interface.
- **Email Automation**: Automate sending emails with attachments and manage subscriptions through custom lists.
- **File Uploads**: Facilitate the uploading and management of files associated with different models.
- **Custom Utilities**: Includes utilities for exporting data to CSV files, sending notifications via email, and handling CSV imports.

## Models

### Data Entry App
- `Student`: Manages student data with fields like roll number, name, and age.
- `Customer`: Manages customer information.
- `Employee`: Handles comprehensive details about employees including financials.

### Emails App
- `List`: Represents a mailing list.
- `Subscriber`: Links subscribers to specific email lists.
- `Email`: Manages the emails sent to lists with rich text content and optional attachments.

### Uploads App
- `Upload`: Handles file uploads and stores references to the associated models.

## Installation

To set up the project locally, follow these steps:

1. **Clone the repository**:
   ```bash
   git clone https://github.com/your-username/django_automation_apps.git

1. **Navigate to the project directory:**
`cd django_automation_apps
`

3. **Install dependencies:**
`pip install -r requirements.txt
`

4. **Apply migrations:**
`python manage.py makemigrations
`
`python manage.py migrate
`

5. **Run the development server:**
`python manage.py runserver
`

Access the application via http://127.0.0.1:8000 in your web browser.


### Configuration

**Ensure you configure the following in your settings.py:**

- DATABASES to link to your database of choice.
- SECRET_KEY for security measures.
- DEBUG should be set to False in a production environment.

**Utilizing Utilities**

- Email Notifications: To send email notifications, utilize the send_email_notification function provided in utils.py.
- CSV Operations: For exporting and validating CSV data against Django models, use the corresponding functions in utils.py.
- 




