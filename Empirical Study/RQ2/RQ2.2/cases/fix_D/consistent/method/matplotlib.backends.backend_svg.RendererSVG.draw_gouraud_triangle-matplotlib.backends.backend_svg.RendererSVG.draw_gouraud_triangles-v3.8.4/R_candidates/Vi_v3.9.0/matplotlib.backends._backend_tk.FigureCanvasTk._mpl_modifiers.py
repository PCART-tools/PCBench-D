    @staticmethod
    def _mpl_modifiers(event, *, exclude=None):
        # add modifier keys to the key string. Bit details originate from
        # http://effbot.org/tkinterbook/tkinter-events-and-bindings.htm
        # BIT_SHIFT = 0x001; BIT_CAPSLOCK = 0x002; BIT_CONTROL = 0x004;
        # BIT_LEFT_ALT = 0x008; BIT_NUMLOCK = 0x010; BIT_RIGHT_ALT = 0x080;
        # BIT_MB_1 = 0x100; BIT_MB_2 = 0x200; BIT_MB_3 = 0x400;
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
