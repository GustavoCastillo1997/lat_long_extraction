import requests
import logging
import time


def get_maps_url(link_url: str, headers) -> str:
    response = requests.get(link_url, headers=headers)
    logging.info('Enviando requisição web...')
    logging.info(f'Status da requisição: {response.status_code}')
    time.sleep(0.5)
    return response.url


def get_maps_url_retry(link_url: str, headers, attempt: int, max_attempts: int) -> str:
    while attempt < max_attempts:
        logging.info('Formato da URL nao reconhecido!')
        logging.info(f'Realizando {attempt + 1}ª tentativa.')
        data = get_maps_url(link_url, headers=headers)
        if 'goo.gl' in data:
            attempt += 1
        else:
            logging.info(f'Nova URL: {data}')
            return data
        time.sleep(1)
