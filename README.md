Zen Coding for Gedit
====================

Zen Coding is a plugin for high-speed HTML, XML, XSL (or any other structured code format)
coding and editing. The core of this plugin is a powerful abbreviation engine which allows you to
expand expressions - similar to CSS selectors - into HTML code.

- [Homepage](http://code.google.com/p/zen-coding/)
- [Demo video](http://vimeo.com/7405114)
- [Examples and usage](http://www.smashingmagazine.com/2009/11/21/zen-coding-a-new-way-to-write-html-code/)
- [Descriptions of features](http://code.google.com/p/zen-coding/wiki/Actions)

This plugin integrates Zen Coding into Gedit.

Features
--------

Zen Coding is a swiss army knife for common CSS and XHTML tasks. [Read this](http://code.google.com/p/zen-coding/wiki/Actions) 
for details. Note that almost every action highly depends on current caret
position inside text editor.

With this plugin, you can:

- Expand abbreviation with `Ctrl+E`
- Expand abbreviation as you type with `Ctrl+Alt+E`
- Wrap with abbreviation with `Ctrl+Shift+E`
- Balance tag inward or outward with `Ctrl+Alt+I` or `Ctrl+Alt+O`
- Merge lines with `Ctrl+Alt+M`
- Go to previous or next edit point with `Alt+Left` and `Alt+Right`
- Remove tag with `Ctrl+Alt+R`
- Split or join tags with `Ctrl+Alt+J`
- Toggle comment with `Ctrl+Alt+C`

Shortcuts can be changed in `zencoding/plugin.py` to fit your needs.

Installation
------------

1. Download [zip](http://github.com/mikecrittenden/zen-coding-gedit/zipball/master) or [tar](http://github.com/mikecrittenden/zen-coding-gedit/tarball/master) source and unpack it.
2. *Gedit 2: Move `zencoding.gedit-plugin` and the `zencoding` folder into `~/.gnome2/gedit/plugins/` 
	 *Gedit 3: Move `zencoding.plugin` and the `zencoding` folder into `~/.local/share/gedit/plugins/` 
2. 
3. In Gedit, go to Edit &rarr; Preferences &rarr; Plugins to enable the plugin.
4. Try it out using the shortcut keys listed above.
Credits
-------

- [Sergey Chikuyonok](http://chikuyonok.ru/) - the creator of Zen Coding
- [Franck Marcia](http://github.com/fmarcia) - the author of this Gedit plugin
- [Mike Crittenden](http://mikethecoder.com) - the maintainer of this Gedit plugin
