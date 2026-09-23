    @staticmethod
    def _mpl_modifiers(event, *, exclude=None):
        # Add modifier keys to the key string. Bit values are inferred from
        # the implementation of tkinter.Event.__repr__ (1, 2, 4, 8, ... =
        # Shift, Lock, Control, Mod1, ..., Mod5, Button1, ..., Button5)
        # In general, the modifier key is excluded from the modifier flag,
        # however this is not the case on "darwin", so double check that
        # we aren't adding repeat modifier flags to a modifier key.
        modifiers = [
            ("ctrl", 1 << 2, "control"),
            ("alt", 1 << 17, "alt"),
            ("shift", 1 << 0, "shift"),
        ] if sys.platform == "win32" else [
            ("ctrl", 1 << 2, "control"),
            ("alt", 1 << 4, "alt"),
            ("shift", 1 << 0, "shift"),
            ("cmd", 1 << 3, "cmd"),
        ] if sys.platform == "darwin" else [
            ("ctrl", 1 << 2, "control"),
            ("alt", 1 << 3, "alt"),
            ("shift", 1 << 0, "shift"),
            ("super", 1 << 6, "super"),
        ]
        return [name for name, mask, key in modifiers
                if event.state & mask and exclude != key]
