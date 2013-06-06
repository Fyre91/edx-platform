import os
import hashlib
import re

from .config import config


def is_empty(dictionary):
    if dictionary:
        return False
    return True


class cd:
    """
    Wrap change directory

    From http://stackoverflow.com/questions/431684/how-do-i-cd-in-python
    """

    def __init__(self, newPath):
        self.newPath = newPath

    def __enter__(self):
        self.savedPath = os.getcwd()
        os.chdir(self.newPath)

    def __exit__(self, etype, value, traceback):
        os.chdir(self.savedPath)


def hash_files_dirs(files, dirs=[]):
    """
    Hash files and directories together into a single hash.
    Hash files by contents and directories by children filenames.

    files and dirs are fully qualified paths.
    """
    print "testing hash_files_dirs"

    m = hashlib.md5()

    for file_path in files:
        print "adding file to hash: %s" % file_path
        with open(file_path, 'r') as f:
            body = f.read()
            m.update(body)

    for dir_path in dirs:
        print "adding dir to hash: %s" % dir_path
        children_names = os.listdir(dir_path)
        children_names_string = ', '.join(children_names)
        print "found children_names_string: %s" % children_names_string
        m.update(children_names_string)

    return m.hexdigest()


def has_changed_files_dirs(callback, files, dirs=[]):
    """
    if files in files or dirs differs from the stored hash, then run callback(true) and return true.
    else run callback(false) and return false

    callback is callable with one argument specifying whether the files/dirs have changed
    callback should do all modifications to files/dirs so that the new hash can be computed after
    """

    # cache_file_name = files[0].gsub(/\W+/, '-').sub(/-+$/, '')) + '.md5'
    cache_file_name = files[0]
    cache_file_name = re.sub(r'\W+', '-', cache_file_name)
    cache_file_name = re.sub(r'-+$', '', cache_file_name)
    cache_file_name += '.md5'

    cache_file = os.path.join(config['PREREQS_MD5_DIR'], cache_file_name)

    now_hash = hash_files_dirs(files, dirs)

    if os.path.isfile(cache_file):
        with open(cache_file, 'r') as f:
            last_hash = f.read()
    else:
        last_hash = None

    # if the file doesn't exist, or the hash has changed, write the new hash and return true
    if last_hash == now_hash:
        callback(False)
        return False
    else:
        callback(True)
        with open(cache_file, 'w') as f:
            f.write(hash_files_dirs(files, dirs))
        return True
