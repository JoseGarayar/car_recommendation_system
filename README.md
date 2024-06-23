# Proyecto 2


## Commands

1. To run project in local

```bash
docker-compose -f local.yml up --build
```

2. To create superuser (all privileges)

```bash
docker-compose -f local.yml run --rm django python manage.py createsuperuser
```

3. To make migrations (not needed unless some changes in DB models has been applied)

```bash
docker-compose -f local.yml run --rm django python manage.py makemigrations
```

