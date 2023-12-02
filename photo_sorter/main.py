"""
Script for importing and sorting photos.

The structure is
./Pictures/{yyyy}/{yyyy}-Q{q}/{yyyy}-{mm}-{dd}
./Videos/{yyyy}/{yyyy}-Q{q}/{yyyy}-{mm}-{dd}

"""

import argparse
import os
import datetime
import shutil
import logging

#Setting up logging
logging.basicConfig(filename=f'./logs/log_{datetime.datetime.now().strftime("%Y-%m-%dT%H-%M-%S")}.log', level=logging.INFO, format='%(asctime)s %(message)s')


def get_creation_datetime(file_name: str) -> datetime:
    """
    Get the creation datetime from a file

    """

    file_epoch = os.path.getmtime(file_name)
    file_date = datetime.datetime.fromtimestamp(file_epoch)
    
    return file_date


def get_file_type(file_name: str) -> str:
    """
    Gives the subfolder depending on the file extension

    """

    if file_name.endswith('.NEF'):
        subfolder = 'Pictures'
    elif file_name.endswith('.MOV'):
        subfolder = 'Videos'
    elif file_name.endswith('.JPG'):
        subfolder = 'PicturesJPG'
    else:
        subfolder = 'Overig'
    
    return subfolder


def get_filelist(dir:str) -> list:
    """
    Returns a list of all files

    """

    file_list = []

    for root, dirs, files in os.walk(dir):
    # select file name
        for file in files:
            file_list.append(os.path.join(root, file))
    
    return file_list


def make_folder(path):
    """
    Make the folder structure, if it not exists

    """

    if not os.path.isdir(path):
        os.makedirs(path)


def copy_file(file, destination, file_name):
    """
    copies the file to the destination.

    """

    target = os.path.join(destination, file_name)
    if not os.path.exists(target):
        shutil.copy2(file, target)
    else:
        logging.warning(f'File {file} is not copied because it already exists')


def read_arguments():
    """
    Accepts and requires two arguments:
    --in_dir : The folder to read
    --out_dir : The folder where the photos and videos are stored

    """

    parser = argparse.ArgumentParser()
    parser.add_argument('in_dir', help='Specifiy the input folder', type=str)
    parser.add_argument('out_dir', help='Specify the output folder', type=str)

    return parser.parse_args()
    

def run_app():
    """
    Main function. 

    """
    
    # Get CLI arguments
    arguments = read_arguments()
    logging.info(f'Start sorting and copying files')
    logging.info(f'Input folder: {arguments.in_dir}')
    logging.info(f'Output folder: {arguments.out_dir}')

    # Check if the folders exist
    if os.path.isdir(arguments.in_dir) and os.path.isdir(arguments.out_dir):
        # Make a list of all the files
        files = get_filelist(arguments.in_dir)
        for file in files:
            file_name = os.path.basename(file)
            if not file_name.startswith('.'):
                file_date = get_creation_datetime(file)
                file_type = get_file_type(file)
                quarter = int((int(file_date.strftime('%m')) / 4 )) + 1
                year = file_date.strftime('%Y')
                destination = os.path.join(arguments.out_dir, file_type, year , f'{year}-Q{quarter}', file_date.strftime('%Y-%m-%d'))
                make_folder(destination)
                copy_file(file, destination, file_name)

    else:
        logging.error("One or both of the directories is not a folder.")
    logging.info('Process finished')

if __name__ == '__main__':
    run_app()
