def error_msg_gtk(msg, parent=None):
    if parent is not None:  # find the toplevel Gtk.Window
        parent = parent.get_toplevel()
        if not parent.is_toplevel():
            parent = None
    if not isinstance(msg, str):
        msg = ','.join(map(str, msg))
    dialog = Gtk.MessageDialog(
        parent=parent, type=Gtk.MessageType.ERROR, buttons=Gtk.ButtonsType.OK,
        message_format=msg)
    dialog.run()
    dialog.destroy()
