release: python manage.py migrate --noinput
web: uwsgi --master --processes 2 --threads 1 --wsgi-file BauerDude/wsgi.py --callable application --http-socket :$PORT --die-on-term
