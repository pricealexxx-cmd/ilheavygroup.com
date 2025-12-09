# Настройка EmailJS для формы контактов

## Шаги настройки:

### 1. Создайте аккаунт на EmailJS
- Перейдите на https://www.emailjs.com/
- Зарегистрируйтесь или войдите в аккаунт

### 2. Создайте Email Service
- В Dashboard перейдите в "Email Services"
- Нажмите "Add New Service"
- Выберите ваш email провайдер (Gmail, Outlook, и т.д.)
- Следуйте инструкциям для подключения
- **Скопируйте Service ID** (например: `service_xxxxxxx`)

### 3. Создайте Email Template
- Перейдите в "Email Templates"
- Нажмите "Create New Template"
- Используйте следующий шаблон:

**Subject:**
```
New Contact Form Submission from {{from_name}}
```

**Content:**
```
New Contact Form Submission
===========================

Name: {{from_name}}
Email: {{from_email}}
Phone: {{from_phone}}
Company: {{company}}
Address: {{address}}
City: {{city}}
State: {{state}}
Product Interest: {{product_interest}}

Message:
{{message}}

---
This email was sent from the contact form on ilheavygroup.com
```

- **Скопируйте Template ID** (например: `template_xxxxxxx`)

### 4. Получите Public Key
- Перейдите в "Account" → "General"
- Найдите "Public Key"
- **Скопируйте Public Key** (например: `xxxxxxxxxxxxx`)

### 5. Обновите код на сайте

Откройте файл `contact.html` и найдите строку:
```javascript
emailjs.init("YOUR_PUBLIC_KEY");
```
Замените `YOUR_PUBLIC_KEY` на ваш Public Key.

Откройте файл `script.js` и найдите строки:
```javascript
const EMAILJS_SERVICE_ID = 'YOUR_SERVICE_ID';
const EMAILJS_TEMPLATE_ID = 'YOUR_TEMPLATE_ID';
```
Замените:
- `YOUR_SERVICE_ID` на ваш Service ID
- `YOUR_TEMPLATE_ID` на ваш Template ID

### 6. Проверьте настройки
- Убедитесь, что в EmailJS Template все переменные совпадают с теми, что используются в коде
- Проверьте, что Service правильно подключен к вашему email

## Переменные, используемые в форме:
- `from_name` - Имя отправителя
- `from_email` - Email отправителя
- `from_phone` - Телефон отправителя
- `company` - Название компании (опционально)
- `address` - Адрес (опционально)
- `city` - Город (опционально)
- `state` - Штат (опционально)
- `product_interest` - Интересующий продукт
- `message` - Сообщение

## Примечания:
- Поле "Company Name" уже сделано опциональным (не требуется для заполнения)
- EmailJS имеет бесплатный план с ограничением 200 писем в месяц
- Для production рекомендуется использовать платный план

