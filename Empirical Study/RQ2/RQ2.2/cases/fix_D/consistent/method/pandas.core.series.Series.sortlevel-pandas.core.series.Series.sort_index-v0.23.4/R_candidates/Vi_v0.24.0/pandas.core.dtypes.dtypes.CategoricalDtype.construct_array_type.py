    @classmethod
    def construct_array_type(cls):
        """
        Return the array type associated with this dtype

        Returns
        -------
        type
        """
        from pandas import Categorical
        return Categorical
