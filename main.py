from time import sleep

from environ import Env
import requests
import telegram


if __name__ == '__main__':
    env = Env()
    env.read_env()

    devman_api_token = env('DEVMAN_AUTH_TOKEN')
    devman_tg_bot_token = env('DEVMAN_BOT_TELEGRAM_TOKEN')
    user_chat_id = env('USER_CHAT_ID')

    bot = telegram.Bot(token=devman_tg_bot_token)

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
                params=params,
            )
            response.raise_for_status()
            response_context = response.json()
            if response_context['status'] == 'timeout':
                params['timestamp'] = response_context.get('timestamp_to_request')
                continue
            attempts = response_context['new_attempts']
            for attempt in attempts:
                message_text = [
                    f"Ваша работа <b>{attempt['lesson_title']}</b> вернулась с проверки",
                    "",
                    "<b>Работа принята преподавателем, можно приступать к следующему уроку!</b>",
                    "",
                    f"<a href=\"{attempt['lesson_url']}\">Ссылка на урок</a>"
                ]
                if attempt['is_negative']:
                    message_text[2] = "<b>Работа не принята!</b>"

                bot.send_message(
                    text='\n'.join(message_text),
                    chat_id=user_chat_id,
                    parse_mode=telegram.ParseMode.HTML
                )
        except requests.exceptions.ReadTimeout:
            print('The server is not responding. Trying again')
        except requests.exceptions.ConnectionError:
            print('Connection lost. Trying again')
            sleep(1)
