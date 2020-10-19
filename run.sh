#!/bin/bash

gunicorn --bind 0.0.0.0:8000 --workers=1 En_group_bot.wsgi
