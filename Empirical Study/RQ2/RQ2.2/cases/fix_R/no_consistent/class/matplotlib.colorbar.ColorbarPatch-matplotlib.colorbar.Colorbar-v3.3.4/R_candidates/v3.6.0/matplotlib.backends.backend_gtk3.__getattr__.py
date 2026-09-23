@_api.caching_module_getattr  # module-level deprecations
class __getattr__:
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
        except TypeError:
            return {}

    icon_filename = _api.deprecated("3.6", obj_type="")(property(
        lambda self:
        "matplotlib.png" if sys.platform == "win32" else "matplotlib.svg"))
    window_icon = _api.deprecated("3.6", obj_type="")(property(
        lambda self:
        str(cbook._get_data_path("images", __getattr__("icon_filename")))))
