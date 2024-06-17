# Proyecto 2


## Commands

```bash
docker-compose -f local.yml run --rm django python manage.py createsuperuser
docker-compose -f local.yml run --rm django python manage.py makemigrations