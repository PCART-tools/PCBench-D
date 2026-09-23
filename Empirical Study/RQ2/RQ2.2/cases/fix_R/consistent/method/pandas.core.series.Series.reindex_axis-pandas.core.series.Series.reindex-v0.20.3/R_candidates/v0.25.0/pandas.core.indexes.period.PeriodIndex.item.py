    def item(self):
        """
        return the first element of the underlying data as a python
        scalar

        .. deprecated 0.25.0

        """
        warnings.warn(
            "`item` has been deprecated and will be removed in a " "future version",
            FutureWarning,
            stacklevel=2,
        )
        # TODO(DatetimeArray): remove
        if len(self) == 1:
            return self[0]
        else:
            # copy numpy's message here because Py26 raises an IndexError
            raise ValueError(
                "can only convert an array of size 1 to a " "Python scalar"
            )
