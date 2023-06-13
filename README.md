# Сервис уведомлений для студентов devman.org 

Telegram-бот для получения уведомлений о статусе проверки работ на образовательной платформе [Devman](https://dvmn.org/)

![image](https://github.com/dmitriev-ilya/devman_notice_bot/assets/67222917/a95c94c8-6fc3-4644-9e28-aac8d3c5fe3c)


## Установка

Скачайте файлы из репозитория. Python3 должен быть уже установлен. 

Затем используйте `pip` (или `pip3`) для установки зависимостей:
```
pip install -r requirements.txt
```
Помимо этого, для работы понадобится создать файл `.env` в корневом каталоге проекта. Данный файл необходим для работы с переменными окружения и должен содержать в себе переменные: 
```
DEVMAN_AUTH_TOKEN=<DEVMAN_AUTH_TOKEN>
DEVMAN_BOT_TELEGRAM_TOKEN=<DEVMAN_BOT_TELEGRAM_TOKEN>
USER_CHAT_ID=<USER_CHAT_ID>
``` 
Для получения `DEVMAN_AUTH_TOKEN` необходимо обратиться к ментору или пройти урок "Отправляем уведомления о проверке работ" на Девмане. 

Также необходимо создать Telegram-бота для получения `DEVMAN_BOT_TELEGRAM_TOKEN`. Для этого нужно обратиться к [@BotFather](https://telegram.me/BotFather). Подробная инструкция по настройке и созданию бота приведена здесь - [Инструкция по созданию Telegram-бота](https://way23.ru/%D1%80%D0%B5%D0%B3%D0%B8%D1%81%D1%82%D1%80%D0%B0%D1%86%D0%B8%D1%8F-%D0%B1%D0%BE%D1%82%D0%B0-%D0%B2-telegram.html)

`USER_CHAT_ID` - ID пользователя в Telegram, которому бот будет отправлять уведомления. Узнать свой `USER_CHAT_ID`  можно, обратившись к боту [@userinfobot](https://telegram.me/userinfobot)

## Использование скриптов

Для запуска бота в консоли, находясь в папке с проектом, используйте следующую команду:

```
python3 main.py
```
