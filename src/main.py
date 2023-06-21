import csv
import logging
from re import compile, search
from urllib.parse import urljoin

from requests_cache import CachedSession
from bs4 import BeautifulSoup
from tqdm import tqdm

from configs import configure_argument_parser, configure_logging
from constants import (BASE_DIR, EXPECTED_STATUS,
                       MAIN_DOC_URL, MAIN_PEP_URL,
                       STATUS_PEP, STATUS_PEP_PATH, RESULTS_DIR)
from exceptions import ParserFindTagException
from outputs import control_output
from utils import find_tag, get_response, get_soup, get_status


def whats_new(session):
    whats_new_url = urljoin(MAIN_DOC_URL, 'whatsnew/')
    soup = get_soup(session, whats_new_url)
    sections_by_python = soup.select(
        '#what-s-new-in-python div.toctree-wrapper li.toctree-l1'
    )
    results = [('Ссылка на статью', 'Заголовок', 'Редактор, Автор')]
    for section in tqdm(sections_by_python):
        version_a_tag = find_tag(section, 'a')
        href = version_a_tag['href']
        version_link = urljoin(whats_new_url, href)
        response = get_response(session, version_link)
        if response is None:
            continue
        soup = BeautifulSoup(response.text, features='lxml')
        h1 = find_tag(soup, 'h1')
        dl = find_tag(soup, 'dl')
        dl_text = dl.text.replace('\n', ' ')
        results.append((version_link, h1.text, dl_text))
    return results


def latest_versions(session):
    soup = get_soup(session, MAIN_DOC_URL)
    ul_tags = soup.select('div.sphinxsidebarwrapper ul')

    for ul in ul_tags:
        if 'All versions' in ul.text:
            a_tags = ul.find_all('a')
            break
    else:
        raise ParserFindTagException('Ничего не нашлось')
    results = [('Ссылка на документацию', 'Версия', 'Статус')]
    pattern = r'Python (?P<version>\d\.\d+) \((?P<status>.*)\)'
    for a_tag in a_tags:
        link = a_tag['href']
        text_match = search(pattern, a_tag.text)
        if text_match is not None:
            version, status = text_match.groups()
        else:
            version, status = a_tag.text, ''
        results.append((link, version, status))
    return results


def download(session):
    downloads_url = urljoin(MAIN_DOC_URL, 'download.html')
    soup = get_soup(session, downloads_url)
    main_tag = find_tag(soup, 'div', attrs={'role': 'main'})
    table_tag = find_tag(main_tag, 'table', attrs={'class': 'docutils'})
    pdf_a4_tag = find_tag(
        table_tag, 'a', attrs={'href': compile(r'.+pdf-a4\.zip$')}
    )
    pdf_a4_link = pdf_a4_tag['href']
    archive_url = urljoin(downloads_url, pdf_a4_link)
    filename = archive_url.split('/')[-1]
    DOWNLOADS_DIR = BASE_DIR / 'downloads'
    DOWNLOADS_DIR .mkdir(exist_ok=True)
    archive_path = DOWNLOADS_DIR / filename
    response = session.get(archive_url)

    with open(archive_path, 'wb') as file:
        file.write(response.content)
    logging.info(f'Архив был загружен и сохранён: {archive_path}')


def pep(session):
    response = get_response(session, MAIN_PEP_URL)
    if response is None:
        return
    soup = BeautifulSoup(response.text, 'lxml')
    rows_tag = soup.select('#numerical-index tr')
    rows_tag.pop(0)
    results = []
    logs = []
    total_pep_statuses = {}
    total = 0
    for row in tqdm(rows_tag):
        pep_tag = find_tag(row, 'a', attrs={'href': compile(r'pep-\d+$')})
        status_tag = find_tag(row, 'abbr')
        pep_link = pep_tag['href']
        pep_url = urljoin(MAIN_PEP_URL, pep_link)
        if len(status_tag.text) == 1:
            pep_status = ''
        else:
            pep_status = status_tag.text[1]
        results.append([pep_url, pep_status])
        status = get_status(session, pep_url)
        if status != EXPECTED_STATUS[pep_status]:
            logs.append((f'Несовпадающие статусы {pep_url}. '
                         f'Статус в карточке: {status}. '
                         f'Ожидаемый статус: {EXPECTED_STATUS[pep_status]}'))
        total_pep_statuses[status] = total_pep_statuses.get(status, 0) + 1
        total += 1
    list(map(logging.warning, logs))

    RESULTS_DIR.mkdir(exist_ok=True)

    with open(STATUS_PEP_PATH, 'w') as file:
        writer = csv.writer(file)
        writer.writerow(['Статус', 'Количество'])

        for key, value in total_pep_statuses.items():
            writer.writerow([key, value])
        writer.writerow(['Всего', total])
    logging.info(f'Файл успешно создан: {STATUS_PEP_PATH}')


MODE_TO_FUNCTION = {
    'whats-new': whats_new,
    'latest-versions': latest_versions,
    'download': download,
    'pep': pep
}


def main():
    configure_logging()
    logging.info('Парсер запущен!')
    arg_parser = configure_argument_parser(MODE_TO_FUNCTION.keys())
    args = arg_parser.parse_args()
    logging.info(f'Аргументы командной строки: {args}')
    session = CachedSession()
    if args.clear_cache:
        session.cache.clear()
    parser_mode = args.mode
    results = MODE_TO_FUNCTION[parser_mode](session)
    if results is not None:
        control_output(results, args)
    logging.info('Парсер завершил работу.')


if __name__ == '__main__':
    main()
