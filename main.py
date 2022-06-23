import os
import re
import datetime
import time

BALDURS_GATE_BASE_SAVE_FOLDER = "~\\Documents\\Baldur's Gate - Enhanced Edition\\save\\"


base_save_path = os.path.expanduser(BALDURS_GATE_BASE_SAVE_FOLDER)



def does_folder_name_match_quick_save(folder_name):
    s = re.search(r"000000001-Quick-Save", folder_name)
    return bool(s)



def get_age_folder(folder_full_path):
    folder_stats = os.stat(folder_full_path)

    seconds = time.time()
    modified = folder_stats.st_mtime

    delta = seconds - modified

    return delta



def does_folder_contain_sub_files(folder_full_path, files):
    expected_files = [
        'BALDUR.bmp',
        'BALDUR.gam',
        'BALDUR.SAV',
        'PORTRT0.bmp',
    ]

    for expected_file in expected_files:
        if expected_file not in files:
            return False
    
    for file in files:
        file_full_path = os.path.join(folder_full_path, file)

        file_size = os.path.getsize(file_full_path)

        if file_size<= 0:
            return False


    return True


def get_folder_base_name(full_path):
    return os.path.basename(os.path.normpath(full_path))      



def find_quick_save(os_entries):
    for entry in os_entries:
        full_path = entry[0]
        files = entry[2]

        folder_name = get_folder_base_name(full_path)

        folder_match = does_folder_name_match_quick_save(folder_name)

        files_match = does_folder_contain_sub_files(full_path, files)

        if files_match and folder_match:
            folder_age = get_age_folder(full_path)
            happy_age = folder_age > 2 and folder_age < 60*60

            if happy_age:
                return full_path



def get_save_folder_index(folder_name):
    s = re.match(r"^(\d{9})\-", folder_name)
    if s:
        text = s.groups()[0]
        return int( text ) 



def find_next_available_save_folder_name(os_entries):


    for entry in os_entries:
        full_path = entry[0]

        folder_name = get_folder_base_name(full_path)

        is_save = get_save_folder_index(folder_name)

        if is_save:
            print(folder_name, is_save)
        else:
            print(folder_name, "!"*100, is_save)




def loop():

    list_folders = os.walk(base_save_path)

    safe_quick_save = find_quick_save(list_folders)

    print(safe_quick_save)

    print("-"*80)

    find_next_available_save_folder_name(list_folders)

loop()
