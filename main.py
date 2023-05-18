import requests
from time import sleep
from environ import Env


if __name__ == '__main__':
    env = Env()
    env.read_env()

    devman_api_token = env('DEVMAN_AUTH_TOKEN')

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
            print(response_context)
        except requests.exceptions.ReadTimeout:
            print('The server is not responding. Trying again')
        except requests.exceptions.ConnectionError:
            print('Connection lost. Trying again')
            sleep(1)
