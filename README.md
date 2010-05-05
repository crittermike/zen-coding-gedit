Zen Coding for Gedit
====================
A new way of writing HTML and CSS code for Gedit.

Information
-----------

Zen Coding is an editor plugin for high-speed HTML, XML, XSL (or any other structured code format)
coding and editing. The core of this plugin is a powerful abbreviation engine which allows you to
expand expressions—similar to CSS selectors—into HTML code.

- [Homepage](http://code.google.com/p/zen-coding/)
- [Demo video](http://vimeo.com/7405114)
- [Examples and usage](http://www.smashingmagazine.com/2009/11/21/zen-coding-a-new-way-to-write-html-code/)

This is a Gedit plugin that partially integrates Zen Coding into Gedit.

Features
--------

Zen Coding isn't only a decent abbreviations expander, but also a set of handy tools for common XHTML tasks.
Read [this page](http://code.google.com/p/zen-coding/wiki/Actions) carefully to boost your productivity even
more. Note that almost every action highly depends on current caret position inside text editor. 

- Expand abbreviation with `Ctrl+E`
- Wrap with abbreviation with `Ctrl+Shift+E` (needs gcocoadialog, see Installation and Credits)
- Balance tag inward or outward with `Ctrl+Alt+I` or `Ctrl+Alt+O`
- Merge lines with `Ctrl+Alt+M`
- Go to previous or next edit point with `Alt+Left` and `Alt+Right`
- Update tag image size with `Ctrl+Alt+S` (needs ImageMagick, see Installation and Credits)
- Remove tag with `Ctrl+Alt+R`
- Split or join lines with `Ctrl+Alt+J`
- Toggle comment with `Ctrl+Alt+C`

Menu entries are also available in the Edit menu.
Shortcuts can be changed in `~/.gnome2/gedit/plugins/zencoding/plugin.py` to fit your needs.

Installation
------------

1. Download source
2. Unpack the `zencoding-gedit.plugin` file and the `zencoding` directory into `~/.gnome2/gedit/plugins/`.
3. In order to use "Wrap with abbreviation", [install gcocoadialog](http://mikethecoder.com/2010/05/05/compiling-and-installing-gcocoadialog-in-ubuntu/).
4. In order to use "Update tag image size", install the package `imagemagick`, if not already done.
5. In Gedit, go to Edit -> Preferences -> Plugins to find and enable the plugin.
6. Try it out!

Credits
-------
- [Sergey Chikuyonok](http://chikuyonok.ru/) - the music makers, the dreamers of the dream
- [Mike Crittenden](http://mikethecoder.com) - the maintainer of the Gedit plugin
- [Stuart Langridge](http://www.kryogenix.org/days/2009/09/21/zen-coding-for-gedit) - the original author of the Gedit plugin
- [Mitchell Foral](http://caladbolg.net/) - the author of [gcocoadialog](http://code.google.com/p/gcocoadialog/)
- [ImageMagick Team](http://www.imagemagick.org/) - a software suite to create, edit, and compose bitmap images
- Franck Marcia - the author of this version of Gedit plugin
