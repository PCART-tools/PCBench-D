    def _shallow_copy_with_infer(self, values, **kwargs):
        """
        Create a new Index inferring the class with passed value, don't copy
        the data, use the same object attributes with passed in attributes
        taking precedence.

        *this is an internal non-public method*

        Parameters
        ----------
        values : the values to create the new Index, optional
        kwargs : updates the default attributes for this Index
        """
        attributes = self._get_attributes_dict()
        attributes.update(kwargs)
        attributes["copy"] = False
        if not len(values) and "dtype" not in kwargs:
            attributes["dtype"] = self.dtype
        if self._infer_as_myclass:
            try:
                return self._constructor(values, **attributes)
            except (TypeError, ValueError):
                pass
        return Index(values, **attributes)
