# Airport-API-Service
The system for tracking flights from airports across the whole globe.
***
# Features
- JWT authentication
- Admin panel /admin/
- Documentation is located at /api/doc/swagger/ & /api/doc/redoc/
***
# Installing using GitHub
```
git clone https://github.com/Paul-Starodub/Airport-API-Service
cd Airport-API-Service
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```
---
# .env file
Open file .env.sample and change environment variables to yours. Also rename file extension to .env
***
# Run on local server
- Install PostgreSQL, create DB and User
- Connect DB
- Run:
```
python manage.py migrate
python manage.py runserver
```
- You can download test fixture:
```
python manage.py dumpdata --indent 4 > airport_data.json
```
***
# Run with Docker
Docker should be already installed
```
docker-compose up --build
```
***
# Create/Authenticate User
- Path to create user: api/users
- Path to login user: api/users/token
- Authorize Bearer
- docker exec -it airport bash 
- python manage.py createsuperuser
## Getting access
You can use following:
- superuser:
  - Email: admin@gmail.com
  - Password: vovk7777
- user:
  - Email: red@gmail.com
  - Password: vovk7777
## Note: Make sure to send Token in api urls in Headers as follows
```
key: Authorize
value: Bearer <token>
```
***
# Testing with docker
- docker exec -it airport bash 
- python manage.py test
***
# Stop server
```
docker-compose down
```
