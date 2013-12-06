import sublime, sublime_plugin
import subprocess
import os
import re

def open_wav_file(line_under_cursor, path, wtype):
    """
    looks at the current line and converts from

    this:     me.dir(-1) + "/audio/hihat_02.wav" => string p;
    to this:  "/..fullpath ../audio/hihat_02.wav"

    accepts:  me.dir()  , me.dir(0),  me.dir(-1) , me.dir(-n)
    """

    # if empty between parenthesis quicly set to 0, else let regex find it.
    if "me.dir()" in line_under_cursor:
        levels = 0
    else:
        try:
            dir_pattern = "me.dir\((.*?)\)"
            m = re.search(dir_pattern, line_under_cursor)
            levels = int(m.groups(0)[0])
        except:
            print("not the expected form, see open_wav_file doc_string")
            return

    # find sample_name
    try:
        pattern = "\"(.*" + wtype + ")\""
        m = re.search(pattern, line_under_cursor)
        file_found = m.groups(0)[0]
        #full_path_to_file = os.path.join(path, file_found)
        sublime.status_message(file_found)
        path_strings = [s for s in file_found.split("/") if s]
        print(path, path_strings)

        dest_path = os.sep.join(path.split(os.sep)[:levels])
        full_wav_path = os.path.join(dest_path,*path_strings)

        wave_editor = "C:/Program Files/Audacity/audacity.exe"
        subprocess.call("{0} {1}".format(wave_editor, full_wav_path))

    except:
        print("failure wave!")
        pass

    pass

def open_chuck_file(line_under_cursor, path):

    right_side = line_under_cursor.split("me.dir()")[1].strip() 

    try:
        m = re.search("\"\W(\w*.ck)", right_side)
        file_found = m.groups(0)[0]
        full_path_to_file = os.path.join(path, file_found)
        sublime.status_message(full_path_to_file)
    
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
            # consistent with miniAudicle i'll force the use of
            # me.dir() to be present in the string to mean current 
            # file path. (later dir(-1) will be supported )
            if not "me.dir()" in line_under_cursor:
                sublime.status_message("Machine.add() must contain me.dir()")
            else:
                open_chuck_file(line_under_cursor, path)

        # purely convenience here, stick with how miniAudicle excepts this stuff
        # or you'll run into problems that miniAudicle will not play files because
        # it can't find paths.. it's a bit silly but hey that's the fun.
        # this expects something like :     
        #       me.dir(-1) + "/audio/hihat_02.wav" => string p;

        if "me.dir(" in line_under_cursor:
            sample_types = [".wav", ".aiff", ".mat"]  # extend if needed
            found_types = [(s in line_under_cursor) for s in sample_types]

            for idx, sample_type in enumerate(found_types):
                # stop at the first, and set this line off to the open_wav_file function
                if sample_type:
                    open_wav_file(line_under_cursor, path, sample_types[idx])



                




    def enabled(self):
        view = self.view
        selections = view.sel()

        if selections[0].a == selections[0].b:
            return True        
        
