    def update(self, props):
        """
        Update the properties of this :class:`Artist` from the
        dictionary *prop*.
        """
        def _update_property(self, k, v):
            """sorting out how to update property (setter or setattr)

            Parameters
            ----------
            k : str
                The name of property to update
            v : obj
                The value to assign to the property
            Returns
            -------
            ret : obj or None
                If using a `set_*` method return it's return, else None.
            """
            k = k.lower()
            # white list attributes we want to be able to update through
            # art.update, art.set, setp
            if k in {'axes'}:
                return setattr(self, k, v)
            else:
                func = getattr(self, 'set_' + k, None)
                if not callable(func):
                    raise AttributeError('Unknown property %s' % k)
                return func(v)

        store = self.eventson
        self.eventson = False
        try:
            ret = [_update_property(self, k, v)
                   for k, v in props.items()]
        finally:
            self.eventson = store

        if len(ret):
            self.pchanged()
            self.stale = True
        return ret
