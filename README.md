# test_drf
Marketplace
Постепенно пишется проект
## Idea
Сделать маркетплейс и на основе маркетплейса сделать площадку для продажи обучающих курсов. Со всеми вытекающими, в виде разграничения прав доступа.
Особенность - обязательно использовать DRF, JWT и в последствии подключить CORS для добавления фронтенд-фреймворка react.js.
Далее задеплоить в Docker контейнер и развернуть на VDS.
## Process
Логика маркетплейса полностью готова. Остались лишь пополнения в виде малых функциональных эндпоинстов для фронтенда.
## Install project
В данный момент проект слишком малых размеров. Доступна только логика магазинов и пользователей с разными ролями в разных магазинах.
Тем не менее, все требующиеся пакеты хранятся в requirements.txt.
```
Windows:

py -m venv venv
%VIRTUAL_ENVIRONMENT_DIRECTORY%\venv\Scripts\Activate
py -m pip install requirements.txt
py manage.py makemigrations
py manage.py migrate
py manage.py runserver
  
Linux:

python3 -m venv venv
%VIRTUAL_ENVIRONMENT_DIRECTORY%/venv/bin/activate
python3 -m pip install requirements.txt
python3 manage.py makemigrations
python3 manage.py migrate
python3 manage.py runserver
```
Далее в браузере заходим на localhost:8000 и смотрим результат. Swagger будет добавлен в проект чуть позже.
