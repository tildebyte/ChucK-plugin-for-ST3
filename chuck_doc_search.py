'''
chuck_doc_search.py

author:             Dealga McArdle, 2013
functionality:      opens webbrowser at ugen doc#ugen if ugen is valid.
sublime API docs:   sublimetext.com/docs/2/api_reference.html

[1] Place this .py inside Data/Packages/User/..

[2] add the following line to you user keymap file
    { "keys": ["ctrl+shift+]"], "command": "chuck_doc_search" }

[3] to use, make a selection of for examples "ADSR", then hit ctrl+shift+]
    the webbrowser should pop up

'''
import sublime, sublime_plugin
import webbrowser

ugens = [ugen.lower() for ugen in [
    'dac', 'adc', 'blackhole', 'Gain', 'Noise', 'Impulse', 
    'Step', 'HalfRect', 'FullRect', 'ZeroX', 'BiQuad', 'Filter', 
    'OnePole', 'TwoPole', 'OneZero', 'TwoZero', 'PoleZero', 'LPF', 
    'HPF', 'BPF', 'BRF', 'ResonZ', 'FilterBasic', 'Dyno', 'DelayP', 
    'SndBuf', 'Phasor', 'SinOsc', 'PulseOsc', 'SqrOsc', 'TriOsc', 
    'SawOsc', 'GenX', 'LiSa', 'netout', 'netin', 'Pan2', 'Mix2', 
    'StkInstrument', 'BandedWG', 'BlowBotl', 'BlowHole', 'Bowed', 
    'Brass', 'Clarinet', 'Flute', 'Mandolin', 'ModalBar', 'Moog', 
    'Saxofony', 'Shakers', 'Sitar', 'StifKarp', 'VoicForm', 'FM', 
    'BeeThree', 'FMVoices', 'HevyMetl', 'PercFlut', 'Rhodey', 
    'TubeBell', 'Wurley', 'Delay', 'DelayA', 'DelayL', 'Echo', 
    'Envelope', 'ADSR', 'JCRev', 'NRev', 'PRCRev', 'Chorus', 
    'Modulate', 'PitShift', 'SubNoise', 'WvIn', 'WaveLoop', 'WvOut']]

doc_destinations = {
    "sndbuf2": ["/doc/program/ugen_full.html", "sndbuf"],
    "std": ["/doc/program/stdlib.html"],
    "vm": ["/doc/program/vm.html"],
    "array": ["/doc/language/array.html"],
    "help": ["/doc/language/"],  #overview
    "class": ["/doc/language/class.html"],
    "types": ["/doc/language/type.html"]
}

chuck_princeton = "http://chuck.cs.princeton.edu"

def open_browser(dest, specific=[]):
    url = chuck_princeton + dest
    if specific:
        url += "#" + specific
    webbrowser.open(url)

def std_special_search(ugen):
    std_search = ugen.split('.')
    if len(std_search) == 2:
        library_name, method = std_search
        if not library_name in ["std", "machine", "math"]:
            return
        open_browser(doc_destinations["std"][0], method)
        return True
    return

def find_docs(ugen):
    ugen = ugen.lower().strip()

    if "." in ugen:
        if std_special_search(ugen):
            return
        else:
            print("not recognized as Std / Machine / Math modules")

    if ugen in ugens:
        open_browser("/doc/program/ugen_full.html", ugen)
 
    # the online docs are not complete! 
    elif ugen in doc_destinations.keys():
        doc_url = doc_destinations[ugen]
        
        if len(doc_url) == 2:
            open_browser(*doc_url)
        else:
            webbrowser.open(chuck_princeton + doc_url[0])

    else:
        print('not a ugen, not known, or incorrect spelling')


class ChuckDocSearch(sublime_plugin.TextCommand):
    def run(self, edit):
        if not self.enabled():
            tmsg = 'you must select a ugen object'
            sublime.status_message(tmsg)
            return

        view = self.view
        sel = view.sel()[0]
        ugen = view.substr(sel)
        find_docs(ugen)

    def enabled(self):
        '''only allow 1 selection for version 0.1''' 

        sels   = self.view.sel()    # lists regions, 
        nsels  = len(sels)          # dir(sels[0]) for methods
        fsel   = sels[0]            # first selection

        if nsels == 1 and not fsel.empty():
            return True

