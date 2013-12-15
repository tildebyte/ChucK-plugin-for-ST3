ChucK-plugin-for-ST3
====================

A Sublime Text 3 plugin for ChucK, featuring syntax highlighting, tab completion, snippets (and *maybe* REPL-ish sessions).

- Based on the [Supercollider ST2 plugin] [1].
- [Sublime Text 3] [2].
- [ChucK] [3].

## Installation

 1. Open Sublime Text 3.
 2. Go to Preferences/Browse Packages.
 3. Unpack the [archive](https://github.com/tildebyte/ChucK-plugin-for-ST3/archive/master.zip) into the Packagers folder which should appear.
 4. Change ChucK path in ChucK.sublime-settings specific to your platform.
 5. Restart Sublime Text 3.

## Usage

Currently to get sounds out of Sublime Text 3 + ChucK we've set up a simple build script.
If you are new to SublimeText, the menu to look for is located in *Tools -> Build System*.
If *automatic* is not ticked then tick it, or you can set it manually by selecting ChucK from this list. To hear some sounds:

- Load a *.ck* file or start a new file and save it with a *.ck* extension first (to let Sublime know what kind of file it is).
- Enter your code; notice the beautiful syntax highlighting, completions and hints.
- Hit the shortcut for build (*⌘+B*, or *CTRL+B* by default).
- To stop ChucK, end the build command (See the shortcut listed in *Tools -> Cancel Build*. On OSX, *CTRL+C* should work. Windows has *CTRL+BREAK* listed as the shortcut \[1\]).


## Features

### Summary

- Build / Kill build / Goto error
- Syntax Highlighting
- Completions & Snippets, auto complete and instant access to common code blocks
- Document Search, search docs for selected word
- Shorthand for-loop rewriter called "iternotate" (never write a for-loop by hand again).
- Wav writer, writes current `.ck` to wav
- Open File under cursor, if it's a `.wav` it can open your sound editor, if it's a `.ck` it opens insitu.


#### Build command
- *Build*, *Run*, *Cancel Build*, and *Kill* are implemented. This means you write code, hit the *CTRL+ENTER* shortcut, and Sublime will send the file to play to ChucK . *Run* (*CTRL+SHIFT+ENTER*) will execute ChucK with an `innitialize.ck` *if* one is in the same directory as the file in the current tab - no switching back-and-forth. *Cancel Build* (*CTRL+C* / *CTRL+BREAK*)\[1\] will end that ChucK instance. *Kill* (CTRL+ALT+ENTER) will end the most-recently launched chuck instance, and then the next most-recent, etc. The great thing about keeping the code editing and the ChucK player separate is that if ChucK crashes it doesn't affect Sublime. This is unlike the miniAudicle; if ChucK crashes, most likely so will the miniAudicle.

- Goto error (bound to *F4*). When you encounter an error, if ChucK was able to provide the line on which the error occured, the error information will be printed in the ST status line. Hitting *F4* will navigate the Sublime editor to that line and file (and subsequent lines, if any).

#### Syntax Highlighting
Syntax definition/coloring of all major language constructs (types, syntax etc). If your code looks OK, this is a good first indication that your syntax is correct. There are a few subtle bugs listed at the end in the bugs section, but they do not impede beyond aesthetics.

#### Completions
We've included many objects and methods which appear in the ChucK language. This helps you type less and shows correct spelling for the built-in stuff. Very much a work in progress.

#### Snippets.
Some short, commonly used, syntactical structures (e.g. *while* loops) can be inserted with only a few keystrokes.

- Typing `pr` and hitting enter will insert `<<<  >>>;`
- Typing `arr` and enter will insert an array declaration; first enter the type, then hit *TAB*, then fill in the array name. This will produce `@=> <int,string,..etc> array_name[]`.
- [More examples] [4].

#### Doc Search
*chuck_doc_search.py*: searches the ChucK online help for the currently selected word. It takes:
 - Any UGen _name_.
 - Any of the following terms (not case sensitive):
   - help, Array, Std, Math, Machine, Class, Types, and VM
   - Dot methods for `Std` and `Math` will also work; try a doc search on `Math.max` or `Std.mtof`.

#### Iternotate
*iternotate.py*: despite the awkward name, this saves you from typing full for-loops. Enter the shorthand and press the keyboard shortcut and watch it expand.

- `i..n` (where `i` is your chosen iteration variable _name_, and `n` is a number or an int variable).
- `i..array_name[]` can be used if you want to iterate over an array.



```c
// i..5
for(0 => int i; i<5; i++){
    i;
}

// i..num_times
for(0 => int i; i<num_times; i++){
    i;
}

// i..iterable[  or  i..iterable[]
for(0 => int i; i<iterable.cap(); i++){
    iterable[i];
}
```

#### Wav Writer

default shortcut: "ctrl+shift+w"

Writes the current ChucK file as stereo wav to disk. We use the concept of an *inline console* to tell *chuck_wav_writer.py* what to do. An inline console is a specific set of instructions in the form of a comment. For example:

```c
SinOsc d => dac;
20::second => now;  // %> 20:demo_sound
```
or, add a gain value. Range 0.0 and upwards. The default, when omitted, is 1.0
```c
SinOsc d => dac;
20::second => now;  // %> 20:demo_sound:0.67
```

If the cursor caret is on the line with the comment using the `%>` token it will try to parse what is after it. "20" means you want that many seconds, *demo_sound* is the name of the output stereo wav you will record.
  - This feature uses a threaded sub process; it allows you to use Sublime while ChucK writes the wav to disk.
  - To use the wav writer you must add the path to [wav_writer_wgain.ck] [13] in [Chuck.sublime-settings] [15]

#### Context Menu additions

- _*Open file under cursor*_:
  - If you have a line like `Machine.add(me.dir() + "/kicks.ck")`, and want to see that file, simply place the key caret on that line and right-click to get the context menu. Choose "Open file under cursor..", to open the file in the current Sublime Text view.
  - If you have a soundfile referenced with `me.dir() + "/sound.wav"` Sublime will attempt to open the `.wav` in your configured sound editor.
- _*Archive project*_: will archive the current folder and subfolders as an uncompressed zip, it will automatically add a time postfix to the filename.



## TODO

#### Issue Tracker
The [issue tracker] [5] is a good place to look if you encounter a bug, or to justify/defend a feature request. It's where we go to discuss ideas and resolve bugs.


#### *Tools > ChucK* sub menu:
The menu is implemented but currently it is a stub, so avoid using it for now. There are
renovations going on in the code for those menu items. We have no clear timeframe for this todo, it may even happen that the ChucK menu is ditched in favour of the REPL as a console, or inline console comment-commands as implemented in *chuck_wav_writer.py*.

The list:

  - [x] Start ChucK in `--shell` mode (server).
  - [x] Kill ChucK server.
  - [~] Add shred (currently open file). (WIP, once this works the rest work automatically)
  - [ ] Add selection as shred (sends everything enclosed in `{}` as an "on the fly" shred).
  - [ ] Replace/remove shred by name.
  - [ ] Replace/remove shred by id.
  - [ ] Remove all shreds.

## Notes
The default keybinds for *chuck_doc_search* and *iternotate* conflict with *Fold/Unfold*.

## Known bugs
Probably many, but we are aware of these:

- While we stil rely on the build script to play chuck files, if you `Build` a shred while another shred is playing, you cannot stop the first shred anymore.
  - Workaround: Open Sublime's Python console and enter `import subprocess` then `subprocess.call(["chuck", "--kill"])`. This kills it *with fire*.
- using `.cap()` will render the rest of the line in white.
- `//` comments will sometimes cause weird highlighting in the comment itself.
- Doc Search currently behaves differently under firefox and webkit (chrome, safari..etc). This has to do with these browsers not implementing `url#section` the same way. This issue is compounded by the ChucK docs using inconsistent rules for named ids. More about this topic [here] [12]
- Sublime's architecture uses a *plugin_host* process which may crash if you are printing out too much with too little time between printing intervals. For example printing two messages per 20 ms, for 30 second duration will bring *plugin_host* to its knees. When the *plugin_host* crashes ChucK will probably still keep playing until the piece ends or you terminate the ChucK process. If your piece doesn't have a built in end, then end Chuck from Task Manager or  Activity Monitor. You will need to restart Sublime to continue using the ChucK plugin. This is not something the authors of this ChucK plugin can fix. 


## Authors

- [quaestor] [6]
- [zeffii] [7]
- [Sharov Anton] [8]
- [Nathan Leiby] [9]

## Thanks

- [Geoffroy Montel] [10] for the ST2 Supercollider plugin.
- Sharov Anton (initial Build command).
- Nathan Leiby (syntax highlighter conversion of textmate files by [tasmo] [11]).
- [Brian Harrington] [14] (Pointed out the need for platform-specific settings).


#### Testing:

- Sergey Kazakov
- Paul Anderson
- Petros Lafazanidis
- Santiago Braida

\[1\] *CTRL+BREAK* doesn't seem to work with all keyboards.

[1]: http://github.com/geoffroymontel/supercollider-package-for-sublime-text    "Supercollider ST2 plugin home"
[2]: http://www.sublimetext.com/3   "Sublime Text 3 home"
[3]: http://chuck.cs.princeton.edu    "ChucK home"
[4]: http://github.com/tildebyte/ChucK-plugin-for-ST3/tree/master/snippets     "More examples"
[5]: http://github.com/tildebyte/ChucK-plugin-for-ST3/issues?state=open    "GitHub Issue Tracker"
[6]: http://github.com/tildebyte    "tildebyte on GitHub"
[7]: http://www.coursera.org/user/i/daff1a17ed112d8df2602bc10fa57a3b    "dealga at Coursera"
[8]: http://www.coursera.org/user/i/6591636f6ce50babb61bb547c721fac4    "Sharov Anton at Coursera"
[9]: http://github.com/nathanleiby    "Nathan Leiby on GitHub"
[10]: http://schemawound.com    "Geoffroy Montel"
[11]: http://github.com/tasmo   "tasmo on GitHub"
[12]: http://github.com/tildebyte/ChucK-plugin-for-ST3/issues/7    "UGen lookup seems to be case-sensitive"
[13]: https://github.com/tildebyte/ChucK-plugin-for-ST3/blob/master/wav_writer_wgain.ck     "wave writer addon"
[14]: https://github.com/bdharrington7   "Brian Harrington on GitHub"
[15]: settings/ChucK.sublime-settings#L23   "wavewriter location"
