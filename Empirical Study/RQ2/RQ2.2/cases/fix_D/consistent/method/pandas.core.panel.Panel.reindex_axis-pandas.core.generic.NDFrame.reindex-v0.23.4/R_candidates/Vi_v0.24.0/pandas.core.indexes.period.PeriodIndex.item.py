    def item(self):
        """
        return the first element of the underlying data as a python
        scalar
        """
        # TODO(DatetimeArray): remove
        if len(self) == 1:
            return self[0]
        else:
            # copy numpy's message here because Py26 raises an IndexError
            raise ValueError('can only convert an array of size 1 to a '
                             'Python scalar')
