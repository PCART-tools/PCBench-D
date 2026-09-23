    def __delitem__(self, key) -> None:
        """
        Delete item
        """
        deleted = False

        maybe_shortcut = False
        if self.ndim == 2 and isinstance(self.columns, MultiIndex):
            try:
                # By using engine's __contains__ we effectively
                # restrict to same-length tuples
                maybe_shortcut = key not in self.columns._engine
            except TypeError:
                pass

        if maybe_shortcut:
            # Allow shorthand to delete all columns whose first len(key)
            # elements match key:
            if not isinstance(key, tuple):
                key = (key,)
            for col in self.columns:
                if isinstance(col, tuple) and col[: len(key)] == key:
                    del self[col]
                    deleted = True
        if not deleted:
            # If the above loop ran and didn't delete anything because
            # there was no match, this call should raise the appropriate
            # exception:
            loc = self.axes[-1].get_loc(key)
            self._mgr = self._mgr.idelete(loc)

        # delete from the caches
        try:
            del self._item_cache[key]
        except KeyError:
            pass
