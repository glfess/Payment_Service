
---

# 💳 Payment Processing Service

Асинхронный микросервис для обработки платежей с использованием паттерна **Transactional Outbox**, гарантированной доставкой событий и защитой от дублирования запросов.

---

## 🚀 Основные возможности

### 🔹 Transactional Outbox

Гарантирует атомарность:

* сохранения платежа в БД
* и постановки события в очередь RabbitMQ

Это исключает рассинхронизацию между системой хранения и брокером сообщений.

---

### 🔹 Идемпотентность

Защита от повторных списаний при сетевых сбоях:

* используется заголовок `Idempotency-Key`
* повторные запросы не создают дубликаты операций

---

### 🔹 Отказоустойчивость

**Retry-механизм:**

* экспоненциальная задержка при отправке webhook-уведомлений

**Dead Letter Queue (DLQ):**

* сообщения, не обработанные после 3 попыток, отправляются в отдельную очередь

---

### 🔹 Эмуляция платежного шлюза

* время обработки: **2–5 секунд**
* вероятность успеха: **90%**

---

## 🛠 Стек технологий

| Компонент      | Технология                        |
| -------------- | --------------------------------- |
| Framework      | FastAPI + Pydantic v2             |
| База данных    | PostgreSQL + SQLAlchemy 2.0 Async |
| Брокер         | RabbitMQ + FastStream             |
| Миграции       | Alembic                           |
| Инфраструктура | Docker, Docker Compose            |

---

## 📦 Быстрый запуск

### 1. Клонирование репозитория

```bash
git clone https://github.com/glfess/Payment_Service.git
cd payment_service
```

---

### 2. Запуск проекта

```bash
docker-compose up --build
```

Будут подняты:

* API сервис
* Consumer (воркер)
* PostgreSQL
* RabbitMQ

---

## 📖 API

⚠️ Для всех эндпоинтов обязателен заголовок:

```
X-API-Key: my_super_secret_key
```

---

### 1. Создание платежа

**POST** `/api/v1/payments`

#### Headers

```
X-API-Key: my_super_secret_key
Idempotency-Key: <unique_uuid_v4>
```

#### Body

```json
{
  "amount": 1000.50,
  "currency": "RUB",
  "description": "Оплата подписки",
  "meta_data": {"user_id": 42},
  "webhook_url": "https://example.com/callback"
}
```

#### Response (202 Accepted)

```json
{
  "payment_id": "a4a956df-0588-4a43-91ed-9e6ad81dbc2c",
  "status": "pending",
  "created_at": "2026-04-10T06:30:00"
}
```

---

### 2. Получение информации о платеже

**GET** `/api/v1/payments/{payment_id}`

#### Response

```json
{
  "id": "a4a956df-0588-4a43-91ed-9e6ad81dbc2c",
  "amount": 1000.50,
  "currency": "RUB",
  "status": "succeeded",
  "description": "Оплата подписки",
  "meta_data": {"user_id": 42},
  "created_at": "2026-04-10T06:30:00",
  "updated_at": "2026-04-10T06:30:05"
}
```

---

## 📊 Архитектура и очереди

* **Основная очередь:** `payments.new`
* **Dead Letter Queue:** `payments.failed`

Сообщения, не обработанные после 3 попыток, автоматически попадают в DLQ.

---

## 🐇 RabbitMQ Management UI

Доступ к панели управления:

```
http://localhost:15673
```

**Логин / пароль:**

```
guest / guest
```