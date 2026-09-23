    def _get_key(self, event):
        val = event.keysym_num
        if val in self.keyvald:
            key = self.keyvald[val]
        elif (val == 0 and sys.platform == 'darwin'
              and event.keycode in self._keycode_lookup):
            key = self._keycode_lookup[event.keycode]
        elif val < 256:
            key = chr(val)
        else:
            key = None

        # add modifier keys to the key string. Bit details originate from
        # http://effbot.org/tkinterbook/tkinter-events-and-bindings.htm
        # BIT_SHIFT = 0x001; BIT_CAPSLOCK = 0x002; BIT_CONTROL = 0x004;
        # BIT_LEFT_ALT = 0x008; BIT_NUMLOCK = 0x010; BIT_RIGHT_ALT = 0x080;
        # BIT_MB_1 = 0x100; BIT_MB_2 = 0x200; BIT_MB_3 = 0x400;
        # In general, the modifier key is excluded from the modifier flag,
        # however this is not the case on "darwin", so double check that
        # we aren't adding repeat modifier flags to a modifier key.
        if sys.platform == 'win32':
            modifiers = [(17, 'alt', 'alt'),
                         (2, 'ctrl', 'control'),
                         ]
        elif sys.platform == 'darwin':
            modifiers = [(3, 'super', 'super'),
                         (4, 'alt', 'alt'),
                         (2, 'ctrl', 'control'),
                         ]
        else:
            modifiers = [(6, 'super', 'super'),
                         (3, 'alt', 'alt'),
                         (2, 'ctrl', 'control'),
                         ]

        if key is not None:
            # note, shift is not added to the keys as this is already accounted for
            for bitmask, prefix, key_name in modifiers:
                if event.state & (1 << bitmask) and key_name not in key:
                    key = '{0}+{1}'.format(prefix, key)

        return key
