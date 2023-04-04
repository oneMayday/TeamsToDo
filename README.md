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
	
Выполняет миграции:


	python manage.py migrate
	
Запускаем сервер:


	python manage.py runserver

</details>
