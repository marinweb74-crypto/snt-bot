# SNT Survey Bot

Telegram-бот для автоматизированного анкетирования председателей СНТ/ТСН по вопросам взыскания задолженностей.

## Возможности

- 10-шаговый опрос с inline-кнопками и навигацией «Назад»
- Множественный выбор (multi-select) в вопросах
- Валидация данных (имя, телефон в формате РФ)
- Сохранение анкет в PostgreSQL
- Уведомления в Telegram-группу при каждой новой анкете
- Публикация постов с кнопкой в канал по команде `/post`
- FSM-состояния хранятся в PostgreSQL (устойчивость к перезапускам)

## Стек технологий

- **Python 3.11+**
- **aiogram 3.x** — асинхронный фреймворк для Telegram Bot API
- **PostgreSQL** — хранение анкет и FSM-состояний
- **asyncpg** — асинхронный драйвер PostgreSQL
- **Docker** — контейнеризация для деплоя

## Архитектура

```
bot/
├── main.py              # Точка входа, инициализация бота и БД
├── config.py            # Конфигурация из переменных окружения
├── db.py                # Пул соединений PostgreSQL, схема, CRUD
├── storage.py           # FSM-хранилище на базе PostgreSQL
├── states.py            # Конечный автомат (FSM) — состояния опроса
├── keyboards.py         # Inline-клавиатуры для всех вопросов
├── handlers/
│   ├── start.py         # /start — приветствие и запуск опроса
│   ├── survey.py        # Логика 10 вопросов, валидация, навигация
│   ├── post.py          # /post — публикация в канал
│   ├── notify.py        # Уведомления в группу администраторов
│   └── fallback.py      # Обработка некорректных сообщений
├── Dockerfile
├── Procfile
└── requirements.txt
```

## Паттерны и подходы

- **FSM (Finite State Machine)** — каждый вопрос = отдельное состояние, переходы строго контролируются
- **Persistent Storage** — кастомная реализация `BaseStorage` поверх PostgreSQL для сохранения состояний между перезапусками
- **Graceful Error Handling** — ошибки БД не блокируют пользовательский опыт
- **Fallback Handlers** — перехват сообщений без активного состояния

## Запуск

### Переменные окружения

```env
BOT_TOKEN=telegram_bot_token
DATABASE_URL=postgresql://user:password@host:5432/dbname
NOTIFY_CHAT_ID=-1001234567890
```

### Локально

```bash
pip install -r requirements.txt
python main.py
```

### Docker

```bash
docker build -t snt-bot .
docker run --env-file .env snt-bot
```

### Railway (облако)

1. Подключить репозиторий на [railway.app](https://railway.app)
2. Добавить сервис PostgreSQL
3. Указать переменные окружения
4. Deploy

## Схема базы данных

```sql
CREATE TABLE surveys (
    id SERIAL PRIMARY KEY,
    telegram_id BIGINT NOT NULL,
    telegram_username VARCHAR(255),
    role VARCHAR(50) NOT NULL,
    name VARCHAR(255) NOT NULL,
    is_member BOOLEAN NOT NULL,
    is_sole_owner BOOLEAN NOT NULL,
    debt_period VARCHAR(50) NOT NULL,
    debt_amount VARCHAR(50) NOT NULL,
    actions_taken TEXT[] NOT NULL,
    actions_other VARCHAR(500),
    has_written_response BOOLEAN NOT NULL,
    debtor_data TEXT[] NOT NULL,
    contact_phone VARCHAR(20) NOT NULL,
    created_at TIMESTAMP DEFAULT NOW()
);
```

## Лицензия

MIT
