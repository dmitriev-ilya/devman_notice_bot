from time import sleep
import textwrap
import logging

from environ import Env
import requests
import telegram


logger = logging.getLogger('telegram')


class TelegramLogsHandler(logging.Handler):

    def __init__(self, tg_bot, chat_id):
        super().__init__()
        self.chat_id = chat_id
        self.tg_bot = tg_bot

    def emit(self, record):
        log_entry = self.format(record)
        self.tg_bot.send_message(chat_id=self.chat_id, text=log_entry)


if __name__ == '__main__':
    env = Env()
    env.read_env()

    devman_api_token = env('DEVMAN_AUTH_TOKEN')
    devman_tg_bot_token = env('DEVMAN_BOT_TELEGRAM_TOKEN')
    user_chat_id = env('USER_CHAT_ID')

    bot = telegram.Bot(token=devman_tg_bot_token)

    logger.setLevel(logging.INFO)
    logger.addHandler(TelegramLogsHandler(bot, user_chat_id))

    logger.info('Бот запущен')

    headers = {
        'Authorization': f'Token {devman_api_token}'
    }

    devman_long_polling_url = 'https://dvmn.org/api/long_polling/'

    params = {
        'timestamp': None
    }

    while True:
        try:
            response = requests.get(
                devman_long_polling_url,
                headers=headers,
                params=params
            )
            response.raise_for_status()
            devman_api_content = response.json()
            if devman_api_content['status'] == 'timeout':
                params['timestamp'] = devman_api_content.get('timestamp_to_request')
                continue
            attempts = devman_api_content['new_attempts']
            for attempt in attempts:
                attempt_success = 'Работа принята преподавателем, можно приступать к следующему уроку!'
                if attempt['is_negative']:
                    attempt_success = 'Работа не принята!'
                message_text = f"""\
                    Ваша работа <b>{attempt['lesson_title']}</b> вернулась с проверки

                    <b>{attempt_success}</b>

                    <a href=\"{attempt['lesson_url']}\">Ссылка на урок</a>
                """
                dedented_message_text = textwrap.dedent(message_text)

                bot.send_message(
                    text=dedented_message_text,
                    chat_id=user_chat_id,
                    parse_mode=telegram.ParseMode.HTML
                )

        except requests.exceptions.ReadTimeout:
            continue
        except requests.exceptions.ConnectionError:
            logger.error('Соединение потеряно. Пытаюсь переподключиться')
            sleep(1)
        except Exception as err:
            logger.error('Бот упал с ошибкой:')
            logger.error(err, exc_info=True)
