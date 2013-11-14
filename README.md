ChucK-plugin-for-ST3
====================

A Sublime Text 3 plugin for ChucK, featuring syntax highlighting, tab completion, snippets (and *maybe* REPL-ish sessions). Based on the Supercollider ST2 plugin from http://github.com/geoffroymontel/supercollider-package-for-sublime-text.

Sublime Text 3 home page
http://www.sublimetext.com/3

ChucK home page
http://chuck.cs.princeton.edu

## Usage
- Open Sublime Text 3.
- Go to Preferences/Browse Packages.
- Unpack the archive into the Packagers folder which should appear.
- Change ChucK path in ChucK.sublime-settings.
- Restart Sublime Text 3.

## Features
- Search UGen help in ChucK docs (online) (zeffii).
- Run the current ChucK program in ChucK, with the output going
    to an ST terminal window. This runs from the Tools menu
    using the Build command (initial Build command by Sharov Anton).
  - Goto error (bound to F4).
- Syntax definition/coloring (Nathan Leiby).
- Completions (quaestor).
- Snippets (quaestor).
- In Tools, there will be a new ChucK sub menu which allows you to:
  - TODO: Start and stop ChucK.
  - TODO: Stop all sounds.

## Notes
- The default keybinds for UGen lookup and iternotate conflict with fold/unfold.

## Known bugs
Probably many

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
