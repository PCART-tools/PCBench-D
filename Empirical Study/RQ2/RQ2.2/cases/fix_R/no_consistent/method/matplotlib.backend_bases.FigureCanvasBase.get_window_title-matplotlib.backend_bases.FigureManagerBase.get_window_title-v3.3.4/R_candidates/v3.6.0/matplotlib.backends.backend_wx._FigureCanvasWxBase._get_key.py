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

        for meth, prefix, key_name in [
                (event.ControlDown, 'ctrl', 'control'),
                (event.AltDown, 'alt', 'alt'),
                (event.ShiftDown, 'shift', 'shift'),
        ]:
            if meth() and key_name != key:
                if not (key_name == 'shift' and key.isupper()):
                    key = '{0}+{1}'.format(prefix, key)

        return key
