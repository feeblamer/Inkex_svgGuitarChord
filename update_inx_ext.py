import hashlib
import os
import shutil
import argparse
import logging
import sys

logging.basicConfig(level=logging.DEBUG, format='%(funcName)s %(message)s')

CURENT_DIR = './{}'
EXT_DIR = '/home/avm/.config/inkscape/extensions/{}'
inx_file = 'svgGuitarChord.inx'
py_file = 'svgGuitarChord.py'


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
    source_file = CURENT_DIR.format(file_name)
    extension_file = EXT_DIR.format(file_name)
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
                    CURENT_DIR.format(file_name),
                    EXT_DIR.format(file_name),
                 )
                logging.info(f'Файлы расширений {file_name} обновлен')
        else:
            logging.info(f'Расширение уже обновлено')

def backup_files(*file_names):
    for file_name in file_names:
        shutil.copy(
            EXT_DIR.format(file_name),
            EXT_DIR.format(file_name) + '.back',
        )
def restore_backup(*file_names):
   for file_name in file_names:
        shutil.copy(
            EXT_DIR.format(file_name) + '.back',
            EXT_DIR.format(file_name),
        )
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
