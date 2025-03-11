import requests
import logging
import time


def get_maps_url(link_url: str, headers, proxies: dict) -> str:
    response = requests.get(link_url, headers=headers, proxies=proxies)
    logging.info('Enviando requisição web...')
    logging.info(f'Status da requisição: {response.status_code}')
    time.sleep(2)
    return response.url


logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
