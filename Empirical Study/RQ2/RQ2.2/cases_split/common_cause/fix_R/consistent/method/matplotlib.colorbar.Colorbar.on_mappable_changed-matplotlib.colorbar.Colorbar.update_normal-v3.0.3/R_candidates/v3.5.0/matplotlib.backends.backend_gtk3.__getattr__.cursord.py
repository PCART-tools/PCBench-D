    @_api.deprecated("3.5", obj_type="")
    @property
    def cursord(self):
        try:
            new_cursor = functools.partial(
                Gdk.Cursor.new_from_name, Gdk.Display.get_default())
            return {
                Cursors.MOVE:          new_cursor("move"),
                Cursors.HAND:          new_cursor("pointer"),
                Cursors.POINTER:       new_cursor("default"),
                Cursors.SELECT_REGION: new_cursor("crosshair"),
                Cursors.WAIT:          new_cursor("wait"),
            }
        except TypeError as exc:
            return {}
