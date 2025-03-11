import requests
import pandas as pd
import logging
import random
from datetime import datetime


def get_random_user_agent() -> str:
    return random.choice(user_agents)


def get_maps_url(link_url: str) -> str:
    response = requests.get(link_url, headers=headers, proxies=proxies)
    logging.info('Enviando requisição web...')
    logging.info(f'Status da requisição: {response.status_code}')
    return response.url


def lat_long_extract_1(url: str) -> None:
    logging.info('Tratando STRING - Tipo 1')
    url = url.split('@')
    url = url[1].split(',')
    lat_long = url[:2]
    lat_long_list.append(tuple(lat_long))


def lat_long_extract_2(url: str) -> None:
    logging.info('Tratando STRING - Tipo 2')
    url = url.split('/')
    url = url[5].split(",")
    url[1] = str(url[1].split("?"))
    url[1] = url[1][0].replace("+", "")
    lat_long = url
    lat_long_list.append(tuple(lat_long))


def lat_long_extract_3(url: str) -> None:
    logging.info('Tratando STRING - Tipo 3')
    url = url.split('%40')
    url = url[1].split(',')
    lat_long = url[:2]
    lat_long_list.append(tuple(lat_long))


start_time = datetime.now()
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

user_agents = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
    'Chrome/58.0.3029.110 Safari/537.3',
    'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:40.0) Gecko/20100101 Firefox/40.0',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
    'Chrome/58.0.3029.110 Safari/537.3 Edge/16.16299',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_5) AppleWebKit/537.36 (KHTML, like Gecko) '
    'Chrome/58.0.3029.110 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) '
    'Chrome/64.0.3282.140 Safari/537.36'
]

proxies = {'http': '179.107.159.103:8080'}


df_links = pd.read_excel("C:\\Users\\adm\\Documents\\eLog\\MONFREDINI\\LINK ENDEREÇOS AMAZON MONFREDINI.xlsx")
links = list(df_links['LINKS'])
lat_long_list = []

success_counter = 0
fail_counter = 0

logging.info('Iniciando processamento dos links...')

for index, link in enumerate(links):

    headers = {'User-Agent': get_random_user_agent()}

    if link == 0:
        logging.info('Célula vazia!')
        lat_long_list.append(link)
        success_counter += 1
    else:
        data = get_maps_url(link)
        try:
            if '@' in data:
                lat_long_extract_1(data)
                success_counter += 1
            elif 'sorry' in data:
                lat_long_extract_3(data)
                success_counter += 1
            elif 'goo.gl' in data:
                logging.info('Formato da URL nao reconhecido! Seguindo para próxima linha...')
                lat_long_list.append(1)
                fail_counter += 1
            else:
                lat_long_extract_2(data)
                success_counter += 1
        except IndexError:
            print(f'URL problemática: {data}')
            fail_counter += 1
    logging.info(f'{index + 1} linha(s) processada(s)!')

logging.info('Processo finalizado!')

print(lat_long_list)

end_time = datetime.now()
print(f'Tempo de execução: {end_time - start_time}\n')
print(f'Linha(s) com sucesso: {success_counter}\n')
print(f'Linha(s) com falha(s): {fail_counter}\n')
