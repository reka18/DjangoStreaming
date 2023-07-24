#! /bin/bash

printf '** Dropping database **\n'
psql -h localhost -d stream -U rkse -p 5444 <<< 'drop schema public cascade; create schema public;'
printf '** Database dropped **\n\n'

printf '** Removing migrations **\n'
# shellcheck disable=SC2035
rm -rfv **/migrations/0*.py
printf '** Migrations removed **\n\n'

printf '** Creating migrations **\n'
python manage.py makemigrations
printf '** Migrations created **\n\n'

printf '** Migrating **\n'
python manage.py migrate
printf '** Migrated **\n\n'

printf '** Creating superuser **\n'
DJANGO_SUPERUSER_USERNAME=admin \
DJANGO_SUPERUSER_PASSWORD=badpassword! \
DJANGO_SUPERUSER_EMAIL=admin@admin.com \
python manage.py createsuperuser --noinput

printf '** Running application **\n\n'
python manage.py runserver