## Setup
 Clone this repository and go to the project folder:
 <!-- (выбирайте свою папку для проекта) -->
   ```bash
   cd /c/my_folder
   ```
   ```bash
   git clone git@github.com:JacobKleim/IT_Meetup_Service.git
   ```
   ```bash
   cd /c/my_folder/IT_Meetup_Service
   ```
## Environment      
 Сreate and activate a virtual environment  
   ```
   python -m venv venv
   ```
   ```bash
   source venv/Scripts/activate
   ```
## Requirements
   Update the Python package manager to the latest version:
   ```
   python -m pip install --upgrade pip
   ```
   Install dependencies:
   ```
   pip install -r requirements.txt
   ``` 

## Run
   ```
   python manage.py migrate
   ```
   Start the project:
   ```
   python manage.py runserver
   ```

