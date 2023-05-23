  Каталог зимних альпинистских маршрутов Карпат 

Каталог зимних альпинистских маршрутов Карпат
=============================================

Содержание
----------

*   [1. O проекте](#org1)
*   [2. Пакеты и программы, необходимые перед установкой проекта](#org2)
    *   [2.1. Directory tree](#org2-1)
*   [3. Installation (установка)](#org3)
    *   [3.1. Клонирование проекта](#org3-1)
    *   [3.2. Виртуальное окружение](#org3-2)
    *   [3.3. Settings](#org3-3)
    *   [3.4. База данных](#org3-4)
    *   [3.5. Переменные в .env](#org3-5)
    *   [3.6. Миграция моделей в базу данных](#org3-6)
    *   [3.7. Тестовые данные](#org3-7)
    *   [3.8. Тестирование](#org3-8)
    *   [3.9. Сервер](#org3-9)
*   [4. Локализация](#org4)
*   [5. Геоданные пользователей](#org5)

1. О проекте
------------

### 1.1. Краткое описание проекта

Проект предназначен для хранения каталога зимних альпинистских маршрутов на вершины украинских Карпат.  
Список хребтов.  
  
Хребет содержит список вершин.  
Вершина содержит список маршрутов.  
  
К вершине прикручена система комментирования пользователями. Для обмена информацией.  
  
Все объекты могут быть изменены суперадмином в стандартной админке по адресу /admin/  
Админ может добавить пользователя в редакторы (editor roles), после этого на страницах становятся доступны элементы интерфейса, позволяющие изменять объекты в пользовательской части сайта.

2. Пакеты и программы, необходимые перед установкой проекта
-----------------------------------------------------------

*   Python3 должен быть установлен в системе
*   pip3
*   gettext
*   mysql server

### 2.1. Directory tree

      Directory tree
      ==============
      [-] routes
       |--[+] data   <--- хранение файлов
       |--[+] doc    <--- документы
       |--[+] locale <--- переводы строк
       |--[+] routes <-- код проекта 
       |--[+] venv   <-- виртуальная среда
       |----- requirements.txt <-- список необходимых пакетов для pip install
       |----- README.html
       |----- virtualenv_setup.sh <-- установка или обновление виртуальной среды
      

*   Django settings хранятся в `routes/settings.py`

3. Installation (установка)
---------------------------

### 3.1. Клонирование проекта

        git clone https://github.com/kostin-aleks/mountain-routes.git .
        

### 3.2. Виртуальное окружение

Выполните:

        ./virtualenv_setup.sh
        

Используйте виртуальное окружение:

        source venv/bin/activate
        

Установите необходимые пакеты:

        pip install -r requirements.txt
        

### 3.3. Settings

В папке routes выполните:

        cp custom_settings_example.py custom_settings.py 
        cp .env-example .env
        

### 3.4. База данных

По умолчанию проект использует MySQL. Это определяется настройкой словаря DATABASES в settings. Аналогичные словари для SQLite и PostgreSQL закомментированы.

*   Создайте пустую базу данных.
*   Добавьте пользователя с правами рута для этой базы данных. (Или дайте права существующему пользователю).
*   Пропишите настройки DATABASE_NAME, DATABASE_USER, DATABASE_PASSWORD, DATABASE_HOST, DATABASE_PORT в .env

### 3.5. Переменные в .env

Часть необходимых настроек прописали в предыдущем пункте для базы данных.

*   Для регистрации нового пользователя используется email. Нужно прописать настройки почтового сервера в .env
*   Пропишите количество комментариев на странице COMMENTS_PER_PAGE
*   Установите SECRET_KEY. Воспользуйтесь [рецептом](https://www.educative.io/answers/how-to-generate-a-django-secretkey) или для теста пропишите длинную строку.

### 3.6. Миграция моделей в базу данных

Попробуйте запустить

./manage.py

Если получили ошибку, возможно, нужно войти в виртуальное окружение:

source venv/bin/activate

Запустите миграцию:

./manage.py migrate

### 3.7. Тестовые данные

Попробуйте запустить

./manage.py

Если получили ошибку, возможно, нужно войти в виртуальное окружение:

source venv/bin/activate

*   Создайте суперюзера.
    
    ./manage.py createsuperuser
    
    После простого диалога получите пользователя с правами суперадмина. Сохраните для себя логин и пароль.
*   Заполните базу данных определёнными тестовыми данными:
    
    ./manage.py init_routes_data
    
*   Добавьте тестовые комментарии к какой-нибудь вершине. Например для вершины Близница:
    
    ./manage.py add_comments_to_the_peak -p bliznitsa
    
    Эта команда добавляет 20 комментариев. Можно добавлять такими порциями любое количество.

### 3.8. Тестирование

Попробуйте запустить

./manage.py

Если получили ошибку, возможно, нужно войти в виртуальное окружение:

source venv/bin/activate

Запустите тесты:

./manage.py test

### 3.9. Сервер

Попробуйте запустить

./manage.py

Если получили ошибку, возможно, нужно войти в виртуальное окружение:

source venv/bin/activate

Запустите локальный сервер:

./manage.py runserver

По умолчанию сервер доступен по адресу http://127.0.0.1:8000/  
Можно указать порт.

4. Локализация
--------------

Используется стандартный способ локализации Django на основе gettext.  
Сначала сбор переводимых строк.

      ./manage makemessages --all --ignore data --ignore venv
      ./manage.py makemessages --all --ignore data --ignore venv -d djangojs
      

Затем добавление правильных переводов в файлах .po в папках locale/ и routes/static/js/locale/  
  
И компиляция файлов перевода.

      ./manage.py compilemessages --ignore data --ignore venv
      

5. Геоданные пользователей
--------------------------

Во время сохранения комментария пользователя сохраняется IP из запроса.  
Отдельная команда добавлена для сбора геоданных по IP.  

      ./manage update_geolocation
      

На сервере эта команда будет периодически выполняться скриптом cron.  
Для тестирования можно просто вызвать эту команду вручную.  
Эта задача вынесена в отдельную команду из-за довольно ощутимого времени обработки запроса сторонним сервисом.

Author: Aleksandr Kostin

Created: 2023-05-20