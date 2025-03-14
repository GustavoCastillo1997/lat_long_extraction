import pandas as pd
import logging
from get_maps_url import get_maps_url
from user_agents import get_random_user_agent
from datetime import datetime
from verificator import string_type_verification, string_type_verification_reprocess


start_time = datetime.now()
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

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
        data = get_maps_url(link, headers)
        try:
            if string_type_verification(data, link, headers, lat_long_list) == 'success':
                success_counter += 1
            else:
                fail_counter += 1
        except IndexError:
            print(f'URL problemática: {data}')
            fail_counter += 1
    logging.info(f'{index + 1} linha(s) processada(s)!')

logging.info('Processo finalizado!')

first_processing_success = success_counter
first_processing_fails = fail_counter

print(f'Linha(s) com sucesso: {success_counter}\n')
print(f'Linha(s) com falha(s): {fail_counter}\n')
print(f'Tamanho da lista gerada: {len(lat_long_list)}\n')


success_counter = 0

if 1 in lat_long_list:
    for attempt_at_reprocessing in range(1, 3, 1):

        logging.info(f'\n\n***Tentativa de reprocessamento número {attempt_at_reprocessing}:***\n\n')
        logging.info('Reprocessando links problemáticos...\n')

        for index, item in enumerate(lat_long_list):

            headers = {'User-Agent': get_random_user_agent()}

            if item == 1:
                data = get_maps_url(links[index], headers)
                try:
                    if string_type_verification_reprocess(data, links, index, headers, lat_long_list) == 'success':
                        success_counter += 1
                except IndexError:
                    print(f'URL problemática: {data}')
                logging.info(f'Linha número {index + 1} reprocessada!')
            else:
                pass


print(f'Linha(s) com sucesso após reprocessamento: {success_counter}\n')

print(f'Resultante de linhas com sucesso: {first_processing_success + success_counter}')
print(f'Resultante de linhas com falhas: `{first_processing_fails - success_counter}')

print(lat_long_list)

end_time = datetime.now()
print(f'Tempo de execução: {end_time - start_time}\n')
