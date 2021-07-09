python manage.py migrate
gunicorn satellite_tracker.wsgi:application --bind 0.0.0.0:8000 --log-level info --timeout 180  --workers 3
