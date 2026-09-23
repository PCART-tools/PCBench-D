    def _get_key(self, keyval, keycode, state):
        unikey = chr(Gdk.keyval_to_unicode(keyval))
        key = cbook._unikey_or_keysym_to_mplkey(
            unikey,
            Gdk.keyval_name(keyval))
        modifiers = [
            ("ctrl", Gdk.ModifierType.CONTROL_MASK, "control"),
            ("alt", Gdk.ModifierType.ALT_MASK, "alt"),
            ("shift", Gdk.ModifierType.SHIFT_MASK, "shift"),
            ("super", Gdk.ModifierType.SUPER_MASK, "super"),
        ]
        mods = [
            mod for mod, mask, mod_key in modifiers
            if (mod_key != key and state & mask
                and not (mod == "shift" and unikey.isprintable()))]
        return "+".join([*mods, key])
