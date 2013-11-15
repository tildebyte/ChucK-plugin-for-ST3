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

def open_browser(dest, specific=[]):
    chuck_princeton = "http://chuck.cs.princeton.edu"
    url = chuck_princeton + dest
    if specific:
        url += "#" + specific
    webbrowser.open(url)

def find_docs(ugen):
    ugen = ugen.lower().strip()

    if ugen == "std":
        open_browser("/doc/program/stdlib.html")
        return

    if ugen in ugens:
        open_browser("/doc/program/ugen_full.html", ugen)
    # the online docs are not complete! 
    elif ugen in ["SndBuf2"]:
        print("{0} is valid.. search for SndBuf instead".format(ugen))
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

