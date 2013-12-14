import sublime, sublime_plugin
import os
import re
import sys
import subprocess
from subprocess import PIPE
from ChucK.chuck_python import send_multi_gist as gists

def get_full_path_to_file(levels, file_found, path):
    path_strings = [s for s in file_found.split("/") if s]
    dest_path = os.sep.join(path.split(os.sep)[:levels])
    return os.path.join(dest_path,*path_strings)

def get_levels(line_under_cursor):
    # if empty between parenthesis quicly set to 0, else let regex find it.
    levels = None
    if "me.dir()" in line_under_cursor:
        levels = 0
    else:
        try:
            dir_pattern = "me.dir\((.*?)\)"
            m = re.search(dir_pattern, line_under_cursor)
            levels = int(m.groups(0)[0])
        except:
            print("malformed me.dir(), remove spaces..")

    return levels

def open_file(line_under_cursor, path, levels, file_type):
    """
    accepts:  me.dir()  , me.dir(0),  me.dir(-n)
    :         me.dir(-1) + "/audio/hihat_02.wav";
    :         Machine.add(me.dir() + "/some_path.ck)";
    """

    try:
        pattern = "\"(.*" + file_type + ")\"?"
        m = re.search(pattern, line_under_cursor)
        file_found = m.groups(0)[0]
        full_path = get_full_path_to_file(levels, file_found, path)

    except:
        print("failure! ", file_type)
        return

    finally:
        if file_type == ".ck":
            window = sublime.active_window()           
            window.open_file(full_path)

        # has to be a sound file
        else:
            settings = sublime.load_settings("ChucK.sublime-settings")
            wave_editor = settings.get("wave_editor")
            subprocess.call("{0} {1}".format(wave_editor, full_path))


def check_file(line_under_cursor, path):
    """ figures out if the line contains a file in the expected notation."""

    # does it have a path? if not, ditch return no ifs ands or buts
    levels = get_levels(line_under_cursor)
    if levels == None:
        print("please let us know in what context you get this error.")
        return 

    # is it a sound?
    file_types = [".wav", ".aiff", ".mat", ".ck"]  # extend if needed
    found_types = [(s in line_under_cursor) for s in file_types]

    # enters here if the filetype is recognized.
    if any(found_types):
        for i, file_type in enumerate(found_types):
            if file_type:
                open_file(line_under_cursor, path, levels, file_types[i])
        return


def probe_chuck():

    try:
        k = subprocess.Popen(["chuck", "--probe"], stdout=PIPE, stderr=PIPE)
        out, err = k.communicate()

        # finds the last section, generally midi information.
        info = "".join(err.decode().split('\r\n')[-1:])
        for i in info.split("[chuck]:"):
            print(i)

    except:
        print("this may be difficult to debug, ..please let me (zeffii) know")

def attempt_upload(self, view):
    file_path = view.file_name()
    path = os.path.dirname(file_path)
    current_folder_name = path.split(os.sep)[-1]
    # full_path = os.path.abspath(path)

    # a convenience function for checking if a file can 
    # be omitted because it starts with the same name
    same_name = lambda filename: filename.startswith(current_folder_name)

    def text_based(filename):
        gistable_files = ["ck", "txt", "md", "py", "csv"]
        try:
            if filename.split(".")[-1] in gistable_files:
                print(filename.split(".")[-1])
                return True
        except:
            print("bleeeeep! ignoring files without extensions..")
        
        return False

    gist_files_dict = {}
    
    # no folders, just files. for now.
    for dirname, subdirs, files in os.walk(os.path.relpath(path)):
        
        # only do this folder.
        if not dirname.endswith(current_folder_name):
            continue

        for filename in files:
            if not same_name(filename) and text_based(filename):
                print("adding: ", filename)
                this_file_path = os.path.join(dirname, filename)

                # add filename as key and file content as sub_dict
                with open(this_file_path) as current_file:
                    file_content = "".join(current_file.readlines())
                    print(file_content)
                    gist_files_dict[filename] = {"content": file_content}

        public = True
        gists.upload(gist_files_dict, current_folder_name, public)

    return


class ChuckOpener(sublime_plugin.TextCommand):
    def run(self, edit):
        view = self.view
        selections = view.sel()
        sel = view.line(selections[0])

        line_under_cursor = view.substr(sel)
        sublime.status_message(line_under_cursor)

        file_path = view.file_name()
        path = os.path.dirname(file_path)

        if "MidiIn" in line_under_cursor:
            probe_chuck()
            return

        # dispense with the %> prefix, it's a pain to type
        if "// gist -m" in line_under_cursor:
            attempt_upload(self, view)
            return

        if not "me.dir(" in line_under_cursor:
            sublime.status_message("line must contain some form of me.dir()")
        else:
            check_file(line_under_cursor, path)


    def enabled(self):
        view = self.view
        selections = view.sel()

        if selections[0].a == selections[0].b:
            return True        
        
