# Сервис уведомлений
Сервис уведомлений.

## <br><b>Тех.данные</b>

Сревис сделан на FastAPI и APScheduler(использует sqlite)

База данных используется MongoDB

## <br><b>Установка</b>

### <br><b>Откройте консоль</b>

<b>Выполните в консоли</b>             
    <details><summary> Команду: </summary>
```
git clone https://github.com/IgV52/api_notification_service.git
```
</details>

### <br><b>Настройка</b>

<b>Создайте файл .env в каталоге api_notification_service и добавьте туда следующие настройки:</b>
    <details>
    <summary> Параметры: </summary></b>
```

MONGO_URL = адрес базы данных [можно создать бд тут -> (https://www.mongodb.com/cloud/atlas/register))
URL_MSG_SEND = адрес внешнего сервиса
URL_SCHEDULER = 'sqlite:///'+ os.path.join(basedir, 'db_task', 'jobs.sqlite')
TOKEN = токен для доступа к внешнему сервису

```
</details>

## <br><b>Запуск</b>

<br><b>Зайдите в каталог api_notification_service</b>

### <br><b>Откройте консоль</b>

<b>Выполните в консоли</b>             
    <details><summary> Команду: </summary>
```
docker-compose up --build
```
</details>

## <br><b>Описание</b>

В сервисе реализованы три конечные точки

1. Client имеет метод [post,put,delete]

Создает пользователя, обновляет, удаляет.

2. Dispath имеет метод [post,put,delete]

Создает задачу, обновляет, удаляет.

3. Stats имеет метод [get]

Показывает все текущие задачи и сообщения отправленные по этим задачам.
Можно посмотреть информацию о задаче по ее номеру.

Адреc/docs#/ - Описание реализованных методов в формате OpenAPI

## <br><b>Тесты</b>

Что бы выполнить тесты установите виртуальное окружение

Активируйте виртуальное окружение

Установите зависимости из requirements.txt

Выполните в консоли команду pytest
