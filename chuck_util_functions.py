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
    if "me.dir()" in line_under_cursor:
        levels = 0
    else:
        try:
            dir_pattern = "me.dir\((.*?)\)"
            m = re.search(dir_pattern, line_under_cursor)
            levels = int(m.groups(0)[0])
        except:
            print("malformed me.dir(), remove spaces..")
            return None
    
    return levels

def open_wav_file(line_under_cursor, path, wtype):
    """
    looks at the current line and converts from
    this:     me.dir(-1) + "/audio/hihat_02.wav" => string p;
    to this:  "/..fullpath ../audio/hihat_02.wav"
    accepts:  me.dir()  , me.dir(0),  me.dir(-1) , me.dir(-n)
    """

    # if empty between parenthesis quicly set to 0, else let regex find it.
    levels = get_levels(line_under_cursor)
    if levels == None:
        print("please let us know in what context you get this error.")
        return 

    # find sample_name
    try:
        pattern = "\"(.*" + wtype + ")\""
        m = re.search(pattern, line_under_cursor)
        file_found = m.groups(0)[0]
        full_wav_path = get_full_path_to_file(levels, file_found, path)

        settings = sublime.load_settings("ChucK.sublime-settings")
        wave_editor = settings.get("wave_editor")
        subprocess.call("{0} {1}".format(wave_editor, full_wav_path))

    except:
        print("failure wave!")
        pass

    pass

def open_chuck_file(line_under_cursor, path):
    right_side = line_under_cursor.strip()

    levels = get_levels(line_under_cursor)
    if levels == None:
        print("please let us know in what context you get this error.")
        return 

    try:
        m = re.search("\"\W(\w*.ck)", right_side)
        file_found = m.groups(0)[0]
        full_path_to_file = get_full_path_to_file(levels, file_found, path)

        window = sublime.active_window()           
        window.open_file(full_path_to_file)

    except:
        print("failure!")
        pass


class ChuckOpener(sublime_plugin.TextCommand):
    def run(self, edit):
        view = self.view
        selections = view.sel()
        sel = view.line(selections[0])

        line_under_cursor = view.substr(sel)
        sublime.status_message(line_under_cursor)

        file_path = view.file_name()
        path = os.path.dirname(file_path)

        if "Machine.add(" in line_under_cursor:
            # consistent with miniAudicle forcing the use of
            # some form of me.dir() can use  empty, or 0 or -1, -2 etc..
            if not "me.dir(" in line_under_cursor:
                sublime.status_message("Machine.add() must contain me.dir()")
            else:
                open_chuck_file(line_under_cursor, path)

        # purely convenience here, stick with how miniAudicle expects this stuff
        # or you run into problems and it won't find files.  
        # normal form:   me.dir(-1) + "/audio/hihat_02.wav" => string p;  

        if "me.dir(" in line_under_cursor:
            sample_types = [".wav", ".aiff", ".mat"]  # extend if needed
            found_types = [(s in line_under_cursor) for s in sample_types]

            for idx, sample_type in enumerate(found_types):
                # stop immediately, go with first find.
                if sample_type:
                    open_wav_file(line_under_cursor, path, sample_types[idx])

    def enabled(self):
        view = self.view
        selections = view.sel()

        if selections[0].a == selections[0].b:
            return True        
        
