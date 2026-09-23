    @classmethod
    def _simple_new(cls, array: IntervalArray, name: Label = None):
        """
        Construct from an IntervalArray

        Parameters
        ----------
        array : IntervalArray
        name : Label, default None
            Attached as result.name
        """
        assert isinstance(array, IntervalArray), type(array)

        result = IntervalMixin.__new__(cls)
        result._data = array
        result.name = name
        result._cache = {}
        result._reset_identity()
        return result
