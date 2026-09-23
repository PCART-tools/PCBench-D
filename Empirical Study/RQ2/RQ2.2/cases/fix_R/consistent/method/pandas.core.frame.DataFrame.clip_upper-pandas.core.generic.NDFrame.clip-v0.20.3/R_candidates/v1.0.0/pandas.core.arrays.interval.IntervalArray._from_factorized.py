    @classmethod
    def _from_factorized(cls, values, original):
        if len(values) == 0:
            # An empty array returns object-dtype here. We can't create
            # a new IA from an (empty) object-dtype array, so turn it into the
            # correct dtype.
            values = values.astype(original.dtype.subtype)
        return cls(values, closed=original.closed)
