import shutil
import sys
import os


def check_env():
    # command_env = ['samtools', 'bedtools', 'weblogo']
    command_env = ['samtools', 'bedtools']

    print('Checking the environment variable...')
    for i in command_env:
        if shutil.which(i):
            print('\n  ' + i + ' exists in environment variable.')
        else:
            print('\n  ' + i + ' is not in environment variable. You can install it using conda command.\n\n')


            print('    First, add the bioconda channel as well as the other channels bioconda depends on:')

            print('      conda config --add channels defaults')
            print('      conda config --add channels conda-forge')
            print('      conda config --add channels bioconda')

            print('\n')

            print('    Second, run the install command:')
            print('      conda install ' + i + '\n\n')
            sys.exit()

    print('\nThe commands required by the program already exist in the environment variables.')
    print('#####' * 20)
    print('\n')
    # print('\nProgram is running the next step\n\n')
    return

def copy_file(source_dir = None, dest_dir = None):
    source = source_dir
    destination = dest_dir
    source_files = os.listdir(source)
    for f in source_files:
        file = source + f
        shutil.copy(file, destination)
    return

def remove_dir(path = None):
    remove_dir = path
    shutil.rmtree(remove_dir)
    return





