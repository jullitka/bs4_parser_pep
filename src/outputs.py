import csv
import logging
from datetime import datetime

from prettytable import PrettyTable

from constants import BASE_DIR, DATETIME_FORMAT


def default_output(results, *args):
    for row in results:
        print(*row)


def pretty_output(results, *args):
    table = PrettyTable()
    table.field_names = results[0]
    table.align = 'l'
    table.add_rows(results[1:])
    print(table)


def file_output(results, cli_args):
    results_dir = BASE_DIR / 'results'
    results_dir.mkdir(exist_ok=True)
    parser_mode = cli_args.mode
    now_formatted = datetime.now().strftime(DATETIME_FORMAT)
    file_name = f'{parser_mode}_{now_formatted}.csv'
    file_path = results_dir / file_name
    with open(file_path, 'w', encoding='utf-8') as f:
        csv.writer(f, dialect='unix').writerows(results)
    logging.info(f'Файл с результатами был сохранён: {file_path}')


OUTPUTS = {
    'pretty': pretty_output,
    'file': file_output,
    None: default_output
}


def control_output(results, cli_args):
    output = cli_args.output
    OUTPUTS[output](results, cli_args)
