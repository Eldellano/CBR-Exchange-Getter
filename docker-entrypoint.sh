#!/bin/bash

# пауза перед применением миграций
echo "Start Entrypoint - Sleep"
sleep 10

# применение миграций
echo "Migrate"
python main.py migrate

# пауза
echo "Sleep"
sleep 3

# запуск web сервера
echo "Starting API"
python main.py start_api
