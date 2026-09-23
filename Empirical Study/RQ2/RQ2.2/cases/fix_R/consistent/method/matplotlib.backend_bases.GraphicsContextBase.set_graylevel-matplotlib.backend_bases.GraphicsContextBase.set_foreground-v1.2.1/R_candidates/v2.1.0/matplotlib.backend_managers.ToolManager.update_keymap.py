    def update_keymap(self, name, *keys):
        """
        Set the keymap to associate with the specified tool

        Parameters
        ----------
        name : string
            Name of the Tool
        keys : keys to associate with the Tool
        """

        if name not in self._tools:
            raise KeyError('%s not in Tools' % name)

        self._remove_keys(name)

        for key in keys:
            for k in validate_stringlist(key):
                if k in self._keys:
                    warnings.warn('Key %s changed from %s to %s' %
                                  (k, self._keys[k], name))
                self._keys[k] = name
