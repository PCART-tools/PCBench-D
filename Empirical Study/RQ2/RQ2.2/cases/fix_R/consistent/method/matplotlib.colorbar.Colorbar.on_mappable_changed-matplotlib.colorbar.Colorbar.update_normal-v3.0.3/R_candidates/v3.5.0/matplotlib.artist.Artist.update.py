    def update(self, props):
        """
        Update this artist's properties from the dict *props*.

        Parameters
        ----------
        props : dict
        """
        ret = []
        with cbook._setattr_cm(self, eventson=False):
            for k, v in props.items():
                # Allow attributes we want to be able to update through
                # art.update, art.set, setp.
                if k == "axes":
                    ret.append(setattr(self, k, v))
                else:
                    func = getattr(self, f"set_{k}", None)
                    if not callable(func):
                        raise AttributeError(f"{type(self).__name__!r} object "
                                             f"has no property {k!r}")
                    ret.append(func(v))
        if ret:
            self.pchanged()
            self.stale = True
        return ret
