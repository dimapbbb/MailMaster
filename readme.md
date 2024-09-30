Вас приветсвует Мастер рассылок 

Для запуска сервиса: 
I) Добавить файл .env в корень проекта, заполнить его по примеру .env.sample

II) Загрузить фикстуры с первначальными данными
1) python manage.py loaddata fixtures/blog_data
2) python manage.py loaddata fixtures/users_data
3) python manage.py loaddata fextures/newsletterap_data
4) python manage.py loaddata fixtures/recepients_data
5) python manage.py loaddata fixtures/auth_data

III) Запустить сервер
python manage.py runserver
