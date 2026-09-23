    def _get_key(self, event):
        unikey = event.char
        key = cbook._unikey_or_keysym_to_mplkey(unikey, event.keysym)

        # add modifier keys to the key string. Bit details originate from
        # http://effbot.org/tkinterbook/tkinter-events-and-bindings.htm
        # BIT_SHIFT = 0x001; BIT_CAPSLOCK = 0x002; BIT_CONTROL = 0x004;
        # BIT_LEFT_ALT = 0x008; BIT_NUMLOCK = 0x010; BIT_RIGHT_ALT = 0x080;
        # BIT_MB_1 = 0x100; BIT_MB_2 = 0x200; BIT_MB_3 = 0x400;
        # In general, the modifier key is excluded from the modifier flag,
        # however this is not the case on "darwin", so double check that
        # we aren't adding repeat modifier flags to a modifier key.
        if sys.platform == 'win32':
            modifiers = [(2, 'ctrl', 'control'),
                         (17, 'alt', 'alt'),
                         (0, 'shift', 'shift'),
                         ]
        elif sys.platform == 'darwin':
            modifiers = [(2, 'ctrl', 'control'),
                         (4, 'alt', 'alt'),
                         (0, 'shift', 'shift'),
                         (3, 'super', 'super'),
                         ]
        else:
            modifiers = [(2, 'ctrl', 'control'),
                         (3, 'alt', 'alt'),
                         (0, 'shift', 'shift'),
                         (6, 'super', 'super'),
                         ]

        if key is not None:
            # shift is not added to the keys as this is already accounted for
            for bitmask, prefix, key_name in modifiers:
                if event.state & (1 << bitmask) and key_name not in key:
                    if not (prefix == 'shift' and unikey):
                        key = '{0}+{1}'.format(prefix, key)

        return key
