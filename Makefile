run:  env
	flask run

clean:
	rm DCTCS.db

env:
	export FLASK_ENV=development FLASK_APP=./backend/app.py