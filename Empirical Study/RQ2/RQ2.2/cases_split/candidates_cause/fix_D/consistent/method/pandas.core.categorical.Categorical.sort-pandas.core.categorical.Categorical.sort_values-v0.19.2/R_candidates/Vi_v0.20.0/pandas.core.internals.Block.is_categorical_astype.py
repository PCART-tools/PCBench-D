    def is_categorical_astype(self, dtype):
        """
        validate that we have a astypeable to categorical,
        returns a boolean if we are a categorical
        """
        if is_categorical_dtype(dtype):
            if dtype == CategoricalDtype():
                return True

            # this is a pd.Categorical, but is not
            # a valid type for astypeing
            raise TypeError("invalid type {0} for astype".format(dtype))

        return False
