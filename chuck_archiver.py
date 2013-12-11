import sublime, sublime_plugin
import os
import zipfile
import time

def postfix():
    """
    the default is:  "archive_postfix": "_%Y_%m_%d_%H-%M"
    see python docs for time.strftime.
    """
    settings = sublime.load_settings("ChucK.sublime-settings")
    postfix_re = settings.get("archive_postfix")
    return time.strftime(postfix_re)

def zip_current_directory(path):
    current_folder_name = path.split(os.sep)[-1]
    full_path = os.path.abspath(path)

    # store os.cwd , then switch to path of directory 
    old_dir = os.getcwd()
    os.chdir(path)
    zipname = current_folder_name + postfix() + ".zip"

    with zipfile.ZipFile(zipname, "w") as archive:
        for dirname, subdirs, files in os.walk(os.path.relpath(path)):
            if not dirname == ".":
                archive.write(dirname)

            for filename in files:
                if not filename.startswith(current_folder_name):
                    archive.write(os.path.join(dirname, filename))

    # this might be overkill, i don't know.
    os.chdir(old_dir) # revert back to python's original dir.
    print("wrote", zipname, ": success!")


class DirZipper(sublime_plugin.TextCommand):
    def run(self, edit):
        view = self.view
        file_path = view.file_name()
        path = os.path.dirname(file_path)
        zip_current_directory(path)

