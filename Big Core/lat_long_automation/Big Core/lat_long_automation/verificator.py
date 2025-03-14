import logging
from lat_long_extraction import lat_long_extract_1, lat_long_extract_2, lat_long_extract_3
from get_maps_url import get_maps_url_retry


def string_type_verification(data: str, link: str, headers, lat_long_list: list):
    if '@' in data:
        lat_long_list.append(lat_long_extract_1(data))
        return 'success'
    elif 'sorry' in data:
        lat_long_list.append(lat_long_extract_3(data))
        return 'success'
    elif 'goo.gl' in data:
        return string_type_not_valid_case(link, headers, lat_long_list)
    else:
        lat_long_list.append(lat_long_extract_2(data))
        return 'success'


def string_type_not_valid_case(link: str, headers, lat_long_list: list):
    data = get_maps_url_retry(link, headers)
    if isinstance(data, str):
        if 'goo.gl' in data:
            lat_long_list.append(1)
            logging.info('Não foi possível obter uma URL válida, passando para próxima linha.')
            return 'fail'
        # else:
    else:
        lat_long_list.append(1)
        logging.info('Não foi possível obter uma URL válida, passando para próxima linha.')
        return 'fail'


def string_type_verification_reprocess(data: str, links: list, index: int, headers, lat_long_list: list):
    if '@' in data:
        lat_long_list[index] = lat_long_extract_1(data)
        return 'success'
    elif 'sorry' in data:
        lat_long_list[index] = lat_long_extract_3(data)
        return 'success'
    elif 'goo.gl' in data:
        return string_type_not_valid_case_reprocess(links, index, headers, lat_long_list)
    else:
        lat_long_list[index] = lat_long_extract_2(data)
        return 'success'


def string_type_not_valid_case_reprocess(links: list, index: int, headers, lat_long_list: list):
    data = get_maps_url_retry(links[index], headers)
    if isinstance(data, str):
        if 'goo.gl' in data:
            lat_long_list[index] = 1
            logging.info('Não foi possível obter uma URL válida, passando para próxima linha.')
            return 'fail'
        # else:
    else:
        lat_long_list[index] = 1
        logging.info('Não foi possível obter uma URL válida, passando para próxima linha.')
        return 'fail'
