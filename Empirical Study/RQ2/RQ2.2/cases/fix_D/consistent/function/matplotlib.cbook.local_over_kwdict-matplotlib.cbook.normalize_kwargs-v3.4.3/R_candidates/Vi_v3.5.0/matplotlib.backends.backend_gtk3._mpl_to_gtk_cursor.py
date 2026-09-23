@functools.lru_cache()
def _mpl_to_gtk_cursor(mpl_cursor):
    name = _api.check_getitem({
        Cursors.MOVE: "move",
        Cursors.HAND: "pointer",
        Cursors.POINTER: "default",
        Cursors.SELECT_REGION: "crosshair",
        Cursors.WAIT: "wait",
        Cursors.RESIZE_HORIZONTAL: "ew-resize",
        Cursors.RESIZE_VERTICAL: "ns-resize",
    }, cursor=mpl_cursor)
    return Gdk.Cursor.new_from_name(Gdk.Display.get_default(), name)
