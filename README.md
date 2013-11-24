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
Build and Cancel Build are implemented. This means you write code hit the cmd+B / ctrl+B and sublime will send
chuck the file to play. Cancel Build will end that ChucK instance. The great thing about keeping the code editing
and the ChucK player separate is that if ChucK crashes this doesn't affect Sublime. This is unlike if you edit 
inside the miniAudicle, if chuck crashes most likely so will the miniAudicle.

- Goto error (bound to F4). When you encounter an error, if ChucK was able to provide the line 
 on which the error occured, then hitting f4 will navigate the sublime editor to that line.

#### Syntax Highlighting  
Syntax definition / coloring of all major language constructs (types, syntax etc). If code looks alright
this is a good first indication that your code syntax is correct. There are a few subtle bugs listed at 
the end in the bugs section, but they do not impede beyond aesthetics.

#### Completions  
We've assembled most of the names of objects and methods that appear in the ChucK language. 
This helps you type less and show correct spelling of the built-in stuff. Very much a work in progress.

#### Snippets.  
Often short, commonly used, syntactical structures can be inserted with only a few keystrokes.
([examples](https://github.com/tildebyte/ChucK-plugin-for-ST3/tree/master/snippets))
 
#### Doc Search
`chuck_doc_search.py`: searches the ChucK online help for a currently selected word. it takes:
 - Any `Ugen` _name_
 - Any of the following terms (not case sensitive):
   - `arrays, std, math, machine, help, class, types, and vm`  
   - dot methods for `Std` and `Math` will also work, try doc search: `Math.max` or `Std.mtof`.

#### Iternotate  
`iternotate.py`: despite the awkward name this saves you from writing out full for-loops, Write the shorthand and
press the keyboard shortcut and watch it expand.  

- `i..n` (where `i` is your chosen iteration variable _name_, and `n` is a number)  
- `i..some_array` can be used if you want to iterate over an array. 


```c
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
Writes the current ChucK file as stereo wav to disk. We use the concept of an inline console to tell `wav_writer.py` 
what to do. An inline console is a specific set of instructions in the form of a comment. For example: 

```c
SinOsc d => dac;  
20::second => now;   // %> 20:demo_sound
```

If the cursor caret is on the line with the comment using that `%>` token it will try to parse what 
is after it. `20` means you want that many seconds, `demo_sound` is the name of the output stereo wav 
you will record.  
- This feature uses a threaded sub process, it allows you to use sublime while chuck writes
the wav to disk.
- Currently you need a copy of `wav_writer.ck` in the same directory as the `.ck` you wish to record.

## TODO  

#### Tools > ChucK sub menu:  
The menu is implemented but currently it is a stub, so avoid using it for now. There are 
renovations going on in the code for those menu items. We have no clear timeframe for this todo, it may even 
happen that the ChucK menu is ditched in favour of the REPL as a console or inline console 
comment-commands as implemented wav_writer.

the list:  

  - start ChucK in `--shell` mode (server).
  - kill ChucK server.
  - add shred (current open file)
  - add selection as shred (sends everything enclosed in { } as an 'on the fly' shred)
  - replace / remove shred named x
  - replace / remove shred by id
  - remove all shreds.


## Notes
- The default keybinds for `chuck_doc_search` and `iternotate` conflict with fold/unfold.

## Known bugs
Probably many, but we are aware of these:
- If you build a shred while another shred is playing, you can not stop the first shred  
    - a work around for losing context of ChucK like that is to open Sublime's Python console   
    and enter `import subprocess` then `subprocess.call(["chuck", "--kill"])`. This kills it with fire.

- using `.cap()` will render the rest of the line in white. 


## Authors
[quaestor](http://github.com/tildebyte)  
[zeffii](http://www.coursera.org/user/i/daff1a17ed112d8df2602bc10fa57a3b)  
[Sharov Anton](http://www.coursera.org/user/i/6591636f6ce50babb61bb547c721fac4)  
[Nathan Leiby](http://github.com/nathanleiby)  

## Thanks

- Geoffroy Montel (http://schemawound.com) for the ST2 Supercollider plugin.
- Sharov Anton (initial Build command)
- Nathan Leiby (syntax highlighter conversion of textmate files by [tasmo](http://tasmo.github.com/ChucK.tmbundle)).


#### Testing:

- Sergey Kazakov
- Paul Anderson
- Petros Lafazanidis
- Santiago Braida
