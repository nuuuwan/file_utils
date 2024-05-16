import os
import sys

from utils import JSONFile


def get_dir_info_nocache(dir_path):
    assert os.path.isdir(dir_path), 'dir_path must be a valid directory'

    print(f'Analyzing {dir_path[:32]}...', end='\r')
    files = {}
    dirs = {}
    total_size = 0
    for child_name in os.listdir(dir_path):
        child_path = os.path.join(dir_path, child_name)
        if os.path.isdir(child_path):
            try:
                d_child = get_dir_info_nocache(child_path)
            except:
                print(f'⚠️ Error analyzing {child_path}')
                continue
            total_size += d_child['total_size']
            dirs[child_name] = d_child
        else:
            file_path = os.path.join(dir_path, child_name)
            file_size = os.path.getsize(file_path)
            files[child_name] = file_size
            total_size += file_size
    dir_name = os.path.basename(os.path.abspath(dir_path))
    d = dict(
        dir_name=dir_name,
        total_size=total_size,
    )
    if files:
        d['files'] = dict(sorted(files.items(), key=lambda x: x[1]))
    if dirs:
        d['dirs'] = dict(
            sorted(dirs.items(), key=lambda x: x[1]['total_size'])
        )
    return d


def get_dir_info(dir_path):
    info_path = os.path.join(dir_path, 'dir_info.json')
    info_path_file = JSONFile(info_path)
    if info_path_file.exists:
        return info_path_file.read()

    info = get_dir_info_nocache(dir_path)
    info_path_file.write(info)
    print(f'Wrote {info_path}.')
    print('')
    return info


def print_dir_info_only(d):
    MIN_FILE_SIZE = 1024 * 1024 * 0.9
    if d['total_size'] < MIN_FILE_SIZE:
        return
    size_m = d['total_size'] / 1024 / 1024
    print(f'{size_m:.1f}MB'.rjust(12), d['dir_name'])


def print_important_info(dir_path):
    print('')
    print(os.path.abspath(dir_path))

    dir_info = get_dir_info(dir_path)
    for dir in dir_info.get('dirs', {}).values():
        print_dir_info_only(dir)
    print('-' * 32)
    print_dir_info_only(dir_info)
    print('=' * 32)


if __name__ == '__main__':
    print_important_info(sys.argv[1])
