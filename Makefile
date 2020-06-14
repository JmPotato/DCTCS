run-backend-dev:
	export FLASK_ENV=development FLASK_APP=./backend/app.py
	flask run