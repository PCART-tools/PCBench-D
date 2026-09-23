    @staticmethod
    def _mpl_modifiers(event=None, *, exclude=None):
        mod_table = [
            ("ctrl", wx.MOD_CONTROL, wx.WXK_CONTROL),
            ("alt", wx.MOD_ALT, wx.WXK_ALT),
            ("shift", wx.MOD_SHIFT, wx.WXK_SHIFT),
        ]
        if event is not None:
            modifiers = event.GetModifiers()
            return [name for name, mod, key in mod_table
                    if modifiers & mod and exclude != key]
        else:
            return [name for name, mod, key in mod_table
                    if wx.GetKeyState(key)]
