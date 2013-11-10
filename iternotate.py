'''
author: Dealga McArdle, 2013. 
 
http://www.sublimetext.com/docs/2/api_reference.html
 
Installation
- place iteration_notation.py in Data/Packages/User
- place dictionary entry in Keybindings, User
{ "keys": ["ctrl+shift+["], "command": "iternotate" }
 
Usage

Select the shorthand i..4 or i..iterable like below, select the full line 
(including whitespace if there). Then press ctrl+shift+[ 

The plugin will output
 
  // i..5
  for(0 => int i; i<5; i++){
      i;
  }
  
  // i..iterable
  for(0 => int i; i<iterable.cap(); i++){
      iterable[i];
  }
'''

import sublime, sublime_plugin


def check_is_loopform(istr):
    # returns non None only if everything seems ok.

    # does not support tabs, but could. I don't use tabs so meh.
    # some preprocessing, count spaces to the left, store this
    restr = istr.lstrip()
    spaces = len(istr) - len(restr)
    restr = restr.strip()
    
    # python 2.6 has no 'startswith'
    msg = """must be like:  i..n  or  i..iterable\n
- i can be any identifier\
- n can be any integer"""
    if (not ".." in restr):
        print(msg)
        return

    # explicitly split on space
    elements = restr.split("..")
    if (not len(elements) == 2):
        print(msg)
        return

    # will return information in last element about how to rewrite   
    return [spaces, elements, elements[1].isnumeric()]
      

def perform_replacement(istr):
    content = check_is_loopform(istr)

    if not content:
        print("read the debug statements carefully")
        return 

    ostr = """\
{0}for(0 => int {1}; {1}<{2}.cap(); {1}++){{
{0}    {2}[{1}];\n{0}}}"""

    ostr2 = """\
{0}for(0 => int {1}; {1}<{2}; {1}++){{
{0}    {1};\n{0}}}"""


    amount_space = " "*content[0]
    ident = content[1][0]  # i
    iterable = content[1][1]    # some_array or digit
    nbased = content[2]
    replace_string = ostr2 if nbased else ostr

    return replace_string.format(amount_space, ident, iterable)

def nothing_selected():
    sublime.status_message('nothing selected, fool')

class Iternotate(sublime_plugin.TextCommand):
    def run(self, edit):
        if not self.enabled():
            nothing_selected()
            return

        # sublime.status_message('here too')

        view = self.view
        sel = view.sel()[0]

        # just selected region
        selection = view.substr(sel)
        final = perform_replacement(selection)

        if not final:
            return

        #edit = view.begin_edit()    # stick onto undo stack
        self.view.replace(edit, sel, final)

        # finalize this edit, use as one undo level
        #view.end_edit(edit)

    
    def enabled(self):
        '''only allow 1 selection for version 0.1''' 

        sels   = self.view.sel()    # lists regions, 
        nsels  = len(sels)          # dir(sels[0]) for methods
        fsel   = sels[0]            # first selection

        if nsels == 1 and not fsel.empty():
            return True

