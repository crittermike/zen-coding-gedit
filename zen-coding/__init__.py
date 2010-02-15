#
# @file __init__.py
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2, or (at your option)
# any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place - Suite 330, Boston, MA 02111-1307, USA.
#
# Zen Coding - http://code.google.com/p/zen-coding
# Gedit Plugin - http://github.com/mikecrittenden/zen-coding-gedit
#
# Heavily based on Guillaume Chazarain's completion.py


import gedit, gobject, string, gtk, re, zen_core

class ZenCodingPlugin(gedit.Plugin):
	"""
	A Gedit plugin to implement Zen Coding's HTML and CSS shorthand expander.

	This file adds the menu items and keyboard shortcuts to the UI and connects
	those items with the good stuff (i.e., the code expansion).
	"""

	def __init__(self):
		gedit.Plugin.__init__(self)

	def activate(self, window):
		"Gedit callback: install the completion feature into the UI"

		# Get the UI manager into a variable.
		ui_manager = window.get_ui_manager()

		# Create the Action Group.
		action_group = gtk.ActionGroup("GeditZenCodingPluginActions")

		# Create the GTK action to be used to connect the key combo
		# to the Zen Coding expansion (i.e., the good stuff).
		complete_action = gtk.Action(name="ZenCodingAction",
		                             label="Expand Zen code...",
		                             tooltip="Expand Zen Code in document to raw HTML",
		                             stock_id=gtk.STOCK_GO_FORWARD)

		# Connect the newly created action with key combo
		complete_action.connect("activate",
		                        lambda a: self.expand_zencode(window))
		action_group.add_action_with_accel(complete_action,
		                                   "<Ctrl><Shift>E")

        # Insert the action group into the UI manager
		ui_manager.insert_action_group(action_group, 0)

		# @TODO: Figure out what these lines do
		ui_merge_id = ui_manager.new_merge_id()
		ui_manager.add_ui(ui_merge_id,
		                  "/MenuBar/EditMenu/EditOps_5",
		                  "ZenCoding",
		                  "ZenCodingAction",
		                  gtk.UI_MANAGER_MENUITEM, False)
		ui_manager.__ui_data__ = (action_group, ui_merge_id)

	def deactivate(self, window):
		"Gedit callback: get rid of the completion feature"

		# Grab the UI manager and put it into a variable.
		ui_manager = window.get_ui_manager()

		(action_group, ui_merge_id) = ui_manager.__ui_data__

		# Remove the UI data, action group, and UI itself for the plugin from Gedit
		del ui_manager.__ui_data__
		ui_manager.remove_action_group(action_group)
		ui_manager.remove_ui(ui_merge_id)


	def expand_zencode(self, window):
		"The action which handles the code expansion itself."

        # Get the window's active view's buffer.
		buffer = window.get_active_view().get_buffer()

        # Grab the current cursor position.
		cursor_iter = buffer.get_iter_at_mark(buffer.get_insert())

		# Grab the first character in the line.
		line_iter = cursor_iter.copy()
		line_iter.set_line_offset(0)

		# Grab the text from the start of the line to the cursor.
		line = buffer.get_text(line_iter, cursor_iter)

		# Grab the line's indention and store it.
		indent = re.match(r"\s*", line).group()

		# Find the last space in the line and remove it, setting a variable
		# 'before' to the current line.
		words = line.split(" ")
		before = words[-1].lstrip()
		if not before:
		    return

        # Using the 'before' variable, convert it from Zen Code
        # to expanded code. If there isn't anything, just return.
		after = zen_core.expand_abbreviation(before,'html','xhtml')
		if not after:
		    return

		# We are currently lame and do not know how to do placeholders.
		# So remove all | characters from after.
		after = after.replace("|", "")

		# Automatically indent the string based on how far the line was indented.
		after = zen_core.pad_string(after,indent)

		# Delete the last word in the line (i.e., the 'before' text, aka the
		# Zen un-expanded code), so that we can replace it.
		word_iter = cursor_iter.copy()
		position_in_line = cursor_iter.get_line_index() - len(before)
		word_iter.set_line_index(position_in_line)
		buffer.delete(word_iter, cursor_iter)

		# Insert the new expanded text.
		buffer.insert_at_cursor(after)

