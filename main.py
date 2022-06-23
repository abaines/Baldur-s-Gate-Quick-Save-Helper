import os
import re
import datetime
import time

BALDURS_GATE_BASE_SAVE_FOLDER = "~\\Documents\\Baldur's Gate - Enhanced Edition\\save\\"


base_save_path = os.path.expanduser(BALDURS_GATE_BASE_SAVE_FOLDER)



def does_folder_name_match(folder_name):
    s = re.search("000000001-Quick-Save", folder_name)
    return bool(s)



def get_age_folder(folder_full_path):
    folder_stats = os.stat(folder_full_path)

    seconds = time.time()
    modified = folder_stats.st_mtime

    delta = seconds - modified

    return delta

    print(folder_full_path,"modified = {}".format(datetime.datetime.fromtimestamp(modified)), delta)





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



def find_quick_save(os_entries):
    for entry in os_entries:
        full_path = entry[0]
        files = entry[2]

        folder_name = os.path.basename(os.path.normpath(full_path))      

        folder_match = does_folder_name_match(folder_name)

        files_match = does_folder_contain_sub_files(full_path, files)

        if files_match and folder_match:
            folder_age = get_age_folder(full_path)
            print(folder_name,folder_match,files_match, folder_age)





def loop():

    list_folders = os.walk(base_save_path)

    find_quick_save(list_folders)

loop()
