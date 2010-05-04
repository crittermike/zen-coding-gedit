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

Currently implemented for Gedit:

- Expand abbreviation with `Ctrl+E`
- Wrap with abbreviation with `Ctrl+Shift+E`
- Balance tag inward or outward with `Ctrl+Alt+I` or `Ctrl+Alt+O`
- Go to previous or next edit point with `Alt+Left` and `Alt+Right`

Menu entries are also available in the Edit menu.
Shortcuts can be changed in `~/.gnome2/gedit/plugins/zencoding/plugin.py` to fit your needs.

Installation
------------

1. Download source
2. Unpack the `zencoding-gedit.plugin` file and the `zencoding` directory into `~/.gnome2/gedit/plugins/`.
3. Unpack the `gcocoadialog` file into `/usr/bin/` (compiled for Ubuntu amd64, make sure to `chmod +x` it) or compile it yourself from [here](http://code.google.com/p/gcocoadialog/).
4. In Gedit, go to Edit -> Preferences -> Plugins to find and enable the plugin.
5. Try it out!

Credits
-------
- [Sergey Chikuyonok](http://chikuyonok.ru/) - the music makers, the dreamers of the dream
- [Mike Crittenden](http://mikethecoder.com) - the maintainer of the Gedit plugin
- [Stuart Langridge](http://www.kryogenix.org/days/2009/09/21/zen-coding-for-gedit) - the original author of the Gedit plugin
- [Mitchell Foral](http://caladbolg.net/) - the author of [gcocoadialog](http://code.google.com/p/gcocoadialog/)
- Franck Marcia - the author of this version of Gedit plugin
