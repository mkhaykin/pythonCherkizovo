# pythonCherkizovo

Тестовое задание: [ТЗ](/docs/ТЗ.docx)

Стек: 
 - Python 3.10: tkinter, pyodbc;
 - MS SQL 2017;
 - Excel | OpenOffice;
 - Docker.

## Развертывание

### Переменные среды
Для запуска и тестирования проекта требуется создать файл `.env` с переменными окружения.    
Пример файла: [`.env.example`](.env.example)

#### Параметры подключения к ms sql:
`MSSQL_SERVER` - ip адрес / имя хоста (например, 127.0.0.1 для локальной установки)   
`MSSQL_PORT` - порт (порт по-умолчанию 1433)  
`MSSQL_SA_PASSWORD` - пароль пользователя sa (нужен для создания объектов)  
`MSSQL_DATABASE`- имя базы (например, TestDB)  
`MSSQL_USERNAME`- пользователь базы (например, db_user)  
`MSSQL_PASSWORD`- пароль пользователя (например, Q1q)    

### Скрипт создания объектов
Файл скрипта [db-create.sql](db-create.sql)

Необходимо внести изменения в первые 3 строчки: требуется указать те же данные, 
что и в `.env` файле.  
```
:setvar db_name <MSSQL_DATABASE>
:setvar user_uid <MSSQL_USERNAME>
:setvar user_pwd <MSSQL_PASSWORD>
```
Например:
```
:setvar db_name TestDB
:setvar user_uid db_user
:setvar user_pwd Q1q
```


### С использованием Docker.
Запускаем
```shell
docker compose up -d
```
Создается 2 контейнера:
- mssql - собственно БД;
- mssql_conf - контейнер для конфигурирования mssql (создание пользователя, таблицы, sp).

### Без использования Docker.
Необходимо создать в БД требуемые объекты вручную.   
Ссылка на файл скрипта [db-create.sql](db-create.sql)  

## Запуск приложения:
### Дополнительное ПО:
Для работы с MS SQL использует ODBC Driver 18 for SQL Server.  

#### Windows
Для установки по Windows следует скачать и установить дополнительное ПО: [Скачивание драйвера ODBC Driver for SQL Server](https://learn.microsoft.com/ru-ru/sql/connect/odbc/download-odbc-driver-for-sql-server?view=sql-server-ver16)  

#### Linux
```shell
sudo apt install unixodbc-dev
```
Для ubuntu дополнительно:
```shell
if ! [[ "18.04 20.04 22.04 23.04" == *"$(lsb_release -rs)"* ]];
then
    echo "Ubuntu $(lsb_release -rs) is not currently supported.";
    exit;
fi

curl https://packages.microsoft.com/keys/microsoft.asc | sudo tee /etc/apt/trusted.gpg.d/microsoft.asc
curl https://packages.microsoft.com/config/ubuntu/$(lsb_release -rs)/prod.list | sudo tee /etc/apt/sources.list.d/mssql-release.list

sudo apt-get update
sudo ACCEPT_EULA=Y apt-get install -y msodbcsql18
# optional: for bcp and sqlcmd
sudo ACCEPT_EULA=Y apt-get install -y mssql-tools18
echo 'export PATH="$PATH:/opt/mssql-tools18/bin"' >> ~/.bashrc
source ~/.bashrc
# optional: for unixODBC development headers
sudo apt-get install -y unixodbc-dev
```

#### Python
Требования к версии python не выставлялись, поэтому предполагается, что используется версия 3.10 
```sh
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python src/main.py
deactivate
```

Файл для загрузки `data.xlsb` находится в `./import`

## Ограничения / замечания:
 - MS SQL поднимается в docker, без указаний кодировок и прочих настроек, т.е. с кириллицей ~~может~~ точно будет работать некорректно. 
Но в текущем задании у нас кириллицы нет (кроме строки 160444 с артикулом "#ошибка", в отчете эта строка фигурирует как "#??????");
 - Для создания таблицы / процедуры развертывается отдельный контейнер, он находится в нормально выключенном состоянии;  
 - Загрузка идет пакетами по 100 записей. Полагаю правильнее было бы грузить 
данные bulk-ом;
 - Данные загружаются непосредственно в основную таблицу, правильнее было бы загружать их
через временную;
 - Тестировалось на linux, под windows может быть что-то пойдет не так ...
 - Есть определенные проблемы с фризами в процессе загрузки при открытии about. 
Есть откровенные неопрятности в коде, но полагаю для тестового проекта это может быть приемлемо;
 - Для чтения данных используется pandas, что в данном проекте избыточно.