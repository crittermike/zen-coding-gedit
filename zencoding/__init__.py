#
# @file __init__.py
# Does the heavy lifting behind connecting Zen Coding to Gedit.
#

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
        "Gedit callback: install the expansion feature into the UI"

        ui_manager = window.get_ui_manager()
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
        "Gedit callback: get rid of the expansion feature"

        ui_manager = window.get_ui_manager()
        (action_group, ui_merge_id) = ui_manager.__ui_data__

        # Remove the UI data, action group, and UI itself from Gedit
        del ui_manager.__ui_data__
        ui_manager.remove_action_group(action_group)
        ui_manager.remove_ui(ui_merge_id)


    def expand_zencode(self, window):
        "The action which handles the code expansion itself."

        view = window.get_active_view()
        buffer = view.get_buffer()

        # Grab the current cursor position.
        cursor_iter = buffer.get_iter_at_mark(buffer.get_insert())

        # Grab the first character in the line.
        line_iter = cursor_iter.copy()
        line_iter.set_line_offset(0)

        # Grab the text from the start of the line to the cursor.
        line = buffer.get_text(line_iter, cursor_iter)

        # Find the last space in the line and remove it, setting a variable
        # 'before' to the current line.
        words = line.split(" ")
        before = words[-1].lstrip()
        if not before:
            return

        # Get the language of the current document. Second line prevents an error
        # if first line returns None.
        lang = window.get_active_document().get_language()
        lang = lang and lang.get_name()

        # Using the 'before' variable, convert it from Zen Code
        # to expanded code. If there isn't anything, just return.
        if lang == 'CSS':
            after = zen_core.expand_abbreviation(before,'css','xhtml')
        else:
            after = zen_core.expand_abbreviation(before,'html','xhtml')
        if not after:
            return

        # Grab the line's indentation and store it.
        indent = re.match(r"\s*", line).group()

        # Automatically indent the string and replace \t (tab) with the
        # correct number of spaces.
        after = zen_core.pad_string(after,indent)
        if view.get_insert_spaces_instead_of_tabs():
            tabsize = view.get_tab_width()
            spaces = " " * tabsize
            after = after.replace("\t",spaces)

        # We are currently lame and do not know how to do placeholders.
        # So remove all | characters from after.
        after = after.replace("|", "")

        # Delete the last word in the line (i.e., the 'before' text, aka the
        # Zen un-expanded code), so that we can replace it.
        word_iter = cursor_iter.copy()
        position_in_line = cursor_iter.get_line_index() - len(before)
        word_iter.set_line_index(position_in_line)
        buffer.delete(word_iter, cursor_iter)

        # Insert the new expanded text.
        buffer.insert_at_cursor(after)

