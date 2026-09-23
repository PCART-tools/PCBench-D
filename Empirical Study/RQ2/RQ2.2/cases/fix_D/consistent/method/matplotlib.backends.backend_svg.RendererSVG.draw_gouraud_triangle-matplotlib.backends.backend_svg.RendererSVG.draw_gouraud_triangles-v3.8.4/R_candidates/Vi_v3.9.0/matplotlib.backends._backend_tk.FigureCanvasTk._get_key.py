    def _get_key(self, event):
        unikey = event.char
        key = cbook._unikey_or_keysym_to_mplkey(unikey, event.keysym)
        if key is not None:
            mods = self._mpl_modifiers(event, exclude=key)
            # shift is not added to the keys as this is already accounted for.
            if "shift" in mods and unikey:
                mods.remove("shift")
            return "+".join([*mods, key])
