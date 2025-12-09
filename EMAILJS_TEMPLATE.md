# Шаблон EmailJS для формы контактов

## Переменные, которые отправляются из формы:

- `{{from_name}}` - Имя отправителя (обязательно)
- `{{from_email}}` - Email отправителя (обязательно)
- `{{from_phone}}` - Телефон отправителя (обязательно)
- `{{company}}` - Название компании (опционально, может быть "Not provided")
- `{{product_interest}}` - Интересующий продукт
- `{{message}}` - Сообщение от пользователя (обязательно)
- `{{to_email}}` - Email получателя (info@ilheavygroup.com)

## Шаблон для EmailJS:

### Вариант 1: Простой текстовый шаблон

**Subject (Тема письма):**
```
New Contact Form Submission from {{from_name}}
```

**Content (Содержимое):**
```
New Contact Form Submission
===========================

Contact Information:
-------------------
Name: {{from_name}}
Email: {{from_email}}
Phone: {{from_phone}}
Company: {{company}}

Product Interest: {{product_interest}}

Message:
--------
{{message}}

---
This email was sent from the contact form on ilheavygroup.com
```

### Вариант 2: HTML шаблон (рекомендуется)

**Subject (Тема письма):**
```
New Contact Form Submission from {{from_name}}
```

**Content (Содержимое) - выберите "HTML" в EmailJS:**
```html
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <style>
        body {
            font-family: Arial, sans-serif;
            line-height: 1.6;
            color: #333;
            max-width: 600px;
            margin: 0 auto;
            padding: 20px;
        }
        .header {
            background-color: #dc2626;
            color: white;
            padding: 20px;
            text-align: center;
            border-radius: 5px 5px 0 0;
        }
        .content {
            background-color: #f9f9f9;
            padding: 20px;
            border: 1px solid #ddd;
            border-top: none;
            border-radius: 0 0 5px 5px;
        }
        .section {
            margin-bottom: 20px;
        }
        .section-title {
            font-weight: bold;
            color: #dc2626;
            margin-bottom: 10px;
            border-bottom: 2px solid #dc2626;
            padding-bottom: 5px;
        }
        .field {
            margin-bottom: 8px;
        }
        .field-label {
            font-weight: bold;
            display: inline-block;
            width: 150px;
        }
        .message-box {
            background-color: white;
            padding: 15px;
            border-left: 4px solid #dc2626;
            margin-top: 10px;
        }
        .footer {
            margin-top: 20px;
            padding-top: 20px;
            border-top: 1px solid #ddd;
            font-size: 12px;
            color: #666;
            text-align: center;
        }
    </style>
</head>
<body>
    <div class="header">
        <h2>New Contact Form Submission</h2>
    </div>
    <div class="content">
        <div class="section">
            <div class="section-title">Contact Information</div>
            <div class="field">
                <span class="field-label">Name:</span>
                {{from_name}}
            </div>
            <div class="field">
                <span class="field-label">Email:</span>
                <a href="mailto:{{from_email}}">{{from_email}}</a>
            </div>
            <div class="field">
                <span class="field-label">Phone:</span>
                <a href="tel:{{from_phone}}">{{from_phone}}</a>
            </div>
            <div class="field">
                <span class="field-label">Company:</span>
                {{company}}
            </div>
        </div>
        
        <div class="section">
            <div class="section-title">Product Interest</div>
            <div>{{product_interest}}</div>
        </div>
        
        <div class="section">
            <div class="section-title">Message</div>
            <div class="message-box">
                {{message}}
            </div>
        </div>
        
        <div class="footer">
            <p>This email was sent from the contact form on <a href="https://ilheavygroup.com">ilheavygroup.com</a></p>
            <p>Reply to: <a href="mailto:{{from_email}}">{{from_email}}</a></p>
        </div>
    </div>
</body>
</html>
```

## Инструкция по созданию шаблона в EmailJS:

1. Войдите в ваш аккаунт EmailJS
2. Перейдите в раздел **"Email Templates"**
3. Нажмите **"Create New Template"**
4. Заполните:
   - **Template Name:** "IL Heavy Group Contact Form"
   - **Subject:** Скопируйте тему из варианта выше
   - **Content:** Выберите тип (Plain Text или HTML) и вставьте соответствующий шаблон
5. Убедитесь, что все переменные в двойных фигурных скобках `{{variable_name}}` совпадают с теми, что указаны выше
6. Нажмите **"Save"**
7. Скопируйте **Template ID** (начинается с `template_`)

## Важные замечания:

- Все переменные должны быть в формате `{{variable_name}}` (двойные фигурные скобки)
- Переменные чувствительны к регистру: используйте точно `{{from_name}}`, а не `{{From_Name}}`
- Если поле не заполнено, будет отправлено "Not provided"
- HTML шаблон выглядит профессиональнее и легче читается
- EmailJS автоматически заменит переменные на реальные значения из формы

