import pygtk
pygtk.require('2.0')
import gtk

class WrapDialog():

    def __init__(self, editor, x, y, text=""):

        self.editor = editor
        self.exit = False
        self.done = False
        self.abbreviation = text

        self.window = gtk.Window(gtk.WINDOW_TOPLEVEL)
        self.window.set_decorated(False)
        self.window.connect("destroy", self.quit)
        self.window.connect("focus-out-event", self.focus_lost)
        self.window.connect("key-press-event", self.key_pressed)
        self.window.set_resizable(False)
        self.window.move(x - 15, y - 35)

        self.frame = gtk.Frame()
        self.window.add(self.frame)
        self.frame.show()

        self.box = gtk.HBox()
        self.frame.add(self.box)
        self.box.show()
        
        self.entry = gtk.Entry()
        self.entry.connect("changed", self.update)
        self.entry.set_text(text)
        self.entry.set_icon_from_icon_name(gtk.ENTRY_ICON_PRIMARY, 'zencoding')
        self.entry.set_width_chars(48)
        self.box.pack_start(self.entry, True, True, 4)
        self.entry.show()

        self.window.show()

    def key_pressed(widget, what, event):
        if event.keyval == 65293: # Return
            widget.exit = True
            widget.quit()
        elif event.keyval == 65289: # Tab
            widget.exit = True
            widget.quit()
        elif event.keyval == 65307: # Escape
            widget.exit = False
            widget.done = widget.editor.do_wrap_with_abbreviation(widget.done, '')
            widget.quit()
        else:
            return False
            
    def focus_lost(self, widget=None, event=None):
        widget.exit = True
        widget.quit()

    def update(self, entry):
        self.abbreviation = self.entry.get_text()
        self.done = self.editor.do_wrap_with_abbreviation(self.done, self.abbreviation)

    def quit(self, widget=None, event=None):
        self.window.hide()
        self.window.destroy()
        gtk.main_quit()

    def main(self):
        gtk.main()

def main(editor, window, text=""):

    # ensure the caret is hidden
    editor.view.set_cursor_visible(False)
    
    # get coordinates of the cursor
    offset_start, offset_end = editor.get_selection_range()
    insert = editor.buffer.get_iter_at_offset(offset_start)
    location = editor.view.get_iter_location(insert)
    window = editor.view.get_window(gtk.TEXT_WINDOW_TEXT)
    xo, yo = window.get_origin()
    xb, yb = editor.view.buffer_to_window_coords(gtk.TEXT_WINDOW_TEXT, location.x + location.width, location.y)

    # open dialog at coordinates with eventual text
    wrap_dialog = WrapDialog(editor, xo + xb, yo + yb, text)
    wrap_dialog.main()

    # show the caret again
    editor.view.set_cursor_visible(True)

    # return exit status and abbreviation
    return wrap_dialog.done and wrap_dialog.exit, wrap_dialog.abbreviation

