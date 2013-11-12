ChucK-plugin-for-ST3
====================

A Sublime Text 3 plugin for ChucK, featuring REPL-ish command, syntax highlighting, and eventually snippets (and *maybe* tab-completion[1]). Based on the Supercollider ST2 plugin from http://github.com/geoffroymontel/supercollider-package-for-sublime-text.

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
- In Tools, there is a new ChucK sub menu which allows you to :
  - TODO: start and stop ChucK.
  - TODO: stop all sounds.
  - IN PROGRESS: search UGen help in ChucK docs (online) (zeffii).
  - Run the current ChucK program in ChucK, with the output going
        to a ST terminal window. This runs from the Tools menu
        using the Build command (initial Build command by Sharov Anton).
- Syntax definition/coloring (Nathan Leiby).
- Completions (quaestor).

## Notes
- The default keybinds for UGen lookup and iternotate conflict with fold/unfold

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

[1] Currently working to some extent.
