Zen Coding for Gedit
====================
A new way of writing HTML and CSS code for Gedit

Information
-----------

Zen Coding is an editor plugin for high-speed HTML, XML, XSL (or any other structured code format)
coding and editing. The core of this plugin is a powerful abbreviation engine which allows you to
expand expressions—similar to CSS selectors—into HTML code.

- [Homepage](http://code.google.com/p/zen-coding/)
- [Demo video](http://vimeo.com/7405114)
- [Examples and usage](http://www.smashingmagazine.com/2009/11/21/zen-coding-a-new-way-to-write-html-code/)

This plugin fully integrates Zen Coding into Gedit.

Features
--------

Zen Coding isn't only a decent abbreviations expander but also a set of handy tools for common XHTML tasks.
Read [this page](http://code.google.com/p/zen-coding/wiki/Actions) thoroughly for details.
Note that almost every action highly depends on current caret position inside text editor.

With this plugin, you can:

- Expand abbreviation with `Ctrl+E`
- Wrap with abbreviation with `Ctrl+Shift+E`
- Balance tag inward or outward with `Ctrl+Alt+I` or `Ctrl+Alt+O`
- Merge lines with `Ctrl+Alt+M`
- Go to previous or next edit point with `Alt+Left` and `Alt+Right`
- Update tag image size with `Ctrl+Alt+S`
- Remove tag with `Ctrl+Alt+R`
- Split or join tags with `Ctrl+Alt+J`
- Toggle comment with `Ctrl+Alt+C`
- Create your own abbreviations and snippets.

Shortcuts can be changed in `~/.gnome2/gedit/plugins/zencoding/plugin.py` to fit your needs.

Installation
------------

1. Download [zip](http://github.com/fmarcia/zen-coding-gedit/zipball/master) or [tar](http://github.com/fmarcia/zen-coding-gedit/tarball/master) source and unpack it.
2. Run `./install.sh`
3. In order to use "Update tag image size", install `imagemagick`
4. In Gedit, go to Edit -> Preferences -> Plugins to find and enable the plugin.
5. Try it out!

Credits
-------
- [Sergey Chikuyonok](http://chikuyonok.ru/) - the creator of Zen Coding
- [Franck Marcia](http://github.com/fmarcia) - the author of this Gedit plugin
- [Mike Crittenden](http://mikethecoder.com) - the author of the previous Gedit plugin
- [Stuart Langridge](http://www.kryogenix.org/days/2009/09/21/zen-coding-for-gedit) - the author of the original Gedit plugin

