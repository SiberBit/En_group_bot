#!/bin/bash

#exec gunicorn --bind=0.0.0.0:8080 --workers=1 wsgi:app
gunicorn --bind 0.0.0.0:8000 --workers=1 En_group_bot.wsgi
