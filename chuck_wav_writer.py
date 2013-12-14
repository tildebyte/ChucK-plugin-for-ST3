import sublime
import sublime_plugin
import subprocess
import threading
import os

usage_string_ck_wav_writer = """\
the form to write in is:  // %> 20:new_wavename.
//  is to keep it a comment, ignored by ChucK.
%>  is to indicate you intend to use the comment to send commands.
20  indicates how many seconds to record.
:   is a delimiter for the next command.
new_wavename   can be anything you want, just don't use punctuation."""


class Ck_wav_writer(sublime_plugin.TextCommand):
    def run(self, edit):
        """
        a copy of wav_writer.ck must be located in the same folder 
        as the .ck you're trying to record. 

        usage: 
        (command line):                    chuck somefile.ck wav_writer.ck:20:new_wavename
        (wav_writer syntax)           :    // %> 20:new_wavename
        (wav_writer syntax with gain) :    // %> 20:new_wavename:0.89

        gain is a float value. (safe between 0.0 to 1.0)
        we can drop the first filename because it refers to the current file at the 
        time.
        """

        view = self.view
        selections = view.sel()

        if selections[0].a == selections[0].b:

            sel = view.line(selections[0])
            selection = view.substr(sel)
            
            song_duration = None
            wav_name = None
            max_amp = None
            try:

                # get the last portion after the comment, split and strip
                found_content = selection.rsplit("//", 1)[1]
                sides = found_content.split("%>")
                right_side = sides[1].strip()
                # song_duration, wav_name = [s.strip() for s in right_side.split(":")]
                found_parameters = [s.strip() for s in right_side.split(":")]
                if len(found_parameters) == 2:
                    max_amp = 1.0
                    song_duration, wav_name = found_parameters
                elif len(found_parameters) == 3:
                    song_duration, wav_name, max_amp = found_parameters

            except:
                print(usage_string_ck_wav_writer) 
                return

            finally:

                if not all([song_duration, wav_name, max_amp]):
                    return

                # compile commands for subprocess.
                file_path = view.file_name()
                file_name = os.path.basename(file_path)
                cwd = os.path.dirname(file_path)

                # rather than writing really ugly python code I will get the
                # user to specify where they have the wav_writer_wgain.ck and 
                # use sublime settings entry in stead. Conforming to how chuck 
                # expects the file paths would lead to headaches and terrible 
                # code. I refuse categorically.
                settings = sublime.load_settings("ChucK.sublime-settings")
                wave_writer_ck_path = settings.get("wav_writer_location") 
                wave_writer_ck_path += "wav_writer_wgain.ck"

                cc = [wave_writer_ck_path, str(song_duration), wav_name, str(max_amp)]
                record_commands = ":".join(cc)
                chuck_init_wav = ["chuck", file_name, record_commands, "-s"]
                print("\nsending:")
                print("> " +  " ".join(chuck_init_wav) + "\n")

                th = Ck_DiskWriter_Thread(cwd, chuck_init_wav)
                th.start()

        
class Ck_DiskWriter_Thread(threading.Thread):
    def __init__(self, cwd, chuck_init_wav):
        self.chuck_init_wav = chuck_init_wav
        self.cwd = cwd
        threading.Thread.__init__(self)

    def run(self):
        print("processing: ", end=" ")
        p = subprocess.Popen(self.chuck_init_wav, 
                        cwd=self.cwd,
                        stdout=subprocess.PIPE, 
                        stderr=subprocess.STDOUT, 
                        shell=True).communicate()

        # don't need to show these...
        # if p:
        #     print(p[0].decode())
        print("complete! ")
