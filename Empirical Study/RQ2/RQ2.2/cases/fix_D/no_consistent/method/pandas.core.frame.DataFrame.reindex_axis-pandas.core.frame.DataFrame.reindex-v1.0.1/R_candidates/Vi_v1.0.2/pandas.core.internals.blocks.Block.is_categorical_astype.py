    def is_categorical_astype(self, dtype):
        """
        validate that we have a astypeable to categorical,
        returns a boolean if we are a categorical
        """
        if dtype is Categorical or dtype is CategoricalDtype:
            # this is a pd.Categorical, but is not
            # a valid type for astypeing
            raise TypeError(f"invalid type {dtype} for astype")

        elif is_categorical_dtype(dtype):
            return True

        return False
