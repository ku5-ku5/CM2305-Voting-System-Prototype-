:: Performs all pip installs for the project

@ECHO ON

cd C:\repos\CM2305-Voting-System-Prototype-\Voting_System

py -m venv venv

venv\Scripts\pip install -r requirements.txt

cd C:\repos\CM2305-Voting-System-Prototype-\Admin_Microservice

py -m venv venv

venv\Scripts\pip install -r C:\repos\CM2305-Voting-System-Prototype-\Admin_Microservice\requirements.txt