    def _values_for_json(self) -> np.ndarray:
        """
        Specify how to render our entries in to_json.

        Notes
        -----
        The dtype on the returned ndarray is not restricted, but for non-native
        types that are not specifically handled in objToJSON.c, to_json is
        liable to raise. In these cases, it may be safer to return an ndarray
        of strings.
        """
        return np.asarray(self)
