    @_api.delete_parameter("3.3", "args")
    def update_keymap(self, name, key, *args):
        """
        Set the keymap to associate with the specified tool.

        Parameters
        ----------
        name : str
            Name of the Tool.
        key : str or list of str
            Keys to associate with the tool.
        """
        if name not in self._tools:
            raise KeyError('%s not in Tools' % name)
        self._remove_keys(name)
        for key in [key, *args]:
            if isinstance(key, str) and validate_stringlist(key) != [key]:
                _api.warn_deprecated(
                    "3.3", message="Passing a list of keys as a single "
                    "comma-separated string is deprecated since %(since)s and "
                    "support will be removed %(removal)s; pass keys as a list "
                    "of strings instead.")
                key = validate_stringlist(key)
            if isinstance(key, str):
                key = [key]
            for k in key:
                if k in self._keys:
                    _api.warn_external(
                        f'Key {k} changed from {self._keys[k]} to {name}')
                self._keys[k] = name
