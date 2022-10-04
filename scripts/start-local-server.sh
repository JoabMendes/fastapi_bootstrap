#!/usr/bin/env bash
set -x
gunicorn app.main:app --chdir /home/"${APP_NAME}"/project/src/ -k uvicorn.workers.UvicornWorker -w 1 --reload --bind 0.0.0.0:5000
