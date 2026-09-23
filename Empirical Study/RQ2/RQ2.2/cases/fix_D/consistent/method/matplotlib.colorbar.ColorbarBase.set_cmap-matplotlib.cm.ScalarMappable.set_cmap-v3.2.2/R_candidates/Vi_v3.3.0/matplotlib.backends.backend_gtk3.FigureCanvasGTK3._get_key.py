    def _get_key(self, event):
        if event.keyval in self.keyvald:
            key = self.keyvald[event.keyval]
        elif event.keyval < 256:
            key = chr(event.keyval)
        else:
            key = None

        modifiers = [
                     (Gdk.ModifierType.MOD4_MASK, 'super'),
                     (Gdk.ModifierType.MOD1_MASK, 'alt'),
                     (Gdk.ModifierType.CONTROL_MASK, 'ctrl'),
                    ]
        for key_mask, prefix in modifiers:
            if event.state & key_mask:
                key = '{0}+{1}'.format(prefix, key)

        return key
