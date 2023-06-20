import logging

from re import search
from requests import RequestException

from exceptions import ParserFindTagException
from constants import EXPECTED_STATUS


def get_response(session, url):
    """Перехват ошибки RequestException"""
    try:
        response = session.get(url)
        response.encoding = 'utf-8'
        return response
    except RequestException:
        logging.exception(
            f'Возникла ошибка при загрузке страницы {url}',
            stack_info=True
        )


def find_tag(soup, tag, attrs=None):
    searched_tag = soup.find(tag, attrs=(attrs or {}))
    if searched_tag is None:
        error_msg = f'Не найден тег {tag} {attrs}'
        logging.error(error_msg, stack_info=True)
        raise ParserFindTagException(error_msg)
    return searched_tag


def regular_pattern(dict_of_keys):
    """Возвращает строку для поиска статусов"""
    string = ''
    for values in dict_of_keys.values():
        for value in values:
            string += value + '|'
    return string[:-1]


def get_status(text):
    """Возвращает статус из карточки"""
    pattern = regular_pattern(EXPECTED_STATUS)
    try:
        return search(pattern, text).group()
    except AttributeError:
        return 'unknown status'
