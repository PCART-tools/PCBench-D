    def bool(self):
        """
        Return the bool of a single element PandasObject.

        This must be a boolean scalar value, either True or False.  Raise a
        ValueError if the PandasObject does not have exactly 1 element, or that
        element is not boolean

        Returns
        -------
        bool
            Same single boolean value converted to bool type.
        """
        v = self.squeeze()
        if isinstance(v, (bool, np.bool_)):
            return bool(v)
        elif is_scalar(v):
            raise ValueError(
                "bool cannot act on a non-boolean single element "
                f"{type(self).__name__}"
            )

        self.__nonzero__()
