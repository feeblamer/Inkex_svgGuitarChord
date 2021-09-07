import hashlib
import os
import pathlib
import shutil
import argparse
import logging
import sys


logging.basicConfig(level=logging.DEBUG, format='%(funcName)s %(message)s')

EXTENSION_NAME = 'svgGuitarChord.{}'
CURENT_PATH = str(pathlib.Path().absolute()) + '/{}'
EXTENSIONS_PATH = str(pathlib.Path.home()) + '/.config/inkscape/extensions/{}'
inx_file = EXTENSION_NAME.format('inx')
py_file = EXTENSION_NAME.format('py')


def hash_sum(file_name, block_size=2 ** 12):
        h = hashlib.md5()
        with open(file_name, 'rb') as f:
            while True:
                hash_block = f.read(block_size)
                if not hash_block:
                    break
                h.update(hash_block)
        return h.hexdigest()


def is_update(file_name):
    source_file = CURENT_PATH.format(file_name)
    extension_file = EXTENSIONS_PATH.format(file_name)
    logging.info(f'Сравниваем хэш суммы для {source_file} и {extension_file}')
    if hash_sum(source_file) != hash_sum(extension_file):
        return True if os.stat(source_file).st_mtime > os.stat(extension_file).st_ctime else False
    return False


def update_extension(*file_names):
    for file_name in file_names:
        if is_update(file_name):
            answer = input('Файл в дериктори расширений старый, обновить Y/n?')
            if answer == 'y' or not answer:
                shutil.copy(
                    CURENT_PATH.format(file_name),
                    EXTENSIONS_PATH.format(file_name),
                 )
                logging.info(f'Файлы расширений {file_name} обновлен')
        else:
            logging.info(f'Расширение уже обновлено')

def backup_files(*file_names):
    for file_name in file_names:
        shutil.copy(
            EXTENSIONS_PATH.format(file_name),
            EXTENSIONS_PATH.format(file_name) + '.back',
        )


def restore_backup(*file_names):
    logging.info(f'Восстановление {file_names[0]}, {file_names[1]} из бэкапа.')
    for file_name in file_names:
        shutil.copy(
            EXTENSIONS_PATH.format(file_name) + '.back',
            EXTENSIONS_PATH.format(file_name),
        )
        logging.info(f'Файл {file_name} восстановлен.')


def create_parser(args):
    parser = argparse.ArgumentParser()
    parser.add_argument('--restore', action='store_true')
    return parser.parse_args(args)


def main():
    backup_files(inx_file, py_file)
    update_extension(inx_file, py_file)


if __name__ == '__main__':
    name_space = create_parser(sys.argv[1:])
    if name_space.restore:
        restore_backup(inx_file, py_file)
    else:
        main()
