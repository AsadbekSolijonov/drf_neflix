mig:
	python manage.py makemigrations
	python manage.py migrate

shell:
	python manage.py shell