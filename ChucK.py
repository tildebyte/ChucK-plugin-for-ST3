import sublime
import sublime_plugin
import sys
import subprocess
import threading
import webbrowser
import os
from queue import Queue, Empty

ON_POSIX = 'posix' in sys.builtin_module_names

def command_dispatcher(chuck_console, commands):
    print("doing command:", commands)
    chuck_console.stdin.write(commands)
    chuck_console.stdin.write("\x0c")
    chuck_console.stdin.flush()

def kill_chuck():
    subprocess.call(["chuck", "--kill"])        
    print("ending a chuck process!")
    return

def com_parser(line_under_cursor, file_name):
    right_side = None

    try:
        found_content = line_under_cursor.rsplit("//", 1)[1]
        found_content = found_content.strip()

        if found_content in ("kill", "%> -k"):
            return "kill"

        # if found_content == "chuck --shell":
        #     return "shell"

        sides = found_content.split("%>")
        right_side = sides[1].strip()

        # this will refer to the name of the current file.ck
        if "this" in right_side:
            right_side = right_side.replace("this", file_name)
       
    except: 
        print("unparsable")
        return

    return right_side


def enqueue_output(out, queue):
    for line in iter(out.readline, b''):
        queue.put(line)
    out.close()


# command to start ChucK interpreter chuck
class Ck_loop_vmCommand(sublime_plugin.WindowCommand):
    chuck_process = None
    chuck_queue = None
    chuck_thread = None
    output_view = None
    panel_name = None

    def run(self):
        # create output panel
        if Ck_loop_vmCommand.output_view is None:
            print("Creating output view for ChucK")
            Ck_loop_vmCommand.panel_name = "ChucK"
            Ck_loop_vmCommand.output_view = self.window.get_output_panel(Ck_loop_vmCommand.panel_name)

        # start ChucK
        if Ck_loop_vmCommand.chuck_thread is None or not Ck_loop_vmCommand.chuck_thread.isAlive():
            settings = sublime.load_settings("ChucK.sublime-settings")
            ck_dir = settings.get("ck_dir")
            ck_exe = settings.get("ck_exe")
            print("Starting ChucK : "+ck_dir + " " + ck_exe)
            
            chuck_init = [ck_exe, '--shell']

            Ck_loop_vmCommand.chuck_process = subprocess.Popen(chuck_init, 
                cwd=ck_dir, bufsize=1, 
                close_fds=ON_POSIX, 
                stdin=subprocess.PIPE, 
                stdout=subprocess.PIPE, 
                stderr=subprocess.STDOUT, 
                universal_newlines=True, shell=True)
                
            Ck_loop_vmCommand.chuck_queue = Queue()

            threading_args = (
                Ck_loop_vmCommand.chuck_process.stdout, 
                Ck_loop_vmCommand.chuck_queue)

            Ck_loop_vmCommand.chuck_thread = threading.Thread(
                target=enqueue_output, 
                args=threading_args)
            
            # thread dies with the program
            Ck_loop_vmCommand.chuck_thread.daemon = True  
            Ck_loop_vmCommand.chuck_thread.start()
            print("ChucK has started")

        sublime.set_timeout(self.scrolldown, 100)
        sublime.set_timeout(self.poll, 1000)

    def poll(self):
        # continue while chuck is running
        if Ck_loop_vmCommand.chuck_thread is not None and Ck_loop_vmCommand.chuck_thread.isAlive():
            ckReturnedSomething = True
            somethingHappened = False

            # edit = Ck_loop_vmCommand.output_view.begin_edit()

            while ckReturnedSomething:
                try:
                    line = Ck_loop_vmCommand.chuck_queue.get_nowait()
                except Empty:
                    ckReturnedSomething = False
                else:
                    somethingHappened = True
                    size = Ck_loop_vmCommand.output_view.size()
                    print('line:', line)
                    content =  line.decode("utf-8", "ignore")
                    Ck_loop_vmCommand.output_view.insert(edit, size, content)

            # Ck_loop_vmCommand.output_view.end_edit(edit)

            if somethingHappened:
                sublime.set_timeout(self.scrolldown, 100)

            sublime.set_timeout(self.poll, 500)

    def scrolldown(self):
        if Ck_loop_vmCommand.output_view is not None:
            Ck_loop_vmCommand.output_view.show(Ck_loop_vmCommand.output_view.size())  # scroll down
            self.window.run_command("show_panel", {"panel": "output." + Ck_loop_vmCommand.panel_name})


# command to stop ChucK interpreter chuck
class Ck_kill_vmCommand(sublime_plugin.WindowCommand):
    def run(self):

        print("Stopping ChucK")
        if Ck_loop_vmCommand.chuck_thread is not None and Ck_loop_vmCommand.chuck_thread.isAlive():
            print('enters here')
            Ck_loop_vmCommand.chuck_process.stdin.write("--kill")
            Ck_loop_vmCommand.chuck_process.stdin.write("\x0c")
            Ck_loop_vmCommand.chuck_process.stdin.flush()
            # subprocess.call(["chuck", "--kill"])   


# command to send the current line to chuck
class Ck_add_shredCommand(sublime_plugin.WindowCommand):
    def run(self):
        if Ck_loop_vmCommand.chuck_thread is not None and Ck_loop_vmCommand.chuck_thread.isAlive():
            view = self.window.active_view()

            print("still allive")
            file_path = view.file_name()
            file_name = os.path.basename(file_path)

            selections = view.sel()
            if not selections[0].a == selections[0].b:
                print("see com shell documentation")
                return
            
            sel = view.line(selections[0])
            line_under_cursor = view.substr(sel)
            
            commands = com_parser(line_under_cursor, file_name)
            if not commands:
                return

            if commands == "kill":
                commands = "--kill"

            command_dispatcher(Ck_loop_vmCommand.chuck_process, commands)


# command to show the ChucK console
class Ck_show_consoleCommand(sublime_plugin.WindowCommand):
    def run(self):
        if Ck_loop_vmCommand.output_view is not None:
            Ck_loop_vmCommand.output_view.show(Ck_loop_vmCommand.output_view.size())  # scroll down
            self.window.run_command("show_panel", {"panel": "output." + Ck_loop_vmCommand.panel_name})


# hide console
class Ck_hide_consoleCommand(sublime_plugin.WindowCommand):
    def run(self):
        if Ck_loop_vmCommand.output_view is not None:
            Ck_loop_vmCommand.output_view.show(Ck_loop_vmCommand.output_view.size())  # scroll down
            self.window.run_command("hide_panel", {"panel": "output." + Ck_loop_vmCommand.panel_name})


# stop all sounds
class Ck_clear_vmCommand(sublime_plugin.WindowCommand):
    def run(self):
        if Ck_loop_vmCommand.chuck_thread is not None and Ck_loop_vmCommand.chuck_thread.isAlive():
            Ck_loop_vmCommand.chuck_process.stdin.write("remove.all")
            Ck_loop_vmCommand.chuck_process.stdin.flush()


