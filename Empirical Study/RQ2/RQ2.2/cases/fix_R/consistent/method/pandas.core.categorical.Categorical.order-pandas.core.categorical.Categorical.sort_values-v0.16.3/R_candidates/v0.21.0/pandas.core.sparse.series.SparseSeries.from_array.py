    @classmethod
    def from_array(cls, arr, index=None, name=None, copy=False,
                   fill_value=None, fastpath=False):
        """
        Simplified alternate constructor
        """
        return cls(arr, index=index, name=name, copy=copy,
                   fill_value=fill_value, fastpath=fastpath)
