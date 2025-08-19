Для запуска постгрес - docker-compose -f docker-compose-local.yaml up -d

Для накатывания миграций если файла alembic.ini еще нет
alembic init migrations

далее вводим ''' alembic revision --autogenerate -m "comment" '''
будут созданы миграции
дальше вводим: alembic upgrade heads


-Для подключения к Postgres локальному нужно заменить значение переменной DB_PORT=5434 на 5433
