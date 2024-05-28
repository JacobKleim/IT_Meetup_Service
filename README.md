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
 Get a bot token using **@BotFather** on Telegram.
 Create [Yookassa shop](https://yookassa.ru/) to use donates features. 
 Create an .env file and put the bot token, yookassa token and shop id in there:
   ```python 
   TELEGRAM_BOT_TOKEN=bot_token
   YOO_API_TOKEN=api_token
   YOO_SHOP_ID=shop_id
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
   ```
   python manage.py bot
   ```
