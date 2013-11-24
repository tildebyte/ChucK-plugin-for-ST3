ChucK-plugin-for-ST3
====================

A Sublime Text 3 plugin for ChucK, featuring syntax highlighting, tab completion, snippets (and *maybe* REPL-ish sessions). Based on the Supercollider ST2 plugin from http://github.com/geoffroymontel/supercollider-package-for-sublime-text.

Sublime Text 3 home page
http://www.sublimetext.com/3

ChucK home page
http://chuck.cs.princeton.edu

## Installation  

 - Open Sublime Text 3.
 - Go to Preferences/Browse Packages.
 - Unpack the archive into the Packagers folder which should appear.
 - Change ChucK path in ChucK.sublime-settings.
 - Restart Sublime Text 3.

## Usage  

 - Currently to get sounds out of SublimeText3 + ChucK we've set up a 
simple build script. If you are new to SublimeText, the menu to look for is located in Tools -> Build System. 
If `automatic` is not ticked then tick it, or you can set it manually by selecting ChucK from this list. To hear some sounds:
    - load a `.ck` file or start a new file and save it with a `.ck` extension first (to let sublime know what kind of file it is)
    - write out your chuck code, notice the beautiful syntax highlighting, completions and hints.
    - hit the shortcut for build (cmd+B, or ctrl+B by default). 
    - to stop chuck, end the build command ( See the shortcut listed in Tools -> Cancel Build )  


## Features

#### Build command  
- ChucK Build command (initial Build command by Sharov Anton).
  - Goto error (bound to F4).

#### Syntax Highlighting  
- Syntax definition/coloring (Nathan Leiby).

#### Completions  
We've assembled most of the names of objects and methods that appear in the ChucK language. 
This helps you if you don't want to type so much or can't recall the names of the built-in stuff. 

- this is a work in progress by quaestor and zeffii.

#### Snippets.  
(short) commonly used syntactical structures are available with only a few keystrokes.
(examples)
 
#### Doc Search
`chuck_doc_search.py`: searches the ChucK online help for a currently selected word. it takes:
 - Any `Ugen` _name_
 - Any of the following terms (not case sensitive):
   - `arrays, std, math, machine, help, class, types, and vm`  
   - dot methods for `Std` and `Math` will also work, try doc search: `Math.max` or `Std.mtof`.

#### Iternotate  
`iternotate.py`: despite the awkward name this saves you from writing out full for-loops, Write the shorthand and
press the keyboard shortcut and watch it expand into the full ChucK for-loop  

`i..n` (where , `i` is your chosen iteration variable _name_, and `n` is a number)
`i..some_array`  

```chuck
// i..5
for(0 => int i; i<5; i++){
    i;
}

// i..iterable
for(0 => int i; i<iterable.cap(); i++){
    iterable[i];
}
```

#### Wav Writer  
Writes the current chuck file as stereo wav to disk. We use the concept of an inline console to tell `wav_writer.py` 
what to do. An inline console is a specific set of instructions in the form of a comment. For example: 

```chuck
SinOsc d => dac;  
20::second => now;   // %> 20:demo_sound
```

If the cursor caret is on the line with the comment using that `%>` token it will try to parse what 
is after it. `20` means you want that many seconds, `demo_sound` is the name of the output stereo wav 
you will record. This feature uses a threaded sub process, it allows you to use sublime whle python 
waits for chuck to write the wav to disk.

#### Tools > ChucK sub menu (todo) :
  - TODO: Stop all sounds.
  - TODO: Start and stop ChucK.
  - TODO: add / replace / remove shreds.

## Notes
- The default keybinds for `chuck_doc_search` and `iternotate` conflict with fold/unfold.

## Known bugs
Probably many
- If you build a shred while another shred is playing, you can not stop the first shred  
    - a work around for losing context of ChucK like that is to open Sublime's Python console   
    and enter `import subprocess` then `subprocess.call(["chuck", "--kill"])`. This kills it with fire.


## Authors
[quaestor](http://github.com/tildebyte)  
[zeffii](http://www.coursera.org/user/i/daff1a17ed112d8df2602bc10fa57a3b)  
[Sharov Anton](http://www.coursera.org/user/i/6591636f6ce50babb61bb547c721fac4)  
[Nathan Leiby](http://github.com/nathanleiby)  

## Thanks

- Geoffroy Montel (http://schemawound.com) for the ST2 Supercollider plugin.

#### Testing:

- Sergey Kazakov
- Paul Anderson
- Petros Lafazanidis
- Santiago Braida
