    @classmethod
    def _simple_new(cls, array, name, closed=None):
        """
        Construct from an IntervalArray

        Parameters
        ----------
        array : IntervalArray
        name : str
            Attached as result.name
        closed : Any
            Ignored.
        """
        result = IntervalMixin.__new__(cls)
        result._data = array
        result.name = name
        result._reset_identity()
        return result
