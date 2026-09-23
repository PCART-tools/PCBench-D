    def _get_key(self, event):
        if event.keyval in self.keyvald:
            key = self.keyvald[event.keyval]
        elif event.keyval < 256:
            key = chr(event.keyval)
        else:
            key = None

        for key_mask, prefix in (
                                 [gdk.MOD4_MASK, 'super'],
                                 [gdk.MOD1_MASK, 'alt'],
                                 [gdk.CONTROL_MASK, 'ctrl'], ):
            if event.state & key_mask:
                key = '{0}+{1}'.format(prefix, key)

        return key
