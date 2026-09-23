    def get_font_config(self):
        """Reinitializes self if relevant rcParams on have changed."""
        if self._rc_cache is None:
            self._rc_cache = dict.fromkeys(self._rc_cache_keys)
        changed = [par for par in self._rc_cache_keys
                   if rcParams[par] != self._rc_cache[par]]
        if changed:
            if DEBUG:
                print('DEBUG following keys changed:', changed)
            for k in changed:
                if DEBUG:
                    print('DEBUG %-20s: %-10s -> %-10s' %
                          (k, self._rc_cache[k], rcParams[k]))
                # deepcopy may not be necessary, but feels more future-proof
                self._rc_cache[k] = copy.deepcopy(rcParams[k])
            if DEBUG:
                print('DEBUG RE-INIT\nold fontconfig:', self._fontconfig)
            self.__init__()
        if DEBUG:
            print('DEBUG fontconfig:', self._fontconfig)
        return self._fontconfig
