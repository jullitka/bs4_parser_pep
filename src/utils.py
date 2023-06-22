from bs4 import BeautifulSoup
from requests import RequestException

from exceptions import FindStatusException, ParserFindTagException


def get_response(session, url, encoding='utf-8'):
    """Перехват ошибки RequestException"""
    try:
        response = session.get(url)
        response.encoding = encoding
        return response
    except RequestException:
        error_msg = f'Возникла ошибка при загрузке страницы {url}'
        raise RequestException(error_msg)


def find_tag(soup, tag, attrs=None):
    searched_tag = soup.find(tag, attrs=(attrs or {}))
    if searched_tag is None:
        error_msg = f'Не найден тег {tag} {attrs}'
        raise ParserFindTagException(error_msg)
    return searched_tag


def get_soup(session, url, features='lxml'):
    response = get_response(session, url)
    try:
        soup = BeautifulSoup(response.text, features)
        return soup
    except AttributeError:
        error_msg = f'Пустой response  при загрузке страницы {url}'
        raise AttributeError(error_msg)


def get_status(session, url):
    """Возвращает статус из карточки"""
    soup = get_soup(session, url)
    table_tag = soup.select('dl.rfc2822.field-list.simple dt')
    for tag in table_tag:
        if tag.text == 'Status:':
            return tag.find_next_sibling('dd').text
    STATUS_ERROR_MSG = 'Не найден статус в карточке PEP '
    raise FindStatusException(STATUS_ERROR_MSG)
