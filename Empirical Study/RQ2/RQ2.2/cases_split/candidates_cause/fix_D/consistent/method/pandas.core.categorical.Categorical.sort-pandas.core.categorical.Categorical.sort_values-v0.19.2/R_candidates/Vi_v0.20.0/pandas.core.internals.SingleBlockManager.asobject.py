    @property
    def asobject(self):
        """
        return a object dtype array. datetime/timedelta like values are boxed
        to Timestamp/Timedelta instances.
        """
        return self._block.get_values(dtype=object)
