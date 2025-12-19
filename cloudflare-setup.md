# Cloudflare Setup для счетчика скачиваний

## ⚠️ ВАЖНО: НЕ создавайте отдельный Worker!

Ваш сайт уже на **Cloudflare Pages**, и функция уже создана в папке `/functions`.
Вам нужно только настроить KV хранилище.

---

## Шаги настройки:

### 1. Откройте ваш существующий Pages проект

1. Зайдите в Cloudflare Dashboard: https://dash.cloudflare.com/
2. Слева выберите **Workers & Pages**
3. Найдите ваш проект **ilheavygroup.com** (или как он называется)
4. Откройте его

### 2. Создать KV Namespace

1. В левом меню Cloudflare Dashboard выберите **Workers & Pages** (главный раздел)
2. Перейдите на вкладку **KV**
3. Нажмите **Create a namespace**
4. Назовите его `DOWNLOAD_COUNTER`
5. Выберите **Free** план
6. Нажмите **Add**
7. **Namespace ID** скопируется автоматически (но он нам не понадобится)

### 3. Подключить KV к вашему Pages проекту

1. Вернитесь к вашему **Pages проекту** (ilheavygroup.com)
2. Откройте вкладку **Settings**
3. В левом меню выберите **Functions**
4. Прокрутите вниз до секции **KV Namespace Bindings**
5. Нажмите **Add binding**
6. Заполните:
   - **Variable name**: `DOWNLOAD_COUNTER` (точное имя!)
   - **KV namespace**: выберите `DOWNLOAD_COUNTER` из выпадающего списка
7. Нажмите **Save**

### 4. Загрузите файлы в проект

После того как добавили KV binding, залейте обновленные файлы:
- Если используете Git → сделайте commit и push
- Если загружаете вручную → загрузите все файлы с папкой `/functions`

### 3. Структура файлов

```
ilheavygroup.com/
├── functions/
│   └── api/
│       └── download-count.js    # API endpoint для счетчика
├── app/
│   ├── count.html               # Страница статистики
│   └── IL_HEAVY_GROUP_LLC.apk   # APK файл
├── app.html                     # Страница скачивания
└── wrangler.toml               # Конфигурация (опционально)
```

### 4. API Endpoints

- **GET** `/api/download-count` - получить текущее количество скачиваний
- **POST** `/api/download-count` - увеличить счетчик на 1

### 5. Проверка работы

1. После деплоя на Cloudflare Pages:
   - Откройте `ilheavygroup.com/app` - должно начаться скачивание
   - Откройте `ilheavygroup.com/app/count` - должна показаться статистика

2. Тестовый запрос:
   ```bash
   curl https://ilheavygroup.com/api/download-count
   ```

### Примечания

- Счетчик начинает с 0 и увеличивается при каждом POST запросе
- KV storage сохраняет данные между запросами
- Cloudflare Pages Functions работают на Edge, так что счетчик доступен глобально
- Автообновление на странице /app/count происходит каждые 5 секунд

