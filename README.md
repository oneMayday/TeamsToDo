<h1>TeamsToDo</h1>
<h2>Описание:</h2>
Альтернатива todo-сервиса для работы в команде. Имеются API для создания рабочих групп, добавления и редактирования задач (статус выполнения, исполнителя).
Доступ к тем или иным API реализован через permissions.

<h2>Порядок установки:</h2>
<details>
<summary>Установка виртуального окружения и зависимостей.</summary>

	
Клонируем репозиторий:
	
	
	https://github.com/oneMayday/TeamsToDo.git
	
Создаем виртуальное окружение и активируем его:
	
	
	python -m venv venv
	Windows: venv\Scripts\activate.bat
	Linux и MacOS: source venv/bin/activate

Переходим в директорию проекта и устанавливаем зависимости:


	pip install -r requirements.txt
	
Переходим в директорию newspaper.


	Файл example.env переименовываем в .env, прописываем в нём свои ключи и данные SMTP сервера.
	
ВыполняеМ миграции:


	python manage.py migrate
	
Запускаем сервер:


	python manage.py runserver

</details>

Эндпоинты:\
!! Все эндопинты доступны только зарегистрированным пользователям + доступ к определенным методам только по permissions !!


'^/api/v1/teamlist/'

	'GET' - получение всех списков, в которых состоит юзер, показываются только те списки, в которых юзер состоит как member.
	'POST" - создание нового списка, поля (title, description, members). Задачи добавляются отдельно каждым юзером.

'^/api/v1/teamlist/d', где d - id списка задач
	
	'GET' - получение информации о конкретном списке задач,
	'PUT", 'DELETE' - обновление/удаление списка, поля (title, description, members). Доступно только владельцу списка.

'^/api/v1/teamlist/d/all_tasks/', где d - id списка задач

	'GET' - получение развернутой информации о всех задачах в конкретном списке.
	
'^/api/v1/tasks/'

	'GET' - получение задач из всех списков в которых юзер состоит как member.
	'POST" - создание новой задачи, поля (title, status, due_date, who_takes, teamlist_relation). Задачу можно добавить только в тот список,
		в котором юзер состоит как member, указать исполнителем можно либо себя, либо оставить null.
	
'^/api/v1/tasks/'

	'GET' - получение всех задач, которые юезр взял для исполнения.
	
'^/api/v1/tasks/d/'

	'GET' - получение расширенных данных о конкретной задаче.
	'PUT'/'DELETE' - изменение/удаление полей задачи. Доступно только владельцу задачи.
	'PATCH' - изменение исполнителя задачи, указать можно только себя, либо оставить поле пустым.
