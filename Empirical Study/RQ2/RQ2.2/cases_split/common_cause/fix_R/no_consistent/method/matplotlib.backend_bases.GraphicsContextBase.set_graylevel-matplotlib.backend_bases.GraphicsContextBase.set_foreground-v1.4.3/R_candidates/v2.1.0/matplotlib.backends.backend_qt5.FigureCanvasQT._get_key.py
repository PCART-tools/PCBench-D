    def _get_key(self, event):
        if not self._keyautorepeat and event.isAutoRepeat():
            return None

        event_key = event.key()
        event_mods = int(event.modifiers())  # actually a bitmask

        # get names of the pressed modifier keys
        # bit twiddling to pick out modifier keys from event_mods bitmask,
        # if event_key is a MODIFIER, it should not be duplicated in mods
        mods = [name for name, mod_key, qt_key in MODIFIER_KEYS
                if event_key != qt_key and (event_mods & mod_key) == mod_key]
        try:
            # for certain keys (enter, left, backspace, etc) use a word for the
            # key, rather than unicode
            key = SPECIAL_KEYS[event_key]
        except KeyError:
            # unicode defines code points up to 0x0010ffff
            # QT will use Key_Codes larger than that for keyboard keys that are
            # are not unicode characters (like multimedia keys)
            # skip these
            # if you really want them, you should add them to SPECIAL_KEYS
            MAX_UNICODE = 0x10ffff
            if event_key > MAX_UNICODE:
                return None

            key = unichr(event_key)
            # qt delivers capitalized letters.  fix capitalization
            # note that capslock is ignored
            if 'shift' in mods:
                mods.remove('shift')
            else:
                key = key.lower()

        mods.reverse()
        return '+'.join(mods + [key])
