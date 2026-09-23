    @classmethod
    def _simple_new(
        cls,
        array: IntervalArray | NDArrayBackedExtensionArray,
        name: Hashable = None,
    ):
        """
        Construct from an ExtensionArray of the appropriate type.

        Parameters
        ----------
        array : ExtensionArray
        name : Label, default None
            Attached as result.name
        """
        assert isinstance(array, cls._data_cls), type(array)

        result = object.__new__(cls)
        result._data = array
        result._name = name
        result._cache = {}
        result._reset_identity()
        return result
