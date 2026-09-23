@_api.caching_module_getattr  # module-level deprecations
class __getattr__:
    IDLE_DELAY = _api.deprecated("3.1", obj_type="", removal="3.6")(property(
        lambda self: 5))
    cursord = _api.deprecated("3.5", obj_type="")(property(lambda self: {
        cursors.MOVE: wx.CURSOR_HAND,
        cursors.HAND: wx.CURSOR_HAND,
        cursors.POINTER: wx.CURSOR_ARROW,
        cursors.SELECT_REGION: wx.CURSOR_CROSS,
        cursors.WAIT: wx.CURSOR_WAIT,
        cursors.RESIZE_HORIZONTAL: wx.CURSOR_SIZEWE,
        cursors.RESIZE_VERTICAL: wx.CURSOR_SIZENS,
    }))
