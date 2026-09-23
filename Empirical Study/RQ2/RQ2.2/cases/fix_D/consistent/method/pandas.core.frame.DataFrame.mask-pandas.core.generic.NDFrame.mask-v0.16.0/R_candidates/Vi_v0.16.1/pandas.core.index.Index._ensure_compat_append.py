    def _ensure_compat_append(self, other):
        """
        prepare the append

        Returns
        -------
        list of to_concat, name of result Index
        """
        name = self.name
        to_concat = [self]

        if isinstance(other, (list, tuple)):
            to_concat = to_concat + list(other)
        else:
            to_concat.append(other)

        for obj in to_concat:
            if (isinstance(obj, Index) and
                obj.name != name and
                obj.name is not None):
                name = None
                break

        to_concat = self._ensure_compat_concat(to_concat)
        to_concat = [x.values if isinstance(x, Index) else x
                     for x in to_concat]
        return to_concat, name
