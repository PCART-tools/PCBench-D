    def squeeze(self, **kwargs):
        """Squeeze length 1 dimensions."""
        nv.validate_squeeze(tuple(), kwargs)

        try:
            return self.iloc[tuple([0 if len(a) == 1 else slice(None)
                                    for a in self.axes])]
        except:
            return self
