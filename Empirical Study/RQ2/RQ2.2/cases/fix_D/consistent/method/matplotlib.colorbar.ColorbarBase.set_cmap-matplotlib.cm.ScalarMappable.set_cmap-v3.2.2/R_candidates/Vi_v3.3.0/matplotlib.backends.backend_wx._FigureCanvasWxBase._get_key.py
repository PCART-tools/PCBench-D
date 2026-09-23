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
            key = None

        for meth, prefix in (
                [event.AltDown, 'alt'],
                [event.ControlDown, 'ctrl'], ):
            if meth():
                key = '{0}+{1}'.format(prefix, key)

        return key
