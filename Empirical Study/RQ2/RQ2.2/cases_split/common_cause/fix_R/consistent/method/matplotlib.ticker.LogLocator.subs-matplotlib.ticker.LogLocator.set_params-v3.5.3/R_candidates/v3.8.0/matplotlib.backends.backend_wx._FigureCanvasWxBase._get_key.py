    def _get_key(self, event):
        keyval = event.KeyCode
        if keyval in self.keyvald:
            key = self.keyvald[keyval]
        elif keyval < 256:
            key = chr(keyval)
            # wx always returns an uppercase, so make it lowercase if the shift
            # key is not depressed (NOTE: this will not handle Caps Lock)
            if not event.ShiftDown():
                key = key.lower()
        else:
            return None
        mods = self._mpl_modifiers(event, exclude=keyval)
        if "shift" in mods and key.isupper():
            mods.remove("shift")
        return "+".join([*mods, key])
