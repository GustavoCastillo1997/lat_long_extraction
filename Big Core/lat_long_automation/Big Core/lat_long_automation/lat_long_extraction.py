import logging


def lat_long_extract_1(url: str) -> tuple:
    logging.info('Tratando STRING - Tipo 1')
    url = url.split('@')
    url = url[1].split(',')
    lat_long = url[:2]
    return tuple(lat_long)


def lat_long_extract_2(url: str) -> tuple:
    logging.info('Tratando STRING - Tipo 2')
    url = url.split('/')
    url = url[5].split(",")
    url[1] = str(url[1].split("?"))
    url[1] = url[1][0].replace("+", "")
    lat_long = url
    return tuple(lat_long)


def lat_long_extract_3(url: str) -> tuple:
    logging.info('Tratando STRING - Tipo 3')
    url = url.split('%40')
    url = url[1].split(',')
    lat_long = url[:2]
    return tuple(lat_long)


logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
