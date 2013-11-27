'''
author: Dealga McArdle, 2013. 
 
http://www.sublimetext.com/docs/3/api_reference.html

Write the shorthand i..4 or i..iterable like below 
then press ctrl+shift+[ (or whatever combo you've set)

The plugin will output
 
  // i..5
  for(0 => int i; i<5; i++){
      i;
  }

  // i..num_times
  for(0 => int i; i<num_times; i++){
      i;
  }
  
  // i..iterable[   or   i..iterable[]
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
    msg = """must be like:  i..n  or  i..num_items  or  i..iterable[]
- i can be any identifier
- n can be any integer
- num_items can be any variable that represents a number
- iterable[] can be any Object with a .cap() method returning a number"""
    if (not ".." in restr):
        print(msg)
        return

    # explicitly split on space
    elements = restr.split("..")
    if (not len(elements) == 2):
        print(msg)
        return

    # will return information in last element about how to rewrite
    # added [] as well because sublime will often autocomplete it anyway.
    if any([elements[1].endswith(opt) for opt in ("[", "[]")]):
        
        # remove last char.
        elements[1] = elements[1][:-1]
        # quick check if last char is part of an array notation, remove that. 
        if elements[1][-1] == "[":
            elements[1] = elements[1][:-1]
        
        is_number = False
    else:
        is_number = True

    return [spaces, elements, is_number]
      

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
    sublime.status_message('nothing selected, or not iterable')

class Iternotate(sublime_plugin.TextCommand):
    def run(self, edit):
        if not self.enabled():
            nothing_selected()
            return

        view = self.view
        selections = view.sel()
        sel = view.line(selections[0])

        # find begin and end points of line, make new Region reference
        full_line_region = sublime.Region(sel.a, sel.b) 

        # get all characters from line
        selection = view.substr(sel)
        final = perform_replacement(selection)

        if not final: 
            return

        view.replace(edit, full_line_region, final)


    def enabled(self):
        sels   = self.view.sel()    # lists regions, 
        if len(sels) > 1:
            print("you have several selections, unselect all")
            return False

        fsel = sels[0]              # caret position, if no selection.
        if not (fsel.a == fsel.b):
            print("unselect everything, cursor caret on the line is sufficient")
            return False

        return True

