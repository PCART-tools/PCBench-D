    def _get_key(self, event):
        event_key = event.key()
        mods = self._mpl_modifiers(exclude=event_key)
        try:
            # for certain keys (enter, left, backspace, etc) use a word for the
            # key, rather than Unicode
            key = SPECIAL_KEYS[event_key]
        except KeyError:
            # Unicode defines code points up to 0x10ffff (sys.maxunicode)
            # QT will use Key_Codes larger than that for keyboard keys that are
            # not Unicode characters (like multimedia keys)
            # skip these
            # if you really want them, you should add them to SPECIAL_KEYS
            if event_key > sys.maxunicode:
                return None

            key = chr(event_key)
            # qt delivers capitalized letters.  fix capitalization
            # note that capslock is ignored
            if 'shift' in mods:
                mods.remove('shift')
            else:
                key = key.lower()

        return '+'.join(mods + [key])
