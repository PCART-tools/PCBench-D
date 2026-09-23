    def _get_key(self, event):
        unikey = chr(Gdk.keyval_to_unicode(event.keyval))
        key = cbook._unikey_or_keysym_to_mplkey(
            unikey,
            Gdk.keyval_name(event.keyval))
        modifiers = [
            (Gdk.ModifierType.CONTROL_MASK, 'ctrl'),
            (Gdk.ModifierType.MOD1_MASK, 'alt'),
            (Gdk.ModifierType.SHIFT_MASK, 'shift'),
            (Gdk.ModifierType.MOD4_MASK, 'super'),
        ]
        for key_mask, prefix in modifiers:
            if event.state & key_mask:
                if not (prefix == 'shift' and unikey.isprintable()):
                    key = f'{prefix}+{key}'
        return key
