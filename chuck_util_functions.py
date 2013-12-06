import sublime, sublime_plugin
import os
import re

class ChuckOpener(sublime_plugin.TextCommand):
    def run(self, edit):
        view = self.view
        selections = view.sel()
        sel = view.line(selections[0])

        line_under_cursor = view.substr(sel)
        sublime.status_message(line_under_cursor)

        if "Machine.add(" in line_under_cursor:

            # to retain consistency with how ChucK forces
            # paths to be written, for now I will also force
            # me.dir() to be present in the string, as a token
            # to mean current file path.

            if not "me.dir()" in line_under_cursor:
                sublime.status_message("Machine.add() must contain me.dir()")

            right_side = line_under_cursor.split("me.dir()")[1].strip() 
            try:
                m = re.search("\"\W(\w*.ck)", right_side)
                file_found = m.groups(0)[0]
                file_path = view.file_name()
                path = os.path.dirname(file_path)
                full_path_to_file = os.path.join(path, file_found)
                sublime.status_message(full_path_to_file)
            
                window = sublime.active_window()           
                window.open_file(full_path_to_file)

            except:
                print("failure!")
                pass


    def enabled(self):
        view = self.view
        selections = view.sel()

        if selections[0].a == selections[0].b:
            return True        
        
