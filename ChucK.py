import sublime
import sublime_plugin
import sys
import subprocess
import threading
import webbrowser

try:
    from Queue import Queue, Empty
except ImportError:
    from queue import Queue, Empty  # python 3.x

ON_POSIX = 'posix' in sys.builtin_module_names


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
            # print "Creating output view for ChucK"
            Ck_loop_vmCommand.panel_name = "ChucK"
            Ck_loop_vmCommand.output_view = self.window.get_output_panel(Ck_loop_vmCommand.panel_name)

        # start ChucK
        if Ck_loop_vmCommand.chuck_thread is None or not Ck_loop_vmCommand.chuck_thread.isAlive():
            settings = sublime.load_settings("ChucK.sublime-settings")
            ck_dir = settings.get("ck_dir")
            ck_exe = settings.get("ck_exe")
            # print "Starting ChucK : "+ck_dir+ck_exe
            Ck_loop_vmCommand.chuck_process = subprocess.Popen([ck_exe, '--loop', '-v2'], cwd=ck_dir, bufsize=1, close_fds=ON_POSIX, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, universal_newlines=True, shell=True)
            Ck_loop_vmCommand.chuck_queue = Queue()
            Ck_loop_vmCommand.chuck_thread = threading.Thread(target=enqueue_output, args=(Ck_loop_vmCommand.chuck_process.stdout, Ck_loop_vmCommand.chuck_queue))
            Ck_loop_vmCommand.chuck_thread.daemon = True  # thread dies with the program
            Ck_loop_vmCommand.chuck_thread.start()
            # print "ChucK has started"

        sublime.set_timeout(self.scrolldown, 100)
        sublime.set_timeout(self.poll, 1000)

    def poll(self):
        # continue while chuck is running
        if Ck_loop_vmCommand.chuck_thread is not None and Ck_loop_vmCommand.chuck_thread.isAlive():
            ckReturnedSomething = True
            somethingHappened = False

            edit = Ck_loop_vmCommand.output_view.begin_edit()

            while ckReturnedSomething:
                try:
                    line = Ck_loop_vmCommand.chuck_queue.get_nowait()
                except Empty:
                    ckReturnedSomething = False
                else:
                    somethingHappened = True
                    Ck_loop_vmCommand.output_view.insert(edit, Ck_loop_vmCommand.output_view.size(), line.decode("utf-8", "ignore"))

            Ck_loop_vmCommand.output_view.end_edit(edit)

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
        # print "Stopping ChucK"
        if Ck_loop_vmCommand.chuck_thread is not None and Ck_loop_vmCommand.chuck_thread.isAlive():
            Ck_loop_vmCommand.chuck_process.stdin.write("--kill")
            Ck_loop_vmCommand.chuck_process.stdin.flush()


# command to send the current line to chuck
class Ck_add_shredCommand(sublime_plugin.WindowCommand):
    def run(self):
        if Ck_loop_vmCommand.chuck_thread is not None and Ck_loop_vmCommand.chuck_thread.isAlive():
            view = self.window.active_view()
            sel = view.sel()
            point = sel[0]
            line = view.line(point)
            line_str = view.substr(line)
            # if the selection comprises of only character and it's a ( or ), expand
            if (point.a == point.b) and (line_str[0] in '()'):
                view.run_command("expand_selection", {"to": "brackets"})
            sel = view.sel()
            region = view.line(sel[0])
            lines = view.substr(region).split("\n")
            for l in lines:
                Ck_loop_vmCommand.chuck_process.stdin.write(l.encode("utf-8", "ignore")+"\n")
            Ck_loop_vmCommand.chuck_process.stdin.write("\x0c")
            Ck_loop_vmCommand.chuck_process.stdin.flush()


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


# search for help on current word on SCCode.org
class Ck_ugen_helpCommand(sublime_plugin.WindowCommand):
    ckcode_ugen_url = None

    def run(self):
        if Ck_ugen_helpCommand.ckcode_ugen_url is None:
            settings = sublime.load_settings("ChucK.sublime-settings")
            Ck_ugen_helpCommand.ckcode_ugen_url = settings.get("ckcode_ugen_url")
        view = self.window.active_view()
        sel = view.sel()
        point = sel[0]
        word = view.word(point)
        webbrowser.open_new_tab(Ck_ugen_helpCommand.ckcode_ugen_url+view.substr(word))
