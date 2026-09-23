    def _get_key(self, event):
        unikey = chr(Gdk.keyval_to_unicode(event.keyval))
        key = cbook._unikey_or_keysym_to_mplkey(
            unikey, Gdk.keyval_name(event.keyval))
        mods = self._mpl_modifiers(event.state, exclude=key)
        if "shift" in mods and unikey.isprintable():
            mods.remove("shift")
        return "+".join([*mods, key])
