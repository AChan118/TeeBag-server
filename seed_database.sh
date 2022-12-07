rm db.sqlite3
rm -rf ./teebagapi/migrations
python3 manage.py makemigrations teebagapi
python3 manage.py migrate
python3 manage.py loaddata profileimages
python3 manage.py loaddata golfers
python3 manage.py loaddata courses
python3 manage.py loaddata rounds
python3 manage.py loaddata holes
python3 manage.py loaddata mybags
python3 manage.py loaddata notes
python3 manage.py loaddata clubs
