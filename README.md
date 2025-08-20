# Tron TX Info API (Django + tronpy)

## Пример ответа
{
  "txid": "21eaf796d80f5c5bb0ecfdb33c7c1da907d716136c0a040526e99a962dc786bc",
  "confirmed": true,
  "block_number": 75011939,
  "block_time": 1755695025000,
  "fee_sun": 0,
  "fee_trx": 0.0,
  "ret": null,
  "contract_result": [""],
  "logs": [],
  "transfer": {
    "contract_type": "TransferContract",
    "from": "TGwqfcMCsar5YXorezZiUg2CM4dr1YFJtV",
    "to": "TSfcUkv1VHvGczbnrgPyRp9jU28AQrX5Ra",
    "amount_sun": 1,
    "amount_trx": 0.000001
  }
}

## Настройка
Создайте .env-файл на основе примера (можно командой в bash):


cp .env.example .env


В .env нужно указать ваш API-ключ TronGrid(https://www.trongrid.io/):


TRON_API_KEY=ваш_ключ


## Быстрый старт (локально)
bash-команды:


git clone https://github.com/username/troninfo_project.git


cd troninfo_project


python -m venv .venv


source .venv/bin/activate   # Windows: .venv\Scripts\activate


pip install -r requirements.txt


python manage.py migrate


python manage.py runserver

## Запуск в Docker
bash-команды:


git clone https://github.com/username/troninfo_project.git


cd troninfo_project


docker-compose up --build

## После запуска сервис будет доступен по адресу:

http://127.0.0.1:8000/api/tron/tx/<txid>/


можно использовать curl-запрос, например


curl http://127.0.0.1:8000/api/tron/tx/21eaf796d80f5c5bb0ecfdb33c7c1da907d716136c0a040526e99a962dc786bc/
