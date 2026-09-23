    @final
    def __finalize__(
        self: NDFrameT, other, method: str | None = None, **kwargs
    ) -> NDFrameT:
        """
        Propagate metadata from other to self.

        Parameters
        ----------
        other : the object from which to get the attributes that we are going
            to propagate
        method : str, optional
            A passed method name providing context on where ``__finalize__``
            was called.

            .. warning::

               The value passed as `method` are not currently considered
               stable across pandas releases.
        """
        if isinstance(other, NDFrame):
            for name in other.attrs:
                self.attrs[name] = other.attrs[name]

            self.flags.allows_duplicate_labels = other.flags.allows_duplicate_labels
            # For subclasses using _metadata.
            for name in set(self._metadata) & set(other._metadata):
                assert isinstance(name, str)
                object.__setattr__(self, name, getattr(other, name, None))

        if method == "concat":
            attrs = other.objs[0].attrs
            check_attrs = all(objs.attrs == attrs for objs in other.objs[1:])
            if check_attrs:
                for name in attrs:
                    self.attrs[name] = attrs[name]

            allows_duplicate_labels = all(
                x.flags.allows_duplicate_labels for x in other.objs
            )
            self.flags.allows_duplicate_labels = allows_duplicate_labels

        return self
