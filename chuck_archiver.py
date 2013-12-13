import sublime, sublime_plugin
import os
import zipfile
import time
import shutil

def get_settings():
    settings = sublime.load_settings("ChucK.sublime-settings")
    archiver_settings = []

    # alias for readability
    ap = archiver_settings.append
    
    ap(time.strftime(settings.get("archive_postfix")))
    ap(settings.get("archive_ignore_list"))
    ap(settings.get("archive_backup_dir"))

    return archiver_settings

def zip_current_directory(path):
    current_folder_name = path.split(os.sep)[-1]
    full_path = os.path.abspath(path)

    # store os.cwd , then switch to path of directory 
    old_dir = os.getcwd()
    os.chdir(path)

    postfix, ignore_list, backup_dir = get_settings()

    zipname = current_folder_name + postfix + ".zip"
    with zipfile.ZipFile(zipname, "w") as archive:
        for dirname, subdirs, files in os.walk(os.path.relpath(path)):
            
            # we can skip any directories in the List
            if any(token in dirname for token in ignore_list):
                continue

            if not dirname == ".":
                archive.write(dirname)

            for filename in files:
                if not filename.startswith(current_folder_name):
                    archive.write(os.path.join(dirname, filename))

    # user may have backup_dir configured, any files saved 
    # with ZipFile will be carbon copied to the directory 
    # listed in sublime settings file
    if os.path.exists(backup_dir):
        print("directory exists!")
        try:
            shutil.copy(zipname, backup_dir)
        except:
            print("something went wrong. stay calm.")
    else:
        print("no backup directory set, or not recognized.")
        print("check capitalization, relative paths and permissions")

    # this might be overkill, i don't know.
    os.chdir(old_dir) # revert back to python's original dir.
    print("wrote", zipname, ": success!")


class DirZipper(sublime_plugin.TextCommand):
    def run(self, edit):
        view = self.view
        file_path = view.file_name()
        path = os.path.dirname(file_path)
        zip_current_directory(path)

