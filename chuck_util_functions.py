import sublime, sublime_plugin
import subprocess
import os
import re

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
    accepts:  me.dir()  , me.dir(0),  me.dir(-1) , me.dir(-n)
    
    opens a sound file if the following is on a line:
        me.dir(-1) + "/audio/hihat_02.wav";

    opens a .ck file if it finds
        Machine.add(me.dir() + "/some_path.ck)";
    """

    try:
        pattern = "\"(.*" + file_type + ")\""
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
    sample_types = [".wav", ".aiff", ".mat"]  # extend if needed
    found_types = [(s in line_under_cursor) for s in sample_types]

    # enters here if the filetype is recognized.
    if any(found_types):
        for i, sample_type in enumerate(found_types):
            if sample_type:
                open_file(line_under_cursor, path, levels, sample_types[i])
        return

    # is it a .ck? 
    if ".ck" in line_under_cursor:
        open_file(line_under_cursor, path, levels, ".ck")


class ChuckOpener(sublime_plugin.TextCommand):
    def run(self, edit):
        view = self.view
        selections = view.sel()
        sel = view.line(selections[0])

        line_under_cursor = view.substr(sel)
        sublime.status_message(line_under_cursor)

        file_path = view.file_name()
        path = os.path.dirname(file_path)

        if not "me.dir(" in line_under_cursor:
            sublime.status_message("line must contain some form of me.dir()")
        else:
            check_file(line_under_cursor, path)


    def enabled(self):
        view = self.view
        selections = view.sel()

        if selections[0].a == selections[0].b:
            return True        
        
