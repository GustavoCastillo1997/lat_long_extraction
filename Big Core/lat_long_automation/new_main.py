import pandas as pd
import logging
from get_maps_url import get_maps_url
from user_agents import get_random_user_agent
from lat_long_extraction import lat_long_extract_1, lat_long_extract_2, lat_long_extract_3
from datetime import datetime


start_time = datetime.now()
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
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
        data = get_maps_url(link, headers, proxies)
        try:
            if '@' in data:
                lat_long_extract_1(data, lat_long_list)
                success_counter += 1
            elif 'sorry' in data:
                lat_long_extract_3(data, lat_long_list)
                success_counter += 1
            elif 'goo.gl' in data:
                logging.info('Formato da URL nao reconhecido! Seguindo para próxima linha...')
                lat_long_list.append(1)
                fail_counter += 1
            else:
                lat_long_extract_2(data, lat_long_list)
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
